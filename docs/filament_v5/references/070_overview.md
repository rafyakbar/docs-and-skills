[Actions](/docs/5.x/actions/overview)

# Overview

## [​](#introduction)Introduction

“Action” is a word that is used quite a bit within the Laravel community. Traditionally, action PHP classes handle “doing” something in your application’s business logic. For instance, logging a user in, sending an email, or creating a new user record in the database. In Filament, actions also handle “doing” something in your app. However, they are a bit different from traditional actions. They are designed to be used in the context of a user interface. For instance, you might have a button to delete a client record, which opens a modal to confirm your decision. When the user clicks the “Delete” button in the modal, the client is deleted. This whole workflow is an “action”.

```
use Filament\Actions\Action;

Action::make('delete')
    ->requiresConfirmation()
    ->action(fn () => $this->client->delete())
```

Actions can also collect extra information from the user. For instance, you might have a button to email a client. When the user clicks the button, a modal opens to collect the email subject and body. When the user clicks the “Send” button in the modal, the email is sent:

```
use Filament\Actions\Action;
use Filament\Forms\Components\RichEditor;
use Filament\Forms\Components\TextInput;
use Illuminate\Support\Facades\Mail;

Action::make('sendEmail')
    ->schema([
        TextInput::make('subject')->required(),
        RichEditor::make('body')->required(),
    ])
    ->action(function (array $data) {
        Mail::to($this->client)
            ->send(new GenericEmail(
                subject: $data['subject'],
                body: $data['body'],
            ));
    })
```

Usually, actions get executed without redirecting the user away from the page. This is because we extensively use Livewire. However, actions can be much simpler, and don’t even need a modal. You can pass a URL to an action, and when the user clicks on the button, they are redirected to that page:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
```

If you are passing user-controlled data to the `url()` method, you should validate that the URL does not use a dangerous scheme such as `javascript:` or `data:`. Failing to do so could expose your application to XSS attacks. The simplest way to guard against this is to wrap the value in Filament’s [`Str::sanitizeUrl()`](/docs/5.x/advanced/security#validating-user-input) helper, which returns `null` for any URL that does not use `http`/`https` (or a relative path).

The entire look of the action’s trigger button and the modal is customizable using fluent PHP methods. We provide a sensible and consistent styling for the UI, but all of this is customizable with CSS.

## [​](#available-actions)Available actions

Filament includes several actions that you can add to your app. Their aim is to simplify the most common Eloquent-related actions:

- [Create](/docs/5.x/actions/create)
- [Edit](/docs/5.x/actions/edit)
- [View](/docs/5.x/actions/view)
- [Delete](/docs/5.x/actions/delete)
- [Replicate](/docs/5.x/actions/replicate)
- [Force-delete](/docs/5.x/actions/force-delete)
- [Restore](/docs/5.x/actions/restore)
- [Import](/docs/5.x/actions/import)
- [Export](/docs/5.x/actions/export)You can also create your own actions to do anything, these are just common ones that we include out of the box.

## [​](#choosing-a-trigger-style)Choosing a trigger style

Out of the box, action triggers have 4 styles - “button”, “link”, “icon button”, and “badge”. “Button” triggers have a background color, label, and optionally an [icon](#setting-an-icon). Usually, this is the default button style, but you can use it manually with the `button()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->button()
```

“Link” triggers have no background color. They must have a label and optionally an [icon](#setting-an-icon). They look like a link that you might find embedded within text. You can switch to that style with the `link()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->link()
```

“Icon button” triggers are circular buttons with an [icon](#setting-an-icon) and no label. You can switch to that style with the `iconButton()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->icon('heroicon-m-pencil-square')
    ->iconButton()
