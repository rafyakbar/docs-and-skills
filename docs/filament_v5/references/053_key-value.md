[Forms](/docs/5.x/forms/overview)

# Key-value

## [​](#introduction)Introduction

The key-value field allows you to interact with one-dimensional JSON object:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
```

If you’re saving the data in Eloquent, you should be sure to add an `array` [cast](https://laravel.com/docs/eloquent-mutators#array-and-json-casting) to the model property:

```
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'meta' => 'array',
        ];
    }

    // ...
}
```

## [​](#adding-rows)Adding rows

An action button is displayed below the field to allow the user to add a new row.

## [​](#setting-the-add-action-button’s-label)Setting the add action button’s label

You may set a label to customize the text that should be displayed in the button for adding a row, using the `addActionLabel()` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->addActionLabel('Add property')
```

### [​](#preventing-the-user-from-adding-rows)Preventing the user from adding rows

You may prevent the user from adding rows using the `addable(false)` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->addable(false)
```

## [​](#deleting-rows)Deleting rows

An action button is displayed on each item to allow the user to delete it.

### [​](#preventing-the-user-from-deleting-rows)Preventing the user from deleting rows

You may prevent the user from deleting rows using the `deletable(false)` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->deletable(false)
```

## [​](#editing-keys)Editing keys

### [​](#customizing-the-key-fields’-label)Customizing the key fields’ label

You may customize the label for the key fields using the `keyLabel()` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->keyLabel('Property name')
```

### [​](#adding-key-field-placeholders)Adding key field placeholders

You may also add placeholders for the key fields using the `keyPlaceholder()` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->keyPlaceholder('Property name')
```

### [​](#preventing-the-user-from-editing-keys)Preventing the user from editing keys

You may prevent the user from editing keys using the `editableKeys(false)` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->editableKeys(false)
```

## [​](#editing-values)Editing values

### [​](#customizing-the-value-fields’-label)Customizing the value fields’ label

You may customize the label for the value fields using the `valueLabel()` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->valueLabel('Property value')
```

### [​](#adding-value-field-placeholders)Adding value field placeholders

You may also add placeholders for the value fields using the `valuePlaceholder()` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->valuePlaceholder('Property value')
```

### [​](#preventing-the-user-from-editing-values)Preventing the user from editing values

You may prevent the user from editing values using the `editableValues(false)` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->editableValues(false)
```

## [​](#reordering-rows)Reordering rows

You can allow the user to reorder rows within the table using the `reorderable()` method:

```
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
    ->reorderable()
```

## [​](#customizing-the-key-value-action-objects)Customizing the key-value action objects

This field uses action objects for easy customization of buttons within it. You can customize these buttons by passing a function to an action registration method. The function has access to the `$action` object, which you can use to [customize it](../actions/overview). The following methods are available to customize the actions:

- `addAction()`
- `deleteAction()`
- `reorderAction()`Here is an example of how you might customize an action:

```
use Filament\Actions\Action;
use Filament\Forms\Components\KeyValue;
use Filament\Support\Icons\Heroicon;

KeyValue::make('meta')
    ->deleteAction(
        fn (Action $action) => $action->icon(Heroicon::XMark),
    )
```

[Textarea](/docs/5.x/forms/textarea)[Color picker](/docs/5.x/forms/color-picker)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
