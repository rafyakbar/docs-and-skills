[Infolists](/docs/5.x/infolists/overview)

# Icon entry

## [​](#introduction)Introduction

Icon entries render an [icon](../styling/icons) representing the state of the entry:

```
use Filament\Infolists\Components\IconEntry;
use Filament\Support\Icons\Heroicon;

IconEntry::make('status')
    ->icon(fn (string $state): Heroicon => match ($state) {
        'draft' => Heroicon::OutlinedPencil,
        'reviewing' => Heroicon::OutlinedClock,
        'published' => Heroicon::OutlinedCheckCircle,
    })
```

## [​](#customizing-the-color)Customizing the color

You may change the [color](../styling/colors) of the icon, using the `color()` method:

```
use Filament\Infolists\Components\IconEntry;

IconEntry::make('status')
    ->color('success')
```

By passing a function to `color()`, you can customize the color based on the state of the entry:

```
use Filament\Infolists\Components\IconEntry;

IconEntry::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'info',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    })
```

## [​](#customizing-the-size)Customizing the size

The default icon size is `IconSize::Large`, but you may customize the size to be either `IconSize::ExtraSmall`, `IconSize::Small`, `IconSize::Medium`, `IconSize::ExtraLarge` or `IconSize::TwoExtraLarge`:

```
use Filament\Infolists\Components\IconEntry;
use Filament\Support\Enums\IconSize;

IconEntry::make('status')
    ->size(IconSize::Medium)
```

## [​](#handling-booleans)Handling booleans

Icon entries can display a check or “X” icon based on the state of the entry, either true or false, using the `boolean()` method:

```
use Filament\Infolists\Components\IconEntry;

IconEntry::make('is_featured')
    ->boolean()
```
> If this attribute in the model class is already cast as a `bool` or `boolean`, Filament is able to detect this, and you do not need to use `boolean()` manually.

Optionally, you may pass a boolean value to control if the icon should be boolean or not:

```
use Filament\Infolists\Components\IconEntry;

IconEntry::make('is_featured')
    ->boolean(FeatureFlag::active())
```

### [​](#customizing-the-boolean-icons)Customizing the boolean icons

You may customize the [icon](../styling/icons) representing each state:

```
use Filament\Infolists\Components\IconEntry;
use Filament\Support\Icons\Heroicon;

IconEntry::make('is_featured')
    ->boolean()
    ->trueIcon(Heroicon::OutlinedCheckBadge)
    ->falseIcon(Heroicon::OutlinedXMark)
```

### [​](#customizing-the-boolean-colors)Customizing the boolean colors

You may customize the icon [color](../styling/colors) representing each state:

```
use Filament\Infolists\Components\IconEntry;

IconEntry::make('is_featured')
    ->boolean()
    ->trueColor('info')
    ->falseColor('warning')
```

[Text entry](/docs/5.x/infolists/text-entry)[Image entry](/docs/5.x/infolists/image-entry)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
