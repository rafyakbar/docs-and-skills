[Forms](/docs/5.x/forms/overview)

# Overview

## [​](#introduction)Introduction

Filament’s forms package allows you to easily build dynamic forms in your app. It’s used within other Filament packages to render forms within [panel resources](/docs/5.x/resources), [action modals](/docs/5.x/actions/modals), [table filters](/docs/5.x/tables/filters), and more. Learning how to build forms is essential to learning how to use these Filament packages. This guide will walk you through the basics of building forms with Filament’s form package. If you’re planning to add a new form to your own Livewire component, you should [do that first](/docs/5.x/components/form) and then come back. If you’re adding a form to a [panel resource](/docs/5.x/resources), or another Filament package, you’re ready to go!

## [​](#form-fields)Form fields

Form field classes can be found in the `Filament\Form\Components` namespace. They reside within the schema array of components. Filament ships with many types of field, suitable for editing different types of data:

- [Text input](/docs/5.x/forms/text-input)
- [Select](/docs/5.x/forms/select)
- [Checkbox](/docs/5.x/forms/checkbox)
- [Toggle](/docs/5.x/forms/toggle)
- [Checkbox list](/docs/5.x/forms/checkbox-list)
- [Radio](/docs/5.x/forms/radio)
- [Date-time picker](/docs/5.x/forms/date-time-picker)
- [File upload](/docs/5.x/forms/file-upload)
- [Rich editor](/docs/5.x/forms/rich-editor)
- [Markdown editor](/docs/5.x/forms/markdown-editor)
- [Repeater](/docs/5.x/forms/repeater)
- [Builder](/docs/5.x/forms/builder)
- [Tags input](/docs/5.x/forms/tags-input)
- [Textarea](/docs/5.x/forms/textarea)
- [Key-value](/docs/5.x/forms/key-value)
- [Color picker](/docs/5.x/forms/color-picker)
- [Toggle buttons](/docs/5.x/forms/toggle-buttons)
- [Slider](/docs/5.x/forms/slider)
- [Code editor](/docs/5.x/forms/code-editor)
- [Hidden](/docs/5.x/forms/hidden)You may also [create your own custom fields](/docs/5.x/forms/custom-fields) to edit data however you wish. Fields may be created using the static `make()` method, passing its unique name. Usually, the name of a field corresponds to the name of an attribute on an Eloquent model:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
```

You may use “dot notation” to bind fields to keys in arrays:

```
use Filament\Forms\Components\TextInput;

TextInput::make('socials.github_url')
```

## [​](#validating-fields)Validating fields

In Laravel, validation rules are usually defined in arrays like `['required', 'max:255']` or a combined string like `required|max:255`. This is fine if you’re exclusively working in the backend with simple form requests. But Filament is also able to give your users frontend validation, so they can fix their mistakes before any backend requests are made. In Filament, you can add validation rules to your fields by using methods like `required()` and `maxLength()`. This is also advantageous over Laravel’s validation syntax, since your IDE can autocomplete these methods:

```
use Filament\Forms\Components\DateTimePicker;
use Filament\Forms\Components\RichEditor;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Section;

TextInput::make('name')
    ->required()
    ->maxLength(255)
```

In this example, the fields is `required()`, and has a `maxLength()`. We have [methods for most of Laravel’s validation rules](/docs/5.x/forms/validation#available-rules), and you can even add your own [custom rules](/docs/5.x/forms/validation#custom-rules).

## [​](#setting-a-field’s-label)Setting a field’s label

By default, the label of the field will be automatically determined based on its name. To override the field’s label, you may use the `label()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->label('Full name')
```

Customizing the label in this way is useful if you wish to use a [translation string for localization](https://laravel.com/docs/localization#retrieving-translation-strings):

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->label(__('fields.name'))
```

