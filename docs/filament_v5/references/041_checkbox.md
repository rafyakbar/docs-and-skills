[Forms](/docs/5.x/forms/overview)

# Checkbox

## [​](#introduction)Introduction

The checkbox component, similar to a [toggle](./toggle), allows you to interact a boolean value.

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')
```

If you’re saving the boolean value using Eloquent, you should be sure to add a `boolean` [cast](https://laravel.com/docs/eloquent-mutators#attribute-casting) to the model property:

```
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'is_admin' => 'boolean',
        ];
    }

    // ...
}
```

## [​](#positioning-the-label-above)Positioning the label above

Checkbox fields have two layout modes, inline and stacked. By default, they are inline. When the checkbox is inline, its label is adjacent to it:

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')
    ->inline()
```

When the checkbox is stacked, its label is above it:

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')
    ->inline(false)
```

## [​](#checkbox-validation)Checkbox validation

As well as all rules listed on the [validation](./validation) page, there are additional rules that are specific to checkboxes.

### [​](#accepted-validation)Accepted validation

You may ensure that the checkbox is checked using the `accepted()` method:

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('terms_of_service')
    ->accepted()
```

Optionally, you may pass a boolean value to control if the validation rule should be applied or not:

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('terms_of_service')
    ->accepted(FeatureFlag::active())
```

### [​](#declined-validation)Declined validation

You may ensure that the checkbox is not checked using the `declined()` method:

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_under_18')
    ->declined()
```

Optionally, you may pass a boolean value to control if the validation rule should be applied or not:

```
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_under_18')
    ->declined(FeatureFlag::active())
```

[Select](/docs/5.x/forms/select)[Toggle](/docs/5.x/forms/toggle)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
