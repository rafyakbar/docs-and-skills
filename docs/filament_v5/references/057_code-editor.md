[Forms](/docs/5.x/forms/overview)

# Code editor

## [​](#introduction)Introduction

The code editor component allows you to write code in a textarea with line numbers. By default, no syntax highlighting is applied.

```
use Filament\Forms\Components\CodeEditor;

CodeEditor::make('code')
```

## [​](#using-language-syntax-highlighting)Using language syntax highlighting

You may change the language syntax highlighting of the code editor using the `language()` method. The editor supports the following languages:

- C++
- CSS
- Go
- HTML
- Java
- JavaScript
- JSON
- Markdown
- PHP
- Python
- SQL
- XML
- YAMLYou can open the `Filament\Forms\Components\CodeEditor\Enums\Language` enum class to see this list. To switch to using JavaScript syntax highlighting, you can use the `Language::JavaScript` enum value:

```
use Filament\Forms\Components\CodeEditor;
use Filament\Forms\Components\CodeEditor\Enums\Language;

CodeEditor::make('code')
    ->language(Language::JavaScript)
```

## [​](#allowing-lines-to-wrap)Allowing lines to wrap

By default, long lines in the code editor will create a horizontal scrollbar. If you would like to allow long lines to wrap instead, you may use the `wrap()` method:

```
use Filament\Forms\Components\CodeEditor;

CodeEditor::make('code')
    ->wrap()
```

[Slider](/docs/5.x/forms/slider)[Hidden](/docs/5.x/forms/hidden)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
