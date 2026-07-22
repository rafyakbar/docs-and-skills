[Tables](/docs/5.x/tables/overview)

# Empty state

## [​](#introduction)Introduction

The table’s “empty state” is rendered when there are no rows in the table.

## [​](#setting-the-empty-state-heading)Setting the empty state heading

To customize the heading of the empty state, use the `emptyStateHeading()` method:

```
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateHeading('No posts yet');
}
```

## [​](#setting-the-empty-state-description)Setting the empty state description

To customize the description of the empty state, use the `emptyStateDescription()` method:

```
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateDescription('Once you write your first post, it will appear here.');
}
```

## [​](#setting-the-empty-state-icon)Setting the empty state icon

To customize the [icon](../styling/icons) of the empty state, use the `emptyStateIcon()` method:

```
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateIcon('heroicon-o-bookmark');
}
```

## [​](#adding-empty-state-actions)Adding empty state actions

You can add [Actions](./actions) to the empty state to prompt users to take action. Pass these to the `emptyStateActions()` method:

```
use Filament\Actions\Action;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateActions([
            Action::make('create')
                ->label('Create post')
                ->url(route('posts.create'))
                ->icon('heroicon-m-plus')
                ->button(),
        ]);
}
```

## [​](#using-a-custom-empty-state-view)Using a custom empty state view

You may use a completely custom empty state view by passing it to the `emptyState()` method:

```
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyState(view('tables.posts.empty-state'));
}
```

[Grouping rows](/docs/5.x/tables/grouping)[Custom data](/docs/5.x/tables/custom-data)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
