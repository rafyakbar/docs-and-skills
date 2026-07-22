[Forms](/docs/5.x/forms/overview)

# Text input

## [​](#introduction)Introduction

The text input allows you to interact with a string:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
```

## [​](#setting-the-html-input-type)Setting the HTML input type

You may set the type of string using a set of methods. Some, such as `email()`, also provide validation:

```
use Filament\Forms\Components\TextInput;

TextInput::make('text')
    ->email() // or
    ->numeric() // or
    ->integer() // or
    ->password() // or
    ->tel() // or
    ->url()
```

You may instead use the `type()` method to pass another [HTML input type](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#input_types):

```
use Filament\Forms\Components\TextInput;

TextInput::make('backgroundColor')
    ->type('color')
```

The individual type methods also allow you to pass in a boolean value to control if the field should be that or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('text')
    ->email(FeatureFlag::active()) // or
    ->numeric(FeatureFlag::active()) // or
    ->integer(FeatureFlag::active()) // or
    ->password(FeatureFlag::active()) // or
    ->tel(FeatureFlag::active()) // or
    ->url(FeatureFlag::active())
```

## [​](#setting-the-html-input-mode)Setting the HTML input mode

You may set the [`inputmode` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#inputmode) of the input using the `inputMode()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('text')
    ->numeric()
    ->inputMode('decimal')
```

## [​](#setting-the-numeric-step)Setting the numeric step

You may set the [`step` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#step) of the input using the `step()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('number')
    ->numeric()
    ->step(100)
```

## [​](#autocompleting-text)Autocompleting text

You may allow the text to be [autocompleted by the browser](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#autocomplete) using the `autocomplete()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('password')
    ->password()
    ->autocomplete('new-password')
```

As a shortcut for `autocomplete="off"`, you may use `autocomplete(false)`:

```
use Filament\Forms\Components\TextInput;

TextInput::make('password')
    ->password()
    ->autocomplete(false)
```

For more complex autocomplete options, text inputs also support [datalists](#autocompleting-text-with-a-datalist).

### [​](#autocompleting-text-with-a-datalist)Autocompleting text with a datalist

You may specify [datalist](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist) options for a text input using the `datalist()` method:

```
TextInput::make('manufacturer')
    ->datalist([
        'BMW',
        'Ford',
        'Mercedes-Benz',
        'Porsche',
        'Toyota',
        'Volkswagen',
    ])
```

Datalists provide autocomplete options to users when they use a text input. However, these are purely recommendations, and the user is still able to type any value into the input. If you’re looking to strictly limit users to a set of predefined options, check out the [select field](./select).

## [​](#autocapitalizing-text)Autocapitalizing text

You may allow the text to be [autocapitalized by the browser](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#autocapitalize) using the `autocapitalize()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->autocapitalize('words')
```

## [​](#adding-affix-text-aside-the-field)Adding affix text aside the field

You may place text before and after the input using the `prefix()` and `suffix()` methods:

```
use Filament\Forms\Components\TextInput;

TextInput::make('domain')
    ->prefix('https://')
    ->suffix('.com')
```

### [​](#using-icons-as-affixes)Using icons as affixes

You may place an [icon](../styling/icons) before and after the input using the `prefixIcon()` and `suffixIcon()` methods:

```
use Filament\Forms\Components\TextInput;
use Filament\Support\Icons\Heroicon;

TextInput::make('domain')
    ->url()
    ->suffixIcon(Heroicon::GlobeAlt)
```

#### [​](#setting-the-affix-icon’s-color)Setting the affix icon’s color

Affix icons are gray by default, but you may set a different color using the `prefixIconColor()` and `suffixIconColor()` methods:

```
use Filament\Forms\Components\TextInput;
use Filament\Support\Icons\Heroicon;

TextInput::make('domain')
    ->url()
    ->suffixIcon(Heroicon::CheckCircle)
    ->suffixIconColor('success')
```

### [​](#using-actions-as-affixes)Using actions as affixes

You may place an [action](../actions) before and after the input using the `prefixAction()` and `suffixAction()` methods:

```
use Filament\Actions\Action;
use Filament\Forms\Components\TextInput;
use Filament\Support\Icons\Heroicon;

TextInput::make('cost')
    ->prefix('€')
    ->suffixAction(
        Action::make('copyCostToPrice')
            ->icon(Heroicon::Clipboard),
    )
```

## [​](#revealable-password-inputs)Revealable password inputs

When using `password()`, you can also make the input `revealable()`, so that the user can see a plain text version of the password they’re typing by clicking a button:

```
use Filament\Forms\Components\TextInput;

TextInput::make('password')
    ->password()
    ->revealable()
```

Optionally, you may pass a boolean value to control if the input should be revealable or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('password')
    ->password()
    ->revealable(FeatureFlag::active())
```

## [​](#allowing-the-text-to-be-copied-to-the-clipboard)Allowing the text to be copied to the clipboard

You may make the text copyable, such that clicking on a button next to the input copies the text to the clipboard, and optionally specify a custom confirmation message and duration in milliseconds:

```
use Filament\Forms\Components\TextInput;

TextInput::make('apiKey')
    ->label('API key')
    ->copyable(copyMessage: 'Copied!', copyMessageDuration: 1500)
```

Optionally, you may pass a boolean value to control if the text should be copyable or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('apiKey')
    ->label('API key')
    ->copyable(FeatureFlag::active())
```

This feature only works when SSL is enabled for the app.

## [​](#input-masking)Input masking

Input masking is the practice of defining a format that the input value must conform to. In Filament, you may use the `mask()` method to configure an [Alpine.js mask](https://alpinejs.dev/plugins/mask#x-mask):

```
use Filament\Forms\Components\TextInput;

TextInput::make('birthday')
    ->mask('99/99/9999')
    ->placeholder('MM/DD/YYYY')
```

To use a [dynamic mask](https://alpinejs.dev/plugins/mask#mask-functions), wrap the JavaScript in a `RawJs` object:

```
use Filament\Forms\Components\TextInput;
use Filament\Support\RawJs;

TextInput::make('cardNumber')
    ->mask(RawJs::make(<<<'JS'
        $input.startsWith('34') || $input.startsWith('37') ? '9999 999999 99999' : '9999 9999 9999 9999'
    JS))
```

Alpine.js will send the entire masked value to the server, so you may need to strip certain characters from the state before validating the field and saving it. You can do this with the `stripCharacters()` method, passing in a character or an array of characters to remove from the masked value:

```
use Filament\Forms\Components\TextInput;
use Filament\Support\RawJs;

TextInput::make('amount')
    ->mask(RawJs::make('$money($input)'))
    ->stripCharacters(',')
    ->numeric()
```

## [​](#trimming-whitespace)Trimming whitespace

You can automatically trim whitespace from the beginning and end of the input value using the `trim()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->trim()
```

You may want to enable trimming globally for all text inputs, similar to Laravel’s `TrimStrings` middleware. You can do this in a service provider using the `configureUsing()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::configureUsing(function (TextInput $component): void {
    $component->trim();
});
```

## [​](#making-the-field-read-only)Making the field read-only

Not to be confused with [disabling the field](./overview#disabling-a-field), you may make the field “read-only” using the `readOnly()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->readOnly()
```

There are a few differences, compared to [`disabled()`](./overview#disabling-a-field):

- When using `readOnly()`, the field will still be sent to the server when the form is submitted. It can be mutated with the browser console, or via JavaScript. You can use [`saved(false)`](./overview#preventing-a-field-from-being-saved) to prevent this.
- There are no styling changes, such as less opacity, when using `readOnly()`.
- The field is still focusable when using `readOnly()`.Optionally, you may pass a boolean value to control if the field should be read-only or not:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->readOnly(FeatureFlag::active())
```

## [​](#text-input-validation)Text input validation

As well as all rules listed on the [validation](./validation) page, there are additional rules that are specific to text inputs.

### [​](#length-validation)Length validation

You may limit the length of the input by setting the `minLength()` and `maxLength()` methods. These methods add both frontend and backend validation:

```
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->minLength(2)
    ->maxLength(255)
```

You can also specify the exact length of the input by setting the `length()`. This method adds both frontend and backend validation:

```
use Filament\Forms\Components\TextInput;

TextInput::make('code')
    ->length(8)
```

### [​](#size-validation)Size validation

You may validate the minimum and maximum value of a numeric input by setting the `minValue()` and `maxValue()` methods:

```
use Filament\Forms\Components\TextInput;

TextInput::make('number')
    ->numeric()
    ->minValue(1)
    ->maxValue(100)
```

### [​](#phone-number-validation)Phone number validation

When using a `tel()` field, the value will be validated using: `/^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$/`. If you wish to change that, then you can use the `telRegex()` method:

```
use Filament\Forms\Components\TextInput;

TextInput::make('phone')
    ->tel()
    ->telRegex('/^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$/')
```

Alternatively, to customize the `telRegex()` across all fields, use a service provider:

```
use Filament\Forms\Components\TextInput;

TextInput::configureUsing(function (TextInput $component): void {
    $component->telRegex('/^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$/');
});
```

[Overview](/docs/5.x/forms/overview)[Select](/docs/5.x/forms/select)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
