[Infolists](/docs/5.x/infolists/overview)

# Image entry

## [​](#introduction)Introduction

Infolists can render images, based on the path in the state of the entry:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
```

In this case, the `header_image` state could contain `posts/header-images/4281246003439.jpg`, which is relative to the root directory of the storage disk. The storage disk is defined in the [configuration file](/docs/5.x/introduction/installation#publishing-configuration), `local` by default. You can also set the `FILESYSTEM_DISK` environment variable to change this. Alternatively, the state could contain an absolute URL to an image, such as `https://example.com/images/header.jpg`.

## [​](#setting-the-alt-text)Setting the alt text

You should set descriptive alt text on your images so that screen reader users understand what each image shows. Use the `alt()` method:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->alt('Article header image')
```

If you do not set any alt text, the image is rendered with an empty `alt` attribute, which marks it as decorative for assistive technology.

When an image [links to a URL](/docs/5.x/infolists/overview#opening-a-url-when-an-entry-is-clicked), its alt text becomes the accessible name of the link. Always set meaningful `alt()` text on linked images, otherwise screen reader users will encounter a link with no name.

## [​](#managing-the-image-disk)Managing the image disk

The default storage disk is defined in the [configuration file](/docs/5.x/introduction/installation#publishing-configuration), `local` by default. You can also set the `FILESYSTEM_DISK` environment variable to change this. If you want to deviate from the default disk, you may pass a custom disk name to the `disk()` method:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->disk('s3')
```

## [​](#public-images)Public images

By default, Filament will generate temporary URLs to images in the filesystem, unless the [disk](#managing-the-image-disk) is set to `public`. If your images are stored in a public disk, you can set the `visibility()` to `public`:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->visibility('public')
```

## [​](#customizing-the-size)Customizing the size

You may customize the image size by passing a `imageWidth()` and `imageHeight()`, or both with `imageSize()`:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->imageWidth(200)

ImageEntry::make('header_image')
    ->imageHeight(50)

ImageEntry::make('author.avatar')
    ->imageSize(40)
```

### [​](#square-images)Square images

You may display the image using a 1:1 aspect ratio:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->square()
```

Optionally, you may pass a boolean value to control if the image should be square or not:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->square(FeatureFlag::active())
```

## [​](#circular-images)Circular images

You may make the image fully rounded, which is useful for rendering avatars:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->circular()
```

Optionally, you may pass a boolean value to control if the image should be circular or not:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->circular(FeatureFlag::active())
```

## [​](#adding-a-default-image-url)Adding a default image URL

You can display a placeholder image if one doesn’t exist yet, by passing a URL to the `defaultImageUrl()` method:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->defaultImageUrl(url('storage/posts/header-images/default.jpg'))
```

## [​](#stacking-images)Stacking images

You may display multiple images as a stack of overlapping images by using `stacked()`:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
```

Optionally, you may pass a boolean value to control if the images should be stacked or not:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked(FeatureFlag::active())
```

### [​](#customizing-the-stacked-ring-width)Customizing the stacked ring width

The default ring width is `3`, but you may customize it to be from `0` to `8`:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->ring(5)
```

### [​](#customizing-the-stacked-overlap)Customizing the stacked overlap

The default overlap is `4`, but you may customize it to be from `0` to `8`:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->overlap(2)
```

## [​](#setting-a-limit)Setting a limit

You may limit the maximum number of images you want to display by passing `limit()`:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
```

### [​](#showing-the-remaining-images-count)Showing the remaining images count

When you set a limit you may also display the count of remaining images by passing `limitedRemainingText()`.

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText()
```

Optionally, you may pass a boolean value to control if the remaining text should be displayed or not:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText(FeatureFlag::active())
```

#### [​](#customizing-the-limited-remaining-text-size)Customizing the limited remaining text size

By default, the size of the remaining text is `TextSize::Small`. You can customize this to be `TextSize::ExtraSmall`, `TextSize::Medium` or `TextSize::Large` using the `size` parameter:

```
use Filament\Infolists\Components\ImageEntry;
use Filament\Support\Enums\TextSize;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText(size: TextSize::Large)
```

## [​](#prevent-file-existence-checks)Prevent file existence checks

When the schema is loaded, it will automatically detect whether the images exist to prevent errors for missing files. This is all done on the backend. When using remote storage with many images, this can be time-consuming. You can use the `checkFileExistence(false)` method to disable this feature:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('attachment')
    ->checkFileExistence(false)
```

## [​](#adding-extra-html-attributes-to-the-image)Adding extra HTML attributes to the image

You can pass extra HTML attributes to the `<img>` element via the `extraImgAttributes()` method. The attributes should be represented by an array, where the key is the attribute name and the value is the attribute value:

```
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('logo')
    ->extraImgAttributes([
        'alt' => 'Logo',
        'loading' => 'lazy',
    ])
```

By default, calling `extraImgAttributes()` multiple times will overwrite the previous attributes. If you wish to merge the attributes instead, you can pass `merge: true` to the method.

[Icon entry](/docs/5.x/infolists/icon-entry)[Color entry](/docs/5.x/infolists/color-entry)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
