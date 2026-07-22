# Strings

- [Introduction](#introduction)
- [Available Methods](#available-methods)

## [Introduction](#introduction)

Laravel includes a variety of functions for manipulating string values. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient.

## [Available Methods](#available-methods)

### [Strings](#strings-method-list)

[__](#method-__) [class_basename](#method-class-basename) [e](#method-e) [preg_replace_array](#method-preg-replace-array) [Str::after](#method-str-after) [Str::afterLast](#method-str-after-last) [Str::apa](#method-str-apa) [Str::ascii](#method-str-ascii) [Str::before](#method-str-before) [Str::beforeLast](#method-str-before-last) [Str::between](#method-str-between) [Str::betweenFirst](#method-str-between-first) [Str::camel](#method-camel-case) [Str::charAt](#method-char-at) [Str::chopStart](#method-str-chop-start) [Str::chopEnd](#method-str-chop-end) [Str::contains](#method-str-contains) [Str::containsAll](#method-str-contains-all) [Str::counted](#method-str-counted) [Str::doesntContain](#method-str-doesnt-contain) [Str::doesntEndWith](#method-str-doesnt-end-with) [Str::doesntStartWith](#method-str-doesnt-start-with) [Str::deduplicate](#method-deduplicate) [Str::endsWith](#method-ends-with) [Str::excerpt](#method-excerpt) [Str::finish](#method-str-finish) [Str::fromBase64](#method-str-from-base64) [Str::headline](#method-str-headline) [Str::initials](#method-str-initials) [Str::inlineMarkdown](#method-str-inline-markdown) [Str::is](#method-str-is) [Str::isAscii](#method-str-is-ascii) [Str::isJson](#method-str-is-json) [Str::isUlid](#method-str-is-ulid) [Str::isUrl](#method-str-is-url) [Str::isUuid](#method-str-is-uuid) [Str::kebab](#method-kebab-case) [Str::lcfirst](#method-str-lcfirst) [Str::length](#method-str-length) [Str::limit](#method-str-limit) [Str::lower](#method-str-lower) [Str::markdown](#method-str-markdown) [Str::mask](#method-str-mask) [Str::match](#method-str-match) [Str::matchAll](#method-str-match-all) [Str::isMatch](#method-str-is-match) [Str::orderedUuid](#method-str-ordered-uuid) [Str::padBoth](#method-str-padboth) [Str::padLeft](#method-str-padleft) [Str::padRight](#method-str-padright) [Str::password](#method-str-password) [Str::plural](#method-str-plural) [Str::pluralStudly](#method-str-plural-studly) [Str::position](#method-str-position) [Str::random](#method-str-random) [Str::remove](#method-str-remove) [Str::repeat](#method-str-repeat) [Str::replace](#method-str-replace) [Str::replaceArray](#method-str-replace-array) [Str::replaceFirst](#method-str-replace-first) [Str::replaceLast](#method-str-replace-last) [Str::replaceMatches](#method-str-replace-matches) [Str::replaceStart](#method-str-replace-start) [Str::replaceEnd](#method-str-replace-end) [Str::reverse](#method-str-reverse) [Str::singular](#method-str-singular) [Str::slug](#method-str-slug) [Str::snake](#method-snake-case) [Str::squish](#method-str-squish) [Str::start](#method-str-start) [Str::startsWith](#method-starts-with) [Str::studly](#method-studly-case) [Str::substr](#method-str-substr) [Str::substrCount](#method-str-substrcount) [Str::substrReplace](#method-str-substrreplace) [Str::swap](#method-str-swap) [Str::take](#method-take) [Str::title](#method-title-case) [Str::toBase64](#method-str-to-base64) [Str::transliterate](#method-str-transliterate) [Str::trim](#method-str-trim) [Str::ltrim](#method-str-ltrim) [Str::rtrim](#method-str-rtrim) [Str::ucfirst](#method-str-ucfirst) [Str::ucsplit](#method-str-ucsplit) [Str::ucwords](#method-str-ucwords) [Str::upper](#method-str-upper) [Str::ulid](#method-str-ulid) [Str::unwrap](#method-str-unwrap) [Str::uuid](#method-str-uuid) [Str::uuid7](#method-str-uuid7) [Str::wordCount](#method-str-word-count) [Str::wordWrap](#method-str-word-wrap) [Str::words](#method-str-words) [Str::wrap](#method-str-wrap) [str](#method-str) [trans](#method-trans) [trans_choice](#method-trans-choice)

### [Fluent Strings](#fluent-strings-method-list)

[after](#method-fluent-str-after) [afterLast](#method-fluent-str-after-last) [apa](#method-fluent-str-apa) [append](#method-fluent-str-append) [ascii](#method-fluent-str-ascii) [basename](#method-fluent-str-basename) [before](#method-fluent-str-before) [beforeLast](#method-fluent-str-before-last) [between](#method-fluent-str-between) [betweenFirst](#method-fluent-str-between-first) [camel](#method-fluent-str-camel) [charAt](#method-fluent-str-char-at) [classBasename](#method-fluent-str-class-basename) [chopStart](#method-fluent-str-chop-start) [chopEnd](#method-fluent-str-chop-end) [contains](#method-fluent-str-contains) [containsAll](#method-fluent-str-contains-all) [counted](#method-fluent-str-counted) [decrypt](#method-fluent-str-decrypt) [deduplicate](#method-fluent-str-deduplicate) [dirname](#method-fluent-str-dirname) [doesntContain](#method-fluent-str-doesnt-contain) [doesntEndWith](#method-fluent-str-doesnt-end-with) [doesntStartWith](#method-fluent-str-doesnt-start-with) [encrypt](#method-fluent-str-encrypt) [endsWith](#method-fluent-str-ends-with) [exactly](#method-fluent-str-exactly) [excerpt](#method-fluent-str-excerpt) [explode](#method-fluent-str-explode) [finish](#method-fluent-str-finish) [fromBase64](#method-fluent-str-from-base64) [hash](#method-fluent-str-hash) [headline](#method-fluent-str-headline) [initials](#method-fluent-str-initials) [inlineMarkdown](#method-fluent-str-inline-markdown) [is](#method-fluent-str-is) [isAscii](#method-fluent-str-is-ascii) [isEmpty](#method-fluent-str-is-empty) [isNotEmpty](#method-fluent-str-is-not-empty) [isJson](#method-fluent-str-is-json) [isUlid](#method-fluent-str-is-ulid) [isUrl](#method-fluent-str-is-url) [isUuid](#method-fluent-str-is-uuid) [kebab](#method-fluent-str-kebab) [lcfirst](#method-fluent-str-lcfirst) [length](#method-fluent-str-length) [limit](#method-fluent-str-limit) [lower](#method-fluent-str-lower) [markdown](#method-fluent-str-markdown) [mask](#method-fluent-str-mask) [match](#method-fluent-str-match) [matchAll](#method-fluent-str-match-all) [isMatch](#method-fluent-str-is-match) [newLine](#method-fluent-str-new-line) [padBoth](#method-fluent-str-padboth) [padLeft](#method-fluent-str-padleft) [padRight](#method-fluent-str-padright) [pipe](#method-fluent-str-pipe) [plural](#method-fluent-str-plural) [position](#method-fluent-str-position) [prepend](#method-fluent-str-prepend) [remove](#method-fluent-str-remove) [repeat](#method-fluent-str-repeat) [replace](#method-fluent-str-replace) [replaceArray](#method-fluent-str-replace-array) [replaceFirst](#method-fluent-str-replace-first) [replaceLast](#method-fluent-str-replace-last) [replaceMatches](#method-fluent-str-replace-matches) [replaceStart](#method-fluent-str-replace-start) [replaceEnd](#method-fluent-str-replace-end) [scan](#method-fluent-str-scan) [singular](#method-fluent-str-singular) [slug](#method-fluent-str-slug) [snake](#method-fluent-str-snake) [split](#method-fluent-str-split) [squish](#method-fluent-str-squish) [start](#method-fluent-str-start) [startsWith](#method-fluent-str-starts-with) [stripTags](#method-fluent-str-strip-tags) [studly](#method-fluent-str-studly) [substr](#method-fluent-str-substr) [substrReplace](#method-fluent-str-substrreplace) [swap](#method-fluent-str-swap) [take](#method-fluent-str-take) [tap](#method-fluent-str-tap) [test](#method-fluent-str-test) [title](#method-fluent-str-title) [toBase64](#method-fluent-str-to-base64) [toHtmlString](#method-fluent-str-to-html-string) [toUri](#method-fluent-str-to-uri) [transliterate](#method-fluent-str-transliterate) [trim](#method-fluent-str-trim) [ltrim](#method-fluent-str-ltrim) [rtrim](#method-fluent-str-rtrim) [ucfirst](#method-fluent-str-ucfirst) [ucsplit](#method-fluent-str-ucsplit) [ucwords](#method-fluent-str-ucwords) [unwrap](#method-fluent-str-unwrap) [upper](#method-fluent-str-upper) [when](#method-fluent-str-when) [whenContains](#method-fluent-str-when-contains) [whenContainsAll](#method-fluent-str-when-contains-all) [whenDoesntEndWith](#method-fluent-str-when-doesnt-end-with) [whenDoesntStartWith](#method-fluent-str-when-doesnt-start-with) [whenEmpty](#method-fluent-str-when-empty) [whenNotEmpty](#method-fluent-str-when-not-empty) [whenStartsWith](#method-fluent-str-when-starts-with) [whenEndsWith](#method-fluent-str-when-ends-with) [whenExactly](#method-fluent-str-when-exactly) [whenNotExactly](#method-fluent-str-when-not-exactly) [whenIs](#method-fluent-str-when-is) [whenIsAscii](#method-fluent-str-when-is-ascii) [whenIsUlid](#method-fluent-str-when-is-ulid) [whenIsUuid](#method-fluent-str-when-is-uuid) [whenTest](#method-fluent-str-when-test) [wordCount](#method-fluent-str-word-count) [words](#method-fluent-str-words) [wrap](#method-fluent-str-wrap)

## [Strings](#strings)

#### [`__()`](#method-__)

The `__` function translates the given translation string or translation key using your [language files](/docs/13.x/localization):

```
1echo __('Welcome to our application');

2 

3echo __('messages.welcome');
```

If the specified translation string or key does not exist, the `__` function will return the given value. So, using the example above, the `__` function would return `messages.welcome` if that translation key does not exist.

#### [`class_basename()`](#method-class-basename)

The `class_basename` function returns the class name of the given class with the class's namespace removed:

```
1$class = class_basename('Foo\Bar\Baz');

2 

3// Baz
```

#### [`e()`](#method-e)

The `e` function runs PHP's `htmlspecialchars` function with the `double_encode` option set to `true` by default:

```
1echo e('<html>foo</html>');

2 

3// &lt;html&gt;foo&lt;/html&gt;
```

#### [`preg_replace_array()`](#method-preg-replace-array)

The `preg_replace_array` function replaces a given pattern in the string sequentially using an array:

```
1$string = 'The event will take place between :start and :end';

2 

3$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

4 

5// The event will take place between 8:30 and 9:00
```

#### [`Str::after()`](#method-str-after)

The `Str::after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::after('This is my name', 'This is');

4 

5// ' my name'
```

#### [`Str::afterLast()`](#method-str-after-last)

The `Str::afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

4 

5// 'Controller'
```

#### [`Str::apa()`](#method-str-apa)

The `Str::apa` method converts the given string to title case following the [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case):

```
1use Illuminate\Support\Str;

2 

3$title = Str::apa('Creating A Project');

4 

5// 'Creating a Project'
```

#### [`Str::ascii()`](#method-str-ascii)

The `Str::ascii` method will attempt to transliterate the string into an ASCII value:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::ascii('û');

4 

5// 'u'
```

#### [`Str::before()`](#method-str-before)

The `Str::before` method returns everything before the given value in a string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::before('This is my name', 'my name');

4 

5// 'This is '
```

#### [`Str::beforeLast()`](#method-str-before-last)

The `Str::beforeLast` method returns everything before the last occurrence of the given value in a string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::beforeLast('This is my name', 'is');

4 

5// 'This '
```

#### [`Str::between()`](#method-str-between)

The `Str::between` method returns the portion of a string between two values:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::between('This is my name', 'This', 'name');

4 

5// ' is my '
```

#### [`Str::betweenFirst()`](#method-str-between-first)

The `Str::betweenFirst` method returns the smallest possible portion of a string between two values:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

4 

5// 'a'
```

#### [`Str::camel()`](#method-camel-case)

The `Str::camel` method converts the given string to `camelCase`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::camel('foo_bar');

4 

5// 'fooBar'
```

#### [`Str::charAt()`](#method-char-at)

The `Str::charAt` method returns the character at the specified index. If the index is out of bounds, `false` is returned:

```
1use Illuminate\Support\Str;

2 

3$character = Str::charAt('This is my name.', 6);

4 

5// 's'
```

#### [`Str::chopStart()`](#method-str-chop-start)

The `Str::chopStart` method removes the first occurrence of the given value only if the value appears at the start of the string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::chopStart('https://laravel.com', 'https://');

4 

5// 'laravel.com'
```

You may also pass an array as the second argument. If the string starts with any of the values in the array then that value will be removed from string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

4 

5// 'laravel.com'
```

#### [`Str::chopEnd()`](#method-str-chop-end)

The `Str::chopEnd` method removes the last occurrence of the given value only if the value appears at the end of the string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::chopEnd('app/Models/Photograph.php', '.php');

4 

5// 'app/Models/Photograph'
```

You may also pass an array as the second argument. If the string ends with any of the values in the array then that value will be removed from string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

4 

5// 'laravel.com'
```

#### [`Str::contains()`](#method-str-contains)

The `Str::contains` method determines if the given string contains the given value. By default, this method is case sensitive:

```
1use Illuminate\Support\Str;

2 

3$contains = Str::contains('This is my name', 'my');

4 

5// true
```

You may also pass an array of values to determine if the given string contains any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$contains = Str::contains('This is my name', ['my', 'foo']);

4 

5// true
```

You may disable case sensitivity by setting the `ignoreCase` argument to `true`:

```
1use Illuminate\Support\Str;

2 

3$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

4 

5// true
```

#### [`Str::containsAll()`](#method-str-contains-all)

The `Str::containsAll` method determines if the given string contains all of the values in a given array:

```
1use Illuminate\Support\Str;

2 

3$containsAll = Str::containsAll('This is my name', ['my', 'name']);

4 

5// true
```

You may disable case sensitivity by setting the `ignoreCase` argument to `true`:

```
1use Illuminate\Support\Str;

2 

3$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

4 

5// true
```

#### [`Str::doesntContain()`](#method-str-doesnt-contain)

The `Str::doesntContain` method determines if the given string doesn't contain the given value. By default, this method is case sensitive:

```
1use Illuminate\Support\Str;

2 

3$doesntContain = Str::doesntContain('This is name', 'my');

4 

5// true
```

You may also pass an array of values to determine if the given string doesn't contain any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$doesntContain = Str::doesntContain('This is name', ['my', 'framework']);

4 

5// true
```

You may disable case sensitivity by setting the `ignoreCase` argument to `true`:

```
1use Illuminate\Support\Str;

2 

3$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

4 

5// true
```

#### [`Str::deduplicate()`](#method-deduplicate)

The `Str::deduplicate` method replaces consecutive instances of a character with a single instance of that character in the given string. By default, the method deduplicates spaces:

```
1use Illuminate\Support\Str;

2 

3$result = Str::deduplicate('The   Laravel   Framework');

4 

5// The Laravel Framework
```

You may specify a different character to deduplicate by passing it in as the second argument to the method:

```
1use Illuminate\Support\Str;

2 

3$result = Str::deduplicate('The---Laravel---Framework', '-');

4 

5// The-Laravel-Framework
```

#### [`Str::doesntEndWith()`](#method-str-doesnt-end-with)

The `Str::doesntEndWith` method determines if the given string doesn't end with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::doesntEndWith('This is my name', 'dog');

4 

5// true
```

You may also pass an array of values to determine if the given string doesn't end with any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$result = Str::doesntEndWith('This is my name', ['this', 'foo']);

4 

5// true

6 

7$result = Str::doesntEndWith('This is my name', ['name', 'foo']);

8 

9// false
```

#### [`Str::doesntStartWith()`](#method-str-doesnt-start-with)

The `Str::doesntStartWith` method determines if the given string doesn't begin with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::doesntStartWith('This is my name', 'That');

4 

5// true
```

If an array of possible values is passed, the `doesntStartWith` method will return `true` if the string doesn't begin with any of the given values:

```
1$result = Str::doesntStartWith('This is my name', ['What', 'That', 'There']);

2 

3// true
```

#### [`Str::endsWith()`](#method-ends-with)

The `Str::endsWith` method determines if the given string ends with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::endsWith('This is my name', 'name');

4 

5// true
```

You may also pass an array of values to determine if the given string ends with any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$result = Str::endsWith('This is my name', ['name', 'foo']);

4 

5// true

6 

7$result = Str::endsWith('This is my name', ['this', 'foo']);

8 

9// false
```

#### [`Str::excerpt()`](#method-excerpt)

The `Str::excerpt` method extracts an excerpt from a given string that matches the first instance of a phrase within that string:

```
1use Illuminate\Support\Str;

2 

3$excerpt = Str::excerpt('This is my name', 'my', [

4    'radius' => 3

5]);

6 

7// '...is my na...'
```

The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string.

In addition, you may use the `omission` option to define the string that will be prepended and appended to the truncated string:

```
1use Illuminate\Support\Str;

2 

3$excerpt = Str::excerpt('This is my name', 'name', [

4    'radius' => 3,

5    'omission' => '(...) '

6]);

7 

8// '(...) my name'
```

#### [`Str::finish()`](#method-str-finish)

The `Str::finish` method adds a single instance of the given value to a string if it does not already end with that value:

```
1use Illuminate\Support\Str;

2 

3$adjusted = Str::finish('this/string', '/');

4 

5// this/string/

6 

7$adjusted = Str::finish('this/string/', '/');

8 

9// this/string/
```

#### [`Str::fromBase64()`](#method-str-from-base64)

The `Str::fromBase64` method decodes the given Base64 string:

```
1use Illuminate\Support\Str;

2 

3$decoded = Str::fromBase64('TGFyYXZlbA==');

4 

5// Laravel
```

#### [`Str::headline()`](#method-str-headline)

The `Str::headline` method will convert strings delimited by casing, hyphens, or underscores into a space delimited string with each word's first letter capitalized:

```
1use Illuminate\Support\Str;

2 

3$headline = Str::headline('steve_jobs');

4 

5// Steve Jobs

6 

7$headline = Str::headline('EmailNotificationSent');

8 

9// Email Notification Sent
```

#### [`Str::initials()`](#method-str-initials)

The `Str::initials` method will return the initials of a given string, optionally capitalizing them:

```
1use Illuminate\Support\Str;

2 

3$initials = Str::initials('taylor otwell');

4 

5// to

6 

7$initials = Str::initials('taylor otwell', capitalize: true);

8 

9// TO
```

#### [`Str::inlineMarkdown()`](#method-str-inline-markdown)

The `Str::inlineMarkdown` method converts GitHub flavored Markdown into inline HTML using [CommonMark](https://commonmark.thephpleague.com/). However, unlike the `markdown` method, it does not wrap all generated HTML in a block-level element:

```
1use Illuminate\Support\Str;

2 

3$html = Str::inlineMarkdown('**Laravel**');

4 

5// <strong>Laravel</strong>
```

#### Markdown Security

By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier:

```
1use Illuminate\Support\Str;

2 

3Str::inlineMarkdown('Inject: <script>alert("Hello XSS!");</script>', [

4    'html_input' => 'strip',

5    'allow_unsafe_links' => false,

6]);

7 

8// Inject: alert(&quot;Hello XSS!&quot;);
```

#### [`Str::is()`](#method-str-is)

The `Str::is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values:

```
1use Illuminate\Support\Str;

2 

3$matches = Str::is('foo*', 'foobar');

4 

5// true

6 

7$matches = Str::is('baz*', 'foobar');

8 

9// false
```

You may disable case sensitivity by setting the `ignoreCase` argument to `true`:

```
1use Illuminate\Support\Str;

2 

3$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

4 

5// true
```

#### [`Str::isAscii()`](#method-str-is-ascii)

The `Str::isAscii` method determines if a given string is 7-bit ASCII:

```
1use Illuminate\Support\Str;

2 

3$isAscii = Str::isAscii('Taylor');

4 

5// true

6 

7$isAscii = Str::isAscii('ü');

8 

9// false
```

#### [`Str::isJson()`](#method-str-is-json)

The `Str::isJson` method determines if the given string is valid JSON:

```
 1use Illuminate\Support\Str;

 2 

 3$result = Str::isJson('[1,2,3]');

 4 

 5// true

 6 

 7$result = Str::isJson('{"first": "John", "last": "Doe"}');

 8 

 9// true

10 

11$result = Str::isJson('{first: "John", last: "Doe"}');

12 

13// false
```

#### [`Str::isUrl()`](#method-str-is-url)

The `Str::isUrl` method determines if the given string is a valid URL:

```
1use Illuminate\Support\Str;

2 

3$isUrl = Str::isUrl('http://example.com');

4 

5// true

6 

7$isUrl = Str::isUrl('laravel');

8 

9// false
```

The `isUrl` method considers a wide range of protocols as valid. However, you may specify the protocols that should be considered valid by providing them to the `isUrl` method:

```
1$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

#### [`Str::isUlid()`](#method-str-is-ulid)

The `Str::isUlid` method determines if the given string is a valid ULID:

```
1use Illuminate\Support\Str;

2 

3$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

4 

5// true

6 

7$isUlid = Str::isUlid('laravel');

8 

9// false
```

#### [`Str::isUuid()`](#method-str-is-uuid)

The `Str::isUuid` method determines if the given string is a valid UUID:

```
1use Illuminate\Support\Str;

2 

3$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

4 

5// true

6 

7$isUuid = Str::isUuid('laravel');

8 

9// false
```

You may also validate that the given UUID matches a UUID specification by version (1, 3, 4, 5, 6, 7, or 8):

```
1use Illuminate\Support\Str;

2 

3$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 4);

4 

5// true

6 

7$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 1);

8 

9// false
```

#### [`Str::kebab()`](#method-kebab-case)

The `Str::kebab` method converts the given string to `kebab-case`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::kebab('fooBar');

4 

5// foo-bar
```

#### [`Str::lcfirst()`](#method-str-lcfirst)

The `Str::lcfirst` method returns the given string with the first character lowercased:

```
1use Illuminate\Support\Str;

2 

3$string = Str::lcfirst('Foo Bar');

4 

5// foo Bar
```

#### [`Str::length()`](#method-str-length)

The `Str::length` method returns the length of the given string:

```
1use Illuminate\Support\Str;

2 

3$length = Str::length('Laravel');

4 

5// 7
```

#### [`Str::limit()`](#method-str-limit)

The `Str::limit` method truncates the given string to the specified length:

```
1use Illuminate\Support\Str;

2 

3$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

4 

5// The quick brown fox...
```

You may pass a third argument to the method to change the string that will be appended to the end of the truncated string:

```
1$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

2 

3// The quick brown fox (...)
```

If you would like to preserve complete words when truncating the string, you may utilize the `preserveWords` argument. When this argument is `true`, the string will be truncated to the nearest complete word boundary:

```
1$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

2 

3// The quick...
```

#### [`Str::lower()`](#method-str-lower)

The `Str::lower` method converts the given string to lowercase:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::lower('LARAVEL');

4 

5// laravel
```

#### [`Str::markdown()`](#method-str-markdown)

The `Str::markdown` method converts GitHub flavored Markdown into HTML using [CommonMark](https://commonmark.thephpleague.com/):

```
 1use Illuminate\Support\Str;

 2 

 3$html = Str::markdown('# Laravel');

 4 

 5// <h1>Laravel</h1>

 6 

 7$html = Str::markdown('# Taylor <b>Otwell</b>', [

 8    'html_input' => 'strip',

 9]);

10 

11// <h1>Taylor Otwell</h1>
```

#### Markdown Security

By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier:

```
1use Illuminate\Support\Str;

2 

3Str::markdown('Inject: <script>alert("Hello XSS!");</script>', [

4    'html_input' => 'strip',

5    'allow_unsafe_links' => false,

6]);

7 

8// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

#### [`Str::mask()`](#method-str-mask)

The `Str::mask` method masks a portion of a string with a repeated character, and may be used to obfuscate segments of strings such as email addresses and phone numbers:

```
1use Illuminate\Support\Str;

2 

3$string = Str::mask('[[email protected]](/cdn-cgi/l/email-protection)', '*', 3);

4 

5// tay***************
```

If needed, you may provide a negative number as the third argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string:

```
1$string = Str::mask('[[email protected]](/cdn-cgi/l/email-protection)', '*', -15, 3);

2 

3// tay***@example.com
```

#### [`Str::match()`](#method-str-match)

The `Str::match` method will return the portion of a string that matches a given regular expression pattern:

```
1use Illuminate\Support\Str;

2 

3$result = Str::match('/bar/', 'foo bar');

4 

5// 'bar'

6 

7$result = Str::match('/foo (.*)/', 'foo bar');

8 

9// 'bar'
```

#### [`Str::matchAll()`](#method-str-match-all)

The `Str::matchAll` method will return a collection containing the portions of a string that match a given regular expression pattern:

```
1use Illuminate\Support\Str;

2 

3$result = Str::matchAll('/bar/', 'bar foo bar');

4 

5// collect(['bar', 'bar'])
```

If you specify a matching group within the expression, Laravel will return a collection of the first matching group's matches:

```
1use Illuminate\Support\Str;

2 

3$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

4 

5// collect(['un', 'ly']);
```

If no matches are found, an empty collection will be returned.

#### [`Str::isMatch()`](#method-str-is-match)

The `Str::isMatch` method will return `true` if the string matches a given regular expression:

```
1use Illuminate\Support\Str;

2 

3$result = Str::isMatch('/foo (.*)/', 'foo bar');

4 

5// true

6 

7$result = Str::isMatch('/foo (.*)/', 'laravel');

8 

9// false
```

#### [`Str::orderedUuid()`](#method-str-ordered-uuid)

The `Str::orderedUuid` method generates a "timestamp first" UUID that may be efficiently stored in an indexed database column. Each UUID that is generated using this method will be sorted after UUIDs previously generated using the method:

```
1use Illuminate\Support\Str;

2 

3return (string) Str::orderedUuid();
```

#### [`Str::padBoth()`](#method-str-padboth)

The `Str::padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches a desired length:

```
1use Illuminate\Support\Str;

2 

3$padded = Str::padBoth('James', 10, '_');

4 

5// '__James___'

6 

7$padded = Str::padBoth('James', 10);

8 

9// '  James   '
```

#### [`Str::padLeft()`](#method-str-padleft)

The `Str::padLeft` method wraps PHP's `str_pad` function, padding the left side of a string with another string until the final string reaches a desired length:

```
1use Illuminate\Support\Str;

2 

3$padded = Str::padLeft('James', 10, '-=');

4 

5// '-=-=-James'

6 

7$padded = Str::padLeft('James', 10);

8 

9// '     James'
```

#### [`Str::padRight()`](#method-str-padright)

The `Str::padRight` method wraps PHP's `str_pad` function, padding the right side of a string with another string until the final string reaches a desired length:

```
1use Illuminate\Support\Str;

2 

3$padded = Str::padRight('James', 10, '-');

4 

5// 'James-----'

6 

7$padded = Str::padRight('James', 10);

8 

9// 'James     '
```

#### [`Str::password()`](#method-str-password)

The `Str::password` method may be used to generate a secure, random password of a given length. The password will consist of a combination of letters, numbers, symbols, and spaces. By default, passwords are 32 characters long:

```
1use Illuminate\Support\Str;

2 

3$password = Str::password();

4 

5// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

6 

7$password = Str::password(12);

8 

9// 'qwuar>#V|i]N'
```

#### [`Str::counted()`](#method-str-counted)

The `Str::counted` method converts a singular word string to its singular or plural form based on the given count and prefixes the result with the formatted count:

```
1use Illuminate\Support\Str;

2 

3$label = Str::counted('order', 1);

4 

5// 1 order

6 

7$label = Str::counted('order', 1000);

8 

9// 1,000 orders
```

#### [`Str::plural()`](#method-str-plural)

The `Str::plural` method converts a singular word string to its plural form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/13.x/localization#pluralization-language):

```
1use Illuminate\Support\Str;

2 

3$plural = Str::plural('car');

4 

5// cars

6 

7$plural = Str::plural('child');

8 

9// children
```

You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string:

```
1use Illuminate\Support\Str;

2 

3$plural = Str::plural('child', 2);

4 

5// children

6 

7$singular = Str::plural('child', 1);

8 

9// child
```

The `prependCount` argument may be provided to prefix the pluralized string with the formatted `$count`:

```
1use Illuminate\Support\Str;

2 

3$label = Str::plural('car', 1000, prependCount: true);

4 

5// 1,000 cars
```

#### [`Str::pluralStudly()`](#method-str-plural-studly)

The `Str::pluralStudly` method converts a singular word string formatted in studly caps case to its plural form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/13.x/localization#pluralization-language):

```
1use Illuminate\Support\Str;

2 

3$plural = Str::pluralStudly('VerifiedHuman');

4 

5// VerifiedHumans

6 

7$plural = Str::pluralStudly('UserFeedback');

8 

9// UserFeedback
```

You may provide an integer as a second argument to the function to retrieve the singular or plural form of the string:

```
1use Illuminate\Support\Str;

2 

3$plural = Str::pluralStudly('VerifiedHuman', 2);

4 

5// VerifiedHumans

6 

7$singular = Str::pluralStudly('VerifiedHuman', 1);

8 

9// VerifiedHuman
```

#### [`Str::position()`](#method-str-position)

The `Str::position` method returns the position of the first occurrence of a substring in a string. If the substring does not exist in the given string, `false` is returned:

```
1use Illuminate\Support\Str;

2 

3$position = Str::position('Hello, World!', 'Hello');

4 

5// 0

6 

7$position = Str::position('Hello, World!', 'W');

8 

9// 7
```

#### [`Str::random()`](#method-str-random)

The `Str::random` method generates a random string of the specified length. This function uses PHP's `random_bytes` function:

```
1use Illuminate\Support\Str;

2 

3$random = Str::random(40);
```

During testing, it may be useful to "fake" the value that is returned by the `Str::random` method. To accomplish this, you may use the `createRandomStringsUsing` method:

```
1Str::createRandomStringsUsing(function () {

2    return 'fake-random-string';

3});
```

To instruct the `random` method to return to generating random strings normally, you may invoke the `createRandomStringsNormally` method:

```
1Str::createRandomStringsNormally();
```

#### [`Str::remove()`](#method-str-remove)

The `Str::remove` method removes the given value or array of values from the string:

```
1use Illuminate\Support\Str;

2 

3$string = 'Peter Piper picked a peck of pickled peppers.';

4 

5$removed = Str::remove('e', $string);

6 

7// Ptr Pipr pickd a pck of pickld ppprs.
```

You may also pass `false` as a third argument to the `remove` method to ignore case when removing strings.

#### [`Str::repeat()`](#method-str-repeat)

The `Str::repeat` method repeats the given string:

```
1use Illuminate\Support\Str;

2 

3$string = 'a';

4 

5$repeat = Str::repeat($string, 5);

6 

7// aaaaa
```

#### [`Str::replace()`](#method-str-replace)

The `Str::replace` method replaces a given string within the string:

```
1use Illuminate\Support\Str;

2 

3$string = 'Laravel 11.x';

4 

5$replaced = Str::replace('11.x', '12.x', $string);

6 

7// Laravel 12.x
```

The `replace` method also accepts a `caseSensitive` argument. By default, the `replace` method is case sensitive:

```
1$replaced = Str::replace(

2    'php',

3    'Laravel',

4    'PHP Framework for Web Artisans',

5    caseSensitive: false

6);

7 

8// Laravel Framework for Web Artisans
```

#### [`Str::replaceArray()`](#method-str-replace-array)

The `Str::replaceArray` method replaces a given value in the string sequentially using an array:

```
1use Illuminate\Support\Str;

2 

3$string = 'The event will take place between ? and ?';

4 

5$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

6 

7// The event will take place between 8:30 and 9:00
```

#### [`Str::replaceFirst()`](#method-str-replace-first)

The `Str::replaceFirst` method replaces the first occurrence of a given value in a string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

4 

5// a quick brown fox jumps over the lazy dog
```

#### [`Str::replaceLast()`](#method-str-replace-last)

The `Str::replaceLast` method replaces the last occurrence of a given value in a string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

4 

5// the quick brown fox jumps over a lazy dog
```

#### [`Str::replaceMatches()`](#method-str-replace-matches)

The `Str::replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::replaceMatches(

4    pattern: '/[^A-Za-z0-9]++/',

5    replace: '',

6    subject: '(+1) 501-555-1000'

7)

8 

9// '15015551000'
```

The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::replaceMatches('/\d/', function (array $matches) {

4    return '['.$matches[0].']';

5}, '123');

6 

7// '[1][2][3]'
```

#### [`Str::replaceStart()`](#method-str-replace-start)

The `Str::replaceStart` method replaces the first occurrence of the given value only if the value appears at the start of the string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

4 

5// Laravel World

6 

7$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

8 

9// Hello World
```

#### [`Str::replaceEnd()`](#method-str-replace-end)

The `Str::replaceEnd` method replaces the last occurrence of the given value only if the value appears at the end of the string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

4 

5// Hello Laravel

6 

7$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

8 

9// Hello World
```

#### [`Str::reverse()`](#method-str-reverse)

The `Str::reverse` method reverses the given string:

```
1use Illuminate\Support\Str;

2 

3$reversed = Str::reverse('Hello World');

4 

5// dlroW olleH
```

#### [`Str::singular()`](#method-str-singular)

The `Str::singular` method converts a string to its singular form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/13.x/localization#pluralization-language):

```
1use Illuminate\Support\Str;

2 

3$singular = Str::singular('cars');

4 

5// car

6 

7$singular = Str::singular('children');

8 

9// child
```

#### [`Str::slug()`](#method-str-slug)

The `Str::slug` method generates a URL-friendly "slug" from the given string:

```
1use Illuminate\Support\Str;

2 

3$slug = Str::slug('Laravel 5 Framework', '-');

4 

5// laravel-5-framework
```

#### [`Str::snake()`](#method-snake-case)

The `Str::snake` method converts the given string to `snake_case`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::snake('fooBar');

4 

5// foo_bar

6 

7$converted = Str::snake('fooBar', '-');

8 

9// foo-bar
```

#### [`Str::squish()`](#method-str-squish)

The `Str::squish` method removes all extraneous white space from a string, including extraneous white space between words:

```
1use Illuminate\Support\Str;

2 

3$string = Str::squish('    laravel    framework    ');

4 

5// laravel framework
```

#### [`Str::start()`](#method-str-start)

The `Str::start` method adds a single instance of the given value to a string if it does not already start with that value:

```
1use Illuminate\Support\Str;

2 

3$adjusted = Str::start('this/string', '/');

4 

5// /this/string

6 

7$adjusted = Str::start('/this/string', '/');

8 

9// /this/string
```

#### [`Str::startsWith()`](#method-starts-with)

The `Str::startsWith` method determines if the given string begins with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::startsWith('This is my name', 'This');

4 

5// true
```

If an array of possible values is passed, the `startsWith` method will return `true` if the string begins with any of the given values:

```
1$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

2 

3// true
```

#### [`Str::studly()`](#method-studly-case)

The `Str::studly` method converts the given string to `StudlyCase`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::studly('foo_bar');

4 

5// FooBar
```

#### [`Str::substr()`](#method-str-substr)

The `Str::substr` method returns the portion of string specified by the start and length parameters:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::substr('The Laravel Framework', 4, 7);

4 

5// Laravel
```

#### [`Str::substrCount()`](#method-str-substrcount)

The `Str::substrCount` method returns the number of occurrences of a given value in the given string:

```
1use Illuminate\Support\Str;

2 

3$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

4 

5// 2
```

#### [`Str::substrReplace()`](#method-str-substrreplace)

The `Str::substrReplace` method replaces text within a portion of a string, starting at the position specified by the third argument and replacing the number of characters specified by the fourth argument. Passing `0` to the method's fourth argument will insert the string at the specified position without replacing any of the existing characters in the string:

```
1use Illuminate\Support\Str;

2 

3$result = Str::substrReplace('1300', ':', 2);

4// 13:

5 

6$result = Str::substrReplace('1300', ':', 2, 0);

7// 13:00
```

#### [`Str::swap()`](#method-str-swap)

The `Str::swap` method replaces multiple values in the given string using PHP's `strtr` function:

```
1use Illuminate\Support\Str;

2 

3$string = Str::swap([

4    'Tacos' => 'Burritos',

5    'great' => 'fantastic',

6], 'Tacos are great!');

7 

8// Burritos are fantastic!
```

#### [`Str::take()`](#method-take)

The `Str::take` method returns a specified number of characters from the beginning of a string:

```
1use Illuminate\Support\Str;

2 

3$taken = Str::take('Build something amazing!', 5);

4 

5// Build
```

#### [`Str::title()`](#method-title-case)

The `Str::title` method converts the given string to `Title Case`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::title('a nice title uses the correct case');

4 

5// A Nice Title Uses The Correct Case
```

#### [`Str::toBase64()`](#method-str-to-base64)

The `Str::toBase64` method converts the given string to Base64:

```
1use Illuminate\Support\Str;

2 

3$base64 = Str::toBase64('Laravel');

4 

5// TGFyYXZlbA==
```

#### [`Str::transliterate()`](#method-str-transliterate)

The `Str::transliterate` method will attempt to convert a given string into its closest ASCII representation:

```
1use Illuminate\Support\Str;

2 

3$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

4 

5// '[[email protected]](/cdn-cgi/l/email-protection)'
```

#### [`Str::trim()`](#method-str-trim)

The `Str::trim` method strips whitespace (or other characters) from the beginning and end of the given string. Unlike PHP's native `trim` function, the `Str::trim` method also removes unicode whitespace characters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::trim(' foo bar ');

4 

5// 'foo bar'
```

#### [`Str::ltrim()`](#method-str-ltrim)

The `Str::ltrim` method strips whitespace (or other characters) from the beginning of the given string. Unlike PHP's native `ltrim` function, the `Str::ltrim` method also removes unicode whitespace characters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::ltrim('  foo bar  ');

4 

5// 'foo bar  '
```

#### [`Str::rtrim()`](#method-str-rtrim)

The `Str::rtrim` method strips whitespace (or other characters) from the end of the given string. Unlike PHP's native `rtrim` function, the `Str::rtrim` method also removes unicode whitespace characters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::rtrim('  foo bar  ');

4 

5// '  foo bar'
```

#### [`Str::ucfirst()`](#method-str-ucfirst)

The `Str::ucfirst` method returns the given string with the first character capitalized:

```
1use Illuminate\Support\Str;

2 

3$string = Str::ucfirst('foo bar');

4 

5// Foo bar
```

#### [`Str::ucsplit()`](#method-str-ucsplit)

The `Str::ucsplit` method splits the given string into an array by uppercase characters:

```
1use Illuminate\Support\Str;

2 

3$segments = Str::ucsplit('FooBar');

4 

5// [0 => 'Foo', 1 => 'Bar']
```

#### [`Str::ucwords()`](#method-str-ucwords)

The `Str::ucwords` method converts the first character of each word in the given string to uppercase:

```
1use Illuminate\Support\Str;

2 

3$string = Str::ucwords('laravel framework');

4 

5// Laravel Framework
```

#### [`Str::upper()`](#method-str-upper)

The `Str::upper` method converts the given string to uppercase:

```
1use Illuminate\Support\Str;

2 

3$string = Str::upper('laravel');

4 

5// LARAVEL
```

#### [`Str::ulid()`](#method-str-ulid)

The `Str::ulid` method generates a ULID, which is a compact, time-ordered unique identifier:

```
1use Illuminate\Support\Str;

2 

3return (string) Str::ulid();

4 

5// 01gd6r360bp37zj17nxb55yv40
```

If you would like to retrieve a `Illuminate\Support\Carbon` date instance representing the date and time that a given ULID was created, you may use the `createFromId` method provided by Laravel's Carbon integration:

```
1use Illuminate\Support\Carbon;

2use Illuminate\Support\Str;

3 

4$date = Carbon::createFromId((string) Str::ulid());
```

During testing, it may be useful to "fake" the value that is returned by the `Str::ulid` method. To accomplish this, you may use the `createUlidsUsing` method:

```
1use Symfony\Component\Uid\Ulid;

2 

3Str::createUlidsUsing(function () {

4    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');

5});
```

To instruct the `ulid` method to return to generating ULIDs normally, you may invoke the `createUlidsNormally` method:

```
1Str::createUlidsNormally();
```

#### [`Str::unwrap()`](#method-str-unwrap)

The `Str::unwrap` method removes the specified strings from the beginning and end of a given string:

```
1use Illuminate\Support\Str;

2 

3Str::unwrap('-Laravel-', '-');

4 

5// Laravel

6 

7Str::unwrap('{framework: "Laravel"}', '{', '}');

8 

9// framework: "Laravel"
```

#### [`Str::uuid()`](#method-str-uuid)

The `Str::uuid` method generates a UUID (version 4):

```
1use Illuminate\Support\Str;

2 

3return (string) Str::uuid();
```

During testing, it may be useful to "fake" the value that is returned by the `Str::uuid` method. To accomplish this, you may use the `createUuidsUsing` method:

```
1use Ramsey\Uuid\Uuid;

2 

3Str::createUuidsUsing(function () {

4    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');

5});
```

To instruct the `uuid` method to return to generating UUIDs normally, you may invoke the `createUuidsNormally` method:

```
1Str::createUuidsNormally();
```

#### [`Str::uuid7()`](#method-str-uuid7)

The `Str::uuid7` method generates a UUID (version 7):

```
1use Illuminate\Support\Str;

2 

3return (string) Str::uuid7();
```

A `DateTimeInterface` may be passed as an optional parameter which will be used to generate the ordered UUID:

```
1return (string) Str::uuid7(time: now());
```

#### [`Str::wordCount()`](#method-str-word-count)

The `Str::wordCount` method returns the number of words that a string contains:

```
1use Illuminate\Support\Str;

2 

3Str::wordCount('Hello, world!'); // 2
```

#### [`Str::wordWrap()`](#method-str-word-wrap)

The `Str::wordWrap` method wraps a string to a given number of characters:

```
 1use Illuminate\Support\Str;

 2 

 3$text = "The quick brown fox jumped over the lazy dog."

 4 

 5Str::wordWrap($text, characters: 20, break: "<br />\n");

 6 

 7/*

 8The quick brown fox<br />

 9jumped over the lazy<br />

10dog.

11*/
```

#### [`Str::words()`](#method-str-words)

The `Str::words` method limits the number of words in a string. An additional string may be passed to this method via its third argument to specify which string should be appended to the end of the truncated string:

```
1use Illuminate\Support\Str;

2 

3return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

4 

5// Perfectly balanced, as >>>
```

#### [`Str::wrap()`](#method-str-wrap)

The `Str::wrap` method wraps the given string with an additional string or pair of strings:

```
1use Illuminate\Support\Str;

2 

3Str::wrap('Laravel', '"');

4 

5// "Laravel"

6 

7Str::wrap('is', before: 'This ', after: ' Laravel!');

8 

9// This is Laravel!
```

#### [`str()`](#method-str)

The `str` function returns a new `Illuminate\Support\Stringable` instance of the given string. This function is equivalent to the `Str::of` method:

```
1$string = str('Taylor')->append(' Otwell');

2 

3// 'Taylor Otwell'
```

If no argument is provided to the `str` function, the function returns an instance of `Illuminate\Support\Str`:

```
1$snake = str()->snake('FooBar');

2 

3// 'foo_bar'
```

#### [`trans()`](#method-trans)

The `trans` function translates the given translation key using your [language files](/docs/13.x/localization):

```
1echo trans('messages.welcome');
```

If the specified translation key does not exist, the `trans` function will return the given key. So, using the example above, the `trans` function would return `messages.welcome` if the translation key does not exist.

#### [`trans_choice()`](#method-trans-choice)

The `trans_choice` function translates the given translation key with inflection:

```
1echo trans_choice('messages.notifications', $unreadCount);
```

If the specified translation key does not exist, the `trans_choice` function will return the given key. So, using the example above, the `trans_choice` function would return `messages.notifications` if the translation key does not exist.

## [Fluent Strings](#fluent-strings)

Fluent strings provide a more fluent, object-oriented interface for working with string values, allowing you to chain multiple string operations together using a more readable syntax compared to traditional string operations.

#### [`after`](#method-fluent-str-after)

The `after` method returns everything after the given value in a string. The entire string will be returned if the value does not exist within the string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::of('This is my name')->after('This is');

4 

5// ' my name'
```

#### [`afterLast`](#method-fluent-str-after-last)

The `afterLast` method returns everything after the last occurrence of the given value in a string. The entire string will be returned if the value does not exist within the string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

4 

5// 'Controller'
```

#### [`apa`](#method-fluent-str-apa)

The `apa` method converts the given string to title case following the [APA guidelines](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case):

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('a nice title uses the correct case')->apa();

4 

5// A Nice Title Uses the Correct Case
```

#### [`append`](#method-fluent-str-append)

The `append` method appends the given values to the string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Taylor')->append(' Otwell');

4 

5// 'Taylor Otwell'
```

#### [`ascii`](#method-fluent-str-ascii)

The `ascii` method will attempt to transliterate the string into an ASCII value:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('ü')->ascii();

4 

5// 'u'
```

#### [`basename`](#method-fluent-str-basename)

The `basename` method will return the trailing name component of the given string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('/foo/bar/baz')->basename();

4 

5// 'baz'
```

If needed, you may provide an "extension" that will be removed from the trailing component:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

4 

5// 'baz'
```

#### [`before`](#method-fluent-str-before)

The `before` method returns everything before the given value in a string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::of('This is my name')->before('my name');

4 

5// 'This is '
```

#### [`beforeLast`](#method-fluent-str-before-last)

The `beforeLast` method returns everything before the last occurrence of the given value in a string:

```
1use Illuminate\Support\Str;

2 

3$slice = Str::of('This is my name')->beforeLast('is');

4 

5// 'This '
```

#### [`between`](#method-fluent-str-between)

The `between` method returns the portion of a string between two values:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('This is my name')->between('This', 'name');

4 

5// ' is my '
```

#### [`betweenFirst`](#method-fluent-str-between-first)

The `betweenFirst` method returns the smallest possible portion of a string between two values:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

4 

5// 'a'
```

#### [`camel`](#method-fluent-str-camel)

The `camel` method converts the given string to `camelCase`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('foo_bar')->camel();

4 

5// 'fooBar'
```

#### [`charAt`](#method-fluent-str-char-at)

The `charAt` method returns the character at the specified index. If the index is out of bounds, `false` is returned:

```
1use Illuminate\Support\Str;

2 

3$character = Str::of('This is my name.')->charAt(6);

4 

5// 's'
```

#### [`classBasename`](#method-fluent-str-class-basename)

The `classBasename` method returns the class name of the given class with the class's namespace removed:

```
1use Illuminate\Support\Str;

2 

3$class = Str::of('Foo\Bar\Baz')->classBasename();

4 

5// 'Baz'
```

#### [`chopStart`](#method-fluent-str-chop-start)

The `chopStart` method removes the first occurrence of the given value only if the value appears at the start of the string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::of('https://laravel.com')->chopStart('https://');

4 

5// 'laravel.com'
```

You may also pass an array. If the string starts with any of the values in the array then that value will be removed from string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::of('http://laravel.com')->chopStart(['https://', 'http://']);

4 

5// 'laravel.com'
```

#### [`chopEnd`](#method-fluent-str-chop-end)

The `chopEnd` method removes the last occurrence of the given value only if the value appears at the end of the string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::of('https://laravel.com')->chopEnd('.com');

4 

5// 'https://laravel'
```

You may also pass an array. If the string ends with any of the values in the array then that value will be removed from string:

```
1use Illuminate\Support\Str;

2 

3$url = Str::of('http://laravel.com')->chopEnd(['.com', '.io']);

4 

5// 'http://laravel'
```

#### [`contains`](#method-fluent-str-contains)

The `contains` method determines if the given string contains the given value. By default, this method is case sensitive:

```
1use Illuminate\Support\Str;

2 

3$contains = Str::of('This is my name')->contains('my');

4 

5// true
```

You may also pass an array of values to determine if the given string contains any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$contains = Str::of('This is my name')->contains(['my', 'foo']);

4 

5// true
```

You can disable case sensitivity by setting the `ignoreCase` argument to `true`:

```
1use Illuminate\Support\Str;

2 

3$contains = Str::of('This is my name')->contains('MY', ignoreCase: true);

4 

5// true
```

#### [`containsAll`](#method-fluent-str-contains-all)

The `containsAll` method determines if the given string contains all of the values in the given array:

```
1use Illuminate\Support\Str;

2 

3$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

4 

5// true
```

You can disable case sensitivity by setting the `ignoreCase` argument to `true`:

```
1use Illuminate\Support\Str;

2 

3$containsAll = Str::of('This is my name')->containsAll(['MY', 'NAME'], ignoreCase: true);

4 

5// true
```

#### [`decrypt`](#method-fluent-str-decrypt)

The `decrypt` method [decrypts](/docs/13.x/encryption) the encrypted string:

```
1use Illuminate\Support\Str;

2 

3$decrypted = $encrypted->decrypt();

4 

5// 'secret'
```

For the inverse of `decrypt`, see the [encrypt](#method-fluent-str-encrypt) method.

#### [`deduplicate`](#method-fluent-str-deduplicate)

The `deduplicate` method replaces consecutive instances of a character with a single instance of that character in the given string. By default, the method deduplicates spaces:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('The   Laravel   Framework')->deduplicate();

4 

5// The Laravel Framework
```

You may specify a different character to deduplicate by passing it in as the second argument to the method:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('The---Laravel---Framework')->deduplicate('-');

4 

5// The-Laravel-Framework
```

#### [`dirname`](#method-fluent-str-dirname)

The `dirname` method returns the parent directory portion of the given string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('/foo/bar/baz')->dirname();

4 

5// '/foo/bar'
```

If necessary, you may specify how many directory levels you wish to trim from the string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('/foo/bar/baz')->dirname(2);

4 

5// '/foo'
```

#### [`doesntContain()`](#method-fluent-str-doesnt-contain)

The `doesntContain` method determines if the given string does not contain the given value. This method is the inverse of the [contains](#method-fluent-str-contains) method. By default, this method is case sensitive:

```
1use Illuminate\Support\Str;

2 

3$doesntContain = Str::of('This is name')->doesntContain('my');

4 

5// true
```

You may also pass an array of values to determine if the given string does not contain any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$doesntContain = Str::of('This is name')->doesntContain(['my', 'framework']);

4 

5// true
```

You may disable case sensitivity by setting the `ignoreCase` argument to `true`:

```
1use Illuminate\Support\Str;

2 

3$doesntContain = Str::of('This is my name')->doesntContain('MY', ignoreCase: true);

4 

5// false
```

#### [`doesntEndWith`](#method-fluent-str-doesnt-end-with)

The `doesntEndWith` method determines if the given string doesn't end with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->doesntEndWith('dog');

4 

5// true
```

You may also pass an array of values to determine if the given string doesn't end with any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->doesntEndWith(['this', 'foo']);

4 

5// true

6 

7$result = Str::of('This is my name')->doesntEndWith(['name', 'foo']);

8 

9// false
```

#### [`doesntStartWith`](#method-fluent-str-doesnt-start-with)

The `doesntStartWith` method determines if the given string doesn't begin with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->doesntStartWith('That');

4 

5// true
```

You may also pass an array of values to determine if the given string doesn't start with any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->doesntStartWith(['What', 'That', 'There']);

4 

5// true
```

#### [`encrypt`](#method-fluent-str-encrypt)

The `encrypt` method [encrypts](/docs/13.x/encryption) the string:

```
1use Illuminate\Support\Str;

2 

3$encrypted = Str::of('secret')->encrypt();
```

For the inverse of `encrypt`, see the [decrypt](#method-fluent-str-decrypt) method.

#### [`endsWith`](#method-fluent-str-ends-with)

The `endsWith` method determines if the given string ends with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->endsWith('name');

4 

5// true
```

You may also pass an array of values to determine if the given string ends with any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->endsWith(['name', 'foo']);

4 

5// true

6 

7$result = Str::of('This is my name')->endsWith(['this', 'foo']);

8 

9// false
```

#### [`exactly`](#method-fluent-str-exactly)

The `exactly` method determines if the given string is an exact match with another string:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('Laravel')->exactly('Laravel');

4 

5// true
```

#### [`excerpt`](#method-fluent-str-excerpt)

The `excerpt` method extracts an excerpt from the string that matches the first instance of a phrase within that string:

```
1use Illuminate\Support\Str;

2 

3$excerpt = Str::of('This is my name')->excerpt('my', [

4    'radius' => 3

5]);

6 

7// '...is my na...'
```

The `radius` option, which defaults to `100`, allows you to define the number of characters that should appear on each side of the truncated string.

In addition, you may use the `omission` option to change the string that will be prepended and appended to the truncated string:

```
1use Illuminate\Support\Str;

2 

3$excerpt = Str::of('This is my name')->excerpt('name', [

4    'radius' => 3,

5    'omission' => '(...) '

6]);

7 

8// '(...) my name'
```

#### [`explode`](#method-fluent-str-explode)

The `explode` method splits the string by the given delimiter and returns a collection containing each section of the split string:

```
1use Illuminate\Support\Str;

2 

3$collection = Str::of('foo bar baz')->explode(' ');

4 

5// collect(['foo', 'bar', 'baz'])
```

#### [`finish`](#method-fluent-str-finish)

The `finish` method adds a single instance of the given value to a string if it does not already end with that value:

```
1use Illuminate\Support\Str;

2 

3$adjusted = Str::of('this/string')->finish('/');

4 

5// this/string/

6 

7$adjusted = Str::of('this/string/')->finish('/');

8 

9// this/string/
```

#### [`fromBase64`](#method-fluent-str-from-base64)

The `fromBase64` method decodes the given Base64 string:

```
1use Illuminate\Support\Str;

2 

3$decoded = Str::of('TGFyYXZlbA==')->fromBase64();

4 

5// Laravel
```

#### [`hash`](#method-fluent-str-hash)

The `hash` method hashes the string using the given [algorithm](https://www.php.net/manual/en/function.hash-algos.php):

```
1use Illuminate\Support\Str;

2 

3$hashed = Str::of('secret')->hash(algorithm: 'sha256');

4 

5// '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
```

#### [`headline`](#method-fluent-str-headline)

The `headline` method will convert strings delimited by casing, hyphens, or underscores into a space delimited string with each word's first letter capitalized:

```
1use Illuminate\Support\Str;

2 

3$headline = Str::of('taylor_otwell')->headline();

4 

5// Taylor Otwell

6 

7$headline = Str::of('EmailNotificationSent')->headline();

8 

9// Email Notification Sent
```

#### [`initials`](#method-fluent-str-initials)

The `initials` method will convert the string to its initials:

```
1use Illuminate\Support\Str;

2 

3$initials = Str::of('Taylor Otwell')->initials()->upper();

4 

5// TO
```

#### [`inlineMarkdown`](#method-fluent-str-inline-markdown)

The `inlineMarkdown` method converts GitHub flavored Markdown into inline HTML using [CommonMark](https://commonmark.thephpleague.com/). However, unlike the `markdown` method, it does not wrap all generated HTML in a block-level element:

```
1use Illuminate\Support\Str;

2 

3$html = Str::of('**Laravel**')->inlineMarkdown();

4 

5// <strong>Laravel</strong>
```

#### Markdown Security

By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier:

```
1use Illuminate\Support\Str;

2 

3Str::of('Inject: <script>alert("Hello XSS!");</script>')->inlineMarkdown([

4    'html_input' => 'strip',

5    'allow_unsafe_links' => false,

6]);

7 

8// Inject: alert(&quot;Hello XSS!&quot;);
```

#### [`is`](#method-fluent-str-is)

The `is` method determines if a given string matches a given pattern. Asterisks may be used as wildcard values

```
1use Illuminate\Support\Str;

2 

3$matches = Str::of('foobar')->is('foo*');

4 

5// true

6 

7$matches = Str::of('foobar')->is('baz*');

8 

9// false
```

#### [`isAscii`](#method-fluent-str-is-ascii)

The `isAscii` method determines if a given string is an ASCII string:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('Taylor')->isAscii();

4 

5// true

6 

7$result = Str::of('ü')->isAscii();

8 

9// false
```

#### [`isEmpty`](#method-fluent-str-is-empty)

The `isEmpty` method determines if the given string is empty:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('  ')->trim()->isEmpty();

4 

5// true

6 

7$result = Str::of('Laravel')->trim()->isEmpty();

8 

9// false
```

#### [`isNotEmpty`](#method-fluent-str-is-not-empty)

The `isNotEmpty` method determines if the given string is not empty:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('  ')->trim()->isNotEmpty();

4 

5// false

6 

7$result = Str::of('Laravel')->trim()->isNotEmpty();

8 

9// true
```

#### [`isJson`](#method-fluent-str-is-json)

The `isJson` method determines if a given string is valid JSON:

```
 1use Illuminate\Support\Str;

 2 

 3$result = Str::of('[1,2,3]')->isJson();

 4 

 5// true

 6 

 7$result = Str::of('{"first": "John", "last": "Doe"}')->isJson();

 8 

 9// true

10 

11$result = Str::of('{first: "John", last: "Doe"}')->isJson();

12 

13// false
```

#### [`isUlid`](#method-fluent-str-is-ulid)

The `isUlid` method determines if a given string is a ULID:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

4 

5// true

6 

7$result = Str::of('Taylor')->isUlid();

8 

9// false
```

#### [`isUrl`](#method-fluent-str-is-url)

The `isUrl` method determines if a given string is a URL:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('http://example.com')->isUrl();

4 

5// true

6 

7$result = Str::of('Taylor')->isUrl();

8 

9// false
```

The `isUrl` method considers a wide range of protocols as valid. However, you may specify the protocols that should be considered valid by providing them to the `isUrl` method:

```
1$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

#### [`isUuid`](#method-fluent-str-is-uuid)

The `isUuid` method determines if a given string is a UUID:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

4 

5// true

6 

7$result = Str::of('Taylor')->isUuid();

8 

9// false
```

You may also validate that the given UUID matches a UUID specification by version (1, 3, 4, 5, 6, 7, or 8):

```
1use Illuminate\Support\Str;

2 

3$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 4);

4 

5// true

6 

7$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 1);

8 

9// false
```

#### [`kebab`](#method-fluent-str-kebab)

The `kebab` method converts the given string to `kebab-case`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('fooBar')->kebab();

4 

5// foo-bar
```

#### [`lcfirst`](#method-fluent-str-lcfirst)

The `lcfirst` method returns the given string with the first character lowercased:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Foo Bar')->lcfirst();

4 

5// foo Bar
```

#### [`length`](#method-fluent-str-length)

The `length` method returns the length of the given string:

```
1use Illuminate\Support\Str;

2 

3$length = Str::of('Laravel')->length();

4 

5// 7
```

#### [`limit`](#method-fluent-str-limit)

The `limit` method truncates the given string to the specified length:

```
1use Illuminate\Support\Str;

2 

3$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

4 

5// The quick brown fox...
```

You may also pass a second argument to change the string that will be appended to the end of the truncated string:

```
1$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

2 

3// The quick brown fox (...)
```

If you would like to preserve complete words when truncating the string, you may utilize the `preserveWords` argument. When this argument is `true`, the string will be truncated to the nearest complete word boundary:

```
1$truncated = Str::of('The quick brown fox')->limit(12, preserveWords: true);

2 

3// The quick...
```

#### [`lower`](#method-fluent-str-lower)

The `lower` method converts the given string to lowercase:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('LARAVEL')->lower();

4 

5// 'laravel'
```

#### [`markdown`](#method-fluent-str-markdown)

The `markdown` method converts GitHub flavored Markdown into HTML:

```
 1use Illuminate\Support\Str;

 2 

 3$html = Str::of('# Laravel')->markdown();

 4 

 5// <h1>Laravel</h1>

 6 

 7$html = Str::of('# Taylor <b>Otwell</b>')->markdown([

 8    'html_input' => 'strip',

 9]);

10 

11// <h1>Taylor Otwell</h1>
```

#### Markdown Security

By default, Markdown supports raw HTML, which will expose Cross-Site Scripting (XSS) vulnerabilities when used with raw user input. As per the [CommonMark Security documentation](https://commonmark.thephpleague.com/security/), you may use the `html_input` option to either escape or strip raw HTML, and the `allow_unsafe_links` option to specify whether to allow unsafe links. If you need to allow some raw HTML, you should pass your compiled Markdown through an HTML Purifier:

```
1use Illuminate\Support\Str;

2 

3Str::of('Inject: <script>alert("Hello XSS!");</script>')->markdown([

4    'html_input' => 'strip',

5    'allow_unsafe_links' => false,

6]);

7 

8// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

#### [`mask`](#method-fluent-str-mask)

The `mask` method masks a portion of a string with a repeated character, and may be used to obfuscate segments of strings such as email addresses and phone numbers:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('[[email protected]](/cdn-cgi/l/email-protection)')->mask('*', 3);

4 

5// tay***************
```

If needed, you may provide negative numbers as the third or fourth argument to the `mask` method, which will instruct the method to begin masking at the given distance from the end of the string:

```
1$string = Str::of('[[email protected]](/cdn-cgi/l/email-protection)')->mask('*', -15, 3);

2 

3// tay***@example.com

4 

5$string = Str::of('[[email protected]](/cdn-cgi/l/email-protection)')->mask('*', 4, -4);

6 

7// tayl**********.com
```

#### [`match`](#method-fluent-str-match)

The `match` method will return the portion of a string that matches a given regular expression pattern:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('foo bar')->match('/bar/');

4 

5// 'bar'

6 

7$result = Str::of('foo bar')->match('/foo (.*)/');

8 

9// 'bar'
```

#### [`matchAll`](#method-fluent-str-match-all)

The `matchAll` method will return a collection containing the portions of a string that match a given regular expression pattern:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('bar foo bar')->matchAll('/bar/');

4 

5// collect(['bar', 'bar'])
```

If you specify a matching group within the expression, Laravel will return a collection of the first matching group's matches:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

4 

5// collect(['un', 'ly']);
```

If no matches are found, an empty collection will be returned.

#### [`isMatch`](#method-fluent-str-is-match)

The `isMatch` method will return `true` if the string matches a given regular expression:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('foo bar')->isMatch('/foo (.*)/');

4 

5// true

6 

7$result = Str::of('laravel')->isMatch('/foo (.*)/');

8 

9// false
```

#### [`newLine`](#method-fluent-str-new-line)

The `newLine` method appends an "end of line" character to a string:

```
1use Illuminate\Support\Str;

2 

3$padded = Str::of('Laravel')->newLine()->append('Framework');

4 

5// 'Laravel

6//  Framework'
```

#### [`padBoth`](#method-fluent-str-padboth)

The `padBoth` method wraps PHP's `str_pad` function, padding both sides of a string with another string until the final string reaches the desired length:

```
1use Illuminate\Support\Str;

2 

3$padded = Str::of('James')->padBoth(10, '_');

4 

5// '__James___'

6 

7$padded = Str::of('James')->padBoth(10);

8 

9// '  James   '
```

#### [`padLeft`](#method-fluent-str-padleft)

The `padLeft` method wraps PHP's `str_pad` function, padding the left side of a string with another string until the final string reaches the desired length:

```
1use Illuminate\Support\Str;

2 

3$padded = Str::of('James')->padLeft(10, '-=');

4 

5// '-=-=-James'

6 

7$padded = Str::of('James')->padLeft(10);

8 

9// '     James'
```

#### [`padRight`](#method-fluent-str-padright)

The `padRight` method wraps PHP's `str_pad` function, padding the right side of a string with another string until the final string reaches the desired length:

```
1use Illuminate\Support\Str;

2 

3$padded = Str::of('James')->padRight(10, '-');

4 

5// 'James-----'

6 

7$padded = Str::of('James')->padRight(10);

8 

9// 'James     '
```

#### [`pipe`](#method-fluent-str-pipe)

The `pipe` method allows you to transform the string by passing its current value to the given callable:

```
 1use Illuminate\Support\Str;

 2use Illuminate\Support\Stringable;

 3 

 4$hash = Str::of('Laravel')->pipe('md5')->prepend('Checksum: ');

 5 

 6// 'Checksum: a5c95b86291ea299fcbe64458ed12702'

 7 

 8$closure = Str::of('foo')->pipe(function (Stringable $str) {

 9    return 'bar';

10});

11 

12// 'bar'
```

#### [`counted`](#method-fluent-str-counted)

The `counted` method converts a singular word string to its singular or plural form based on the given count and prefixes the result with the formatted count:

```
1use Illuminate\Support\Str;

2 

3$label = Str::of('order')->counted(1);

4 

5// 1 order

6 

7$label = Str::of('order')->counted(1000);

8 

9// 1,000 orders
```

#### [`plural`](#method-fluent-str-plural)

The `plural` method converts a singular word string to its plural form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/13.x/localization#pluralization-language):

```
1use Illuminate\Support\Str;

2 

3$plural = Str::of('car')->plural();

4 

5// cars

6 

7$plural = Str::of('child')->plural();

8 

9// children
```

You may provide an integer argument to the function to retrieve the singular or plural form of the string:

```
1use Illuminate\Support\Str;

2 

3$plural = Str::of('child')->plural(2);

4 

5// children

6 

7$plural = Str::of('child')->plural(1);

8 

9// child
```

You may provide the `prependCount` argument to prefix the pluralized string with the formatted `$count`:

```
1use Illuminate\Support\Str;

2 

3$label = Str::of('car')->plural(1000, prependCount: true);

4 

5// 1,000 cars
```

#### [`position`](#method-fluent-str-position)

The `position` method returns the position of the first occurrence of a substring in a string. If the substring does not exist within the string, `false` is returned:

```
1use Illuminate\Support\Str;

2 

3$position = Str::of('Hello, World!')->position('Hello');

4 

5// 0

6 

7$position = Str::of('Hello, World!')->position('W');

8 

9// 7
```

#### [`prepend`](#method-fluent-str-prepend)

The `prepend` method prepends the given values onto the string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Framework')->prepend('Laravel ');

4 

5// Laravel Framework
```

#### [`remove`](#method-fluent-str-remove)

The `remove` method removes the given value or array of values from the string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Arkansas is quite beautiful!')->remove('quite ');

4 

5// Arkansas is beautiful!
```

You may also pass `false` as a second parameter to ignore case when removing strings.

#### [`repeat`](#method-fluent-str-repeat)

The `repeat` method repeats the given string:

```
1use Illuminate\Support\Str;

2 

3$repeated = Str::of('a')->repeat(5);

4 

5// aaaaa
```

#### [`replace`](#method-fluent-str-replace)

The `replace` method replaces a given string within the string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

4 

5// Laravel 7.x
```

The `replace` method also accepts a `caseSensitive` argument. By default, the `replace` method is case sensitive:

```
1$replaced = Str::of('macOS 13.x')->replace(

2    'macOS', 'iOS', caseSensitive: false

3);
```

#### [`replaceArray`](#method-fluent-str-replace-array)

The `replaceArray` method replaces a given value in the string sequentially using an array:

```
1use Illuminate\Support\Str;

2 

3$string = 'The event will take place between ? and ?';

4 

5$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

6 

7// The event will take place between 8:30 and 9:00
```

#### [`replaceFirst`](#method-fluent-str-replace-first)

The `replaceFirst` method replaces the first occurrence of a given value in a string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

4 

5// a quick brown fox jumps over the lazy dog
```

#### [`replaceLast`](#method-fluent-str-replace-last)

The `replaceLast` method replaces the last occurrence of a given value in a string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

4 

5// the quick brown fox jumps over a lazy dog
```

#### [`replaceMatches`](#method-fluent-str-replace-matches)

The `replaceMatches` method replaces all portions of a string matching a pattern with the given replacement string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

4 

5// '15015551000'
```

The `replaceMatches` method also accepts a closure that will be invoked with each portion of the string matching the given pattern, allowing you to perform the replacement logic within the closure and return the replaced value:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::of('123')->replaceMatches('/\d/', function (array $matches) {

4    return '['.$matches[0].']';

5});

6 

7// '[1][2][3]'
```

#### [`replaceStart`](#method-fluent-str-replace-start)

The `replaceStart` method replaces the first occurrence of the given value only if the value appears at the start of the string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::of('Hello World')->replaceStart('Hello', 'Laravel');

4 

5// Laravel World

6 

7$replaced = Str::of('Hello World')->replaceStart('World', 'Laravel');

8 

9// Hello World
```

#### [`replaceEnd`](#method-fluent-str-replace-end)

The `replaceEnd` method replaces the last occurrence of the given value only if the value appears at the end of the string:

```
1use Illuminate\Support\Str;

2 

3$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

4 

5// Hello Laravel

6 

7$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

8 

9// Hello World
```

#### [`scan`](#method-fluent-str-scan)

The `scan` method parses input from a string into a collection according to a format supported by the [`sscanf` PHP function](https://www.php.net/manual/en/function.sscanf.php):

```
1use Illuminate\Support\Str;

2 

3$collection = Str::of('filename.jpg')->scan('%[^.].%s');

4 

5// collect(['filename', 'jpg'])
```

#### [`singular`](#method-fluent-str-singular)

The `singular` method converts a string to its singular form. This function supports [any of the languages supported by Laravel's pluralizer](/docs/13.x/localization#pluralization-language):

```
1use Illuminate\Support\Str;

2 

3$singular = Str::of('cars')->singular();

4 

5// car

6 

7$singular = Str::of('children')->singular();

8 

9// child
```

#### [`slug`](#method-fluent-str-slug)

The `slug` method generates a URL-friendly "slug" from the given string:

```
1use Illuminate\Support\Str;

2 

3$slug = Str::of('Laravel Framework')->slug('-');

4 

5// laravel-framework
```

#### [`snake`](#method-fluent-str-snake)

The `snake` method converts the given string to `snake_case`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('fooBar')->snake();

4 

5// foo_bar
```

#### [`split`](#method-fluent-str-split)

The `split` method splits a string into a collection using a regular expression:

```
1use Illuminate\Support\Str;

2 

3$segments = Str::of('one, two, three')->split('/[\s,]+/');

4 

5// collect(["one", "two", "three"])
```

#### [`squish`](#method-fluent-str-squish)

The `squish` method removes all extraneous white space from a string, including extraneous white space between words:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('    laravel    framework    ')->squish();

4 

5// laravel framework
```

#### [`start`](#method-fluent-str-start)

The `start` method adds a single instance of the given value to a string if it does not already start with that value:

```
1use Illuminate\Support\Str;

2 

3$adjusted = Str::of('this/string')->start('/');

4 

5// /this/string

6 

7$adjusted = Str::of('/this/string')->start('/');

8 

9// /this/string
```

#### [`startsWith`](#method-fluent-str-starts-with)

The `startsWith` method determines if the given string begins with the given value:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->startsWith('This');

4 

5// true
```

You may also pass an array of values to determine if the given string starts with any of the values in the array:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('This is my name')->startsWith(['This', 'That']);

4 

5// true
```

#### [`stripTags`](#method-fluent-str-strip-tags)

The `stripTags` method removes all HTML and PHP tags from a string:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags();

4 

5// Taylor Otwell

6 

7$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags('<b>');

8 

9// Taylor <b>Otwell</b>
```

#### [`studly`](#method-fluent-str-studly)

The `studly` method converts the given string to `StudlyCase`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('foo_bar')->studly();

4 

5// FooBar
```

#### [`substr`](#method-fluent-str-substr)

The `substr` method returns the portion of the string specified by the given start and length parameters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Laravel Framework')->substr(8);

4 

5// Framework

6 

7$string = Str::of('Laravel Framework')->substr(8, 5);

8 

9// Frame
```

#### [`substrReplace`](#method-fluent-str-substrreplace)

The `substrReplace` method replaces text within a portion of a string, starting at the position specified by the second argument and replacing the number of characters specified by the third argument. Passing `0` to the method's third argument will insert the string at the specified position without replacing any of the existing characters in the string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('1300')->substrReplace(':', 2);

4 

5// 13:

6 

7$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

8 

9// The Laravel Framework
```

#### [`swap`](#method-fluent-str-swap)

The `swap` method replaces multiple values in the string using PHP's `strtr` function:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Tacos are great!')

4    ->swap([

5        'Tacos' => 'Burritos',

6        'great' => 'fantastic',

7    ]);

8 

9// Burritos are fantastic!
```

#### [`take`](#method-fluent-str-take)

The `take` method returns a specified number of characters from the beginning of the string:

```
1use Illuminate\Support\Str;

2 

3$taken = Str::of('Build something amazing!')->take(5);

4 

5// Build
```

#### [`tap`](#method-fluent-str-tap)

The `tap` method passes the string to the given closure, allowing you to examine and interact with the string while not affecting the string itself. The original string is returned by the `tap` method regardless of what is returned by the closure:

```
 1use Illuminate\Support\Str;

 2use Illuminate\Support\Stringable;

 3 

 4$string = Str::of('Laravel')

 5    ->append(' Framework')

 6    ->tap(function (Stringable $string) {

 7        dump('String after append: '.$string);

 8    })

 9    ->upper();

10 

11// LARAVEL FRAMEWORK
```

#### [`test`](#method-fluent-str-test)

The `test` method determines if a string matches the given regular expression pattern:

```
1use Illuminate\Support\Str;

2 

3$result = Str::of('Laravel Framework')->test('/Laravel/');

4 

5// true
```

#### [`title`](#method-fluent-str-title)

The `title` method converts the given string to `Title Case`:

```
1use Illuminate\Support\Str;

2 

3$converted = Str::of('a nice title uses the correct case')->title();

4 

5// A Nice Title Uses The Correct Case
```

#### [`toBase64`](#method-fluent-str-to-base64)

The `toBase64` method converts the given string to Base64:

```
1use Illuminate\Support\Str;

2 

3$base64 = Str::of('Laravel')->toBase64();

4 

5// TGFyYXZlbA==
```

#### [`toHtmlString`](#method-fluent-str-to-html-string)

The `toHtmlString` method converts the given string to an instance of `Illuminate\Support\HtmlString`, which will not be escaped when rendered in Blade templates:

```
1use Illuminate\Support\Str;

2 

3$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

#### [`toUri`](#method-fluent-str-to-uri)

The `toUri` method converts the given string to an instance of [Illuminate\Support\Uri](/docs/13.x/helpers#uri):

```
1use Illuminate\Support\Str;

2 

3$uri = Str::of('https://example.com')->toUri();
```

#### [`transliterate`](#method-fluent-str-transliterate)

The `transliterate` method will attempt to convert a given string into its closest ASCII representation:

```
1use Illuminate\Support\Str;

2 

3$email = Str::of('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ')->transliterate()

4 

5// '[[email protected]](/cdn-cgi/l/email-protection)'
```

#### [`trim`](#method-fluent-str-trim)

The `trim` method trims the given string. Unlike PHP's native `trim` function, Laravel's `trim` method also removes unicode whitespace characters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('  Laravel  ')->trim();

4 

5// 'Laravel'

6 

7$string = Str::of('/Laravel/')->trim('/');

8 

9// 'Laravel'
```

#### [`ltrim`](#method-fluent-str-ltrim)

The `ltrim` method trims the left side of the string. Unlike PHP's native `ltrim` function, Laravel's `ltrim` method also removes unicode whitespace characters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('  Laravel  ')->ltrim();

4 

5// 'Laravel  '

6 

7$string = Str::of('/Laravel/')->ltrim('/');

8 

9// 'Laravel/'
```

#### [`rtrim`](#method-fluent-str-rtrim)

The `rtrim` method trims the right side of the given string. Unlike PHP's native `rtrim` function, Laravel's `rtrim` method also removes unicode whitespace characters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('  Laravel  ')->rtrim();

4 

5// '  Laravel'

6 

7$string = Str::of('/Laravel/')->rtrim('/');

8 

9// '/Laravel'
```

#### [`ucfirst`](#method-fluent-str-ucfirst)

The `ucfirst` method returns the given string with the first character capitalized:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('foo bar')->ucfirst();

4 

5// Foo bar
```

#### [`ucsplit`](#method-fluent-str-ucsplit)

The `ucsplit` method splits the given string into a collection by uppercase characters:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Foo Bar')->ucsplit();

4 

5// collect(['Foo ', 'Bar'])
```

#### [`ucwords`](#method-fluent-str-ucwords)

The `ucwords` method converts the first character of each word in the given string to uppercase:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('laravel framework')->ucwords();

4 

5// Laravel Framework
```

#### [`unwrap`](#method-fluent-str-unwrap)

The `unwrap` method removes the specified strings from the beginning and end of a given string:

```
1use Illuminate\Support\Str;

2 

3Str::of('-Laravel-')->unwrap('-');

4 

5// Laravel

6 

7Str::of('{framework: "Laravel"}')->unwrap('{', '}');

8 

9// framework: "Laravel"
```

#### [`upper`](#method-fluent-str-upper)

The `upper` method converts the given string to uppercase:

```
1use Illuminate\Support\Str;

2 

3$adjusted = Str::of('laravel')->upper();

4 

5// LARAVEL
```

#### [`when`](#method-fluent-str-when)

The `when` method invokes the given closure if a given condition is `true`. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('Taylor')

5    ->when(true, function (Stringable $string) {

6        return $string->append(' Otwell');

7    });

8 

9// 'Taylor Otwell'
```

If necessary, you may pass another closure as the third parameter to the `when` method. This closure will execute if the condition parameter evaluates to `false`.

#### [`whenContains`](#method-fluent-str-when-contains)

The `whenContains` method invokes the given closure if the string contains the given value. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('tony stark')

5    ->whenContains('tony', function (Stringable $string) {

6        return $string->title();

7    });

8 

9// 'Tony Stark'
```

If necessary, you may pass another closure as the third parameter. The closure will be invoked if the string does not contain the given value.

You may also pass an array of values to determine if the given string contains any of the values in the array:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('tony stark')

5    ->whenContains(['tony', 'hulk'], function (Stringable $string) {

6        return $string->title();

7    });

8 

9// Tony Stark
```

#### [`whenContainsAll`](#method-fluent-str-when-contains-all)

The `whenContainsAll` method invokes the given closure if the string contains all of the given sub-strings. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('tony stark')

5    ->whenContainsAll(['tony', 'stark'], function (Stringable $string) {

6        return $string->title();

7    });

8 

9// 'Tony Stark'
```

If necessary, you may pass another closure as the third parameter. The closure will be invoked if the condition parameter evaluates to `false`.

#### [`whenDoesntEndWith`](#method-fluent-str-when-doesnt-end-with)

The `whenDoesntEndWith` method invokes the given closure if the string doesn't end with the given sub-string. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('disney world')->whenDoesntEndWith('land', function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Disney World'
```

#### [`whenDoesntStartWith`](#method-fluent-str-when-doesnt-start-with)

The `whenDoesntStartWith` method invokes the given closure if the string doesn't start with the given sub-string. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('disney world')->whenDoesntStartWith('sea', function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Disney World'
```

#### [`whenEmpty`](#method-fluent-str-when-empty)

The `whenEmpty` method invokes the given closure if the string is empty. If the closure returns a value, that value will also be returned by the `whenEmpty` method. If the closure does not return a value, the fluent string instance will be returned:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('  ')->trim()->whenEmpty(function (Stringable $string) {

5    return $string->prepend('Laravel');

6});

7 

8// 'Laravel'
```

#### [`whenNotEmpty`](#method-fluent-str-when-not-empty)

The `whenNotEmpty` method invokes the given closure if the string is not empty. If the closure returns a value, that value will also be returned by the `whenNotEmpty` method. If the closure does not return a value, the fluent string instance will be returned:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('Framework')->whenNotEmpty(function (Stringable $string) {

5    return $string->prepend('Laravel ');

6});

7 

8// 'Laravel Framework'
```

#### [`whenStartsWith`](#method-fluent-str-when-starts-with)

The `whenStartsWith` method invokes the given closure if the string starts with the given sub-string. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('disney world')->whenStartsWith('disney', function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Disney World'
```

#### [`whenEndsWith`](#method-fluent-str-when-ends-with)

The `whenEndsWith` method invokes the given closure if the string ends with the given sub-string. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('disney world')->whenEndsWith('world', function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Disney World'
```

#### [`whenExactly`](#method-fluent-str-when-exactly)

The `whenExactly` method invokes the given closure if the string exactly matches the given string. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('laravel')->whenExactly('laravel', function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Laravel'
```

#### [`whenNotExactly`](#method-fluent-str-when-not-exactly)

The `whenNotExactly` method invokes the given closure if the string does not exactly match the given string. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('framework')->whenNotExactly('laravel', function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Framework'
```

#### [`whenIs`](#method-fluent-str-when-is)

The `whenIs` method invokes the given closure if the string matches a given pattern. Asterisks may be used as wildcard values. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('foo/bar')->whenIs('foo/*', function (Stringable $string) {

5    return $string->append('/baz');

6});

7 

8// 'foo/bar/baz'
```

#### [`whenIsAscii`](#method-fluent-str-when-is-ascii)

The `whenIsAscii` method invokes the given closure if the string is 7-bit ASCII. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('laravel')->whenIsAscii(function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Laravel'
```

#### [`whenIsUlid`](#method-fluent-str-when-is-ulid)

The `whenIsUlid` method invokes the given closure if the string is a valid ULID. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function (Stringable $string) {

4    return $string->substr(0, 8);

5});

6 

7// '01gd6r36'
```

#### [`whenIsUuid`](#method-fluent-str-when-is-uuid)

The `whenIsUuid` method invokes the given closure if the string is a valid UUID. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function (Stringable $string) {

5    return $string->substr(0, 8);

6});

7 

8// 'a0a2a2d2'
```

#### [`whenTest`](#method-fluent-str-when-test)

The `whenTest` method invokes the given closure if the string matches the given regular expression. The closure will receive the fluent string instance:

```
1use Illuminate\Support\Str;

2use Illuminate\Support\Stringable;

3 

4$string = Str::of('laravel framework')->whenTest('/laravel/', function (Stringable $string) {

5    return $string->title();

6});

7 

8// 'Laravel Framework'
```

#### [`wordCount`](#method-fluent-str-word-count)

The `wordCount` method returns the number of words that a string contains:

```
1use Illuminate\Support\Str;

2 

3Str::of('Hello, world!')->wordCount(); // 2
```

#### [`words`](#method-fluent-str-words)

The `words` method limits the number of words in a string. If necessary, you may specify an additional string that will be appended to the truncated string:

```
1use Illuminate\Support\Str;

2 

3$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

4 

5// Perfectly balanced, as >>>
```

#### [`wrap`](#method-fluent-str-wrap)

The `wrap` method wraps the given string with an additional string or pair of strings:

```
1use Illuminate\Support\Str;

2 

3Str::of('Laravel')->wrap('"');

4 

5// "Laravel"

6 

7Str::is('is')->wrap(before: 'This ', after: ' Laravel!');

8 

9// This is Laravel!
```
