[Infolists](/docs/5.x/infolists/overview)

# Key-value entry

## [​](#introduction)Introduction

The key-value entry allows you to render key-value pairs of data, from a one-dimensional JSON object / PHP array.

```
use Filament\Infolists\Components\KeyValueEntry;

KeyValueEntry::make('meta')
```

For example, the state of this entry might be represented as:

```
[
    'description' => 'Filament is a collection of Laravel packages',
    'og:type' => 'website',
    'og:site_name' => 'Filament',
]
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

## [​](#customizing-the-key-column’s-label)Customizing the key column’s label

You may customize the label for the key column using the `keyLabel()` method:

```
use Filament\Infolists\Components\KeyValueEntry;

KeyValueEntry::make('meta')
    ->keyLabel('Property name')
```

## [​](#customizing-the-value-column’s-label)Customizing the value column’s label

You may customize the label for the value column using the `valueLabel()` method:

```
use Filament\Infolists\Components\KeyValueEntry;

KeyValueEntry::make('meta')
    ->valueLabel('Property value')
```

[Code entry](/docs/5.x/infolists/code-entry)[Repeatable entry](/docs/5.x/infolists/repeatable-entry)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
