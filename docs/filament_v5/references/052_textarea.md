[Forms](/docs/5.x/forms/overview)

# Textarea

## [​](#introduction)Introduction

The textarea allows you to interact with a multi-line string:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
```

## [​](#resizing-the-textarea)Resizing the textarea

You may change the size of the textarea by defining the `rows()` and `cols()` methods:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->rows(10)
    ->cols(20)
```

### [​](#autosizing-the-textarea)Autosizing the textarea

You may allow the textarea to automatically resize to fit its content by setting the `autosize()` method:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->autosize()
```

Optionally, you may pass a boolean value to control if the textarea should be autosizeable or not:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->autosize(FeatureFlag::active())
```

## [​](#making-the-field-read-only)Making the field read-only

Not to be confused with [disabling the field](./overview#disabling-a-field), you may make the field “read-only” using the `readOnly()` method:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->readOnly()
```

There are a few differences, compared to [`disabled()`](./overview#disabling-a-field):

- When using `readOnly()`, the field will still be sent to the server when the form is submitted. It can be mutated with the browser console, or via JavaScript. You can use [`saved(false)`](./overview#preventing-a-field-from-being-saved) to prevent this.
- There are no styling changes, such as less opacity, when using `readOnly()`.
- The field is still focusable when using `readOnly()`.Optionally, you may pass a boolean value to control if the field should be read-only or not:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->readOnly(FeatureFlag::active())
```

## [​](#disabling-grammarly-checks)Disabling Grammarly checks

If the user has Grammarly installed and you would like to prevent it from analyzing the contents of the textarea, you can use the `disableGrammarly()` method:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->disableGrammarly()
```

Optionally, you may pass a boolean value to control if the field should disable Grammarly checks or not:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->disableGrammarly(FeatureFlag::active())
```

## [​](#trimming-whitespace)Trimming whitespace

You can automatically trim whitespace from the beginning and end of the textarea value using the `trim()` method:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->trim()
```

You may want to enable trimming globally for all textareas, similar to Laravel’s `TrimStrings` middleware. You can do this in a service provider using the `configureUsing()` method:

```
use Filament\Forms\Components\Textarea;

Textarea::configureUsing(function (Textarea $component): void {
    $component->trim();
});
```

## [​](#textarea-validation)Textarea validation

As well as all rules listed on the [validation](./validation) page, there are additional rules that are specific to textareas.

### [​](#length-validation)Length validation

You may limit the length of the textarea by setting the `minLength()` and `maxLength()` methods. These methods add both frontend and backend validation:

```
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->minLength(2)
    ->maxLength(1024)
```

You can also specify the exact length of the textarea by setting the `length()`. This method adds both frontend and backend validation:

```
use Filament\Forms\Components\Textarea;

Textarea::make('question')
    ->length(100)
```

[Tags input](/docs/5.x/forms/tags-input)[Key-value](/docs/5.x/forms/key-value)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