```

“Badge” triggers have a background color, label, and optionally an [icon](#setting-an-icon). You can use a badge as trigger using the `badge()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->badge()
```

### [​](#using-an-icon-button-on-mobile-devices-only)Using an icon button on mobile devices only

You may want to use a button style with a label on desktop, but remove the label on mobile. This will transform it into an icon button. You can do this with the `labeledFrom()` method, passing in the responsive [breakpoint](https://tailwindcss.com/docs/responsive-design#overview) at which you want the label to be added to the button:

```
use Filament\Actions\Action;

Action::make('edit')
    ->icon('heroicon-m-pencil-square')
    ->button()
    ->labeledFrom('md')
```

## [​](#setting-a-label)Setting a label

By default, the label of the trigger button is generated from its name. You may customize this using the `label()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->label('Edit post')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
```

## [​](#setting-a-color)Setting a color

Buttons may have a [color](/docs/5.x/styling/colors) to indicate their significance:

```
use Filament\Actions\Action;

Action::make('delete')
    ->color('danger')
```

## [​](#setting-a-size)Setting a size

Buttons come in 3 sizes - `Size::Small`, `Size::Medium` or `Size::Large`. You can change the size of the action’s trigger using the `size()` method:

```
use Filament\Actions\Action;
use Filament\Support\Enums\Size;

Action::make('create')
    ->size(Size::Large)
```

## [​](#setting-an-icon)Setting an icon

Buttons may have an [icon](/docs/5.x/styling/icons) to add more detail to the UI. You can set the icon using the `icon()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->icon('heroicon-m-pencil-square')
```

You can also change the icon’s position to be after the label instead of before it, using the `iconPosition()` method:

```
use Filament\Actions\Action;
use Filament\Support\Enums\IconPosition;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->icon('heroicon-m-pencil-square')
    ->iconPosition(IconPosition::After)
```

## [​](#authorization)Authorization

You may conditionally show or hide actions for certain users. To do this, you can use either the `visible()` or `hidden()` methods:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->visible(auth()->user()->can('update', $this->post))

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->hidden(! auth()->user()->can('update', $this->post))
```

This is useful for authorization of certain actions to only users who have permission.

### [​](#authorization-using-a-policy)Authorization using a policy

You can use a policy to authorize an action. To do this, pass the name of the policy method to the `authorize()` method, and Filament will use the current Eloquent model for that action to find the correct policy:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->authorize('update')
```

If you’re using an action in a panel resource or relation manager, you don’t need to use the `authorize()` method, since Filament will automatically read the policy based on the resource model for the built-in actions like `CreateAction`, `EditAction` and `DeleteAction`. For more information, visit the [resource authorization](/docs/5.x/resources/overview#authorization) section.

If your policy method returns a [response message](https://laravel.com/docs/authorization#policy-responses), you can disable the action instead of hiding it, and add a tooltip containing the message, using the `authorizationTooltip()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->authorize('update')
    ->authorizationTooltip()
```

If the denial does not provide a message (for example, your policy returns plain `false`, or a `Gate::before()` hook short-circuits the check), the action is hidden instead. You can supply a fallback message with `authorizationMessage()` to keep the action visible in that case. You may instead allow the action to still be clickable even if the user is not authorized, but send a notification containing the response message, using the `authorizationNotification()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->authorize('update')
    ->authorizationNotification()
```

As with `authorizationTooltip()`, the action is hidden if the denial does not provide a message, unless you supply a fallback with `authorizationMessage()`.

### [​](#disabling-a-button)Disabling a button

If you want to disable a button instead of hiding it, you can use the `disabled()` method:

```
use Filament\Actions\Action;

Action::make('delete')
    ->disabled()
```

You can conditionally disable a button by passing a boolean to it:

```
use Filament\Actions\Action;

Action::make('delete')
    ->disabled(! auth()->user()->can('delete', $this->post))
```

## [​](#registering-keybindings)Registering keybindings

You can attach keyboard shortcuts to trigger buttons. These use the same key codes as [Mousetrap](https://craig.is/killing/mice):

```
use Filament\Actions\Action;

