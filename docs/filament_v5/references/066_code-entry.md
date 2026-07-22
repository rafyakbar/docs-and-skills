[Infolists](/docs/5.x/infolists/overview)

# Code entry

## [​](#introduction)Introduction

The code entry allows you to present a highlighted code snippet in your infolist. It uses [Phiki](https://github.com/phikiphp/phiki) for code highlighting on the server:

```
use Filament\Infolists\Components\CodeEntry;
use Phiki\Grammar\Grammar;

CodeEntry::make('code')
    ->grammar(Grammar::Php)
```

To use the code entry, you need to first install the [`phiki/phiki`](https://github.com/phikiphp/phiki) Composer package. Filament does not include it by default to allow you to choose which major version of Phiki to use explicitly, since major versions can have different grammars and themes available. You can install the latest version of Phiki using the following command:

```
composer require phiki/phiki
```

## [​](#changing-the-code’s-grammar-language)Changing the code’s grammar (language)

You may change the grammar (language) of the code using the `grammar()` method. Over 200 grammars are available, and you can open the `Phiki\Grammar\Grammar` enum class to see the full list. To switch to use JavaScript as the grammar, you can use the `Grammar::Javascript` enum value:

```
use Filament\Infolists\Components\CodeEntry;
use Phiki\Grammar\Grammar;

CodeEntry::make('code')
    ->grammar(Grammar::Javascript)
```

If your code entry’s content is a PHP array, it will automatically be converted to a JSON string, and the grammar will be set to `Grammar::Json`. You can customize the `JSON_` flags used during conversion with the `jsonFlags()` method.

## [​](#changing-the-code’s-theme-highlighting)Changing the code’s theme (highlighting)

You may change the theme of the code using the `lightTheme()` and `darkTheme()` methods. Over 50 themes are available, and you can open the `Phiki\Theme\Theme` enum class to see the full list. To use the popular `Dracula` theme, you can use the `Theme::Dracula` enum value:

```
use Filament\Infolists\Components\CodeEntry;
use Phiki\Theme\Theme;

CodeEntry::make('code')
    ->lightTheme(Theme::Dracula)
    ->darkTheme(Theme::Dracula)
```

## [​](#allowing-the-code-to-be-copied-to-the-clipboard)Allowing the code to be copied to the clipboard

You may make the code copyable, such that clicking on it copies the code to the clipboard, and optionally specify a custom confirmation message and duration in milliseconds. This feature only works when SSL is enabled for the app.

```
use Filament\Infolists\Components\CodeEntry;

CodeEntry::make('code')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
```

Optionally, you may pass a boolean value to control if the code should be copyable or not:

```
use Filament\Infolists\Components\CodeEntry;

CodeEntry::make('code')
    ->copyable(FeatureFlag::active())
```

[Color entry](/docs/5.x/infolists/color-entry)[Key-value entry](/docs/5.x/infolists/key-value-entry)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
