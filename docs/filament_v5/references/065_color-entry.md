[Infolists](/docs/5.x/infolists/overview)

# Color entry

## [​](#introduction)Introduction

The color entry allows you to show the color preview from a CSS color definition, typically entered using the [color picker field](../forms/color-picker), in one of the supported formats (HEX, HSL, RGB, RGBA).

```
use Filament\Infolists\Components\ColorEntry;

ColorEntry::make('color')
```

## [​](#allowing-the-color-to-be-copied-to-the-clipboard)Allowing the color to be copied to the clipboard

You may make the color copyable, such that clicking on the preview copies the CSS value to the clipboard, and optionally specify a custom confirmation message and duration in milliseconds. This feature only works when SSL is enabled for the app.

```
use Filament\Infolists\Components\ColorEntry;

ColorEntry::make('color')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
```

Optionally, you may pass a boolean value to control if the color should be copyable or not:

```
use Filament\Infolists\Components\ColorEntry;

ColorEntry::make('color')
    ->copyable(FeatureFlag::active())
```

[Image entry](/docs/5.x/infolists/image-entry)[Code entry](/docs/5.x/infolists/code-entry)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