You can also [use a JavaScript expression](#using-javascript-to-determine-text-content) to determine the content of the label, which can read the current values of fields in the form.

### [​](#hiding-a-field’s-label)Hiding a field’s label

It may be tempting to set the label to an empty string to hide it, but this is not recommended. Setting the label to an empty string will not communicate the purpose of the field to screen readers, even if the purpose is clear visually. Instead, you should use the `hiddenLabel()` method, so it is hidden visually but still accessible to screen readers:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->hiddenLabel()
```

Optionally, you may pass a boolean value to control if the label should be hidden or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->hiddenLabel(FeatureFlag::active())
```

## [​](#setting-the-default-value-of-a-field)Setting the default value of a field

Fields may have a default value. The default is only used when a schema is loaded with no data. In a standard [panel resource](/docs/5.x/resources), defaults are used on the Create page, not the Edit page. To define a default value, use the `default()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->default('John')
```

## [​](#disabling-a-field)Disabling a field

You may disable a field to prevent it from being edited by the user:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->disabled()
```

Optionally, you may pass a boolean value to control if the field should be disabled or not:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->disabled(! FeatureFlag::active())
```

Disabling a field will prevent it from being saved. If you’d like it to be saved, but still not editable, use the `saved()` method:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->disabled()
    ->saved()
```

If you choose to save the field when disabled, a skilled user could still edit the field’s value by manipulating Livewire’s JavaScript.

Optionally, you may pass a boolean value to control if the field should be saved or not:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->disabled()
    ->saved(FeatureFlag::active())
```

### [​](#disabling-a-field-based-on-the-current-operation)Disabling a field based on the current operation

The “operation” of a schema is the current action being performed on it. Usually, this is either `create`, `edit` or `view`, if you are using the [panel resource](/docs/5.x/resources). You can disable a field based on the current operation by passing an operation to the `disabledOn()` method:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->disabledOn('edit')

// is the same as

Toggle::make('is_admin')
    ->disabled(fn (string $operation): bool => $operation === 'edit')
```

You can also pass an array of operations to the `disabledOn()` method, and the field will be disabled if the current operation is any of the operations in the array:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->disabledOn(['edit', 'view'])
  
// is the same as

Toggle::make('is_admin')
    ->disabled(fn (string $operation): bool => in_array($operation, ['edit', 'view']))
```

The `disabledOn()` method will overwrite any previous calls to the `disabled()` method, and vice versa.

## [​](#hiding-a-field)Hiding a field

You may hide a field:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->hidden()
```

Optionally, you may pass a boolean value to control if the field should be hidden or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->hidden(! FeatureFlag::active())
```

Alternatively, you may use the `visible()` method to control if the field should be hidden or not. In some situations, this may help to make your code more readable:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->visible(FeatureFlag::active())
```

If both `hidden()` and `visible()` are used, they both need to indicate that the field should be visible for it to be shown.

### [​](#hiding-a-field-using-javascript)Hiding a field using JavaScript

If you need to hide a field based on a user interaction, you can use the `hidden()` or `visible()` methods, passing a function that uses utilities injected to determine whether the field should be hidden or not:

```
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Toggle;

Select::make('role')
    ->options([
        'user' => 'User',
        'staff' => 'Staff',
    ])
    ->live()

Toggle::make('is_admin')
    ->hidden(fn (Get $get): bool => $get('role') !== 'staff')
```

In this example, the `role` field is set to `live()`, which means that the schema will reload the schema each time the `role` field is changed. This will cause the function that is passed to the `hidden()` method to be re-evaluated, which will hide the `is_admin` field if the `role` field is not set to `staff`. However, reloading the schema each time a field causes a network request to be made, since there is no way to re-run the PHP function from the client-side. This is not ideal for performance. Alternatively, you can write JavaScript to hide the field based on the value of another field. This is done by passing a JavaScript expression to the `hiddenJs()` method:

```
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Toggle;

Select::make('role')
    ->options([
        'user' => 'User',
        'staff' => 'Staff',
    ])

Toggle::make('is_admin')
    ->hiddenJs(<<<'JS'
        $get('role') !== 'staff'
        JS)
```

Although the code passed to `hiddenJs()` looks very similar to PHP, it is actually JavaScript. Filament provides the `$get()` utility function to JavaScript that behaves very similar to its PHP equivalent, but without requiring the depended-on field to be `live()`.

Any JavaScript string passed to the `hiddenJs()` method will be executed in the browser, so you should never add user input directly into the string, as it could lead to cross-site scripting (XSS) vulnerabilities. User input from `$state` or `$get()` should never be evaluated as JavaScript code, but is safe to use as a string value, like in the example above.

The `visibleJs()` method is also available, which works in the same way as `hiddenJs()`, but controls if the field should be visible or not:

```
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Toggle;

Select::make('role')
    ->options([
        'user' => 'User',
        'staff' => 'Staff',
    ])

Toggle::make('is_admin')
    ->visibleJs(<<<'JS'
        $get('role') === 'staff'
        JS)
```

Any JavaScript string passed to the `visibleJs()` method will be executed in the browser, so you should never add user input directly into the string, as it could lead to cross-site scripting (XSS) vulnerabilities. User input from `$state` or `$get()` should never be evaluated as JavaScript code, but is safe to use as a string value, like in the example above.

If both `hiddenJs()` and `visibleJs()` are used, they both need to indicate that the field should be visible for it to be shown.

### [​](#hiding-a-field-based-on-the-current-operation)Hiding a field based on the current operation

The “operation” of a schema is the current action being performed on it. Usually, this is either `create`, `edit` or `view`, if you are using the [panel resource](/docs/5.x/resources). You can hide a field based on the current operation by passing an operation to the `hiddenOn()` method:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->hiddenOn('edit')
  
// is the same as

Toggle::make('is_admin')
    ->hidden(fn (string $operation): bool => $operation === 'edit')
```

You can also pass an array of operations to the `hiddenOn()` method, and the field will be hidden if the current operation is any of the operations in the array:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->hiddenOn(['edit', 'view'])
  
// is the same as

Toggle::make('is_admin')
    ->hidden(fn (string $operation): bool => in_array($operation, ['edit', 'view']))
```

The `hiddenOn()` method will overwrite any previous calls to the `hidden()` method, and vice versa.

Alternatively, you may use the `visibleOn()` method to control if the field should be hidden or not. In some situations, this may help to make your code more readable:

```
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->visibleOn('create')

Toggle::make('is_admin')
    ->visibleOn(['create', 'edit'])
```

The `visibleOn()` method will overwrite any previous calls to the `visible()` method, and vice versa.

## [​](#inline-labels)Inline labels

Fields may have their labels displayed inline with the field, rather than above it. This is useful for forms with many fields, where vertical space is at a premium. To display a field’s label inline, use the `inlineLabel()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->inlineLabel()
```

Optionally, you may pass a boolean value to control if the label should be displayed inline or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->inlineLabel(FeatureFlag::active())
```

### [​](#using-inline-labels-in-multiple-places-at-once)Using inline labels in multiple places at once

If you wish to display all labels inline in a [layout component](/docs/5.x/schemas/layouts) like a [section](/docs/5.x/schemas/sections) or [tab](/docs/5.x/schemas/tabs), you can use the `inlineLabel()` on the component itself, and all fields within it will have their labels displayed inline:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Section;

Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email')
            ->label('Email address'),
        TextInput::make('phone')
            ->label('Phone number'),
    ])
```

You can also use `inlineLabel()` on the entire schema to display all labels inline:

```
use Filament\Schemas\Schema;

public function form(Schema $schema): Schema
{
    return $schema
        ->inlineLabel()
        ->components([
            // ...
        ]);
}
```

When using `inlineLabel()` on a layout component or schema, you can still opt-out of inline labels for individual fields by using the `inlineLabel(false)` method on the field:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Section;

Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email')
            ->label('Email address'),
        TextInput::make('phone')
            ->label('Phone number')
            ->inlineLabel(false),
    ])
```

## [​](#autofocusing-a-field-when-the-schema-is-loaded)Autofocusing a field when the schema is loaded

Most fields are autofocusable. Typically, you should aim for the first significant field in your schema to be autofocused for the best user experience. You can nominate a field to be autofocused using the `autofocus()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->autofocus()
```

Optionally, you may pass a boolean value to control if the field should be autofocused or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->autofocus(FeatureFlag::active())
```

## [​](#setting-the-placeholder-of-a-field)Setting the placeholder of a field

Many fields can display a placeholder for when they have no value. This is displayed in the UI but never saved when the form is submitted. You may customize this placeholder using the `placeholder()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->placeholder('John Doe')
```

## [​](#fusing-fields-together-into-a-group)Fusing fields together into a group

A `FusedGroup` component can be used to “fuse” multiple fields together. The following fields can be fused together the best:

- [Text input](/docs/5.x/forms/text-input)
- [Select](/docs/5.x/forms/select)
- [Date-time picker](/docs/5.x/forms/date-time-picker)
- [Color picker](/docs/5.x/forms/color-picker)The fields that should be fused are passed to the `make()` method of the `FusedGroup` component:

```
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\FusedGroup;

FusedGroup::make([
    TextInput::make('city')
        ->placeholder('City'),
    Select::make('country')
        ->placeholder('Country')
        ->options([
            // ...
        ]),
])
```

You can add a label above the group of fields using the `label()` method:

```
use Filament\Schemas\Components\FusedGroup;

