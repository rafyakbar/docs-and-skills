[Schemas](/docs/5.x/schemas/overview)

# Empty states

## [​](#introduction)Introduction

You can display an empty state in your schema to communicate that there is no content to show yet, and to guide the user towards the next action. An empty state requires a heading, but can also have a `description()`, [`icon()`](#adding-an-icon-to-the-empty-state) and [`footer()`](#inserting-actions-and-other-components-in-the-footer-of-an-empty-state):

```
use Filament\Actions\Action;
use Filament\Schemas\Components\EmptyState;
use Filament\Support\Icons\Heroicon;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->icon(Heroicon::OutlinedUser)
    ->footer([
        Action::make('createUser')
            ->icon(Heroicon::Plus),
    ])
```

## [​](#adding-an-icon-to-the-empty-state)Adding an icon to the empty state

You may add an [icon](../styling/icons) to the empty state using the `icon()` method:

```
use Filament\Schemas\Components\EmptyState;
use Filament\Support\Icons\Heroicon;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->icon(Heroicon::OutlinedUser)
```

## [​](#inserting-actions-and-other-components-in-the-footer-of-an-empty-state)Inserting actions and other components in the footer of an empty state

You may insert [actions](../actions) and any other schema component (usually [prime components](./primes)) into the footer of an empty state by passing an array of components to the `footer()` method:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\EmptyState;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->footer([
        Action::make('createUser')
            ->icon(Heroicon::Plus),
    ])
```

## [​](#removing-the-empty-state-container)Removing the empty state container

By default, empty states have a background color, shadow and border. You may remove these styles and just render the content of the empty state without the container using `contained(false)`:

```
use Filament\Schemas\Components\EmptyState;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->contained(false)
```

[Callouts](/docs/5.x/schemas/callouts)[Prime components](/docs/5.x/schemas/primes)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
