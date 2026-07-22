[Actions](/docs/5.x/actions/overview)

# Replicate action

## [​](#introduction)Introduction

Filament includes an action that is able to [replicate](https://laravel.com/docs/eloquent#replicating-models) Eloquent records. You may use it like so:

```
use Filament\Actions\ReplicateAction;

ReplicateAction::make()
```

## [​](#excluding-attributes)Excluding attributes

The `excludeAttributes()` method is used to instruct the action which columns should be excluded from replication:

```
use Filament\Actions\ReplicateAction;

ReplicateAction::make()
    ->excludeAttributes(['slug'])
```

## [​](#customizing-data-before-filling-the-form)Customizing data before filling the form

You may wish to modify the data from a record before it is filled into the form. To do this, you may use the `mutateRecordDataUsing()` method to modify the `$data` array, and return the modified version before it is filled into the form:

```
use Filament\Actions\ReplicateAction;

ReplicateAction::make()
    ->mutateRecordDataUsing(function (array $data): array {
        $data['user_id'] = auth()->id();

        return $data;
    })
```

## [​](#redirecting-after-replication)Redirecting after replication

You may set up a custom redirect when the form is submitted using the `successRedirectUrl()` method:

```
use Filament\Actions\ReplicateAction;

ReplicateAction::make()
    ->successRedirectUrl(route('posts.list'))
```

## [​](#customizing-the-replicate-notification)Customizing the replicate notification

When the record is successfully replicated, a notification is dispatched to the user, which indicates the success of their action. To customize the title of this notification, use the `successNotificationTitle()` method:

```
use Filament\Actions\ReplicateAction;

ReplicateAction::make()
    ->successNotificationTitle('Category replicated')
```

You may customize the entire notification using the `successNotification()` method:

```
use Filament\Actions\ReplicateAction;
use Filament\Notifications\Notification;

ReplicateAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('Category replicated')
            ->body('The category has been replicated successfully.'),
    )
```

To disable the notification altogether, use the `successNotification(null)` method:

```
use Filament\Actions\ReplicateAction;

ReplicateAction::make()
    ->successNotification(null)
```

## [​](#lifecycle-hooks)Lifecycle hooks

Hooks may be used to execute code at various points within the action’s lifecycle, like before the replica is saved.

```
use Filament\Actions\ReplicateAction;
use Illuminate\Database\Eloquent\Model;

ReplicateAction::make()
    ->before(function () {
        // Runs before the record has been replicated.
    })
    ->beforeReplicaSaved(function (Model $replica): void {
        // Runs after the record has been replicated but before it is saved to the database.
    })
    ->after(function (Model $replica): void {
        // Runs after the replica has been saved to the database.
    })
```

## [​](#halting-the-replication-process)Halting the replication process

At any time, you may call `$action->halt()` from inside a lifecycle hook, which will halt the entire replication process:

```
use App\Models\Post;
use Filament\Actions\Action;
use Filament\Actions\ReplicateAction;
use Filament\Notifications\Notification;

ReplicateAction::make()
    ->before(function (ReplicateAction $action, Post $record) {
        if (! $record->team->subscribed()) {
            Notification::make()
                ->warning()
                ->title('You don\'t have an active subscription!')
                ->body('Choose a plan to continue.')
                ->persistent()
                ->actions([
                    Action::make('subscribe')
                        ->button()
                        ->url(route('subscribe'), shouldOpenInNewTab: true),
                ])
                ->send();
  
            $action->halt();
        }
    })
```

If you’d like the action modal to close too, you can completely `cancel()` the action instead of halting it:

```
$action->cancel();
```

[Delete action](/docs/5.x/actions/delete)[Force-delete action](/docs/5.x/actions/force-delete)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
