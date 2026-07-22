[Actions](/docs/5.x/actions/overview)

# Modals

## [​](#introduction)Introduction

Actions may require additional confirmation or input from the user before they run. You may open a modal before an action is executed to do this.

## [​](#confirmation-modals)Confirmation modals

You may require confirmation before an action is run using the `requiresConfirmation()` method. This is useful for particularly destructive actions, such as those that delete records.

```
use App\Models\Post;
use Filament\Actions\Action;

Action::make('delete')
    ->action(fn (Post $record) => $record->delete())
    ->requiresConfirmation()
```

The confirmation modal is not available when a `url()` is set instead of an `action()`. Instead, you should redirect to the URL within the `action()` closure.

Confirmation modals use the `alertdialog` ARIA role instead of `dialog`, so screen readers announce them as alerts and automatically read the modal’s description when they open.

## [​](#controlling-modal-content)Controlling modal content

### [​](#customizing-the-modal’s-heading-description-and-submit-action-label)Customizing the modal’s heading, description, and submit action label

You may customize the heading, description and label of the submit button in the modal:

```
use App\Models\Post;
use Filament\Actions\Action;

Action::make('delete')
    ->action(fn (Post $record) => $record->delete())
    ->requiresConfirmation()
    ->modalHeading('Delete post')
    ->modalDescription('Are you sure you\'d like to delete this post? This cannot be undone.')
    ->modalSubmitActionLabel('Yes, delete it')
```

### [​](#rendering-a-schema-in-a-modal)Rendering a schema in a modal

Filament allows you to render a [schema](/docs/5.x/schemas) in a modal, which allows you to render any of the available components to build a UI. Usually, it is useful to build a form in the schema that can collect extra information from the user before the action runs, but any UI can be rendered:

```
use Filament\Actions\Action;
use Filament\Forms\Components\Checkbox;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Section;

Action::make('viewUser')
    ->schema([
        Grid::make(2)
            ->schema([
                Section::make('Details')
                    ->schema([
                        TextInput::make('name'),
                        Select::make('position')
                            ->options([
                                'developer' => 'Developer',
                                'designer' => 'Designer',
                            ]),
                        Checkbox::make('is_admin'),
                    ]),
                Section::make('Auditing')
                    ->schema([
                        TextEntry::make('created_at')
                            ->dateTime(),
                        TextEntry::make('updated_at')
                            ->dateTime(),
                    ]),
            ]),
    ])
```

#### [​](#rendering-a-form-in-a-modal)Rendering a form in a modal

You may use [form field](/docs/5.x/forms) to create action modal forms. The data from the form is available in the `$data` array of the `action()` closure:

```
use App\Models\Post;
use App\Models\User;
use Filament\Actions\Action;
use Filament\Forms\Components\Select;

Action::make('updateAuthor')
    ->schema([
        Select::make('authorId')
            ->label('Author')
            ->options(User::query()->pluck('name', 'id'))
            ->required(),
    ])
    ->action(function (array $data, Post $record): void {
        $record->author()->associate($data['authorId']);
        $record->save();
    })
```

##### Filling the form with existing data

You may fill the form with existing data, using the `fillForm()` method:

```
use App\Models\Post;
use App\Models\User;
use Filament\Actions\Action;
use Filament\Forms\Components\Select;

Action::make('updateAuthor')
    ->fillForm(fn (Post $record): array => [
        'authorId' => $record->author->id,
    ])
    ->schema([
        Select::make('authorId')
            ->label('Author')
            ->options(User::query()->pluck('name', 'id'))
            ->required(),
    ])
    ->action(function (array $data, Post $record): void {
        $record->author()->associate($data['authorId']);
        $record->save();
    })
```

##### Disabling all form fields

You may wish to disable all form fields in the modal, ensuring the user cannot edit them. You may do so using the `disabledForm()` method:

```
use App\Models\Post;
use Filament\Actions\Action;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\TextInput;

Action::make('approvePost')
    ->schema([
        TextInput::make('title'),
        Textarea::make('content'),
    ])
    ->disabledForm()
    ->action(function (Post $record): void {
        $record->approve();
    })
```

#### [​](#rendering-a-wizard-in-a-modal)Rendering a wizard in a modal

