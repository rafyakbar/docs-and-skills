[Schemas](/docs/5.x/schemas/overview)

# Tabs

## [​](#introduction)Introduction

Some schemas can be long and complex. You may want to use tabs to reduce the number of components that are visible at once:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
```

## [​](#setting-the-default-active-tab)Setting the default active tab

The first tab will be open by default. You can change the default open tab using the `activeTab()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->activeTab(2)
```

## [​](#setting-a-tab-icon)Setting a tab icon

Tabs may have an [icon](/docs/5.x/styling/icons), which you can set using the `icon()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;
use Filament\Support\Icons\Heroicon;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Notifications')
            ->icon(Heroicon::Bell)
            ->schema([
                // ...
            ]),
        // ...
    ])
```

### [​](#setting-the-tab-icon-position)Setting the tab icon position

The icon of the tab may be positioned before or after the label using the `iconPosition()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;
use Filament\Support\Enums\IconPosition;
use Filament\Support\Icons\Heroicon;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Notifications')
            ->icon(Heroicon::Bell)
            ->iconPosition(IconPosition::After)
            ->schema([
                // ...
            ]),
        // ...
    ])
```

## [​](#setting-a-tab-badge)Setting a tab badge

Tabs may have a badge, which you can set using the `badge()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Notifications')
            ->badge(5)
            ->schema([
                // ...
            ]),
        // ...
    ])
```

If you’d like to change the [color](/docs/5.x/styling/colors) for a badge, you can use the `badgeColor()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Notifications')
            ->badge(5)
            ->badgeColor('info')
            ->schema([
                // ...
            ]),
        // ...
    ])
```

### [​](#deferring-the-loading-of-tab-badges)Deferring the loading of tab badges

If you have expensive queries powering your tab badges, the initial page load may be slow. You can defer the loading of tab badges using the `deferBadge()` method, which will load the badge values asynchronously after the page has rendered:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->key('notifications-tabs')
    ->tabs([
        Tab::make('Notifications')
            ->badge(static fn (): int => Notification::query()->where('unread', true->count())
            ->deferBadge()
            ->schema([
                // ...
            ]),
        // ...
    ])
```

The `badge()` value must be returned from a function when using `deferBadge()`. If you pass a raw value like `badge(Notification::query()->count())`, the query runs immediately when the tab is built, defeating the purpose of deferral.The `Tabs` component must have a `key()` set when using `deferBadge()`. Without a key, the deferred badge request cannot identify the correct component on the server.

While the badges are loading, a small loading indicator will appear in place of each deferred badge. Once the data is fetched, the loading indicators will be replaced with the actual badge values.

## [​](#using-grid-columns-within-a-tab)Using grid columns within a tab

You may use the `columns()` method to customize the [grid](/docs/5.x/schemas/layouts#grid-system) within the tab:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ])
            ->columns(3),
        // ...
    ])
```

## [​](#disabling-scrollable-tabs)Disabling scrollable tabs

Tabs are rendered horizontally by default, and are scrollable when they exceed the available width. You may disable scrolling using the `scrollable(false)` method:

```
use Filament\Schemas\Components\Tabs;

Tabs::make('Tabs')
    ->tabs([
        // ...
    ])
    ->scrollable(false)
```

When tabs are not scrollable, the component automatically detects the available width. If not all tabs can fit, a dropdown button will appear. Any tabs that exceed the available width will be grouped inside this dropdown automatically.

## [​](#using-vertical-tabs)Using vertical tabs

You can render the tabs vertically by using the `vertical()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->vertical()
```

Optionally, you can pass a boolean value to the `vertical()` method to control if the tabs should be rendered vertically or not:

```
use Filament\Schemas\Components\Tabs;

Tabs::make('Tabs')
    ->tabs([
        // ...
    ])
    ->vertical(FeatureFlag::active())
```

## [​](#removing-the-styled-container)Removing the styled container

By default, tabs and their content are wrapped in a container styled as a card. You may remove the styled container using `contained()`:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->contained(false)
```

## [​](#persisting-the-current-tab-in-the-user’s-session)Persisting the current tab in the user’s session

By default, the current tab is not persisted in the browser’s local storage. You can change this behavior using the `persistTab()` method. You must also pass in a unique `id()` for the tabs component, to distinguish it from all other sets of tabs in the app. This ID will be used as the key in the local storage to store the current tab:

```
use Filament\Schemas\Components\Tabs;

Tabs::make('Tabs')
    ->tabs([
        // ...
    ])
    ->persistTab()
    ->id('order-tabs')
```

Optionally, the `persistTab()` method accepts a boolean value to control if the active tab should persist or not:

```
use Filament\Schemas\Components\Tabs;

Tabs::make('Tabs')
    ->tabs([
        // ...
    ])
    ->persistTab(FeatureFlag::active())
    ->id('order-tabs')
```

### [​](#persisting-the-current-tab-in-the-url’s-query-string)Persisting the current tab in the URL’s query string

By default, the current tab is not persisted in the URL’s query string. You can change this behavior using the `persistTabInQueryString()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->persistTabInQueryString()
```

When enabled, the current tab is persisted in the URL’s query string using the `tab` key. You can change this key by passing it to the `persistTabInQueryString()` method:

```
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->persistTabInQueryString('settings-tab')
```

[Sections](/docs/5.x/schemas/sections)[Wizards](/docs/5.x/schemas/wizards)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