Action::make('save')
    ->action(fn () => $this->save())
    ->keyBindings(['command+s', 'ctrl+s'])
```

## [​](#adding-a-badge-to-the-corner-of-the-button)Adding a badge to the corner of the button

You can add a badge to the corner of the button, to display whatever you want. It’s useful for displaying a count of something, or a status indicator:

```
use Filament\Actions\Action;

Action::make('filter')
    ->iconButton()
    ->icon('heroicon-m-funnel')
    ->badge(5)
```

You can also pass a [color](/docs/5.x/styling/colors) to be used for the badge:

```
use Filament\Actions\Action;

Action::make('filter')
    ->iconButton()
    ->icon('heroicon-m-funnel')
    ->badge(5)
    ->badgeColor('success')
```

## [​](#outlined-button-style)Outlined button style

When you’re using the “button” trigger style, you might wish to make it less prominent. You could use a different [color](#setting-a-color), but sometimes you might want to make it outlined instead. You can do this with the `outlined()` method:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->button()
    ->outlined()
```

Optionally, you may pass a boolean value to control if the label should be hidden or not:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->button()
    ->outlined(FeatureFlag::active())
```

## [​](#adding-extra-html-attributes-to-an-action)Adding extra HTML attributes to an action

You can pass extra HTML attributes to the action via the `extraAttributes()` method, which will be merged onto its outer HTML element. The attributes should be represented by an array, where the key is the attribute name and the value is the attribute value:

```
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->extraAttributes([
        'title' => 'Edit this post',
    ])
```

By default, calling `extraAttributes()` multiple times will overwrite the previous attributes. If you wish to merge the attributes instead, you can pass `merge: true` to the method.

## [​](#rate-limiting-actions)Rate limiting actions

You can rate limit actions by using the `rateLimit()` method. This method accepts the number of attempts per minute that a user IP address can make. If the user exceeds this limit, the action will not run and a notification will be shown:

```
use Filament\Actions\Action;

Action::make('delete')
    ->rateLimit(5)
```

If the action opens a modal, the rate limit will be applied when the modal is submitted. If an action is opened with arguments or for a specific Eloquent record, the rate limit will apply to each unique combination of arguments or record for each action. The rate limit is also unique to the current Livewire component / page in a panel.

## [​](#customizing-the-rate-limited-notification)Customizing the rate limited notification

When an action is rate limited, a notification is dispatched to the user, which indicates the rate limit. To customize the title of this notification, use the `rateLimitedNotificationTitle()` method:

```
use Filament\Actions\DeleteAction;

DeleteAction::make()
    ->rateLimit(5)
    ->rateLimitedNotificationTitle('Slow down!')
```

You may customize the entire notification using the `rateLimitedNotification()` method:

```
use DanHarrin\LivewireRateLimiting\Exceptions\TooManyRequestsException;
use Filament\Actions\DeleteAction;
use Filament\Notifications\Notification;

DeleteAction::make()
    ->rateLimit(5)
    ->rateLimitedNotification(
       fn (TooManyRequestsException $exception): Notification => Notification::make()
            ->warning()
            ->title('Slow down!')
            ->body("You can try deleting again in {$exception->secondsUntilAvailable} seconds."),
    )
```

### [​](#customizing-the-rate-limit-behavior)Customizing the rate limit behavior

If you wish to customize the rate limit behavior, you can use Laravel’s [rate limiting](https://laravel.com/docs/rate-limiting#basic-usage) features and Filament’s [flash notifications](/docs/5.x/notifications/overview) together in the action. If you want to rate limit immediately when an action modal is opened, you can do so in the `mountUsing()` method:

```
use Filament\Actions\Action;
use Filament\Notifications\Notification;
use Illuminate\Support\Facades\RateLimiter;