You may create a [multistep form wizard](/docs/5.x/schemas/wizards) inside a modal. Instead of using a `schema()`, define a `steps()` array and pass your `Step` objects:

```
use Filament\Actions\Action;
use Filament\Forms\Components\MarkdownEditor;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Toggle;
use Filament\Schemas\Components\Wizard\Step;

Action::make('create')
    ->steps([
        Step::make('Name')
            ->description('Give the category a unique name')
            ->schema([
                TextInput::make('name')
                    ->required()
                    ->live()
                    ->afterStateUpdated(fn ($state, callable $set) => $set('slug', Str::slug($state))),
                TextInput::make('slug')
                    ->disabled()
                    ->required()
                    ->unique(Category::class, 'slug'),
            ])
            ->columns(2),
        Step::make('Description')
            ->description('Add some extra details')
            ->schema([
                MarkdownEditor::make('description'),
            ]),
        Step::make('Visibility')
            ->description('Control who can view it')
            ->schema([
                Toggle::make('is_visible')
                    ->label('Visible to customers.')
                    ->default(true),
            ]),
    ])
```

### [​](#adding-an-icon-inside-the-modal)Adding an icon inside the modal

You may add an [icon](/docs/5.x/styling/icons) inside the modal using the `modalIcon()` method:

```
use App\Models\Post;
use Filament\Actions\Action;

Action::make('delete')
    ->action(fn (Post $record) => $record->delete())
    ->requiresConfirmation()
    ->modalIcon('heroicon-o-trash')
```

By default, the icon will inherit the color of the action button. You may customize the color of the icon using the `modalIconColor()` method:

```
use App\Models\Post;
use Filament\Actions\Action;

Action::make('delete')
    ->action(fn (Post $record) => $record->delete())
    ->requiresConfirmation()
    ->color('danger')
    ->modalIcon('heroicon-o-trash')
    ->modalIconColor('warning')
```

### [​](#customizing-the-alignment-of-modal-content)Customizing the alignment of modal content

