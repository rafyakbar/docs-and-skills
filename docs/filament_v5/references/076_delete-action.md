[Actions](/docs/5.x/actions/overview)

# Delete action

## [​](#introduction)Introduction

Filament includes an action that is able to delete Eloquent records. When the trigger button is clicked, a modal asks the user for confirmation. You may use it like so:

```
use Filament\Actions\DeleteAction;

DeleteAction::make()
```

Or if you want to add it as a table bulk action, so that the user can choose which rows to delete, use `Filament\Actions\DeleteBulkAction`:

```
use Filament\Actions\DeleteBulkAction;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            DeleteBulkAction::make(),
        ]);
}
```

## [​](#redirecting-after-deleting)Redirecting after deleting

You may set up a custom redirect when the record is deleted using the `successRedirectUrl()` method:

```
use Filament\Actions\DeleteAction;

DeleteAction::make()
    ->successRedirectUrl(route('posts.list'))
```

## [​](#customizing-the-delete-notification)Customizing the delete notification

When the record is successfully deleted, a notification is dispatched to the user, which indicates the success of their action. To customize the title of this notification, use the `successNotificationTitle()` method:

```
use Filament\Actions\DeleteAction;

DeleteAction::make()
    ->successNotificationTitle('User deleted')
```

You may customize the entire notification using the `successNotification()` method:

```
use Filament\Actions\DeleteAction;
use Filament\Notifications\Notification;

DeleteAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User deleted')
            ->body('The user has been deleted successfully.'),
    )
```

To disable the notification altogether, use the `successNotification(null)` method:

```
use Filament\Actions\DeleteAction;

DeleteAction::make()
    ->successNotification(null)
```

## [​](#lifecycle-hooks)Lifecycle hooks

You can use the `before()` and `after()` methods to execute code before and after a record is deleted:

```
use Filament\Actions\DeleteAction;

DeleteAction::make()
    ->before(function () {
        // ...
    })
    ->after(function () {
        // ...
    })
```

## [​](#improving-the-performance-of-delete-bulk-actions)Improving the performance of delete bulk actions

By default, the `DeleteBulkAction` will load all Eloquent records into memory, before looping over them and deleting them one by one. If you are deleting a large number of records, you may want to use the `chunkSelectedRecords()` method to fetch a smaller number of records at a time. This will reduce the memory usage of your application:

```
use Filament\Actions\DeleteBulkAction;

DeleteBulkAction::make()
    ->chunkSelectedRecords(250)
```

Filament loads Eloquent records into memory before deleting them for two reasons:

- To allow individual records in the collection to be authorized with a model policy before deletion (using `authorizeIndividualRecords('delete')`, for example).
- To ensure that model events are run when deleting records, such as the `deleting` and `deleted` events in a model observer.If you do not require individual record policy authorization and model events, you can use the `fetchSelectedRecords(false)` method, which will not fetch the records into memory before deleting them, and instead will delete them in a single query:

```
use Filament\Actions\DeleteBulkAction;

DeleteBulkAction::make()
    ->fetchSelectedRecords(false)
```

[View action](/docs/5.x/actions/view)[Replicate action](/docs/5.x/actions/replicate)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