FusedGroup::make([
    // ...
])
    ->label('Location')
```

By default, each field will have its own row. On mobile devices, this is often the most optimal experience, but on desktop you can use the `columns()` method, the same as for [layout components](/docs/5.x/schemas/layouts#grid-system) to display the fields horizontally:

```
use Filament\Schemas\Components\FusedGroup;

FusedGroup::make([
    // ...
])
    ->label('Location')
    ->columns(2)
```

You can adjust the width of the fields in the grid by passing `columnSpan()` to each field:

```
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\FusedGroup;

FusedGroup::make([
    TextInput::make('city')
        ->placeholder('City')
        ->columnSpan(2),
    Select::make('country')
        ->placeholder('Country')
        ->options([
            // ...
        ]),
])
    ->label('Location')
    ->columns(3)
```

## [​](#adding-extra-content-to-a-field)Adding extra content to a field

Fields contain many “slots” where content can be inserted in a child schema. Slots can accept text, [any schema component](/docs/5.x/schemas), [actions](/docs/5.x/actions) and [action groups](/docs/5.x/actions/grouping-actions). Usually, [prime components](/docs/5.x/schemas/primes) are used for content. The following slots are available for all fields:

- `aboveLabel()`
- `beforeLabel()`
- `afterLabel()`
- `belowLabel()`
- `aboveContent()`
- `beforeContent()`
- `afterContent()`
- `belowContent()`
- `aboveErrorMessage()`
- `belowErrorMessage()`To insert plain text, you can pass a string to these methods:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->belowContent('This is the user\'s full name.')
```

To insert a schema component, often a [prime component](/docs/5.x/schemas/primes), you can pass the component to the method:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Text;
use Filament\Support\Enums\FontWeight;

TextInput::make('name')
    ->belowContent(Text::make('This is the user\'s full name.')->weight(FontWeight::Bold))
```

To insert an [action](/docs/5.x/actions) or [action group](/docs/5.x/actions/grouping-actions), you can pass the action or action group to the method:

```
use Filament\Actions\Action;
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->belowContent(Action::make('generate'))
```

If you need a simple action that runs JavaScript without making a network request, you can use the [`actionJs()` method](/docs/5.x/actions/overview#running-javascript-when-an-action-is-clicked). This is useful for simple interactions like updating form field values using `$get()` and `$set()`. Actions using `actionJs()` cannot open modals.

You can insert any combination of content into the slots by passing an array of content to the method:

```
use Filament\Actions\Action;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->belowContent([
        Icon::make(Heroicon::InformationCircle),
        'This is the user\'s full name.',
        Action::make('generate'),
    ])
```

You can also align the content in the slots by passing the array of content to either `Schema::start()` (default), `Schema::end()` or `Schema::between()`:

```
use Filament\Actions\Action;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Flex;
use Filament\Schemas\Components\Icon;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->belowContent(Schema::end([
        Icon::make(Heroicon::InformationCircle),
        'This is the user\'s full name.',
        Action::make('generate'),
    ]))

TextInput::make('name')
    ->belowContent(Schema::between([
        Icon::make(Heroicon::InformationCircle),
        'This is the user\'s full name.',
        Action::make('generate'),
    ]))

TextInput::make('name')
    ->belowContent(Schema::between([
        Flex::make([
            Icon::make(Heroicon::InformationCircle)
                ->grow(false),
            'This is the user\'s full name.',
        ]),
        Action::make('generate'),
    ]))
```

As you can see in the above example for `Schema::between()`, a [`Flex` component](/docs/5.x/schemas/layouts#flex-component) is used to group the icon and text together so they do not have space between them. The icon uses `grow(false)` to prevent it from taking up half of the horizontal space, allowing the text to consume the remaining space.

### [​](#adding-extra-content-above-a-field’s-label)Adding extra content above a field’s label

You can insert extra content above a field’s label using the `aboveLabel()` method. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->aboveLabel([
        Icon::make(Heroicon::Star),
        'This is the content above the field\'s label'
    ])
```

### [​](#adding-extra-content-before-a-field’s-label)Adding extra content before a field’s label

You can insert extra content before a field’s label using the `beforeLabel()` method. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->beforeLabel(Icon::make(Heroicon::Star))
```

### [​](#adding-extra-content-after-a-field’s-label)Adding extra content after a field’s label

You can insert extra content after a field’s label using the `afterLabel()` method. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->afterLabel([
        Icon::make(Heroicon::Star),
        'This is the content after the field\'s label'
    ])
```

By default, the content in the `afterLabel()` schema is aligned to the end of the container. If you wish to align it to the start of the container, you should pass a `Schema::start()` object containing the content:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->afterLabel(Schema::start([
        Icon::make(Heroicon::Star),
        'This is the content after the field\'s label'
    ]))
```

### [​](#adding-extra-content-below-a-field’s-label)Adding extra content below a field’s label

You can insert extra content below a field’s label using the `belowLabel()` method. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->belowLabel([
        Icon::make(Heroicon::Star),
        'This is the content below the field\'s label'
    ])
```

