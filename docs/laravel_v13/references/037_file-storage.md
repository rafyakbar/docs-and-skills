# File Storage

- [Introduction](#introduction)
- [Configuration](#configuration)
  * [The Local Driver](#the-local-driver)
  * [The Public Disk](#the-public-disk)
  * [Driver Prerequisites](#driver-prerequisites)
  * [Scoped and Read-Only Filesystems](#scoped-and-read-only-filesystems)
  * [Amazon S3 Compatible Filesystems](#amazon-s3-compatible-filesystems)
- [Obtaining Disk Instances](#obtaining-disk-instances)
  * [On-Demand Disks](#on-demand-disks)
- [Retrieving Files](#retrieving-files)
  * [Downloading Files](#downloading-files)
  * [File URLs](#file-urls)
  * [Temporary URLs](#temporary-urls)
  * [File Metadata](#file-metadata)
- [Storing Files](#storing-files)
  * [Prepending and Appending To Files](#prepending-appending-to-files)
  * [Copying and Moving Files](#copying-moving-files)
  * [Automatic Streaming](#automatic-streaming)
  * [File Uploads](#file-uploads)
  * [File Visibility](#file-visibility)
  * [Image Manipulation](#image-manipulation)
- [Deleting Files](#deleting-files)
- [Directories](#directories)
- [Testing](#testing)
- [Custom Filesystems](#custom-filesystems)

## [Introduction](#introduction)

Laravel provides a powerful filesystem abstraction thanks to the wonderful [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple drivers for working with local filesystems, SFTP, and Amazon S3. Even better, it's amazingly simple to switch between these storage options between your local development machine and production server as the API remains the same for each system.

## [Configuration](#configuration)

Laravel's filesystem configuration file is located at `config/filesystems.php`. Within this file, you may configure all of your filesystem "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver are included in the configuration file so you can modify the configuration to reflect your storage preferences and credentials.

The `local` driver interacts with files stored locally on the server running the Laravel application, while the `sftp` storage driver is used for SSH key-based FTP. The `s3` driver is used to write to Amazon's S3 cloud storage service.

You may configure as many disks as you like and may even have multiple disks that use the same driver.

### [The Local Driver](#the-local-driver)

When using the `local` driver, all file operations are relative to the `root` directory defined in your `filesystems` configuration file. By default, this value is set to the `storage/app/private` directory. Therefore, the following method would write to `storage/app/private/example.txt`:

```
1use Illuminate\Support\Facades\Storage;

2 

3Storage::disk('local')->put('example.txt', 'Contents');
```

### [The Public Disk](#the-public-disk)

The `public` disk included in your application's `filesystems` configuration file is intended for files that are going to be publicly accessible. By default, the `public` disk uses the `local` driver and stores its files in `storage/app/public`.

If your `public` disk uses the `local` driver and you want to make these files accessible from the web, you should create a symbolic link from source directory `storage/app/public` to target directory `public/storage`:

To create the symbolic link, you may use the `storage:link` Artisan command:

```
1php artisan storage:link
```

Once a file has been stored and the symbolic link has been created, you can create a URL to the files using the `asset` helper:

```
1echo asset('storage/file.txt');
```

You may configure additional symbolic links in your `filesystems` configuration file. Each of the configured links will be created when you run the `storage:link` command:

```
1'links' => [

2    public_path('storage') => storage_path('app/public'),

3    public_path('images') => storage_path('app/images'),

4],
```

The `storage:unlink` command may be used to destroy your configured symbolic links:

```
1php artisan storage:unlink
```

### [Driver Prerequisites](#driver-prerequisites)

#### [S3 Driver Configuration](#s3-driver-configuration)

Before using the S3 driver, you will need to install the Flysystem S3 package via the Composer package manager:

```
1composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

An S3 disk configuration array is located in your `config/filesystems.php` configuration file. Typically, you should configure your S3 information and credentials using the following environment variables which are referenced by the `config/filesystems.php` configuration file:

```
1AWS_ACCESS_KEY_ID=<your-key-id>

2AWS_SECRET_ACCESS_KEY=<your-secret-access-key>

3AWS_DEFAULT_REGION=us-east-1

4AWS_BUCKET=<your-bucket-name>

5AWS_USE_PATH_STYLE_ENDPOINT=false
```

For convenience, these environment variables match the naming convention used by the AWS CLI.

#### [FTP Driver Configuration](#ftp-driver-configuration)

Before using the FTP driver, you will need to install the Flysystem FTP package via the Composer package manager:

```
1composer require league/flysystem-ftp "^3.0"
```

Laravel's Flysystem integrations work great with FTP; however, a sample configuration is not included with the framework's default `config/filesystems.php` configuration file. If you need to configure an FTP filesystem, you may use the configuration example below:

```
 1'ftp' => [

 2    'driver' => 'ftp',

 3    'host' => env('FTP_HOST'),

 4    'username' => env('FTP_USERNAME'),

 5    'password' => env('FTP_PASSWORD'),

 6 

 7    // Optional FTP Settings...

 8    // 'port' => env('FTP_PORT', 21),

 9    // 'root' => env('FTP_ROOT'),

10    // 'passive' => true,

11    // 'ssl' => true,

12    // 'timeout' => 30,

13],
```

#### [SFTP Driver Configuration](#sftp-driver-configuration)

Before using the SFTP driver, you will need to install the Flysystem SFTP package via the Composer package manager:

```
1composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel's Flysystem integrations work great with SFTP; however, a sample configuration is not included with the framework's default `config/filesystems.php` configuration file. If you need to configure an SFTP filesystem, you may use the configuration example below:

```
 1'sftp' => [

 2    'driver' => 'sftp',

 3    'host' => env('SFTP_HOST'),

 4 

 5    // Settings for basic authentication...

 6    'username' => env('SFTP_USERNAME'),

 7    'password' => env('SFTP_PASSWORD'),

 8 

 9    // Settings for SSH key-based authentication with encryption password...

10    'privateKey' => env('SFTP_PRIVATE_KEY'),

11    'passphrase' => env('SFTP_PASSPHRASE'),

12 

13    // Settings for file / directory permissions...

14    'visibility' => 'private', // `private` = 0600, `public` = 0644

15    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

16 

17    // Optional SFTP Settings...

18    // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),

19    // 'maxTries' => 4,

20    // 'passphrase' => env('SFTP_PASSPHRASE'),

21    // 'port' => env('SFTP_PORT', 22),

22    // 'root' => env('SFTP_ROOT', ''),

23    // 'timeout' => 30,

24    // 'useAgent' => true,

25],
```

### [Scoped and Read-Only Filesystems](#scoped-and-read-only-filesystems)

Scoped disks allow you to define a filesystem where all paths are automatically prefixed with a given path prefix. Before creating a scoped filesystem disk, you will need to install an additional Flysystem package via the Composer package manager:

```
1composer require league/flysystem-path-prefixing "^3.0"
```

You may create a path scoped instance of any existing filesystem disk by defining a disk that utilizes the `scoped` driver. For example, you may create a disk which scopes your existing `s3` disk to a specific path prefix, and then every file operation using your scoped disk will utilize the specified prefix:

```
1's3-videos' => [

2    'driver' => 'scoped',

3    'disk' => 's3',

4    'prefix' => 'path/to/videos',

5],
```

"Read-only" disks allow you to create filesystem disks that do not allow write operations. Before using the `read-only` configuration option, you will need to install an additional Flysystem package via the Composer package manager:

```
1composer require league/flysystem-read-only "^3.0"
```

Next, you may include the `read-only` configuration option in one or more of your disk's configuration arrays:

```
1's3-videos' => [

2    'driver' => 's3',

3    // ...

4    'read-only' => true,

5],
```

### [Amazon S3 Compatible Filesystems](#amazon-s3-compatible-filesystems)

By default, your application's `filesystems` configuration file contains a disk configuration for the `s3` disk. In addition to using this disk to interact with [Amazon S3](https://aws.amazon.com/s3/), you may use it to interact with any S3-compatible file storage service such as [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), or [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/).

Typically, after updating the disk's credentials to match the credentials of the service you are planning to use, you only need to update the value of the `endpoint` configuration option. This option's value is typically defined via the `AWS_ENDPOINT` environment variable:

```
1'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```

## [Obtaining Disk Instances](#obtaining-disk-instances)

The `Storage` facade may be used to interact with any of your configured disks. For example, you may use the `put` method on the facade to store an avatar on the default disk. If you call methods on the `Storage` facade without first calling the `disk` method, the method will automatically be passed to the default disk:

```
1use Illuminate\Support\Facades\Storage;

2 

3Storage::put('avatars/1', $content);
```

If your application interacts with multiple disks, you may use the `disk` method on the `Storage` facade to work with files on a particular disk:

```
1Storage::disk('s3')->put('avatars/1', $content);
```

### [On-Demand Disks](#on-demand-disks)

Sometimes you may wish to create a disk at runtime using a given configuration without that configuration actually being present in your application's `filesystems` configuration file. To accomplish this, you may pass a configuration array to the `Storage` facade's `build` method:

```
1use Illuminate\Support\Facades\Storage;

2 

3$disk = Storage::build([

4    'driver' => 'local',

5    'root' => '/path/to/root',

6]);

7 

8$disk->put('image.jpg', $content);
```

## [Retrieving Files](#retrieving-files)

The `get` method may be used to retrieve the contents of a file. The raw string contents of the file will be returned by the method. Remember, all file paths should be specified relative to the disk's "root" location:

```
1$contents = Storage::get('file.jpg');
```

If the file you are retrieving contains JSON, you may use the `json` method to retrieve the file and decode its contents:

```
1$orders = Storage::json('orders.json');
```

The `exists` method may be used to determine if a file exists on the disk:

```
1if (Storage::disk('s3')->exists('file.jpg')) {

2    // ...

3}
```

The `missing` method may be used to determine if a file is missing from the disk:

```
1if (Storage::disk('s3')->missing('file.jpg')) {

2    // ...

3}
```

### [Downloading Files](#downloading-files)

The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method:

```
1return Storage::download('file.jpg');

2 

3return Storage::download('file.jpg', $name, $headers);
```

### [File URLs](#file-urls)

You may use the `url` method to get the URL for a given file. If you are using the `local` driver, this will typically just prepend `/storage` to the given path and return a relative URL to the file. If you are using the `s3` driver, the fully qualified remote URL will be returned:

```
1use Illuminate\Support\Facades\Storage;

2 

3$url = Storage::url('file.jpg');
```

When using the `local` driver, all files that should be publicly accessible should be placed in the `storage/app/public` directory. Furthermore, you should [create a symbolic link](#the-public-disk) at `public/storage` which points to the `storage/app/public` directory.

When using the `local` driver, the return value of `url` is not URL encoded. For this reason, we recommend always storing your files using names that will create valid URLs.

#### [URL Host Customization](#url-host-customization)

If you would like to modify the host for URLs generated using the `Storage` facade, you may add or change the `url` option in the disk's configuration array:

```
1'public' => [

2    'driver' => 'local',

3    'root' => storage_path('app/public'),

4    'url' => env('APP_URL').'/storage',

5    'visibility' => 'public',

6    'throw' => false,

7],
```

### [Temporary URLs](#temporary-urls)

Using the `temporaryUrl` method, you may create temporary URLs to files stored using the `local` and `s3` drivers. This method accepts a path and a `DateTime` instance specifying when the URL should expire:

```
1use Illuminate\Support\Facades\Storage;

2 

3$url = Storage::temporaryUrl(

4    'file.jpg', now()->plus(minutes: 5)

5);
```

#### [Enabling Local Temporary URLs](#enabling-local-temporary-urls)

If you started developing your application before support for temporary URLs was introduced to the `local` driver, you may need to enable local temporary URLs. To do so, add the `serve` option to your `local` disk's configuration array within the `config/filesystems.php` configuration file:

```
1'local' => [

2    'driver' => 'local',

3    'root' => storage_path('app/private'),

4    'serve' => true,

5    'throw' => false,

6],
```

#### [S3 Request Parameters](#s3-request-parameters)

If you need to specify additional [S3 request parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests), you may pass the array of request parameters as the third argument to the `temporaryUrl` method:

```
1$url = Storage::temporaryUrl(

2    'file.jpg',

3    now()->plus(minutes: 5),

4    [

5        'ResponseContentType' => 'application/octet-stream',

6        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',

7    ]

8);
```

#### [Customizing Temporary URLs](#customizing-temporary-urls)

If you need to customize how temporary URLs are created for a specific storage disk, you can use the `buildTemporaryUrlsUsing` method. For example, this can be useful if you have a controller that allows you to download files stored via a disk that doesn't typically support temporary URLs. Usually, this method should be called from the `boot` method of a service provider:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use DateTime;

 6use Illuminate\Support\Facades\Storage;

 7use Illuminate\Support\Facades\URL;

 8use Illuminate\Support\ServiceProvider;

 9 

10class AppServiceProvider extends ServiceProvider

11{

12    /**

13     * Bootstrap any application services.

14     */

15    public function boot(): void

16    {

17        Storage::disk('local')->buildTemporaryUrlsUsing(

18            function (string $path, DateTime $expiration, array $options) {

19                return URL::temporarySignedRoute(

20                    'files.download',

21                    $expiration,

22                    array_merge($options, ['path' => $path])

23                );

24            }

25        );

26    }

27}
```

#### [Temporary Upload URLs](#temporary-upload-urls)

The ability to generate temporary upload URLs is only supported by the `s3` and `local` drivers.

If you need to generate a temporary URL that can be used to upload a file directly from your client-side application, you may use the `temporaryUploadUrl` method. This method accepts a path and a `DateTime` instance specifying when the URL should expire. The `temporaryUploadUrl` method returns an associative array which may be destructured into the upload URL and the headers that should be included with the upload request:

```
1use Illuminate\Support\Facades\Storage;

2 

3['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(

4    'file.jpg', now()->plus(minutes: 5)

5);
```

This method is primarily useful in serverless environments that require the client-side application to directly upload files to a cloud storage system such as Amazon S3.

### [File Metadata](#file-metadata)

In addition to reading and writing files, Laravel can also provide information about the files themselves. For example, the `size` method may be used to get the size of a file in bytes:

```
1use Illuminate\Support\Facades\Storage;

2 

3$size = Storage::size('file.jpg');
```

The `lastModified` method returns the UNIX timestamp of the last time the file was modified:

```
1$time = Storage::lastModified('file.jpg');
```

The MIME type of a given file may be obtained via the `mimeType` method:

```
1$mime = Storage::mimeType('file.jpg');
```

#### [File Paths](#file-paths)

You may use the `path` method to get the path for a given file. If you are using the `local` driver, this will return the absolute path to the file. If you are using the `s3` driver, this method will return the relative path to the file in the S3 bucket:

```
1use Illuminate\Support\Facades\Storage;

2 

3$path = Storage::path('file.jpg');
```

## [Storing Files](#storing-files)

The `put` method may be used to store file contents on a disk. You may also pass a PHP `resource` to the `put` method, which will use Flysystem's underlying stream support. Remember, all file paths should be specified relative to the "root" location configured for the disk:

```
1use Illuminate\Support\Facades\Storage;

2 

3Storage::put('file.jpg', $contents);

4 

5Storage::put('file.jpg', $resource);
```

#### [Failed Writes](#failed-writes)

If the `put` method (or other "write" operations) is unable to write the file to disk, `false` will be returned:

```
1if (! Storage::put('file.jpg', $contents)) {

2    // The file could not be written to disk...

3}
```

If you wish, you may define the `throw` option within your filesystem disk's configuration array. When this option is defined as `true`, "write" methods such as `put` will throw an instance of `League\Flysystem\UnableToWriteFile` when write operations fail:

```
1'public' => [

2    'driver' => 'local',

3    // ...

4    'throw' => true,

5],
```

### [Prepending and Appending To Files](#prepending-appending-to-files)

The `prepend` and `append` methods allow you to write to the beginning or end of a file:

```
1Storage::prepend('file.log', 'Prepended Text');

2 

3Storage::append('file.log', 'Appended Text');
```

### [Copying and Moving Files](#copying-moving-files)

The `copy` method may be used to copy an existing file to a new location on the disk, while the `move` method may be used to rename or move an existing file to a new location:

```
1Storage::copy('old/file.jpg', 'new/file.jpg');

2 

3Storage::move('old/file.jpg', 'new/file.jpg');
```

### [Automatic Streaming](#automatic-streaming)

Streaming files to storage offers significantly reduced memory usage. If you would like Laravel to automatically manage streaming a given file to your storage location, you may use the `putFile` or `putFileAs` method. This method accepts either an `Illuminate\Http\File` or `Illuminate\Http\UploadedFile` instance and will automatically stream the file to your desired location:

```
1use Illuminate\Http\File;

2use Illuminate\Support\Facades\Storage;

3 

4// Automatically generate a unique ID for filename...

5$path = Storage::putFile('photos', new File('/path/to/photo'));

6 

7// Manually specify a filename...

8$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

There are a few important things to note about the `putFile` method. Note that we only specified a directory name and not a filename. By default, the `putFile` method will generate a unique ID to serve as the filename. The file's extension will be determined by examining the file's MIME type. The path to the file will be returned by the `putFile` method so you can store the path, including the generated filename, in your database.

The `putFile` and `putFileAs` methods also accept an argument to specify the "visibility" of the stored file. This is particularly useful if you are storing the file on a cloud disk such as Amazon S3 and would like the file to be publicly accessible via generated URLs:

```
1Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

### [File Uploads](#file-uploads)

In web applications, one of the most common use-cases for storing files is storing user uploaded files such as photos and documents. Laravel makes it very easy to store uploaded files using the `store` method on an uploaded file instance. Call the `store` method with the path at which you wish to store the uploaded file:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Http\Request;

 6 

 7class UserAvatarController extends Controller

 8{

 9    /**

10     * Update the avatar for the user.

11     */

12    public function update(Request $request): string

13    {

14        $path = $request->file('avatar')->store('avatars');

15 

16        return $path;

17    }

18}
```

There are a few important things to note about this example. Note that we only specified a directory name, not a filename. By default, the `store` method will generate a unique ID to serve as the filename. The file's extension will be determined by examining the file's MIME type. The path to the file will be returned by the `store` method so you can store the path, including the generated filename, in your database.

You may also call the `putFile` method on the `Storage` facade to perform the same file storage operation as the example above:

```
1$path = Storage::putFile('avatars', $request->file('avatar'));
```

#### [Specifying a File Name](#specifying-a-file-name)

If you do not want a filename to be automatically assigned to your stored file, you may use the `storeAs` method, which receives the path, the filename, and the (optional) disk as its arguments:

```
1$path = $request->file('avatar')->storeAs(

2    'avatars', $request->user()->id

3);
```

You may also use the `putFileAs` method on the `Storage` facade, which will perform the same file storage operation as the example above:

```
1$path = Storage::putFileAs(

2    'avatars', $request->file('avatar'), $request->user()->id

3);
```

Unprintable and invalid unicode characters will automatically be removed from file paths. Therefore, you may wish to sanitize your file paths before passing them to Laravel's file storage methods. File paths are normalized using the `League\Flysystem\WhitespacePathNormalizer::normalizePath` method.

#### [Specifying a Disk](#specifying-a-disk)

By default, this uploaded file's `store` method will use your default disk. If you would like to specify another disk, pass the disk name as the second argument to the `store` method:

```
1$path = $request->file('avatar')->store(

2    'avatars/'.$request->user()->id, 's3'

3);
```

If you are using the `storeAs` method, you may pass the disk name as the third argument to the method:

```
1$path = $request->file('avatar')->storeAs(

2    'avatars',

3    $request->user()->id,

4    's3'

5);
```

#### [Other Uploaded File Information](#other-uploaded-file-information)

If you would like to get the original name and extension of the uploaded file, you may do so using the `getClientOriginalName` and `getClientOriginalExtension` methods:

```
1$file = $request->file('avatar');

2 

3$name = $file->getClientOriginalName();

4$extension = $file->getClientOriginalExtension();
```

However, keep in mind that the `getClientOriginalName` and `getClientOriginalExtension` methods are considered unsafe, as the file name and extension may be tampered with by a malicious user. For this reason, you should typically prefer the `hashName` and `extension` methods to get a name and an extension for the given file upload:

```
1$file = $request->file('avatar');

2 

3$name = $file->hashName(); // Generate a unique, random name...

4$extension = $file->extension(); // Determine the file's extension based on the file's MIME type...
```

### [File Visibility](#file-visibility)

In Laravel's Flysystem integration, "visibility" is an abstraction of file permissions across multiple platforms. Files may either be declared `public` or `private`. When a file is declared `public`, you are indicating that the file should generally be accessible to others. For example, when using the S3 driver, you may retrieve URLs for `public` files.

You can set the visibility when writing the file via the `put` method:

```
1use Illuminate\Support\Facades\Storage;

2 

3Storage::put('file.jpg', $contents, 'public');
```

If the file has already been stored, its visibility can be retrieved and set via the `getVisibility` and `setVisibility` methods:

```
1$visibility = Storage::getVisibility('file.jpg');

2 

3Storage::setVisibility('file.jpg', 'public');
```

When interacting with uploaded files, you may use the `storePublicly` and `storePubliclyAs` methods to store the uploaded file with `public` visibility:

```
1$path = $request->file('avatar')->storePublicly('avatars', 's3');

2 

3$path = $request->file('avatar')->storePubliclyAs(

4    'avatars',

5    $request->user()->id,

6    's3'

7);
```

### [Image Manipulation](#image-manipulation)

If you need to resize, crop, or convert an uploaded image before storing it, you may use Laravel's [image manipulation features](/docs/13.x/images):

```
1$path = $request->image('avatar')

2    ->cover(400, 400)

3    ->toWebp()

4    ->storePublicly('avatars', 'public');
```

You may also create an image instance from a file already stored on one of your filesystem disks:

```
1$image = Storage::disk('public')->image('avatars/photo.jpg');
```

#### [Local Files and Visibility](#local-files-and-visibility)

When using the `local` driver, `public` [visibility](#file-visibility) translates to `0755` permissions for directories and `0644` permissions for files. You can modify the permissions mappings in your application's `filesystems` configuration file:

```
 1'local' => [

 2    'driver' => 'local',

 3    'root' => storage_path('app'),

 4    'permissions' => [

 5        'file' => [

 6            'public' => 0644,

 7            'private' => 0600,

 8        ],

 9        'dir' => [

10            'public' => 0755,

11            'private' => 0700,

12        ],

13    ],

14    'throw' => false,

15],
```

## [Deleting Files](#deleting-files)

The `delete` method accepts a single filename or an array of files to delete:

```
1use Illuminate\Support\Facades\Storage;

2 

3Storage::delete('file.jpg');

4 

5Storage::delete(['file.jpg', 'file2.jpg']);
```

If necessary, you may specify the disk that the file should be deleted from:

```
1use Illuminate\Support\Facades\Storage;

2 

3Storage::disk('s3')->delete('path/file.jpg');
```

## [Directories](#directories)

#### [Get All Files Within a Directory](#get-all-files-within-a-directory)

The `files` method returns an array of all files within a given directory. If you would like to retrieve a list of all files within a given directory including subdirectories, you may use the `allFiles` method:

```
1use Illuminate\Support\Facades\Storage;

2 

3$files = Storage::files($directory);

4 

5$files = Storage::allFiles($directory);
```

#### [Get All Directories Within a Directory](#get-all-directories-within-a-directory)

The `directories` method returns an array of all directories within a given directory. If you would like to retrieve a list of all directories within a given directory including subdirectories, you may use the `allDirectories` method:

```
1$directories = Storage::directories($directory);

2 

3$directories = Storage::allDirectories($directory);
```

#### [Create a Directory](#create-a-directory)

The `makeDirectory` method will create the given directory, including any needed subdirectories:

```
1Storage::makeDirectory($directory);
```

#### [Delete a Directory](#delete-a-directory)

Finally, the `deleteDirectory` method may be used to remove a directory and all of its files:

```
1Storage::deleteDirectory($directory);
```

## [Testing](#testing)

The `Storage` facade's `fake` method allows you to easily generate a fake disk that, combined with the file generation utilities of the `Illuminate\Http\UploadedFile` class, greatly simplifies the testing of file uploads. For example:

Pest

PHPUnit

```
 1<?php

 2 

 3use Illuminate\Http\UploadedFile;

 4use Illuminate\Support\Facades\Storage;

 5 

 6test('albums can be uploaded', function () {

 7    Storage::fake('photos');

 8 

 9    $response = $this->json('POST', '/photos', [

10        UploadedFile::fake()->image('photo1.jpg'),

11        UploadedFile::fake()->image('photo2.jpg')

12    ]);

13 

14    // Assert one or more files were stored...

15    Storage::disk('photos')->assertExists('photo1.jpg');

16    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

17 

18    // Assert one or more files were not stored...

19    Storage::disk('photos')->assertMissing('missing.jpg');

20    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

21 

22    // Assert that the number of files in a given directory matches the expected count...

23    Storage::disk('photos')->assertCount('/wallpapers', 2);

24 

25    // Assert that a given directory is empty...

26    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

27 

28    // Assert that the disk contains no files...

29    Storage::disk('photos')->assertEmpty();

30});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use Illuminate\Http\UploadedFile;

 6use Illuminate\Support\Facades\Storage;

 7use Tests\TestCase;

 8 

 9class ExampleTest extends TestCase

10{

11    public function test_albums_can_be_uploaded(): void

12    {

13        Storage::fake('photos');

14 

15        $response = $this->json('POST', '/photos', [

16            UploadedFile::fake()->image('photo1.jpg'),

17            UploadedFile::fake()->image('photo2.jpg')

18        ]);

19 

20        // Assert one or more files were stored...

21        Storage::disk('photos')->assertExists('photo1.jpg');

22        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

23 

24        // Assert one or more files were not stored...

25        Storage::disk('photos')->assertMissing('missing.jpg');

26        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

27 

28        // Assert that the number of files in a given directory matches the expected count...

29        Storage::disk('photos')->assertCount('/wallpapers', 2);

30 

31        // Assert that a given directory is empty...

32        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

33 

34        // Assert that the disk contains no files...

35        Storage::disk('photos')->assertEmpty();

36    }

37}
```

By default, the `fake` method will delete all files in its temporary directory. If you would like to keep these files, you may use the "persistentFake" method instead. For more information on testing file uploads, you may consult the [HTTP testing documentation's information on file uploads](/docs/13.x/http-tests#testing-file-uploads).

The `image` method requires the [GD extension](https://www.php.net/manual/en/book.image.php).

## [Custom Filesystems](#custom-filesystems)

Laravel's Flysystem integration provides support for several "drivers" out of the box; however, Flysystem is not limited to these and has adapters for many other storage systems. You can create a custom driver if you want to use one of these additional adapters in your Laravel application.

In order to define a custom filesystem you will need a Flysystem adapter. Let's add a community maintained Dropbox adapter to our project:

```
1composer require spatie/flysystem-dropbox
```

Next, you can register the driver within the `boot` method of one of your application's [service providers](/docs/13.x/providers). To accomplish this, you should use the `extend` method of the `Storage` facade:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Contracts\Foundation\Application;

 6use Illuminate\Filesystem\FilesystemAdapter;

 7use Illuminate\Support\Facades\Storage;

 8use Illuminate\Support\ServiceProvider;

 9use League\Flysystem\Filesystem;

10use Spatie\Dropbox\Client as DropboxClient;

11use Spatie\FlysystemDropbox\DropboxAdapter;

12 

13class AppServiceProvider extends ServiceProvider

14{

15    /**

16     * Register any application services.

17     */

18    public function register(): void

19    {

20        // ...

21    }

22 

23    /**

24     * Bootstrap any application services.

25     */

26    public function boot(): void

27    {

28        Storage::extend('dropbox', function (Application $app, array $config) {

29            $adapter = new DropboxAdapter(new DropboxClient(

30                $config['authorization_token']

31            ));

32 

33            return new FilesystemAdapter(

34                new Filesystem($adapter, $config),

35                $adapter,

36                $config

37            );

38        });

39    }

40}
```

The first argument of the `extend` method is the name of the driver and the second is a closure that receives the `$app` and `$config` variables. The closure must return an instance of `Illuminate\Filesystem\FilesystemAdapter`. The `$config` variable contains the values defined in `config/filesystems.php` for the specified disk.

Once you have created and registered the extension's service provider, you may use the `dropbox` driver in your `config/filesystems.php` configuration file.
