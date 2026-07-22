[Actions](/docs/5.x/actions/overview)

# Edit action

## [​](#introduction)Introduction

Filament includes an action that is able to edit Eloquent records. When the trigger button is clicked, a modal will open with a form inside. The user fills the form, and that data is validated and saved into the database. You may use it like so:

```
use Filament\Actions\EditAction;
use Filament\Forms\Components\TextInput;

EditAction::make()
    ->schema([
        TextInput::make('title')
            ->required()
            ->maxLength(255),
        // ...
    ])
```

## [​](#customizing-data-before-filling-the-form)Customizing data before filling the form

You may wish to modify the data from a record before it is filled into the form. To do this, you may use the `mutateRecordDataUsing()` method to modify the `$data` array, and return the modified version before it is filled into the form:

```
use Filament\Actions\EditAction;

EditAction::make()
    ->mutateRecordDataUsing(function (array $data): array {
        $data['user_id'] = auth()->id();

        return $data;
    })
```

Filament fills the form using the record’s array representation, which is sent to the browser as part of the Livewire request. If your model has a column containing binary data that is not valid UTF-8, such as a `geometry`, `point`, or `blob` column, it cannot be serialized to JSON and the modal will fail to open, often with no error in the Laravel log.To resolve this, add the column to [the `$hidden` array](https://laravel.com/docs/eloquent-serialization#hiding-attributes-from-json) on your model, which excludes it from the model’s array and JSON representations:

```
protected $hidden = ['location'];
```

This applies equally to the [View](/docs/5.x/actions/view) and [Replicate](/docs/5.x/actions/replicate) actions.

## [​](#customizing-data-before-saving)Customizing data before saving

Sometimes, you may wish to modify form data before it is finally saved to the database. To do this, you may use the `mutateDataUsing()` method, which has access to the `$data` as an array, and returns the modified version:

```
use Filament\Actions\EditAction;

EditAction::make()
    ->mutateDataUsing(function (array $data): array {
        $data['last_edited_by_id'] = auth()->id();

        return $data;
    })
```

## [​](#customizing-the-saving-process)Customizing the saving process

You can tweak how the record is updated with the `using()` method:

```
use Filament\Actions\EditAction;
use Illuminate\Database\Eloquent\Model;

EditAction::make()
    ->using(function (Model $record, array $data): Model {
        $record->update($data);

        return $record;
    })
```

## [​](#redirecting-after-saving)Redirecting after saving

You may set up a custom redirect when the form is submitted using the `successRedirectUrl()` method:

```
use Filament\Actions\EditAction;

EditAction::make()
    ->successRedirectUrl(route('posts.list'))
```

If you want to redirect using the created record, use the `$record` parameter:

```
use Filament\Actions\EditAction;
use Illuminate\Database\Eloquent\Model;

EditAction::make()
    ->successRedirectUrl(fn (Model $record): string => route('posts.view', [
        'post' => $record,
    ]))
```

## [​](#customizing-the-save-notification)Customizing the save notification

When the record is successfully updated, a notification is dispatched to the user, which indicates the success of their action. To customize the title of this notification, use the `successNotificationTitle()` method:

```
use Filament\Actions\EditAction;

EditAction::make()
    ->successNotificationTitle('User updated')
```

You may customize the entire notification using the `successNotification()` method:

```
use Filament\Actions\EditAction;
use Filament\Notifications\Notification;

EditAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User updated')
            ->body('The user has been saved successfully.'),
    )
```

To disable the notification altogether, use the `successNotification(null)` method:

```
use Filament\Actions\EditAction;

EditAction::make()
    ->successNotification(null)
```

## [​](#lifecycle-hooks)Lifecycle hooks

Hooks may be used to execute code at various points within the action’s lifecycle, like before a form is saved. There are several available hooks:

```
use Filament\Actions\EditAction;

EditAction::make()
    ->beforeFormFilled(function () {
        // Runs before the form fields are populated from the database.
    })
    ->afterFormFilled(function () {
        // Runs after the form fields are populated from the database.
    })
    ->beforeFormValidated(function () {
        // Runs before the form fields are validated when the form is saved.
    })
    ->afterFormValidated(function () {
        // Runs after the form fields are validated when the form is saved.
    })
    ->before(function () {
        // Runs before the form fields are saved to the database.
    })
    ->after(function () {
        // Runs after the form fields are saved to the database.
    })
```

## [​](#halting-the-saving-process)Halting the saving process

At any time, you may call `$action->halt()` from inside a lifecycle hook or mutation method, which will halt the entire saving process:

```
use App\Models\Post;
use Filament\Actions\Action;
use Filament\Actions\EditAction;
use Filament\Notifications\Notification;

EditAction::make()
    ->before(function (EditAction $action, Post $record) {
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

[Create action](/docs/5.x/actions/create)[View action](/docs/5.x/actions/view)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