This may seem like the same as the [`aboveContent()` method](#adding-extra-content-above-a-fields-content). However, when using [inline labels](#inline-labels), the `aboveContent()` method will place the content above the field, not below the label, since the label is displayed in a separate column to the field content.

### [​](#adding-extra-content-above-a-field’s-content)Adding extra content above a field’s content

You can insert extra content above a field’s content using the `aboveContent()` method. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->aboveContent([
        Icon::make(Heroicon::Star),
        'This is the content above the field\'s content'
    ])
```

This may seem like the same as the [`belowLabel()` method](#adding-extra-content-below-a-fields-label). However, when using [inline labels](#inline-labels), the `belowLabel()` method will place the content below the label, not above the field’s content, since the label is displayed in a separate column to the field content.

### [​](#adding-extra-content-before-a-field’s-content)Adding extra content before a field’s content

You can insert extra content before a field’s content using the `beforeContent()` method. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->beforeContent(Icon::make(Heroicon::Star))
```

Some fields, such as the [text input](/docs/5.x/forms/text-input#adding-affix-text-aside-the-field), [select](/docs/5.x/forms/select#adding-affix-text-aside-the-field), and [date-time picker](/docs/5.x/forms/date-time-picker#adding-affix-text-aside-the-field) fields, have a `prefix()` method to insert content before the field’s content, adjoined to the field itself. This is often a better UI choice than using `beforeContent()`.

### [​](#adding-extra-content-after-a-field’s-content)Adding extra content after a field’s content

You can insert extra content after a field’s content using the `afterContent()` method. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->afterContent(Icon::make(Heroicon::Star))
```

Some fields, such as the [text input](/docs/5.x/forms/text-input#adding-affix-text-aside-the-field), [select](/docs/5.x/forms/select#adding-affix-text-aside-the-field), and [date-time picker](/docs/5.x/forms/date-time-picker#adding-affix-text-aside-the-field) fields, have a `suffix()` method to insert content after the field’s content, adjoined to the field itself. This is often a better UI choice than using `beforeContent()`.

### [​](#adding-extra-content-above-a-field’s-error-message)Adding extra content above a field’s error message

You can insert extra content above a field’s [error message](/docs/5.x/forms/validation) using the `aboveErrorMessage()` method. It will not be visible unless an error message is displayed. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->required()
    ->aboveErrorMessage([
        Icon::make(Heroicon::Star),
        'This is the content above the field\'s error message'
    ])
```

### [​](#adding-extra-content-below-a-field’s-error-message)Adding extra content below a field’s error message

You can insert extra content below a field’s [error message](/docs/5.x/forms/validation) using the `belowErrorMessage()` method. It will not be visible unless an error message is displayed. You can [pass any content](#adding-extra-content-to-a-field) to this method, like text, a schema component, an action, or an action group:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextInput::make('name')
    ->required()
    ->belowErrorMessage([
        Icon::make(Heroicon::Star),
        'This is the content below the field\'s error message'
    ])
```

## [​](#adding-extra-html-attributes-to-a-field)Adding extra HTML attributes to a field

You can pass extra HTML attributes to the field via the `extraAttributes()` method, which will be merged onto its outer HTML element. The attributes should be represented by an array, where the key is the attribute name and the value is the attribute value:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->extraAttributes(['title' => 'Text input'])
```

By default, calling `extraAttributes()` multiple times will overwrite the previous attributes. If you wish to merge the attributes instead, you can pass `merge: true` to the method.

### [​](#adding-extra-html-attributes-to-the-input-element-of-a-field)Adding extra HTML attributes to the input element of a field

Some fields use an underlying `<input>` or `<select>` DOM element, but this is often not the outer element in the field, so the `extraAttributes()` method may not work as you wish. In this case, you may use the `extraInputAttributes()` method, which will merge the attributes onto the `<input>` or `<select>` element in the field’s HTML:

```
use Filament\Forms\Components\TextInput;

TextInput::make('categories')
    ->extraInputAttributes(['width' => 200])
```

By default, calling `extraInputAttributes()` multiple times will overwrite the previous attributes. If you wish to merge the attributes instead, you can pass `merge: true` to the method.

### [​](#adding-extra-html-attributes-to-the-field-wrapper)Adding extra HTML attributes to the field wrapper

You can also pass extra HTML attributes to the very outer element of the “field wrapper” which surrounds the label and content of the field. This is useful if you want to style the label or spacing of the field via CSS, since you could target elements as children of the wrapper:

```
use Filament\Forms\Components\TextInput;

TextInput::make('categories')
    ->extraFieldWrapperAttributes(['class' => 'components-locked'])
```

By default, calling `extraFieldWrapperAttributes()` multiple times will overwrite the previous attributes. If you wish to merge the attributes instead, you can pass `merge: true` to the method.

## [​](#field-utility-injection)Field utility injection

The vast majority of methods used to configure fields accept functions as parameters instead of hardcoded values:

```
use App\Models\User;
use Filament\Forms\Components\DatePicker;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;

DatePicker::make('date_of_birth')
    ->displayFormat(function (): string {
        if (auth()->user()->country_id === 'us') {
            return 'm/d/Y';
        }

        return 'd/m/Y';
    })

Select::make('user_id')
    ->options(function (): array {
        return User::query()->pluck('name', 'id')->all();
    })

TextInput::make('middle_name')
    ->required(fn (): bool => auth()->user()->hasMiddleName())
```

This alone unlocks many customization possibilities. The package is also able to inject many utilities to use inside these functions, as parameters. All customization methods that accept functions as arguments can inject utilities. These injected utilities require specific parameter names to be used. Otherwise, Filament doesn’t know what to inject.

### [​](#injecting-the-current-state-of-the-field)Injecting the current state of the field

If you wish to access the current value (state) of the field, define a `$state` parameter:

```
function ($state) {
    // ...
}
```

#### [​](#injecting-the-raw-state-of-the-field)Injecting the raw state of the field

If a field casts its state automatically to a more useful format, you may wish to access the raw state. To do this, define a `$rawState` parameter:

```
function ($rawState) {
    // ...
}
```

### [​](#injecting-the-state-of-another-field)Injecting the state of another field

You may also retrieve the state (value) of another field from within a callback, using a `$get` parameter:

```
use Filament\Schemas\Components\Utilities\Get;

function (Get $get) {
    $email = $get('email'); // Store the value of the `email` field in the `$email` variable.
    //...
}
```

Unless a form field is [reactive](#the-basics-of-reactivity), the schema will not refresh when the value of the field changes, only when the next user interaction occurs that makes a request to the server. If you need to react to changes in a field’s value, it should be `live()`.

#### [​](#type-safe-retrieval-of-another-field’s-state)Type-safe retrieval of another field’s state

You may use a “typed” method on the `Get` utility to retrieve the state of another field in a type-safe manner:

```
use Filament\Schemas\Components\Utilities\Get;

$get->string('email');
$get->integer('age');
$get->float('price');
$get->boolean('is_admin');
$get->array('tags');
$get->date('published_at');
$get->enum('status', StatusEnum::class);
$get->filled('email'); // Returns the result of the `filled()` helper for the field.
$get->blank('email'); // Returns the result of the `blank()` helper for the field.
```

Each method assumes that the field’s state can’t be `null`. To force a nullable return type, pass the `isNullable: true` argument:

```
use Filament\Schemas\Components\Utilities\Get;

$get->string('email', isNullable: true);
```

### [​](#injecting-the-current-eloquent-record)Injecting the current Eloquent record

You may retrieve the Eloquent record for the current schema using a `$record` parameter:

```
use Illuminate\Database\Eloquent\Model;

function (?Model $record) {
    // ...
}
```

### [​](#injecting-the-current-operation)Injecting the current operation

If you’re writing a schema for a panel resource or relation manager, and you wish to check if a schema is `create`, `edit` or `view`, use the `$operation` parameter:

```
function (string $operation) {
    // ...
}
```

You can manually set a schema’s operation using the `$schema->operation()` method.

### [​](#injecting-the-current-livewire-component-instance)Injecting the current Livewire component instance

If you wish to access the current Livewire component instance, define a `$livewire` parameter:

```
use Livewire\Component;

function (Component $livewire) {
    // ...
}
```

### [​](#injecting-the-current-field-instance)Injecting the current field instance

If you wish to access the current component instance, define a `$component` parameter:

```
use Filament\Forms\Components\Field;

function (Field $component) {
    // ...
}
```

### [​](#injecting-multiple-utilities)Injecting multiple utilities

The parameters are injected dynamically using reflection, so you are able to combine multiple parameters in any order:

```
use Filament\Schemas\Components\Utilities\Get;
use Filament\Schemas\Components\Utilities\Set;
use Livewire\Component as Livewire;

function (Livewire $livewire, Get $get, Set $set) {
    // ...
}
```

### [​](#injecting-dependencies-from-laravel’s-container)Injecting dependencies from Laravel’s container

You may inject anything from Laravel’s container like normal, alongside utilities:

```
use Filament\Schemas\Components\Utilities\Set;
use Illuminate\Http\Request;

function (Request $request, Set $set) {
    // ...
}
```

### [​](#using-javascript-to-determine-text-content)Using JavaScript to determine text content

Methods that allow HTML to be rendered, such as [`label()`](#setting-a-fields-label) and [`Text::make()` passed to a `belowContent()` method](#adding-extra-content-to-a-field) can use JavaScript to calculate their content instead. This is achieved by passing a `JsContent` object to the method, which is `Htmlable`:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\JsContent;

TextInput::make('greetingResponse')
    ->label(JsContent::make(<<<'JS'
        ($get('name') === 'John Doe') ? 'Hello, John!' : 'Hello, stranger!'
        JS
    ))
```

The [`$state`](#injecting-the-current-state-of-the-field) and [`$get`](#injecting-the-state-of-another-field) utilities are available in this JavaScript context, so you can use them to access the state of the field and other fields in the schema.

The string passed to `JsContent` is evaluated in the browser, so you should never concatenate user input into it — that would lead to XSS. Values read at runtime via `$state` or `$get()` are safe to use as string values inside the expression, but should never be evaluated as JavaScript code themselves.

## [​](#the-basics-of-reactivity)The basics of reactivity

[Livewire](https://livewire.laravel.com) is a tool that allows Blade-rendered HTML to dynamically re-render without requiring a full page reload. Filament schemas are built on top of Livewire, so they are able to re-render dynamically, allowing their content to adapt after they are initially rendered. By default, when a user uses a field, the schema will not re-render. Since rendering requires a round-trip to the server, this is a performance optimization. However, if you wish to re-render the schema after the user has interacted with a field, you can use the `live()` method:

```
use Filament\Forms\Components\Select;

Select::make('status')
    ->options([
        'draft' => 'Draft',
        'reviewing' => 'Reviewing',
        'published' => 'Published',
    ])
    ->live()
```

In this example, when the user changes the value of the `status` field, the schema will re-render. This allows you to then make changes to fields in the schema based on the new value of the `status` field. Also, you can [hook in to the field’s lifecycle](#field-updates) to perform custom logic when the field is updated.

### [​](#reactive-fields-on-blur)Reactive fields on blur

By default, when a field is set to `live()`, the schema will re-render every time the field is interacted with. However, this may not be appropriate for some fields like the text input, since making network requests while the user is still typing results in suboptimal performance. You may wish to re-render the schema only after the user has finished using the field, when it becomes out of focus. You can do this using the `live(onBlur: true)` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('username')
    ->live(onBlur: true)
```

### [​](#debouncing-reactive-fields)Debouncing reactive fields

You may wish to find a middle ground between `live()` and `live(onBlur: true)`, using “debouncing”. Debouncing will prevent a network request from being sent until a user has finished typing for a certain period of time. You can do this using the `live(debounce: 500)` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('username')
    ->live(debounce: 500) // Wait 500ms before re-rendering the schema.
```

In this example, `500` is the number of milliseconds to wait before sending a network request. You can customize this number to whatever you want, or even use a string like `'1s'`.

## [​](#field-lifecycle)Field lifecycle

Each field in a schema has a lifecycle, which is the process it goes through when the schema is loaded, when it is interacted with by the user, and when it is submitted. You may customize what happens at each stage of this lifecycle using a function that gets run at that stage.

### [​](#field-hydration)Field hydration

Hydration is the process that fills fields with data. It runs when you call the schema’s `fill()` method. You may customize what happens after a field is hydrated using the `afterStateHydrated()` method. In this example, the `name` field will always be hydrated with the correctly capitalized name:

```
use Closure;
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->required()
    ->afterStateHydrated(function (TextInput $component, string $state) {
        $component->state(ucwords($state));
    })
```

As a shortcut for formatting the field’s state like this when it is hydrated, you can use the `formatStateUsing()` method:

```
use Closure;
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->formatStateUsing(fn (string $state): string => ucwords($state))
```

### [​](#field-updates)Field updates

You may use the `afterStateUpdated()` method to customize what happens after the user updates a field:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->afterStateUpdated(function (?string $state, ?string $old) {
        // ...
    })
```

When using `afterStateUpdated()` on a reactive field, interactions will not feel instant since a network request is made. There are a few ways you can [optimize and avoid rendering](#field-rendering) which will make the interaction feel faster.

#### [​](#setting-the-state-of-another-field)Setting the state of another field

In a similar way to `$get`, you may also set the value of another field from within `afterStateUpdated()`, using a `$set` parameter:

```
use Filament\Schemas\Components\Utilities\Set;

function (Set $set) {
    $set('title', 'Blog Post'); // Set the `title` field to `Blog Post`.
    //...
}
```

When this function is run, the state of the `title` field will be updated, and the schema will re-render with the new title. By default, the `afterStateUpdated()` method of the field you set is not called when you use `$set()`. If you wish to call it, you can pass `shouldCallUpdatedHooks: true` as an argument:

```
use Filament\Schemas\Components\Utilities\Set;

function (Set $set) {
    $set('title', 'Blog Post', shouldCallUpdatedHooks: true);
    //...
}
```

### [​](#field-dehydration)Field dehydration

Dehydration is the process that gets data from the fields in your schemas, optionally transforms it, and returns it. It runs when you call the schema’s `getState()` method, which is usually called when a form is submitted. You may customize how the state is transformed when it is dehydrated using the `dehydrateStateUsing()` function. In this example, the `name` field will always be dehydrated with the correctly capitalized name:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->required()
    ->dehydrateStateUsing(fn (string $state): string => ucwords($state))
```

#### [​](#preventing-a-field-from-being-saved)Preventing a field from being saved

You may prevent a field from being saved altogether using `saved(false)`. In this example, the field will not be present in the array returned from `getState()`, and any relationships associated with the field will not be saved either:

```
use Filament\Forms\Components\TextInput;

TextInput::make('password_confirmation')
    ->password()
    ->saved(false)
```

If your schema auto-saves data to the database, like in a [resource](/docs/5.x/resources), this is useful to prevent a field from being saved to the database if it is purely used for presentational purposes.

Even when a field is not saved, it is still validated. To learn more about this behavior, see the [validation](/docs/5.x/forms/validation#disabling-validation-when-fields-are-not-saved) section.

### [​](#field-rendering)Field rendering

Each time a reactive field is updated, the HTML of the entire Livewire component that the schema belongs to is re-generated and sent to the frontend via a network request. In some cases, this may be overkill, especially if the schema is large and only certain components have changed.

#### [​](#field-partial-rendering)Field partial rendering

In this example, the value of the “name” input is used in the label of the “email” input. The “name” input is [`live()`](#the-basics-of-reactivity), so when the user types in the “name” input, the entire schema is re-rendered. This is not ideal, since only the “email” input needs to be re-rendered:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Utilities\Get;

TextInput::make('name')
    ->live()
  
TextInput::make('email')
    ->label(fn (Get $get): string => filled($get('name')) ? "Email address for {$get('name')}" : 'Email address')
```

In this case, a simple call to `partiallyRenderComponentsAfterStateUpdated()`, passing the names of other fields to re-render, will make the schema re-render only the specified fields [after the state is updated](#field-updates):

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->live()
    ->partiallyRenderComponentsAfterStateUpdated(['email'])
```

Alternatively, you can instruct Filament to re-render the current component only, using `partiallyRenderAfterStateUpdated()`. This is useful if the reactive component is the only one that depends on its current state:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->live()
    ->partiallyRenderAfterStateUpdated()
    ->belowContent(fn (Get $get): ?string => filled($get('name')) ? "Hi, {$get('name')}!" : null)
```

#### [​](#preventing-the-livewire-component-from-rendering-after-a-field-is-updated)Preventing the Livewire component from rendering after a field is updated

If you wish to prevent the Livewire component from re-rendering when a field is [updated](#field-updates), you can use the `skipRenderAfterStateUpdated()` method. This is useful if you want to perform some action when the field is updated, but you don’t want the Livewire component to re-render:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->live()
    ->skipRenderAfterStateUpdated()
    ->afterStateUpdated(function (string $state) {
        // Do something with the state, but don't re-render the Livewire component.
    })
```

Since [setting the state of another field](#setting-the-state-of-another-field) from an `afterStateUpdated()` function using the `$set()` method will actually just mutate the frontend state of fields, you don’t even need a network request in the first place. The `afterStateUpdatedJs()` method accepts a JavaScript expression that runs each time the value of the field changes. The [`$state`](#injecting-the-current-state-of-the-field), [`$get()`](#injecting-the-state-of-another-field) and [`$set()`](#setting-the-state-of-another-field) utilities are available in the JavaScript context, so you can use them to set the state of other fields:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Utilities\Set;

// Old name input that is `live()`, so it makes a network request and render each time it is updated.
TextInput::make('name')
    ->live()
    ->afterStateUpdated(fn (Set $set, ?string $state) => $set('email', ((string) str($state)->replace(' ', '.')->lower()) . '@example.com'))

// New name input that uses `afterStateUpdatedJs()` to set the state of the email field and doesn't make a network request.
TextInput::make('name')
    ->afterStateUpdatedJs(<<<'JS'
        $set('email', ($state ?? '').replaceAll(' ', '.').toLowerCase() + '@example.com')
        JS)
  
TextInput::make('email')
    ->label('Email address')
```

Any JavaScript string passed to the `afterStateUpdatedJs()` method will be executed in the browser, so you should never add user input directly into the string, as it could lead to cross-site scripting (XSS) vulnerabilities. User input from `$state` or `$get()` should never be evaluated as JavaScript code, but is safe to use as a string value, like in the example above.

## [​](#reactive-forms-cookbook)Reactive forms cookbook

This section contains a collection of recipes for common tasks you may need to perform when building an advanced form.

### [​](#conditionally-hiding-a-field)Conditionally hiding a field

To conditionally hide or show a field, you can pass a function to the `hidden()` method, and return `true` or `false` depending on whether you want the field to be hidden or not. The function can [inject utilities](#field-utility-injection) as parameters, so you can do things like check the value of another field:

```
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\Checkbox;
use Filament\Forms\Components\TextInput;

Checkbox::make('is_company')
    ->live()

TextInput::make('company_name')
    ->hidden(fn (Get $get): bool => ! $get('is_company'))
```

In this example, the `is_company` checkbox is [`live()`](#the-basics-of-reactivity). This allows the schema to rerender when the value of the `is_company` field changes. You can access the value of that field from within the `hidden()` function using the [`$get()` utility](#injecting-the-state-of-another-field). The value of the field is inverted using `!` so that the `company_name` field is hidden when the `is_company` field is `false`. Alternatively, you can use the `visible()` method to show a field conditionally. It does the exact inverse of `hidden()`, and could be used if you prefer the clarity of the code when written this way:

```
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\Checkbox;
use Filament\Forms\Components\TextInput;

Checkbox::make('is_company')
    ->live()
  
TextInput::make('company_name')
    ->visible(fn (Get $get): bool => $get('is_company'))
```

Using `live()` means the schema reloads every time the field changes, triggering a network request.
Alternatively, you can use [JavaScript to hide the field based on another field’s value](#hiding-a-field-using-javascript).

### [​](#conditionally-making-a-field-required)Conditionally making a field required

To conditionally make a field required, you can pass a function to the `required()` method, and return `true` or `false` depending on whether you want the field to be required or not. The function can [inject utilities](#field-utility-injection) as parameters, so you can do things like check the value of another field:

```
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\TextInput;

TextInput::make('company_name')
    ->live(onBlur: true)
  
TextInput::make('vat_number')
    ->required(fn (Get $get): bool => filled($get('company_name')))
```

In this example, the `company_name` field is [`live(onBlur: true)`](#reactive-fields-on-blur). This allows the schema to rerender after the value of the `company_name` field changes and the user clicks away. You can access the value of that field from within the `required()` function using the [`$get()` utility](#injecting-the-state-of-another-field). The value of the field is checked using `filled()` so that the `vat_number` field is required when the `company_name` field is not `null` or an empty string. The result is that the `vat_number` field is only required when the `company_name` field is filled in. Using a function is able to make any other [validation rule](/docs/5.x/forms/validation) dynamic in a similar way.

### [​](#generating-a-slug-from-a-title)Generating a slug from a title

To generate a slug from a title while the user is typing, you can use the [`afterStateUpdated()` method](#field-updates) on the title field to [`$set()`](#setting-the-state-of-another-field) the value of the slug field:

```
use Filament\Schemas\Components\Utilities\Set;
use Filament\Forms\Components\TextInput;
use Illuminate\Support\Str;

TextInput::make('title')
    ->live(onBlur: true)
    ->afterStateUpdated(fn (Set $set, ?string $state) => $set('slug', Str::slug($state)))
  
TextInput::make('slug')
```

In this example, the `title` field is [`live(onBlur: true)`](#reactive-fields-on-blur). This allows the schema to rerender when the value of the `title` field changes and the user clicks away. The `afterStateUpdated()` method is used to run a function after the state of the `title` field is updated. The function injects the [`$set()` utility](#setting-the-state-of-another-field) and the new state of the `title` field. The `Str::slug()` utility method is part of Laravel and is used to generate a slug from a string. The `slug` field is then updated using the `$set()` function. One thing to note is that the user may customize the slug manually, and we don’t want to overwrite their changes if the title changes. To prevent this, we can use the old version of the title to work out if the user has modified it themselves. To access the old version of the title, you can inject `$old`, and to get the current value of the slug before it gets changed, we can use the [`$get()` utility](#injecting-the-state-of-another-field):

```
use Filament\Schemas\Components\Utilities\Get;
use Filament\Schemas\Components\Utilities\Set;
use Filament\Forms\Components\TextInput;
use Illuminate\Support\Str;

TextInput::make('title')
    ->live(onBlur: true)
    ->afterStateUpdated(function (Get $get, Set $set, ?string $old, ?string $state) {
        if (($get('slug') ?? '') !== Str::slug($old)) {
            return;
        }
  
        $set('slug', Str::slug($state));
    })
  
TextInput::make('slug')
```

### [​](#dependant-select-options)Dependant select options

To dynamically update the options of a [select field](/docs/5.x/forms/select) based on the value of another field, you can pass a function to the `options()` method of the select field. The function can [inject utilities](#field-utility-injection) as parameters, so you can do things like check the value of another field using the [`$get()` utility](#injecting-the-state-of-another-field):

```
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\Select;

Select::make('category')
    ->options([
        'web' => 'Web development',
        'mobile' => 'Mobile development',
        'design' => 'Design',
    ])
    ->live()

Select::make('sub_category')
    ->options(fn (Get $get): array => match ($get('category')) {
        'web' => [
            'frontend_web' => 'Frontend development',
            'backend_web' => 'Backend development',
        ],
        'mobile' => [
            'ios_mobile' => 'iOS development',
            'android_mobile' => 'Android development',
        ],
        'design' => [
            'app_design' => 'Panel design',
            'marketing_website_design' => 'Marketing website design',
        ],
        default => [],
    })
```

In this example, the `category` field is [`live()`](#the-basics-of-reactivity). This allows the schema to rerender when the value of the `category` field changes. You can access the value of that field from within the `options()` function using the [`$get()` utility](#injecting-the-state-of-another-field). The value of the field is used to determine which options should be available in the `sub_category` field. The `match ()` statement in PHP is used to return an array of options based on the value of the `category` field. The result is that the `sub_category` field will only show options relevant to the selected `category` field. You could adapt this example to use options loaded from an Eloquent model or other data source, by querying within the function:

```
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\Select;
use Illuminate\Support\Collection;

Select::make('category')
    ->options(Category::query()->pluck('name', 'id'))
    ->live()
  
Select::make('sub_category')
    ->options(fn (Get $get): Collection => SubCategory::query()
        ->where('category', $get('category'))
        ->pluck('name', 'id'))
```

### [​](#dynamic-fields-based-on-a-select-option)Dynamic fields based on a select option

You may wish to render a different set of fields based on the value of a field, like a select. To do this, you can pass a function to the `schema()` method of any [layout component](/docs/5.x/schemas/layouts), which checks the value of the field and returns a different schema based on that value. Also, you will need a way to initialise the new fields in the dynamic schema when they are first loaded.

```
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Utilities\Get;

Select::make('type')
    ->options([
        'employee' => 'Employee',
        'freelancer' => 'Freelancer',
    ])
    ->live()
    ->afterStateUpdated(fn (Select $component) => $component
        ->getContainer()
        ->getComponent('dynamicTypeFields')
        ->getChildSchema()
        ->fill())
  
Grid::make(2)
    ->schema(fn (Get $get): array => match ($get('type')) {
        'employee' => [
            TextInput::make('employee_number')
                ->required(),
            FileUpload::make('badge')
                ->image()
                ->required(),
        ],
        'freelancer' => [
            TextInput::make('hourly_rate')
                ->numeric()
                ->required()
                ->prefix('€'),
            FileUpload::make('contract')
                ->required(),
        ],
        default => [],
    })
    ->key('dynamicTypeFields')
```

In this example, the `type` field is [`live()`](#the-basics-of-reactivity). This allows the schema to rerender when the value of the `type` field changes. The `afterStateUpdated()` method is used to run a function after the state of the `type` field is updated. In this case, we [inject the current select field instance](#injecting-the-current-field-instance), which we can then use to get the schema “container” instance that holds both the select and the grid components. With this container, we can target the grid component using a unique key (`dynamicTypeFields`) that we have assigned to it. With that grid component instance, we can call `fill()`, just as we do on a normal form to initialise it. The `schema()` method of the grid component is then used to return a different schema based on the value of the `type` field. This is done by using the [`$get()` utility](#injecting-the-state-of-another-field), and returning a different schema array dynamically.

### [​](#auto-hashing-password-field)Auto-hashing password field

You have a password field:

```
use Filament\Forms\Components\TextInput;

TextInput::make('password')
    ->password()
```

And you can use a [dehydration function](#field-dehydration) to hash the password when the form is submitted:

```
use Filament\Forms\Components\TextInput;
use Illuminate\Support\Facades\Hash;

TextInput::make('password')
    ->password()
    ->dehydrateStateUsing(fn (string $state): string => Hash::make($state))
```

But if your schema is used to change an existing password, you don’t want to overwrite the existing password if the field is empty. You can [prevent the field from being saved](#preventing-a-field-from-being-saved) if the field is null or an empty string (using the `filled()` helper):

```
use Filament\Forms\Components\TextInput;
use Illuminate\Support\Facades\Hash;

TextInput::make('password')
    ->password()
    ->dehydrateStateUsing(fn (string $state): string => Hash::make($state))
    ->saved(fn (?string $state): bool => filled($state))
```

However, you want to require the password to be filled when the user is being created, by [injecting the `$operation` utility](#injecting-the-current-operation), and then [conditionally making the field required](#conditionally-making-a-field-required):

```
use Filament\Forms\Components\TextInput;
use Illuminate\Support\Facades\Hash;

TextInput::make('password')
    ->password()
    ->dehydrateStateUsing(fn (string $state): string => Hash::make($state))
    ->saved(fn (?string $state): bool => filled($state))
    ->required(fn (string $operation): bool => $operation === 'create')
```

In this example, `Hash::make($state)` shows how to use a [dehydration function](#field-dehydration). However, you don’t need to do this if your Model uses `'password' => 'hashed'` in its [casts function — Laravel will handle hashing automatically](https://laravel.com/docs/eloquent-mutators#attribute-casting).

## [​](#saving-data-to-relationships)Saving data to relationships

As well as being able to give structure to fields, [layout components](/docs/5.x/schemas/layouts) are also able to “teleport” their nested fields into a relationship. Filament will handle loading data from a `HasOne`, `BelongsTo` or `MorphOne` Eloquent relationship, and then it will save the data back to the same relationship. To set this behavior up, you can use the `relationship()` method on any layout component:

```
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Fieldset;

Fieldset::make('Metadata')
    ->relationship('metadata')
    ->schema([
        TextInput::make('title'),
        Textarea::make('description'),
        FileUpload::make('image'),
    ])
```

In this example, the `title`, `description` and `image` are automatically loaded from the `metadata` relationship, and saved again when the form is submitted. If the `metadata` record does not exist, it is automatically created. This functionality is not just limited to fieldsets - you can use it with any layout component. For example, you could use a `Group` component which has no styling associated with it:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Group;

Group::make()
    ->relationship('customer')
    ->schema([
        TextInput::make('name')
            ->label('Customer')
            ->required(),
        TextInput::make('email')
            ->label('Email address')
            ->email()
            ->required(),
    ])
```

### [​](#saving-data-to-a-belongsto-or-morphto-relationship)Saving data to a `BelongsTo` or `MorphTo` relationship

Please note that if you are saving the data to a `BelongsTo` or `MorphTo` relationship, then the foreign key column in your database must be `nullable()`. This is because Filament saves the schema first, before saving the relationship. Since the schema is saved first, the foreign ID does not exist yet, so it must be nullable. Immediately after the schema is saved, Filament saves the relationship, which will then fill in the foreign ID and save it again. It is worth noting that if you have an observer on your schema model, then you may need to adapt it to ensure that it does not depend on the relationship existing when it is created. For example, if you have an observer that sends an email to a related record when a schema is created, you may need to switch to using a different hook that runs after the relationship is attached, like `updated()`.

#### [​](#specifying-the-related-model-for-a-morphto-relationship)Specifying the related model for a `MorphTo` relationship

If you are using a `MorphTo` relationship, and you want Filament to be able to create `MorphTo` records instead of just updating them, you need to specify the related model using the `relatedModel` parameter of the `relationship()` method:

```
use App\Models\Organization;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Group;

Group::make()
    ->relationship('customer', relatedModel: Organization::class)
    ->schema([
        // ...
    ])
```

In this example, `customer` is a `MorphTo` relationship, and could be an `Individual` or `Organization`. By specifying the `relatedModel` parameter, Filament will be able to create `Organization` records when the form is submitted. If you do not specify this parameter, Filament will only be able to update existing records.

### [​](#conditionally-saving-data-to-a-relationship)Conditionally saving data to a relationship

Sometimes, saving the related record may be optional. If the user fills out the customer fields, then the customer will be created / updated. Otherwise, the customer will not be created, or will be deleted if it already exists. To do this, you can pass a `condition` function as an argument to `relationship()`, which can use the `$state` of the related form to determine whether the relationship should be saved or not:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Group;

Group::make()
    ->relationship(
        'customer',
        condition: fn (?array $state): bool => filled($state['name']),
    )
    ->schema([
        TextInput::make('name')
            ->label('Customer'),
        TextInput::make('email')
            ->label('Email address')
            ->email()
            ->requiredWith('name'),
    ])
```

In this example, the customer’s name is not `required()`, and the email address is only required when the `name` is filled. The `condition` function is used to check whether the `name` field is filled, and if it is, then the customer will be created / updated. Otherwise, the customer will not be created, or will be deleted if it already exists.

### [​](#saving-relationship-data-when-the-component-is-hidden)Saving relationship data when the component is hidden

By default, if a layout component using `relationship()` is hidden when the form is submitted, Filament skips it entirely — the related record is not created or updated, and any existing record is left untouched. This is usually what you want, since hidden components have no state to save. If you need Filament to save the relationship even when the component is hidden — for example, when its field values are populated by [defaults](#setting-the-default-value-of-a-field) — call `saveRelationshipsWhenHidden()`:

```
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Group;

Group::make()
    ->relationship('metadata')
    ->saveRelationshipsWhenHidden()
    ->hidden()
    ->schema([
        TextInput::make('source')
            ->default('admin'),
    ])
```

Combining `saveRelationshipsWhenHidden()` with a `condition` that returns `false` while the component is hidden will cause any existing related record to be deleted when the form is submitted. If you only want to skip saving when the component is hidden, omit `saveRelationshipsWhenHidden()` and rely on the default behavior instead.

## [​](#global-settings)Global settings

If you wish to change the default behavior of a field globally, then you can call the static `configureUsing()` method inside a service provider’s `boot()` method or a middleware. Pass a closure which is able to modify the component. For example, if you wish to make all [checkboxes `inline(false)`](/docs/5.x/forms/checkbox#positioning-the-label-above), you can do it like so:

```
use Filament\Forms\Components\Checkbox;

Checkbox::configureUsing(function (Checkbox $checkbox): void {
    $checkbox->inline(false);
});
```

Of course, you are still able to overwrite this behavior on each field individually:

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')
    ->inline()
```

[Custom components](/docs/5.x/schemas/custom-components)[Text input](/docs/5.x/forms/text-input)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
