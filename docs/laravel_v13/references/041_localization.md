# Localization

- [Introduction](#introduction)
  * [Publishing the Language Files](#publishing-the-language-files)
  * [Configuring the Locale](#configuring-the-locale)
  * [Pluralization Language](#pluralization-language)
- [Defining Translation Strings](#defining-translation-strings)
  * [Using Short Keys](#using-short-keys)
  * [Using Translation Strings as Keys](#using-translation-strings-as-keys)
- [Retrieving Translation Strings](#retrieving-translation-strings)
  * [Replacing Parameters in Translation Strings](#replacing-parameters-in-translation-strings)
  * [Pluralization](#pluralization)
- [Overriding Package Language Files](#overriding-package-language-files)

## [Introduction](#introduction)

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application.

Laravel provides two ways to manage translation strings. First, language strings may be stored in files within the application's `lang` directory. Within this directory, there may be subdirectories for each language supported by the application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages:

```
1/lang

2    /en

3        messages.php

4    /es

5        messages.php
```

Or, translation strings may be defined within JSON files that are placed within the `lang` directory. When taking this approach, each language supported by your application would have a corresponding JSON file within this directory. This approach is recommended for applications that have a large number of translatable strings:

```
1/lang

2    en.json

3    es.json
```

We'll discuss each approach to managing translation strings within this documentation.

### [Publishing the Language Files](#publishing-the-language-files)

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files or create your own, you should scaffold the `lang` directory via the `lang:publish` Artisan command. The `lang:publish` command will create the `lang` directory in your application and publish the default set of language files used by Laravel:

```
1php artisan lang:publish
```

### [Configuring the Locale](#configuring-the-locale)

The default language for your application is stored in the `config/app.php` configuration file's `locale` configuration option, which is typically set using the `APP_LOCALE` environment variable. You are free to modify this value to suit the needs of your application.

You may also configure a "fallback language", which will be used when the default language does not contain a given translation string. Like the default language, the fallback language is also configured in the `config/app.php` configuration file, and its value is typically set using the `APP_FALLBACK_LOCALE` environment variable.

You may modify the default language for a single HTTP request at runtime using the `setLocale` method provided by the `App` facade:

```
 1use Illuminate\Support\Facades\App;

 2 

 3Route::get('/greeting/{locale}', function (string $locale) {

 4    if (! in_array($locale, ['en', 'es', 'fr'])) {

 5        abort(400);

 6    }

 7 

 8    App::setLocale($locale);

 9 

10    // ...

11});
```

#### [Determining the Current Locale](#determining-the-current-locale)

You may use the `currentLocale` and `isLocale` methods on the `App` facade to determine the current locale or check if the locale is a given value:

```
1use Illuminate\Support\Facades\App;

2 

3$locale = App::currentLocale();

4 

5if (App::isLocale('en')) {

6    // ...

7}
```

### [Pluralization Language](#pluralization-language)

You may instruct Laravel's "pluralizer", which is used by Eloquent and other portions of the framework to convert singular strings to plural strings, to use a language other than English. This may be accomplished by invoking the `useLanguage` method within the `boot` method of one of your application's service providers. The pluralizer's currently supported languages are: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, and `turkish`:

```
 1use Illuminate\Support\Pluralizer;

 2 

 3/**

 4 * Bootstrap any application services.

 5 */

 6public function boot(): void

 7{

 8    Pluralizer::useLanguage('spanish');

 9 

10    // ...

11}
```

If you customize the pluralizer's language, you should explicitly define your Eloquent model's [table names](/docs/13.x/eloquent#table-names).

## [Defining Translation Strings](#defining-translation-strings)

### [Using Short Keys](#using-short-keys)

Typically, translation strings are stored in files within the `lang` directory. Within this directory, there should be a subdirectory for each language supported by your application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages:

```
1/lang

2    /en

3        messages.php

4    /es

5        messages.php
```

All language files return an array of keyed strings. For example:

```
1<?php

2 

3// lang/en/messages.php

4 

5return [

6    'welcome' => 'Welcome to our application!',

7];
```

For languages that differ by territory, you should name the language directories according to the ISO 15897. For example, "en_GB" should be used for British English rather than "en-gb".

### [Using Translation Strings as Keys](#using-translation-strings-as-keys)

For applications with a large number of translatable strings, defining every string with a "short key" can become confusing when referencing the keys in your views and it is cumbersome to continually invent keys for every translation string supported by your application.

For this reason, Laravel also provides support for defining translation strings using the "default" translation of the string as the key. Language files that use translation strings as keys are stored as JSON files in the `lang` directory. For example, if your application has a Spanish translation, you should create a `lang/es.json` file:

```
1{

2    "I love programming.": "Me encanta programar."

3}
```

#### Key / File Conflicts

You should not define translation string keys that conflict with other translation filenames. For example, translating `__('Action')` for the "NL" locale while a `nl/action.php` file exists but a `nl.json` file does not exist will result in the translator returning the entire contents of `nl/action.php`.

## [Retrieving Translation Strings](#retrieving-translation-strings)

You may retrieve translation strings from your language files using the `__` helper function. If you are using "short keys" to define your translation strings, you should pass the file that contains the key and the key itself to the `__` function using "dot" syntax. For example, let's retrieve the `welcome` translation string from the `lang/en/messages.php` language file:

```
1echo __('messages.welcome');
```

If the specified translation string does not exist, the `__` function will return the translation string key. So, using the example above, the `__` function would return `messages.welcome` if the translation string does not exist.

If you are using your [default translation strings as your translation keys](#using-translation-strings-as-keys), you should pass the default translation of your string to the `__` function;

```
1echo __('I love programming.');
```

Again, if the translation string does not exist, the `__` function will return the translation string key that it was given.

If you are using the [Blade templating engine](/docs/13.x/blade), you may use the `{{ }}` echo syntax to display the translation string:

```
1{{ __('messages.welcome') }}
```

### [Replacing Parameters in Translation Strings](#replacing-parameters-in-translation-strings)

If you wish, you may define placeholders in your translation strings. All placeholders are prefixed with a `:`. For example, you may define a welcome message with a placeholder name:

```
1'welcome' => 'Welcome, :name',
```

To replace the placeholders when retrieving a translation string, you may pass an array of replacements as the second argument to the `__` function:

```
1echo __('messages.welcome', ['name' => 'dayle']);
```

If your placeholder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly:

```
1'welcome' => 'Welcome, :NAME', // Welcome, DAYLE

2'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

#### [Object Replacement Formatting](#object-replacement-formatting)

If you attempt to provide an object as a translation placeholder, the object's `__toString` method will be invoked. The [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library.

In these cases, Laravel allows you to register a custom formatting handler for that particular type of object. To accomplish this, you should invoke the translator's `stringable` method. The `stringable` method accepts a closure, which should type-hint the type of object that it is responsible for formatting. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class:

```
 1use Illuminate\Support\Facades\Lang;

 2use Money\Money;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Lang::stringable(function (Money $money) {

10        return $money->formatTo('en_GB');

11    });

12}
```

### [Pluralization](#pluralization)

Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization; however, Laravel can help you translate strings differently based on pluralization rules that you define. Using a `|` character, you may distinguish singular and plural forms of a string:

```
1'apples' => 'There is one apple|There are many apples',
```

Of course, pluralization is also supported when using [translation strings as keys](#using-translation-strings-as-keys):

```
1{

2    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"

3}
```

You may even create more complex pluralization rules which specify translation strings for multiple ranges of values:

```
1'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

After defining a translation string that has pluralization options, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the translation string is returned:

```
1echo trans_choice('messages.apples', 10);
```

You may also define placeholder attributes in pluralization strings. These placeholders may be replaced by passing an array as the third argument to the `trans_choice` function:

```
1'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

2 

3echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

If you would like to display the integer value that was passed to the `trans_choice` function, you may use the built-in `:count` placeholder:

```
1'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

## [Overriding Package Language Files](#overriding-package-language-files)

Some packages may ship with their own language files. Instead of changing the package's core files to tweak these lines, you may override them by placing files in the `lang/vendor/{package}/{locale}` directory.

So, for example, if you need to override the English translation strings in `messages.php` for a package named `skyrim/hearthfire`, you should place a language file at: `lang/vendor/hearthfire/en/messages.php`. Within this file, you should only define the translation strings you wish to override. Any translation strings you don't override will still be loaded from the package's original language files.
