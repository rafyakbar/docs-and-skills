[Forms](/docs/5.x/forms/overview)

# Color picker

## [​](#introduction)Introduction

The color picker component allows you to pick a color in a range of formats. By default, the component uses HEX format:

```
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('color')
```

Clicking the color swatch opens a color picker panel where users can visually select a color:

## [​](#setting-the-color-format)Setting the color format

While HEX format is used by default, you can choose which color format to use:

```
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('hsl_color')
    ->hsl()

ColorPicker::make('rgb_color')
    ->rgb()

ColorPicker::make('rgba_color')
    ->rgba()
```

## [​](#color-picker-validation)Color picker validation

You may use Laravel’s validation rules to validate the values of the color picker:

```
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('hex_color')
    ->regex('/^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b$/')

ColorPicker::make('hsl_color')
    ->hsl()
    ->regex('/^hsl\(\s*(\d+)\s*,\s*(\d*(?:\.\d+)?%)\s*,\s*(\d*(?:\.\d+)?%)\)$/')

ColorPicker::make('rgb_color')
    ->rgb()
    ->regex('/^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$/')

ColorPicker::make('rgba_color')
    ->rgba()
    ->regex('/^rgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d*(?:\.\d+)?)\)$/')
```

[Key-value](/docs/5.x/forms/key-value)[Toggle buttons](/docs/5.x/forms/toggle-buttons)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
