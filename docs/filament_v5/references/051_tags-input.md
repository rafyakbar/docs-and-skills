[Forms](/docs/5.x/forms/overview)

# Tags input

## [​](#introduction)Introduction

The tags input component allows you to interact with a list of tags. By default, tags are stored in JSON:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
```

If you’re saving the JSON tags using Eloquent, you should be sure to add an `array` [cast](https://laravel.com/docs/eloquent-mutators#array-and-json-casting) to the model property:

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
            'tags' => 'array',
        ];
    }

    // ...
}
```

Filament also supports [`spatie/laravel-tags`](https://github.com/spatie/laravel-tags). See our [plugin documentation](https://filamentphp.com/plugins/filament-spatie-tags) for more information.

## [​](#comma-separated-tags)Comma-separated tags

You may allow the tags to be stored in a separated string, instead of JSON. To set this up, pass the separating character to the `separator()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->separator(',')
```

## [​](#autocompleting-tag-suggestions)Autocompleting tag suggestions

Tags inputs may have autocomplete suggestions. To enable this, pass an array of suggestions to the `suggestions()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->suggestions([
        'tailwindcss',
        'alpinejs',
        'laravel',
        'livewire',
    ])
```

## [​](#defining-split-keys)Defining split keys

Split keys allow you to map specific buttons on your user’s keyboard to create a new tag. By default, when the user presses “Enter”, a new tag is created in the input. You may also define other keys to create new tags, such as “Tab” or ” ”. To do this, pass an array of keys to the `splitKeys()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->splitKeys(['Tab', ' '])
```

You can [read more about possible options for keys](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key).

## [​](#adding-a-prefix-and-suffix-to-individual-tags)Adding a prefix and suffix to individual tags

You can add prefix and suffix to tags without modifying the real state of the field. This can be useful if you need to show presentational formatting to users without saving it. This is done with the `tagPrefix()` or `tagSuffix()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('percentages')
    ->tagSuffix('%')
```

## [​](#reordering-tags)Reordering tags

You can allow the user to reorder tags within the field using the `reorderable()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->reorderable()
```

Optionally, you may pass a boolean value to control if the tags should be reorderable or not:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->reorderable(FeatureFlag::active())
```

## [​](#changing-the-color-of-tags)Changing the color of tags

You can change the color of the tags by passing a [color](../styling/colors) to the `color()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->color('danger')
```

## [​](#trimming-whitespace)Trimming whitespace

You can automatically trim whitespace from the beginning and end of each tag using the `trim()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->trim()
```

You may want to enable trimming globally for all tags inputs, similar to Laravel’s `TrimStrings` middleware. You can do this in a service provider using the `configureUsing()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::configureUsing(function (TagsInput $component): void {
    $component->trim();
});
```

## [​](#tags-validation)Tags validation

You may add validation rules for each tag by passing an array of rules to the `nestedRecursiveRules()` method:

```
use Filament\Forms\Components\TagsInput;

TagsInput::make('tags')
    ->nestedRecursiveRules([
        'min:3',
        'max:255',
    ])
```

[Builder](/docs/5.x/forms/builder)[Textarea](/docs/5.x/forms/textarea)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
