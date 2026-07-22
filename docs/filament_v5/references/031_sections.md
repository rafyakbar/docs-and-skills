[Schemas](/docs/5.x/schemas/overview)

# Sections

## [​](#introduction)Introduction

You may want to separate your fields into sections, each with a heading and description. To do this, you can use a section component:

```
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
```

You can also use a section without a header, which just wraps the components in a simple card:

```
use Filament\Schemas\Components\Section;

Section::make()
    ->schema([
        // ...
    ])
```

## [​](#adding-an-icon-to-the-section’s-header)Adding an icon to the section’s header

You may add an [icon](../styling/icons) to the section’s header using the `icon()` method:

```
use Filament\Schemas\Components\Section;
use Filament\Support\Icons\Heroicon;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->icon(Heroicon::ShoppingBag)
    ->schema([
        // ...
    ])
```

## [​](#positioning-the-heading-and-description-aside)Positioning the heading and description aside

You may use the `aside()` to align heading & description on the left, and the components inside a card on the right:

```
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->aside()
    ->schema([
        // ...
    ])
```

Optionally, you may pass a boolean value to control if the section should be aside or not:

```
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->aside(FeatureFlag::active())
    ->schema([
        // ...
    ])
```

## [​](#collapsing-sections)Collapsing sections

Sections may be `collapsible()` to optionally hide long content:

```
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
```

Your sections may be `collapsed()` by default:

```
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsed()
```

Optionally, the `collapsible()` and `collapsed()` methods accept a boolean value to control if the section should be collapsible and collapsed or not:

```
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible(FeatureFlag::active())
    ->collapsed(FeatureFlag::active())
```

### [​](#persisting-collapsed-sections-in-the-user’s-session)Persisting collapsed sections in the user’s session

You can persist whether a section is collapsed in local storage using the `persistCollapsed()` method, so it will remain collapsed when the user refreshes the page:

```
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->persistCollapsed()
```

To persist the collapse state, the local storage needs a unique ID to store the state. This ID is generated based on the heading of the section. If your section does not have a heading, or if you have multiple sections with the same heading that you do not want to collapse together, you can manually specify the `id()` of that section to prevent an ID conflict:

```
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->persistCollapsed()
    ->id('order-cart')
```

Optionally, the `persistCollapsed()` method accepts a boolean value to control if the section should persist its collapsed state or not:

```
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->persistCollapsed(FeatureFlag::active())
```

## [​](#compact-section-styling)Compact section styling

When nesting sections, you can use a more compact styling:

```
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->compact()
```

Optionally, the `compact()` method accepts a boolean value to control if the section should be compact or not:

```
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->compact(FeatureFlag::active())
```

## [​](#secondary-section-styling)Secondary section styling

By default, sections have a contrasting background color, which makes them stand out against a gray background. Secondary styling gives the section a less contrasting background, so it is usually slightly darker. This is a better styling when the background color behind the section is the same color as the default section background color, for example when a section is nested inside another section. Secondary sections can be created using the `secondary()` method:

```
use Filament\Schemas\Components\Section;

Section::make('Notes')
    ->schema([
        // ...
    ])
    ->secondary()
    ->compact()
```

Optionally, the `secondary()` method accepts a boolean value to control if the section should be secondary or not:

```
use Filament\Schemas\Components\Section;

Section::make('Notes')
    ->schema([
        // ...
    ])
    ->secondary(FeatureFlag::active())
```

## [​](#inserting-actions-and-other-components-in-the-header-of-a-section)Inserting actions and other components in the header of a section

You may insert [actions](../actions) and any other schema component (usually [prime components](./primes)) into the header of a section by passing an array of components to the `afterHeader()` method:

```
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->afterHeader([
        Action::make('test'),
    ])
    ->schema([
        // ...
    ])
```

## [​](#inserting-actions-and-other-components-in-the-footer-of-a-section)Inserting actions and other components in the footer of a section

You may insert [actions](../actions) and any other schema component (usually [prime components](./primes)) into the footer of a section by passing an array of components to the `footer()` method:

```
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->footer([
        Action::make('test'),
    ])
```

## [​](#using-grid-columns-within-a-section)Using grid columns within a section

You may use the `columns()` method to easily create a [grid](./layouts#grid-system) within the section:

```
use Filament\Schemas\Components\Section;

Section::make('Heading')
    ->schema([
        // ...
    ])
    ->columns(2)
```

[Layouts](/docs/5.x/schemas/layouts)[Tabs](/docs/5.x/schemas/tabs)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