Action::make('delete')
    ->mountUsing(function () {
        if (RateLimiter::tooManyAttempts(
            $rateLimitKey = 'delete:' . auth()->id(),
            maxAttempts: 5,
        )) {
            Notification::make()
                ->title('Too many attempts')
                ->body('Please try again in ' . RateLimiter::availableIn($rateLimitKey) . ' seconds.')
                ->danger()
                ->send();
  
            return;
        }
  
         RateLimiter::hit($rateLimitKey);
    })
```

If you want to rate limit when an action is run, you can do so in the `action()` method:

```
use Filament\Actions\Action;
use Filament\Notifications\Notification;
use Illuminate\Support\Facades\RateLimiter;

Action::make('delete')
    ->action(function () {
        if (RateLimiter::tooManyAttempts(
            $rateLimitKey = 'delete:' . auth()->id(),
            maxAttempts: 5,
        )) {
            Notification::make()
                ->title('Too many attempts')
                ->body('Please try again in ' . RateLimiter::availableIn($rateLimitKey) . ' seconds.')
                ->danger()
                ->send();
  
            return;
        }
  
         RateLimiter::hit($rateLimitKey);
  
        // ...
    })
```

## [​](#using-actions-in-schemas)Using actions in schemas

Action objects can be inserted anywhere in a [schema](/docs/5.x/schemas/overview), such as in [form field slots](/docs/5.x/forms/overview#adding-extra-content-to-a-field), [section headers and footers](/docs/5.x/schemas/sections), or alongside [prime components](/docs/5.x/schemas/primes). When an action is used in a schema, it has access to the schema’s state via [utility injection](#injecting-utilities-from-a-schema) - you can use `$schemaGet` and `$schemaSet` in closures to read and modify form field values.

```
use Filament\Actions\Action;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Utilities\Get;
use Filament\Schemas\Components\Utilities\Set;

TextInput::make('title')
    ->afterContent(
        Action::make('generateSlug')
            ->action(function (Get $schemaGet, Set $schemaSet) {
                $schemaSet('slug', str($schemaGet('title'))->slug());
            })
    )

TextInput::make('slug')
```

### [​](#adding-a-list-of-actions-to-a-schema)Adding a list of actions to a schema

If you want to render a list of action buttons on their own row in a schema, without attaching them to a specific field, you can wrap them in an `Actions` layout component:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Actions;

Actions::make([
    Action::make('star')
        ->icon('heroicon-m-star'),
    Action::make('resetStars')
        ->icon('heroicon-m-x-mark')
        ->color('danger'),
])
```

You can make the actions span the full width of the schema using the `fullWidth()` method:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Actions;

Actions::make([
    Action::make('star')
        ->icon('heroicon-m-star'),
    Action::make('resetStars')
        ->icon('heroicon-m-x-mark')
        ->color('danger'),
])->fullWidth()
```

You can change the horizontal alignment of the actions using the `alignment()` method:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Actions;
use Filament\Support\Enums\Alignment;

Actions::make([
    Action::make('star')
        ->icon('heroicon-m-star'),
    Action::make('resetStars')
        ->icon('heroicon-m-x-mark')
        ->color('danger'),
])->alignment(Alignment::Center)
```

If the `Actions` component is in a grid alongside other components, you can change its vertical alignment using the `verticalAlignment()` method:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Actions;
use Filament\Support\Enums\VerticalAlignment;

Actions::make([
    Action::make('star')
        ->icon('heroicon-m-star'),
    Action::make('resetStars')
        ->icon('heroicon-m-x-mark')
        ->color('danger'),
])->verticalAlignment(VerticalAlignment::End)
```

### [​](#running-javascript-when-an-action-is-clicked)Running JavaScript when an action is clicked

If you need a simple action that runs JavaScript directly in the browser without making a network request, you can use the `actionJs()` method. This is useful for simple interactions like updating form field values instantly:

```
use Filament\Actions\Action;
use Filament\Forms\Components\TextInput;

