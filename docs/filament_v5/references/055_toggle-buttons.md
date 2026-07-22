[Forms](/docs/5.x/forms/overview)

# Toggle buttons

## [​](#introduction)Introduction

The toggle buttons input provides a group of buttons for selecting a single value, or multiple values, from a list of predefined options:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])
```

## [​](#changing-the-color-of-option-buttons)Changing the color of option buttons

You can change the [color](../styling/colors) of the option buttons using the `colors()` method. Each key in the array should correspond to an option value:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])
    ->colors([
        'draft' => 'info',
        'scheduled' => 'warning',
        'published' => 'success',
    ])
```

If you are using an enum for the options, you can use the [`HasColor` interface](../advanced/enums#enum-colors) to define colors instead.

## [​](#adding-icons-to-option-buttons)Adding icons to option buttons

You can add [icon](../styling/icons) to the option buttons using the `icons()` method. Each key in the array should correspond to an option value, and the value may be any valid [icon](../styling/icons):

```
use Filament\Forms\Components\ToggleButtons;
use Filament\Support\Icons\Heroicon;

ToggleButtons::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])
    ->icons([
        'draft' => Heroicon::OutlinedPencil,
        'scheduled' => Heroicon::OutlinedClock,
        'published' => Heroicon::OutlinedCheckCircle,
    ])
```

If you are using an enum for the options, you can use the [`HasIcon` interface](../advanced/enums#enum-icons) to define icons instead. If you want to display only icons, you can use `hiddenButtonLabels()` to hide the option labels.

## [​](#adding-tooltips-to-option-buttons)Adding tooltips to option buttons

You can add different tooltips to each option button using the `tooltips()` method.

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published',
    ])
    ->tooltips([
        'draft' => 'Set as a draft before publishing.',
        'scheduled' => 'Schedule publishing on a specific date.',
        'published' => 'Publish now',
    ])
```

## [​](#boolean-options)Boolean options

If you want a simple boolean toggle button group, with “Yes” and “No” options, you can use the `boolean()` method:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('feedback')
    ->label('Like this post?')
    ->boolean()
```

The options will have [colors](#changing-the-color-of-option-buttons) and [icons](#adding-icons-to-option-buttons) set up automatically, but you can override these with `colors()` or `icons()`. To customize the “Yes” label, you can use the `trueLabel` argument on the `boolean()` method:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('feedback')
    ->label('Like this post?')
    ->boolean(trueLabel: 'Absolutely!')
```

To customize the “No” label, you can use the `falseLabel` argument on the `boolean()` method:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('feedback')
    ->label('Like this post?')
    ->boolean(falseLabel: 'Not at all!')
```

## [​](#positioning-the-options-inline-with-each-other)Positioning the options inline with each other

You may wish to display the buttons `inline()` with each other:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->inline()
```

Optionally, you may pass a boolean value to control if the buttons should be inline or not:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->inline(FeatureFlag::active())
```

## [​](#grouping-option-buttons)Grouping option buttons

You may wish to group option buttons together so they are more compact, using the `grouped()` method. This also makes them appear horizontally inline with each other:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->grouped()
```

Optionally, you may pass a boolean value to control if the buttons should be grouped or not:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->grouped(FeatureFlag::active())
```

## [​](#selecting-multiple-buttons)Selecting multiple buttons

The `multiple()` method on the `ToggleButtons` component allows you to select multiple values from the list of options:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('technologies')
    ->multiple()
    ->options([
        'tailwind' => 'Tailwind CSS',
        'alpine' => 'Alpine.js',
        'laravel' => 'Laravel',
        'livewire' => 'Laravel Livewire',
    ])
```

These options are returned in JSON format. If you’re saving them using Eloquent, you should be sure to add an `array` [cast](https://laravel.com/docs/eloquent-mutators#array-and-json-casting) to the model property:

```
use Illuminate\Database\Eloquent\Model;

class App extends Model
{
    /**
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'technologies' => 'array',
        ];
    }

    // ...
}
```

Optionally, you may pass a boolean value to control if the buttons should allow multiple selections or not:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('technologies')
    ->multiple(FeatureFlag::active())
    ->options([
        'tailwind' => 'Tailwind CSS',
        'alpine' => 'Alpine.js',
        'laravel' => 'Laravel',
        'livewire' => 'Laravel Livewire',
    ])
```

## [​](#splitting-options-into-columns)Splitting options into columns

You may split options into columns by using the `columns()` method:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('technologies')
    ->options([
        // ...
    ])
    ->columns(2)
```

This method accepts the same options as the `columns()` method of the [grid](../schemas/layouts#grid-system). This allows you to responsively customize the number of columns at various breakpoints.

### [​](#setting-the-grid-direction)Setting the grid direction

By default, when you arrange buttons into columns, they will be listed in order vertically. If you’d like to list them horizontally, you may use the `gridDirection(GridDirection::Row)` method:

```
use Filament\Forms\Components\ToggleButtons;
use Filament\Support\Enums\GridDirection;

ToggleButtons::make('technologies')
    ->options([
        // ...
    ])
    ->columns(2)
    ->gridDirection(GridDirection::Row)
```

## [​](#disabling-specific-options)Disabling specific options

You can disable specific options using the `disableOptionWhen()` method. It accepts a closure, in which you can check if the option with a specific `$value` should be disabled:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published',
    ])
    ->disableOptionWhen(fn (string $value): bool => $value === 'published')
```

If you want to retrieve the options that have not been disabled, e.g. for validation purposes, you can do so using `getEnabledOptions()`:

```
use Filament\Forms\Components\ToggleButtons;

ToggleButtons::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published',
    ])
    ->disableOptionWhen(fn (string $value): bool => $value === 'published')
    ->in(fn (ToggleButtons $component): array => array_keys($component->getEnabledOptions()))
```

For more information about the `in()` function, please see the [Validation documentation](./validation#in).

[Color picker](/docs/5.x/forms/color-picker)[Slider](/docs/5.x/forms/slider)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
