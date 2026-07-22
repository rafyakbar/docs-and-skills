[Actions](/docs/5.x/actions/overview)

# Grouping actions

## [​](#introduction)Introduction

You may group actions together into a dropdown menu by using an `ActionGroup` object. Groups may contain many actions, or other groups:

```
use Filament\Actions\Action;
use Filament\Actions\ActionGroup;

ActionGroup::make([
    Action::make('view'),
    Action::make('edit'),
    Action::make('delete'),
])
```

This page is about customizing the look of the group’s trigger button and dropdown.

## [​](#customizing-the-group-trigger-style)Customizing the group trigger style

The button which opens the dropdown may be customized in the same way as a normal action. [All the methods available for trigger buttons](./overview) may be used to customize the group trigger button:

```
use Filament\Actions\ActionGroup;
use Filament\Support\Enums\Size;

ActionGroup::make([
    // Array of actions
])
    ->label('More actions')
    ->icon('heroicon-m-ellipsis-vertical')
    ->size(Size::Small)
    ->color('primary')
    ->button()
```

### [​](#adding-a-tooltip-to-the-group-trigger-button)Adding a tooltip to the group trigger button

You may add a tooltip to the group trigger button using the `tooltip()` method:

```
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->tooltip('Actions')
```

### [​](#using-a-grouped-button-design)Using a grouped button design

Instead of a dropdown, an action group can render itself as a group of buttons. This design works with and without button labels. To use this feature, use the `buttonGroup()` method:

```
use Filament\Actions\Action;
use Filament\Actions\ActionGroup;
use Filament\Support\Icons\Heroicon;

ActionGroup::make([
    Action::make('edit')
        ->color('gray')
        ->icon(Heroicon::PencilSquare)
        ->hiddenLabel(),
    Action::make('delete')
        ->color('gray')
        ->icon(Heroicon::Trash)
        ->hiddenLabel(),
])
    ->buttonGroup()
```

## [​](#setting-the-placement-of-the-dropdown)Setting the placement of the dropdown

The dropdown may be positioned relative to the trigger button by using the `dropdownPlacement()` method:

```
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->dropdownPlacement('top-start')
```

Alternatively, you may let the dropdown position be automatically determined based on the available space using the `dropdownAutoPlacement()` method:

```
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->dropdownAutoPlacement()
```

## [​](#adding-dividers-between-actions)Adding dividers between actions

You may add dividers between groups of actions by using nested `ActionGroup` objects:

```
use Filament\Actions\ActionGroup;

ActionGroup::make([
    ActionGroup::make([
        // Array of actions
    ])->dropdown(false),
    // Array of actions
])
```

The `dropdown(false)` method puts the actions inside the parent dropdown, instead of a new nested dropdown.

## [​](#setting-the-width-of-the-dropdown)Setting the width of the dropdown

The dropdown may be set to a width by using the `dropdownWidth()` method. Options correspond to [Tailwind’s max-width scale](https://tailwindcss.com/docs/max-width). The options are `ExtraSmall`, `Small`, `Medium`, `Large`, `ExtraLarge`, `TwoExtraLarge`, `ThreeExtraLarge`, `FourExtraLarge`, `FiveExtraLarge`, `SixExtraLarge` and `SevenExtraLarge`:

```
use Filament\Actions\ActionGroup;
use Filament\Support\Enums\Width;

ActionGroup::make([
    // Array of actions
])
    ->dropdownWidth(Width::ExtraSmall)
```

## [​](#controlling-the-dropdown-offset)Controlling the dropdown offset

You may control the offset of the dropdown using the `dropdownOffset()` method, by default the offset is set to `8`.

```
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->dropdownOffset(16)
```

## [​](#controlling-the-maximum-height-of-the-dropdown)Controlling the maximum height of the dropdown

The dropdown content can have a maximum height using the `maxHeight()` method, so that it scrolls. You can pass a [CSS length](https://developer.mozilla.org/en-US/docs/Web/CSS/length):

```
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->maxHeight('400px')
```

[Modals](/docs/5.x/actions/modals)[Create action](/docs/5.x/actions/create)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
