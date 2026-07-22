[Actions](/docs/5.x/actions/overview)

# Force-delete action

## [​](#introduction)Introduction

Filament includes an action that is able to force-delete [soft-deleted](https://laravel.com/docs/eloquent#soft-deleting) Eloquent records. When the trigger button is clicked, a modal asks the user for confirmation. You may use it like so:

```
use Filament\Actions\ForceDeleteAction;

ForceDeleteAction::make()
```

Or if you want to add it as a table bulk action, so that the user can choose which rows to force-delete, use `Filament\Actions\ForceDeleteBulkAction`:

```
use Filament\Actions\ForceDeleteBulkAction;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            ForceDeleteBulkAction::make(),
        ]);
}
```

## [​](#redirecting-after-force-deleting)Redirecting after force-deleting

You may set up a custom redirect when the form is submitted using the `successRedirectUrl()` method:

```
use Filament\Actions\ForceDeleteAction;

ForceDeleteAction::make()
    ->successRedirectUrl(route('posts.list'))
```

## [​](#customizing-the-force-delete-notification)Customizing the force-delete notification

When the record is successfully force-deleted, a notification is dispatched to the user, which indicates the success of their action. To customize the title of this notification, use the `successNotificationTitle()` method:

```
use Filament\Actions\ForceDeleteAction;

ForceDeleteAction::make()
    ->successNotificationTitle('User force-deleted')
```

You may customize the entire notification using the `successNotification()` method:

```
use Filament\Actions\ForceDeleteAction;
use Filament\Notifications\Notification;

ForceDeleteAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User force-deleted')
            ->body('The user has been force-deleted successfully.'),
    )
```

To disable the notification altogether, use the `successNotification(null)` method:

```
use Filament\Actions\ForceDeleteAction;

ForceDeleteAction::make()
    ->successNotification(null)
```

## [​](#lifecycle-hooks)Lifecycle hooks

You can use the `before()` and `after()` methods to execute code before and after a record is force-deleted:

```
use Filament\Actions\ForceDeleteAction;

ForceDeleteAction::make()
    ->before(function () {
        // ...
    })
    ->after(function () {
        // ...
    })
```

## [​](#improving-the-performance-of-force-delete-bulk-actions)Improving the performance of force-delete bulk actions

By default, the `ForceDeleteBulkAction` will load all Eloquent records into memory, before looping over them and deleting them one by one. If you are deleting a large number of records, you may want to use the `chunkSelectedRecords()` method to fetch a smaller number of records at a time. This will reduce the memory usage of your application:

```
use Filament\Actions\ForceDeleteBulkAction;

ForceDeleteBulkAction::make()
    ->chunkSelectedRecords(250)
```

Filament loads Eloquent records into memory before deleting them for two reasons:

- To allow individual records in the collection to be authorized with a model policy before deletion (using `authorizeIndividualRecords('forceDelete')`, for example).
- To ensure that model events are run when deleting records, such as the `forceDeleting` and `forceDeleted` events in a model observer.If you do not require individual record policy authorization and model events, you can use the `fetchSelectedRecords(false)` method, which will not fetch the records into memory before deleting them, and instead will delete them in a single query:

```
use Filament\Actions\ForceDeleteBulkAction;

ForceDeleteBulkAction::make()
    ->fetchSelectedRecords(false)
```

[Replicate action](/docs/5.x/actions/replicate)[Restore action](/docs/5.x/actions/restore)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