TextInput::make('title')
    ->live(onBlur: true)
    ->afterContent(
        Action::make('generateSlug')
            ->actionJs(<<<'JS'
                $set('slug', $get('title').toLowerCase().replaceAll(' ', '-'))
                JS)
    )

TextInput::make('slug')
```

The JavaScript string has access to `$get()` and `$set()` utilities, which allow you to read and modify the state of form fields in the schema.

When using `actionJs()`, the action cannot open a modal or perform any server-side processing. It is intended for simple client-side interactions only. If you need to run PHP code, use the `action()` method instead.

Any JavaScript string passed to the `actionJs()` method will be executed in the browser, so you should never add user input directly into the string, as it could lead to cross-site scripting (XSS) vulnerabilities. User input from `$get()` should never be evaluated as JavaScript code, but is safe to use as a string value.

## [​](#action-utility-injection)Action utility injection

The vast majority of methods used to configure actions accept functions as parameters instead of hardcoded values:

```
use Filament\Actions\Action;

Action::make('edit')
    ->label('Edit post')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
```

This alone unlocks many customization possibilities. The package is also able to inject many utilities to use inside these functions, as parameters. All customization methods that accept functions as arguments can inject utilities. These injected utilities require specific parameter names to be used. Otherwise, Filament doesn’t know what to inject.

### [​](#injecting-the-current-modal-form-data)Injecting the current modal form data

If you wish to access the current [modal form data](/docs/5.x/actions/modals#rendering-a-form-in-a-modal), define a `$data` parameter:

```
function (array $data) {
    // ...
}
```

Be aware that this will be empty if the modal has not been submitted yet.

### [​](#injecting-the-eloquent-record)Injecting the Eloquent record

If your action is associated with an Eloquent record, for example if it is on a table row, you can inject the record using a `$record` parameter:

```
use Illuminate\Database\Eloquent\Model;

function (Model $record) {
    // ...
}
```

### [​](#injecting-the-current-arguments)Injecting the current arguments

If you wish to access the [current arguments](/docs/5.x/components/action#passing-action-arguments) that have been passed to the action, define an `$arguments` parameter:

```
function (array $arguments) {
    // ...
}
```

### [​](#injecting-utilities-from-a-schema)Injecting utilities from a schema

You can access various additional utilities if your action is defined in a schema:

- `$schema` - The schema instance that the action belongs to.
- `$schemaComponent` - The schema component instance that the action belongs to.
- `$schemaComponentState` - The current value of the schema component.
- `$schemaState` - The current value of the schema that this action belongs to, like the current repeater item.
- `$schemaGet` - A function for retrieving values from the schema data. Validation is not run on form fields.
- `$schemaSet` - A function for setting values in the schema data.
- `$schemaOperation` - The current operation being performed by the schema. Usually `create`, `edit`, or `view`.For more information, please visit the [Schemas section](/docs/5.x/schemas/overview#component-utility-injection).

### [​](#injecting-the-current-livewire-component-instance)Injecting the current Livewire component instance

If you wish to access the current Livewire component instance that the action belongs to, define a `$livewire` parameter:

```
use Livewire\Component;

function (Component $livewire) {
    // ...
}
```

### [​](#injecting-the-current-action-instance)Injecting the current action instance

If you wish to access the current action instance, define a `$action` parameter:

```
function (Action $action) {
    // ...
}
```

### [​](#injecting-multiple-utilities)Injecting multiple utilities

The parameters are injected dynamically using reflection, so you are able to combine multiple parameters in any order:

```
use Livewire\Component;

function (array $arguments, Component $livewire) {
    // ...
}
```

### [​](#injecting-dependencies-from-laravel’s-container)Injecting dependencies from Laravel’s container

You may inject anything from Laravel’s container like normal, alongside utilities:

```
use Illuminate\Http\Request;

function (Request $request, array $arguments) {
    // ...
}
```

[Custom entries](/docs/5.x/infolists/custom-entries)[Modals](/docs/5.x/actions/modals)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
