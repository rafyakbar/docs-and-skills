# Image Manipulation

- [Introduction](#introduction)
- [Installation](#installation)
  * [Configuration](#configuration)
- [Reading Images](#reading-images)
  * [Uploaded Files](#uploaded-files)
  * [Storage Files](#storage-files)
  * [Other Sources](#other-sources)
- [Manipulating Images](#manipulating-images)
  * [Resizing Images](#resizing-images)
  * [Other Transformations](#other-transformations)
- [Encoding Images](#encoding-images)
- [Storing Images](#storing-images)
- [Inspecting Images](#inspecting-images)
- [Image Drivers](#image-drivers)
  * [Custom Image Drivers](#custom-image-drivers)
  * [Custom Transformations](#custom-transformations)

## [Introduction](#introduction)

Laravel provides a fluent image manipulation API that allows you to resize, crop, encode, and store images using the same expressive conventions found throughout the framework. Laravel's image features are powered by [Intervention Image](https://image.intervention.io/) and support the GD and Imagick PHP extensions.

The image API is useful when working with uploaded files, files stored on Laravel [filesystem disks](/docs/13.x/filesystem), local files, remote URLs, or raw image bytes:

```
1use Illuminate\Support\Facades\Image;

2 

3$path = Image::fromStorage('avatars/photo.jpg', 'public')

4    ->cover(400, 400)

5    ->toWebp()

6    ->quality(80)

7    ->storePublicly('avatars', 'public');
```

Image manipulation can be CPU and memory-intensive. Consider performing large image processing workloads on a [queued job](/docs/13.x/queues) instead of during the HTTP request that receives the upload.

## [Installation](#installation)

Before using Laravel's image manipulation features, install the Intervention Image package via Composer:

```
1composer require intervention/image:^4.0
```

You should also ensure your PHP installation has either the GD or Imagick extension installed, depending on which driver your application will use.

### [Configuration](#configuration)

Laravel's image configuration file is located at `config/images.php`. If your application does not have an `images` configuration file, you may publish it using the `config:publish` Artisan command:

```
1php artisan config:publish images
```

The image configuration file allows you to specify your application's default image driver. You may also specify the default driver using the `IMAGE_DRIVER` environment variable. The supported drivers are `gd` and `imagick`:

```
1IMAGE_DRIVER=imagick
```

## [Reading Images](#reading-images)

The `Image` facade provides several methods for reading images from common sources. Image contents are loaded lazily, so the source is typically not read until the image is processed or its bytes are requested.

### [Uploaded Files](#uploaded-files)

You may retrieve an uploaded image from an incoming request using the `image` method. This method returns an `Illuminate\Image\Image` instance for the uploaded file, or `null` if the file is not present:

```
 1use Illuminate\Http\Request;

 2 

 3Route::post('/avatar', function (Request $request) {

 4    $request->validate(['avatar' => ['required', 'image']]);

 5 

 6    $path = $request->image('avatar')

 7        ->cover(400, 400)

 8        ->toWebp()

 9        ->storePublicly('avatars', 'public');

10 

11    // ...

12});
```

Alternatively, you may create an image instance from an `Illuminate\Http\UploadedFile` instance using the `fromUpload` method:

```
1use Illuminate\Support\Facades\Image;

2 

3$image = Image::fromUpload($request->file('avatar'));
```

When an image is created from an uploaded file, you may retrieve the underlying uploaded file using the `file` method:

```
1$file = $image->file();
```

### [Storage Files](#storage-files)

You may create an image instance from a file stored on one of your application's [filesystem disks](/docs/13.x/filesystem) using the `fromStorage` method. The first argument is the path to the file, while the second argument is the disk name:

```
1use Illuminate\Support\Facades\Image;

2 

3$image = Image::fromStorage('avatars/photo.jpg', disk: 'public');
```

You may also create image instances directly from a filesystem disk instance using the `image` method:

```
1use Illuminate\Support\Facades\Storage;

2 

3$image = Storage::disk('public')->image('avatars/photo.jpg');
```

### [Other Sources](#other-sources)

The `Image` facade also includes methods for creating image instances from raw bytes, local file paths, remote URLs, and Base64 encoded strings:

```
1use Illuminate\Support\Facades\Image;

2 

3$image = Image::fromBytes($contents);

4$image = Image::fromBase64($base64);

5$image = Image::fromPath(storage_path('app/avatars/photo.jpg'));

6$image = Image::fromUrl('https://example.com/photo.jpg');
```

## [Manipulating Images](#manipulating-images)

Image instances are immutable. Each manipulation method returns a new image instance with the transformation appended to its processing pipeline, allowing methods to be chained fluently:

```
1$image = $request->image('avatar')

2    ->orient()

3    ->cover(400, 400)

4    ->sharpen(10);
```

Transformations are processed in the order they are added to the image pipeline and the image is only encoded once at the end.

### [Resizing Images](#resizing-images)

The `resize` method resizes an image to the given dimensions. You may provide both a width and height, or provide only one dimension using named arguments:

```
1$image = $image->resize(800, 600);

2$image = $image->resize(width: 800);

3$image = $image->resize(height: 600);
```

The `scale` method proportionally scales an image down so that it fits within the given dimensions. This method will never increase the size of an image:

```
1$image = $image->scale(800, 600);

2$image = $image->scale(width: 800);

3$image = $image->scale(height: 600);
```

The `cover` method resizes and crops an image to completely cover the given dimensions:

```
1$image = $image->cover(400, 400);
```

The `contain` method resizes an image to fit within the given dimensions while preserving the entire image. If necessary, empty space will be filled using the optional background color:

```
1$image = $image->contain(400, 400);

2$image = $image->contain(400, 400, '#ffffff');
```

You may crop an image using the `crop` method. The first two arguments are the desired width and height, and the optional third and fourth arguments specify the crop's `x` and `y` coordinates:

```
1$image = $image->crop(300, 200);

2$image = $image->crop(300, 200, x: 50, y: 25);
```

### [Other Transformations](#other-transformations)

Laravel also provides a variety of additional image transformation methods:

```
1$image = $image->orient();

2$image = $image->rotate(90);

3$image = $image->rotate(90, '#ffffff');

4$image = $image->blur(5);

5$image = $image->grayscale();

6$image = $image->sharpen(10);

7$image = $image->flipVertically();

8$image = $image->flipHorizontally();
```

The `orient` method rotates the image according to its EXIF orientation data. The `rotate` method rotates the image clockwise by the given angle and accepts an optional background color. The `blur` and `sharpen` methods accept values between `0` and `100`.

#### [Conditional Transformations](#conditional-transformations)

Image instances support Laravel's `Conditionable` trait, allowing you to conditionally apply transformations using the `when` and `unless` methods:

```
1$image = $request->image('avatar')

2    ->when($request->boolean('crop'), fn ($image) => $image->cover(400, 400))

3    ->unless($request->boolean('preserve_format'), fn ($image) => $image->toWebp());
```

## [Encoding Images](#encoding-images)

By default, processed images are encoded using their original format. However, you may convert the image to another supported format before retrieving or storing it:

```
1$image = $image->toWebp();

2$image = $image->toJpg();

3$image = $image->toJpeg();

4$image = $image->toPng();

5$image = $image->toGif();

6$image = $image->toAvif();

7$image = $image->toBmp();
```

You may use the `quality` method to set the output quality. The quality will be clamped between `1` and `100`:

```
1$image = $image->toWebp()->quality(80);
```

The `optimize` method is a convenient shortcut for converting the image to a given format and setting its quality. By default, images are optimized as WebP images with a quality of `70`:

```
1$image = $image->optimize();

2 

3$image = $image->optimize(format: 'jpg', quality: 85);
```

You may retrieve the processed image contents as a string of bytes, base64 encoded string, or data URI:

```
1$bytes = $image->toBytes();

2$base64 = $image->toBase64();

3$dataUri = $image->toDataUri();
```

An image instance may also be cast to a string to retrieve its processed bytes:

```
1$bytes = (string) $image;
```

## [Storing Images](#storing-images)

The `store` method stores the processed image on one of your application's filesystem disks. Like uploaded files, Laravel will generate a unique filename and return the stored path. The second argument may be used to specify the disk:

```
1$path = $request->image('avatar')

2    ->cover(400, 400)

3    ->store(path: 'avatars');

4 

5$path = $request->image('avatar')

6    ->cover(400, 400)

7    ->store(path: 'avatars', disk: 's3');
```

You may use the `storeAs` method to specify the stored filename:

```
1$path = $request->image('avatar')

2    ->cover(400, 400)

3    ->storeAs(path: 'avatars', name: 'avatar.jpg', disk: 'public');
```

The `storePublicly` and `storePubliclyAs` methods store the image with `public` visibility:

```
1$path = $request->image('avatar')

2    ->cover(400, 400)

3    ->storePublicly(path: 'avatars', disk: 'public');

4 

5$path = $request->image('avatar')

6    ->cover(400, 400)

7    ->storePubliclyAs(path: 'avatars', name: 'avatar.webp', disk: 'public');
```

If the image could not be stored, the storage methods return `false`.

## [Inspecting Images](#inspecting-images)

You may retrieve the image's MIME type, extension, dimensions, width, and height using the following methods:

```
1$mimeType = $image->mimeType();

2$extension = $image->extension();

3 

4[$width, $height] = $image->dimensions();

5$width = $image->width();

6$height = $image->height();
```

These methods operate on the processed image. For example, calling `width` after `cover(400, 400)` will return `400`.

## [Image Drivers](#image-drivers)

### [Custom Image Drivers](#custom-image-drivers)

Laravel's image manager extends Laravel's base `Illuminate\Support\Manager` class. This means you may register custom image drivers using the `extend` method available on the image manager and `Image` facade.

Custom image drivers should implement the `Illuminate\Contracts\Image\Driver` interface. The `process` method receives the original image contents and the ordered `Illuminate\Image\ImagePipeline` that should be applied to the image, and should return the processed image bytes:

```
 1<?php

 2 

 3namespace App\Images;

 4 

 5use Illuminate\Contracts\Image\Driver;

 6use Illuminate\Image\ImagePipeline;

 7 

 8class VipsDriver implements Driver

 9{

10    /**

11     * Process the given image contents with the specified pipeline.

12     */

13    public function process(string $contents, ImagePipeline $pipeline): string

14    {

15        // Apply the pipeline's transformations and output options...

16 

17        return $contents;

18    }

19 

20    /**

21     * Register a transformation handler.

22     */

23    public function transformUsing(string $transformation, callable $callback): static

24    {

25        // Store the handler so it may be applied while processing the pipeline...

26 

27        return $this;

28    }

29}
```

To better understand how to implement a custom image driver, you may review the framework's built-in `Illuminate\Image\Drivers\InterventionDriver` class.

Once you have implemented your custom driver, you may register it using the `Image` facade's `extend` method. Typically, this should be done in the `boot` method of a service provider:

```
 1use App\Images\VipsDriver;

 2use Illuminate\Contracts\Foundation\Application;

 3use Illuminate\Support\Facades\Image;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Image::extend('vips', function (Application $app) {

11        return new VipsDriver;

12    });

13}
```

After registering the driver, you may use it for a specific image using the `using` method:

```
1$image = $request->image('avatar')

2    ->using('vips')

3    ->cover(400, 400);
```

You may also configure a custom driver as your application's default image driver using the `default` option in your application's `config/images.php` configuration file or the `IMAGE_DRIVER` environment variable:

```
1IMAGE_DRIVER=vips
```

### [Custom Transformations](#custom-transformations)

Applications and packages may define custom transformations by creating a class that implements the `Illuminate\Contracts\Image\Transformation` contract. Custom transformations can then be added to an image pipeline using the `transform` method:

```
 1<?php

 2 

 3namespace App\Images\Transformations;

 4 

 5use Illuminate\Contracts\Image\Transformation;

 6 

 7class Pixelate implements Transformation

 8{

 9    public function __construct(

10        public readonly int $size,

11    ) {

12        //

13    }

14}
```

Next, register a handler for the transformation and driver using the `Image` facade's `transformUsing` method. Typically, this should be done in the `boot` method of a service provider:

```
1use App\Images\Transformations\Pixelate;

2use Illuminate\Support\Facades\Image;

3use Intervention\Image\Interfaces\ImageInterface;

4 

5Image::transformUsing('gd', Pixelate::class, function (ImageInterface $image, Pixelate $transformation) {

6    return $image->pixelate($transformation->size);

7});
```

Once the transformation handler has been registered, you may apply the transformation to an image:

```
1use App\Images\Transformations\Pixelate;

2 

3$image = $request->image('avatar')

4    ->transform(new Pixelate(12))

5    ->store('avatars');
```
