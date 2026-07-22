[Actions](/docs/5.x/actions/overview)

# Restore action

## [​](#introduction)Introduction

Filament includes an action that is able to restore [soft-deleted](https://laravel.com/docs/eloquent#soft-deleting) Eloquent records. When the trigger button is clicked, a modal asks the user for confirmation. You may use it like so:

```
use Filament\Actions\RestoreAction;

RestoreAction::make()
```

Or if you want to add it as a table bulk action, so that the user can choose which rows to restore, use `Filament\Actions\RestoreBulkAction`:

```
use Filament\Actions\RestoreBulkAction;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            RestoreBulkAction::make(),
        ]);
}
```

## [​](#redirecting-after-restoring)Redirecting after restoring

You may set up a custom redirect when the form is submitted using the `successRedirectUrl()` method:

```
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->successRedirectUrl(route('posts.list'))
```

## [​](#customizing-the-restore-notification)Customizing the restore notification

When the record is successfully restored, a notification is dispatched to the user, which indicates the success of their action. To customize the title of this notification, use the `successNotificationTitle()` method:

```
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->successNotificationTitle('User restored')
```

You may customize the entire notification using the `successNotification()` method:

```
use Filament\Actions\RestoreAction;
use Filament\Notifications\Notification;

RestoreAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User restored')
            ->body('The user has been restored successfully.'),
    )
```

To disable the notification altogether, use the `successNotification(null)` method:

```
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->successNotification(null)
```

## [​](#lifecycle-hooks)Lifecycle hooks

You can use the `before()` and `after()` methods to execute code before and after a record is restored:

```
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->before(function () {
        // ...
    })
    ->after(function () {
        // ...
    })
```

## [​](#improving-the-performance-of-restore-bulk-actions)Improving the performance of restore bulk actions

By default, the `RestoreBulkAction` will load all Eloquent records into memory, before looping over them and restoring them one by one. If you are restoring a large number of records, you may want to use the `chunkSelectedRecords()` method to fetch a smaller number of records at a time. This will reduce the memory usage of your application:

```
use Filament\Actions\RestoreBulkAction;

RestoreBulkAction::make()
    ->chunkSelectedRecords(250)
```

Filament loads Eloquent records into memory before restoring them for two reasons:

- To allow individual records in the collection to be authorized with a model policy before restoration (using `authorizeIndividualRecords('restore')`, for example).
- To ensure that model events are run when restoring records, such as the `restoring` and `restored` events in a model observer.If you do not require individual record policy authorization and model events, you can use the `fetchSelectedRecords(false)` method, which will not fetch the records into memory before restoring them, and instead will restore them in a single query:

```
use Filament\Actions\RestoreBulkAction;

RestoreBulkAction::make()
    ->fetchSelectedRecords(false)
```

[Force-delete action](/docs/5.x/actions/force-delete)[Import action](/docs/5.x/actions/import)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