By default, modal content will be aligned to the start, or centered if the modal is `xs` or `sm` in [width](#changing-the-modal-width). If you wish to change the alignment of content in a modal, you can use the `modalAlignment()` method and pass it `Alignment::Start` or `Alignment::Center`:

```
use Filament\Actions\Action;
use Filament\Support\Enums\Alignment;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->modalAlignment(Alignment::Center)
```

### [​](#making-the-modal-header-sticky)Making the modal header sticky

The header of a modal scrolls out of view with the modal content when it overflows the modal size. However, slide-overs have a sticky header that’s always visible. You may control this behavior using `stickyModalHeader()`:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->stickyModalHeader()
```

### [​](#making-the-modal-footer-sticky)Making the modal footer sticky

The footer of a modal is rendered inline after the content by default. Slide-overs, however, have a sticky footer that always shows when scrolling the content. You may enable this for a modal too using `stickyModalFooter()`:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->stickyModalFooter()
```

### [​](#custom-modal-content)Custom modal content

You may define custom content to be rendered inside your modal, which you can specify by passing a Blade view into the `modalContent()` method:

```
use App\Models\Post;
use Filament\Actions\Action;

Action::make('advance')
    ->action(fn (Post $record) => $record->advance())
    ->modalContent(view('filament.pages.actions.advance'))
```

#### [​](#passing-data-to-the-custom-modal-content)Passing data to the custom modal content

You can pass data to the view by returning it from a function. For example, if the `$record` of an action is set, you can pass that through to the view:

```
use Filament\Actions\Action;
use Illuminate\Contracts\View\View;

Action::make('advance')
    ->action(fn (Contract $record) => $record->advance())
    ->modalContent(fn (Contract $record): View => view(
        'filament.pages.actions.advance',
        ['record' => $record],
    ))
```

#### [​](#adding-custom-modal-content-below-the-form)Adding custom modal content below the form

By default, the custom content is displayed above the modal form if there is one, but you can add content below using `modalContentFooter()` if you wish:

```
use App\Models\Post;
use Filament\Actions\Action;

Action::make('advance')
    ->action(fn (Post $record) => $record->advance())
    ->modalContentFooter(view('filament.pages.actions.advance'))
```

#### [​](#adding-an-action-to-custom-modal-content)Adding an action to custom modal content

You can add an action button to your custom modal content, which is useful if you want to add a button that performs an action other than the main action. You can do this by registering an action with the `registerModalActions()` method, and then passing it to the view:

```
use App\Models\Post;
use Filament\Actions\Action;
use Illuminate\Contracts\View\View;

Action::make('advance')
    ->registerModalActions([
        Action::make('report')
            ->requiresConfirmation()
            ->action(fn (Post $record) => $record->report()),
    ])
    ->action(fn (Post $record) => $record->advance())
    ->modalContent(fn (Action $action): View => view(
        'filament.pages.actions.advance',
        ['action' => $action],
    ))
```

Now, in the view file, you can render the action button by calling `getModalAction()`:

```
<div>
    {{ $action->getModalAction('report') }}
</div>
```

## [​](#using-a-slide-over-instead-of-a-modal)Using a slide-over instead of a modal

You can open a “slide-over” dialog instead of a modal by using the `slideOver()` method:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->slideOver()
```

Instead of opening in the center of the screen, the modal content will now slide in from the right and consume the entire height of the browser.

### [​](#changing-the-slide-over-position)Changing the slide-over position

By default, slide-overs enter from the end of the screen (the right side in left-to-right languages, the left side in right-to-left languages). You may change this to the start of the screen by passing `SlideOverPosition::Start` to the `slideOverPosition()` method:

```
use Filament\Actions\Action;
use Filament\Support\Enums\SlideOverPosition;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->slideOver()
    ->slideOverPosition(SlideOverPosition::Start)
```

This is useful when the action trigger sits near the start of the viewport — for example, a row action at the beginning of a table row — so the slide-over opens adjacent to its trigger instead of across the screen.

## [​](#changing-the-modal-width)Changing the modal width

You can change the width of the modal by using the `modalWidth()` method. Options correspond to [Tailwind’s max-width scale](https://tailwindcss.com/docs/max-width). The options are `ExtraSmall`, `Small`, `Medium`, `Large`, `ExtraLarge`, `TwoExtraLarge`, `ThreeExtraLarge`, `FourExtraLarge`, `FiveExtraLarge`, `SixExtraLarge`, `SevenExtraLarge`, and `Screen`:

```
use Filament\Actions\Action;
use Filament\Support\Enums\Width;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->modalWidth(Width::FiveExtraLarge)
```

## [​](#executing-code-when-the-modal-opens)Executing code when the modal opens

You may execute code within a closure when the modal opens, by passing it to the `mountUsing()` method:

```
use Filament\Actions\Action;
use Filament\Schemas\Schema;

Action::make('create')
    ->mountUsing(function (Schema $form) {
        $form->fill();

        // ...
    })
```
> The `mountUsing()` method, by default, is used by Filament to initialize the [form](#rendering-a-form-in-a-modal). If you override this method, you will need to call `$form->fill()` to ensure the form is initialized correctly. If you wish to populate the form with data, you can do so by passing an array to the `fill()` method, instead of [using `fillForm()` on the action itself](#filling-the-form-with-existing-data).

## [​](#customizing-the-action-buttons-in-the-footer-of-the-modal)Customizing the action buttons in the footer of the modal

By default, there are two actions in the footer of a modal. The first is a button to submit, which executes the `action()`. The second button closes the modal and cancels the action.

### [​](#modifying-the-default-modal-footer-action-button)Modifying the default modal footer action button

To modify the action instance that is used to render one of the default action buttons, you may pass a closure to the `modalSubmitAction()` and `modalCancelAction()` methods:

```
use Filament\Actions\Action;

Action::make('help')
    ->modalContent(view('actions.help'))
    ->modalCancelAction(fn (Action $action) => $action->label('Close'))
```

The [methods available to customize trigger buttons](/docs/5.x/actions/overview) will work to modify the `$action` instance inside the closure.

To customize the button labels in your modal, the `modalSubmitActionLabel()` and `modalCancelActionLabel()` methods can be used instead of passing a function to `modalSubmitAction()` and `modalCancelAction()`, if you don’t require any further customizations.

### [​](#removing-a-default-modal-footer-action-button)Removing a default modal footer action button

To remove a default action, you may pass `false` to either `modalSubmitAction()` or `modalCancelAction()`:

```
use Filament\Actions\Action;

Action::make('help')
    ->modalContent(view('actions.help'))
    ->modalSubmitAction(false)
```

### [​](#adding-an-extra-modal-action-button-to-the-footer)Adding an extra modal action button to the footer

You may pass an array of extra actions to be rendered, between the default actions, in the footer of the modal using the `extraModalFooterActions()` method:

```
use Filament\Actions\Action;

Action::make('create')
    ->schema([
        // ...
    ])
    // ...
    ->extraModalFooterActions(fn (Action $action): array => [
        $action->makeModalSubmitAction('createAnother', arguments: ['another' => true]),
    ])
```

`$action->makeModalSubmitAction()` returns an action instance that can be customized using the [methods available to customize trigger buttons](/docs/5.x/actions/overview). The second parameter of `makeModalSubmitAction()` allows you to pass an array of arguments that will be accessible inside the action’s `action()` closure as `$arguments`. These could be useful as flags to indicate that the action should behave differently based on the user’s decision:

```
use Filament\Actions\Action;

Action::make('create')
    ->schema([
        // ...
    ])
    // ...
    ->extraModalFooterActions(fn (Action $action): array => [
        $action->makeModalSubmitAction('createAnother', arguments: ['another' => true]),
    ])
    ->action(function (array $data, array $arguments): void {
        // Create

        if ($arguments['another'] ?? false) {
            // Reset the form and don't close the modal
        }
    })
```

#### [​](#opening-another-modal-from-an-extra-footer-action)Opening another modal from an extra footer action

You can nest actions within each other, allowing you to open a new modal from an extra footer action:

```
use Filament\Actions\Action;

Action::make('edit')
    // ...
    ->extraModalFooterActions([
        Action::make('delete')
            ->requiresConfirmation()
            ->action(function () {
                // ...
            }),
    ])
```

Now, the edit modal will have a “Delete” button in the footer, which will open a confirmation modal when clicked. This action is completely independent of the `edit` action, and will not run the `edit` action when it is clicked. In this example though, you probably want to cancel the `edit` action if the `delete` action is run. You can do this using the `cancelParentActions()` method:

```
use Filament\Actions\Action;

Action::make('delete')
    ->requiresConfirmation()
    ->action(function () {
        // ...
    })
    ->cancelParentActions()
```

If you have deep nesting with multiple parent actions, but you don’t want to cancel all of them, you can pass the name of the parent action you want to cancel, including its children, to `cancelParentActions()`:

```
use Filament\Actions\Action;

Action::make('first')
    ->requiresConfirmation()
    ->action(function () {
        // ...
    })
    ->extraModalFooterActions([
        Action::make('second')
            ->requiresConfirmation()
            ->action(function () {
                // ...
            })
            ->extraModalFooterActions([
                Action::make('third')
                    ->requiresConfirmation()
                    ->action(function () {
                        // ...
                    })
                    ->extraModalFooterActions([
                        Action::make('fourth')
                            ->requiresConfirmation()
                            ->action(function () {
                                // ...
                            })
                            ->cancelParentActions('second'),
                    ]),
            ]),
    ])
```

In this example, if the `fourth` action is run, the `second` action is canceled, but so is the `third` action since it is a child of `second`. The `first` action is not canceled, however, since it is the parent of `second`. The `first` action’s modal will remain open.

## [​](#accessing-information-about-parent-actions-from-a-child)Accessing information about parent actions from a child

You can access the instances of parent actions and their raw data and arguments by injecting the `$mountedActions` array in a function used by your nested action. For example, to get the top-most parent action currently active on the page, you can use `$mountedActions[0]`. From there, you can get the raw data for that action by calling `$mountedActions[0]->getRawData()`. Please be aware that raw data is not validated since the action has not been submitted yet:

```
use Filament\Actions\Action;
use Filament\Forms\Components\TextInput;

Action::make('first')
    ->schema([
        TextInput::make('foo'),
    ])
    ->action(function () {
        // ...
    })
    ->extraModalFooterActions([
        Action::make('second')
            ->requiresConfirmation()
            ->action(function (array $mountedActions) {
                dd($mountedActions[0]->getRawData());
  
                // ...
            }),
    ])
```

You can do similar with the current arguments for a parent action, with the `$mountedActions[0]->getArguments()` method. Even if you have multiple layers of nesting, the `$mountedActions` array will contain every action that is currently active, so you can access information about them:

```
use Filament\Actions\Action;

Action::make('first')
    ->schema([
        TextInput::make('foo'),
    ])
    ->action(function () {
        // ...
    })
    ->extraModalFooterActions([
        Action::make('second')
            ->schema([
                TextInput::make('bar'),
            ])
            ->arguments(['number' => 2])
            ->action(function () {
                // ...
            })
            ->extraModalFooterActions([
                Action::make('third')
                    ->schema([
                        TextInput::make('baz'),
                    ])
                    ->arguments(['number' => 3])
                    ->action(function () {
                        // ...
                    })
                    ->extraModalFooterActions([
                        Action::make('fourth')
                            ->requiresConfirmation()
                            ->action(function (array $mountedActions) {
                                dd(
                                    $mountedActions[0]->getRawData(),
                                    $mountedActions[0]->getArguments(),
                                    $mountedActions[1]->getRawData(),
                                    $mountedActions[1]->getArguments(),
                                    $mountedActions[2]->getRawData(),
                                    $mountedActions[2]->getArguments(),
                                );
                                // ...
                            }),
                    ]),
            ]),
    ])
```

## [​](#closing-the-modal)Closing the modal

### [​](#closing-the-modal-by-clicking-away)Closing the modal by clicking away

By default, when you click away from a modal, it will close itself. If you wish to disable this behavior for a specific action, you can use the `closeModalByClickingAway(false)` method:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->closeModalByClickingAway(false)
```

If you’d like to change the behavior for all modals in the application, you can do so by calling `ModalComponent::closedByClickingAway()` inside a service provider or middleware:

```
use Filament\Support\View\Components\ModalComponent;

ModalComponent::closedByClickingAway(false);
```

### [​](#closing-the-modal-by-escaping)Closing the modal by escaping

By default, when you press escape on a modal, it will close itself. If you wish to disable this behavior for a specific action, you can use the `closeModalByEscaping(false)` method:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->closeModalByEscaping(false)
```

If you’d like to change the behavior for all modals in the application, you can do so by calling `ModalComponent::closedByEscaping()` inside a service provider or middleware:

```
use Filament\Support\View\Components\ModalComponent;

ModalComponent::closedByEscaping(false);
```

### [​](#hiding-the-modal-close-button)Hiding the modal close button

By default, modals have a close button in the top right corner. If you wish to hide the close button, you can use the `modalCloseButton(false)` method:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->modalCloseButton(false)
```

If you’d like to hide the close button for all modals in the application, you can do so by calling `ModalComponent::closeButton(false)` inside a service provider or middleware:

```
use Filament\Support\View\Components\ModalComponent;

ModalComponent::closeButton(false);
```

## [​](#making-the-modal-click-through)Making the modal click-through

By default, a modal blocks interaction with the rest of the page while it is open. If you want the user to be able to keep interacting with the page behind the modal, you can make it “click-through” using the `modalClickThrough()` method:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->modalClickThrough()
```

When a modal is click-through, its backdrop is removed, clicks outside the modal window pass through to the page beneath, and the page remains scrollable. The modal can still be closed using its close button or by pressing the escape key.

A click-through modal cannot be closed by clicking away, as that would be incompatible with interacting with the page behind it. Enabling `modalClickThrough()` therefore disables closing by clicking away automatically.

## [​](#preventing-the-modal-from-autofocusing)Preventing the modal from autofocusing

By default, modals will autofocus on the first focusable element when opened. If you wish to disable this behavior, you can use the `modalAutofocus(false)` method:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->modalAutofocus(false)
```

If you’d like to disable autofocus for all modals in the application, you can do so by calling `ModalComponent::autofocus(false)` inside a service provider or middleware:

```
use Filament\Support\View\Components\ModalComponent;

ModalComponent::autofocus(false);
```

## [​](#overlaying-child-action-modals-on-top-of-parent-action-modals)Overlaying child action modals on top of parent action modals

By default, when a child action opens its modal, the parent action’s modal is temporarily closed and then reopened after the child action is dismissed. If you’d like the child action’s modal to instead appear on top of the parent action’s modal (keeping the parent visible underneath), you can use the `overlayParentActions()` method on the child action:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Repeater;

Action::make('editItems')
    ->slideOver()
    ->schema([
        Repeater::make('items')
            ->schema([
                // ...
            ])
            ->deleteAction(
                fn (Action $action) => $action
                    ->requiresConfirmation()
                    ->overlayParentActions(),
            ),
    ])
    ->action(function () {
        // ...
    })
```

In this example, when the user clicks the delete button on a repeater item, the confirmation dialog appears on top of the slide-over instead of the slide-over closing first. This creates a smoother experience, especially for actions inside slide-overs or complex forms where closing and reopening the parent would be disorienting.

## [​](#canceling-parent-actions-when-a-modal-is-closed)Canceling parent actions when a modal is closed

The `cancelParentActions()` method above only cancels parent actions when the child action is run. If the user closes the child’s modal instead — by pressing Escape, clicking the backdrop, or using the close button — by default only that modal is closed, leaving any parent actions still mounted. To also cancel parent actions when the modal is closed, allowing the user to abandon a multi-step flow entirely rather than closing one modal at a time, use the `cancelParentActionsOnClose()` method:

```
use Filament\Actions\Action;

Action::make('createPost')
    ->schema([
        // ...
    ])
    ->extraModalFooterActions([
        Action::make('saveAsDraft')
            ->schema([
                // ...
            ])
            ->cancelParentActionsOnClose()
            ->action(function (): void {
                // ...
            }),
    ])
    ->action(function (array $data): void {
        // ...
    })
```

Now, closing the `saveAsDraft` modal will also cancel the `createPost` action and close its modal. Like `cancelParentActions()`, you can pass the name of a parent action to cancel back to a specific parent, including its children, rather than all of them:

```
use Filament\Actions\Action;

Action::make('editPostMetadata')
    ->schema([
        // ...
    ])
    ->cancelParentActionsOnClose('createPost')
    ->action(function (): void {
        // ...
    })
```

## [​](#optimizing-modal-configuration-methods)Optimizing modal configuration methods

When you use database queries or other heavy operations inside modal configuration methods like `modalHeading()`, they can be executed more than once. This is because Filament uses these methods to decide whether to render the modal or not, and also to render the modal’s content. To skip the check that Filament does to decide whether to render the modal, you can use the `modal()` method, which will inform Filament that the modal exists for this action, and it does not need to check again:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->modal()
```

## [​](#conditionally-hiding-the-modal)Conditionally hiding the modal

You may have a need to conditionally show a modal for confirmation reasons while falling back to the default action. This can be achieved using `modalHidden()`:

```
use Filament\Actions\Action;

Action::make('create')
    ->action(function (array $data): void {
        // ...
    })
    ->modalHidden($this->role !== 'admin')
    ->modalContent(view('filament.pages.actions.create'))
```

## [​](#adding-extra-attributes-to-the-modal-window)Adding extra attributes to the modal window

You can pass extra HTML attributes to the modal window via the `extraModalWindowAttributes()` method, which will be merged onto its outer HTML element. The attributes should be represented by an array, where the key is the attribute name and the value is the attribute value:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->extraModalWindowAttributes(['class' => 'update-author-modal'])
```

By default, calling `extraModalWindowAttributes()` multiple times will overwrite the previous attributes. If you wish to merge the attributes instead, you can pass `merge: true` to the method.

## [​](#adding-extra-attributes-to-the-modal-overlay)Adding extra attributes to the modal overlay

You can pass extra HTML attributes to the modal overlay via the `extraModalOverlayAttributes()`. The attributes should be represented by an array, where the key is the attribute name and the value is the attribute value:

```
use Filament\Actions\Action;

Action::make('updateAuthor')
    ->extraModalOverlayAttributes(['class' => 'update-author-overlay'])
```

By default, calling `extraModalOverlayAttributes()` multiple times will overwrite the previous attributes. If you wish to merge the attributes instead, you can pass `merge: true` to the method.

[Overview](/docs/5.x/actions/overview)[Grouping actions](/docs/5.x/actions/grouping-actions)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
