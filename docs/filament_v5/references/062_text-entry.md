[Infolists](/docs/5.x/infolists/overview)

# Text entry

## [​](#introduction)Introduction

Text entries display simple text:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('title')
```

## [​](#customizing-the-color)Customizing the color

You may set a [color](../styling/colors) for the text:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('status')
    ->color('primary')
```

## [​](#adding-an-icon)Adding an icon

Text entries may also have an [icon](../styling/icons):

```
use Filament\Infolists\Components\TextEntry;
use Filament\Support\Icons\Heroicon;

TextEntry::make('email')
    ->icon(Heroicon::Envelope)
```

You may set the position of an icon using `iconPosition()`:

```
use Filament\Infolists\Components\TextEntry;
use Filament\Support\Enums\IconPosition;
use Filament\Support\Icons\Heroicon;

TextEntry::make('email')
    ->icon(Heroicon::Envelope)
    ->iconPosition(IconPosition::After) // `IconPosition::Before` or `IconPosition::After`
```

The icon color defaults to the text color, but you may customize the icon [color](../styling/colors) separately using `iconColor()`:

```
use Filament\Infolists\Components\TextEntry;
use Filament\Support\Icons\Heroicon;

TextEntry::make('email')
    ->icon(Heroicon::Envelope)
    ->iconColor('primary')
```

## [​](#displaying-as-a-“badge”)Displaying as a “badge”

By default, text is quite plain and has no background color. You can make it appear as a “badge” instead using the `badge()` method. A great use case for this is with statuses, where may want to display a badge with a [color](#customizing-the-color) that matches the status:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('status')
    ->badge()
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'gray',
        'reviewing' => 'warning',
        'published' => 'success',
        'rejected' => 'danger',
    })
```

You may add other things to the badge, like an [icon](#adding-an-icon). Optionally, you may pass a boolean value to control if the text should be in a badge or not:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('status')
    ->badge(FeatureFlag::active())
```

## [​](#formatting)Formatting

When using a text entry, you may want the actual outputted text in the UI to differ from the raw [state](./overview#entry-content-state) of the entry, which is often automatically retrieved from an Eloquent model. Formatting the state allows you to preserve the integrity of the raw data while also allowing it to be presented in a more user-friendly way. To format the state of a text entry without changing the state itself, you can use the `formatStateUsing()` method. This method accepts a function that takes the state as an argument and returns the formatted state:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('status')
    ->formatStateUsing(fn (string $state): string => __("statuses.{$state}"))
```

In this case, the `status` column in the database might contain values like `draft`, `reviewing`, `published`, or `rejected`, but the formatted state will be the translated version of these values.

### [​](#date-formatting)Date formatting

Instead of passing a function to `formatStateUsing()`, you may use the `date()`, `dateTime()`, and `time()` methods to format the entry’s state using [PHP date formatting tokens](https://www.php.net/manual/en/datetime.format.php):

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->date()

TextEntry::make('created_at')
    ->dateTime()

TextEntry::make('created_at')
    ->time()
```

You may customize the date format by passing a custom format string to the `date()`, `dateTime()`, or `time()` method. You may use any [PHP date formatting tokens](https://www.php.net/manual/en/datetime.format.php):

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->date('M j, Y')
  
TextEntry::make('created_at')
    ->dateTime('M j, Y H:i:s')
  
TextEntry::make('created_at')
    ->time('H:i:s')
```

#### [​](#date-formatting-using-carbon-macro-formats)Date formatting using Carbon macro formats

You may use also the `isoDate()`, `isoDateTime()`, and `isoTime()` methods to format the entry’s state using [Carbon’s macro-formats](https://carbon.nesbot.com/docs/#available-macro-formats):

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->isoDate()

TextEntry::make('created_at')
    ->isoDateTime()

TextEntry::make('created_at')
    ->isoTime()
```

You may customize the date format by passing a custom macro format string to the `isoDate()`, `isoDateTime()`, or `isoTime()` method. You may use any [Carbon’s macro-formats](https://carbon.nesbot.com/docs/#available-macro-formats):

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->isoDate('L')

TextEntry::make('created_at')
    ->isoDateTime('LLL')

TextEntry::make('created_at')
    ->isoTime('LT')
```

#### [​](#relative-date-formatting)Relative date formatting

You may use the `since()` method to format the entry’s state using [Carbon’s `diffForHumans()`](https://carbon.nesbot.com/docs/#api-humandiff):

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->since()
```

#### [​](#displaying-a-formatting-date-in-a-tooltip)Displaying a formatting date in a tooltip

Additionally, you can use the `dateTooltip()`, `dateTimeTooltip()`, `timeTooltip()`, `isoDateTooltip()`, `isoDateTimeTooltip()`, `isoTime()`, `isoTimeTooltip()`, or `sinceTooltip()` method to display a formatted date in a [tooltip](./overview#adding-a-tooltip-to-an-entry), often to provide extra information:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->since()
    ->dateTooltip() // Accepts a custom PHP date formatting string

TextEntry::make('created_at')
    ->since()
    ->dateTimeTooltip() // Accepts a custom PHP date formatting string

TextEntry::make('created_at')
    ->since()
    ->timeTooltip() // Accepts a custom PHP date formatting string

TextEntry::make('created_at')
    ->since()
    ->isoDateTooltip() // Accepts a custom Carbon macro format string

TextEntry::make('created_at')
    ->since()
    ->isoDateTimeTooltip() // Accepts a custom Carbon macro format string

TextEntry::make('created_at')
    ->since()
    ->isoTimeTooltip() // Accepts a custom Carbon macro format string

TextEntry::make('created_at')
    ->dateTime()
    ->sinceTooltip()
```

#### [​](#setting-the-timezone-for-date-formatting)Setting the timezone for date formatting

Each of the date formatting methods listed above also accepts a `timezone` argument, which allows you to convert the time set in the state to a different timezone:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->dateTime(timezone: 'America/New_York')
```

You can also pass a timezone to the `timezone()` method of the entry to apply a timezone to all date-time formatting methods at once:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('created_at')
    ->timezone('America/New_York')
    ->dateTime()
```

If you do not pass a `timezone()` to the entry, it will use Filament’s default timezone. You can set Filament’s default timezone using the `FilamentTimezone::set()` method in the `boot()` method of a service provider such as `AppServiceProvider`:

```
use Filament\Support\Facades\FilamentTimezone;

public function boot(): void
{
    FilamentTimezone::set('America/New_York');
}
```

This is useful if you want to set a default timezone for all text entries in your application. It is also used in other places where timezones are used in Filament.

Filament’s default timezone will only apply when the entry stores a time. If the entry stores a date only (`date()` instead of `dateTime()`), the timezone will not be applied. This is to prevent timezone shifts when storing dates without times.

### [​](#number-formatting)Number formatting

Instead of passing a function to `formatStateUsing()`, you can use the `numeric()` method to format an entry as a number:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('stock')
    ->numeric()
```

If you would like to customize the number of decimal places used to format the number with, you can use the `decimalPlaces` argument:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('stock')
    ->numeric(decimalPlaces: 0)
```

By default, your app’s locale will be used to format the number suitably. If you would like to customize the locale used, you can pass it to the `locale` argument:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('stock')
    ->numeric(locale: 'nl')
```

### [​](#money-formatting)Money formatting

Instead of passing a function to `formatStateUsing()`, you can use the `money()` method to easily format amounts of money, in any currency:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('price')
    ->money('EUR')
```

There is also a `divideBy` argument for `money()` that allows you to divide the original value by a number before formatting it. This could be useful if your database stores the price in cents, for example:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('price')
    ->money('EUR', divideBy: 100)
```

By default, your app’s locale will be used to format the money suitably. If you would like to customize the locale used, you can pass it to the `locale` argument:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('price')
    ->money('EUR', locale: 'nl')
```

If you would like to customize the number of decimal places used to format the number with, you can use the `decimalPlaces` argument:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('price')
    ->money('EUR', decimalPlaces: 3)
```

### [​](#rendering-markdown)Rendering Markdown

If your entry value is Markdown, you may render it using `markdown()`:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->markdown()
```

Optionally, you may pass a boolean value to control if the text should be rendered as Markdown or not:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->markdown(FeatureFlag::active())
```

### [​](#rendering-html)Rendering HTML

If your entry value is HTML, you may render it using `html()`:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->html()
```

Optionally, you may pass a boolean value to control if the text should be rendered as HTML or not:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->html(FeatureFlag::active())
```

Filament’s built-in HTML sanitizer permits inline `style` attributes in order to support rich text formatting features such as font colors, text highlighting, and image sizing. This means that CSS properties like `background: url(...)` or `position: fixed` will not be stripped from sanitized HTML. If your content comes from untrusted users, you should consider restricting the default configuration. See the [security documentation](../advanced/security#customizing-the-sanitizer) for details on how to customize the sanitizer.

#### [​](#rendering-raw-html-without-sanitization)Rendering raw HTML without sanitization

If you use this method, then the HTML will be sanitized to remove any potentially unsafe content before it is rendered. If you’d like to opt out of this behavior, you can wrap the HTML in an `HtmlString` object by formatting it:

```
use Filament\Infolists\Components\TextEntry;
use Illuminate\Support\HtmlString;

TextEntry::make('description')
    ->formatStateUsing(fn (string $state): HtmlString => new HtmlString($state))
```

Be cautious when rendering raw HTML, as it may contain malicious content, which can lead to security vulnerabilities in your app such as cross-site scripting (XSS) attacks. Always ensure that the HTML you are rendering is safe before using this method.

Alternatively, you can return a `view()` object from the `formatStateUsing()` method, which will also not be sanitized:

```
use Filament\Infolists\Components\TextEntry;
use Illuminate\Contracts\View\View;

TextEntry::make('description')
    ->formatStateUsing(fn (string $state): View => view(
        'filament.infolists.components.description-entry-content',
        ['state' => $state],
    ))
```

## [​](#listing-multiple-values)Listing multiple values

Multiple values can be rendered in a text entry if its [state](./overview#entry-content-state) is an array. This can happen if you are using an `array` cast on an Eloquent attribute, an Eloquent relationship with multiple results, or if you have passed an array to the [`state()` method](./overview#setting-the-state-of-an-entry). If there are multiple values inside your text entry, they will be comma-separated. You may use the `listWithLineBreaks()` method to display them on new lines instead:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('authors.name')
    ->listWithLineBreaks()
```

Optionally, you may pass a boolean value to control if the text should have line breaks between each item or not:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('authors.name')
    ->listWithLineBreaks(FeatureFlag::active())
```

### [​](#adding-bullet-points-to-the-list)Adding bullet points to the list

You may add a bullet point to each list item using the `bulleted()` method:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('authors.name')
    ->bulleted()
```

Optionally, you may pass a boolean value to control if the text should have bullet points or not:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('authors.name')
    ->bulleted(FeatureFlag::active())
```

### [​](#limiting-the-number-of-values-in-the-list)Limiting the number of values in the list

You can limit the number of values in the list using the `limitList()` method:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('authors.name')
    ->listWithLineBreaks()
    ->limitList(3)
```

#### [​](#expanding-the-limited-list)Expanding the limited list

You can allow the limited items to be expanded and collapsed, using the `expandableLimitedList()` method:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('authors.name')
    ->listWithLineBreaks()
    ->limitList(3)
    ->expandableLimitedList()
```

This is only a feature for `listWithLineBreaks()` or `bulleted()`, where each item is on its own line.

Optionally, you may pass a boolean value to control if the text should be expandable or not:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('authors.name')
    ->listWithLineBreaks()
    ->limitList(3)
    ->expandableLimitedList(FeatureFlag::active())
```

### [​](#splitting-a-single-value-into-multiple-list-items)Splitting a single value into multiple list items

If you want to “explode” a text string from your model into multiple list items, you can do so with the `separator()` method. This is useful for displaying comma-separated tags [as badges](#displaying-as-a-badge), for example:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('tags')
    ->badge()
    ->separator(',')
```

## [​](#aggregating-relationships)Aggregating relationships

Filament provides several methods for aggregating a relationship field, including `avg()`, `max()`, `min()` and `sum()`. For instance, if you wish to show the average of a field on all related records, you may use the `avg()` method:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('users_avg_age')->avg('users', 'age')
```

In this example, `users` is the name of the relationship, while `age` is the field that is being averaged. The name of the entry must be `users_avg_age`, as this is the convention that [Laravel uses](https://laravel.com/docs/eloquent-relationships#other-aggregate-functions) for storing the result. If you’d like to scope the relationship before aggregating, you can pass an array to the method, where the key is the relationship name and the value is the function to scope the Eloquent query with:

```
use Filament\Infolists\Components\TextEntry;
use Illuminate\Database\Eloquent\Builder;

TextEntry::make('users_avg_age')->avg([
    'users' => fn (Builder $query) => $query->where('is_active', true),
], 'age')
```

## [​](#customizing-the-text-size)Customizing the text size

Text entries have small font size by default, but you may change this to `TextSize::ExtraSmall`, `TextSize::Medium`, or `TextSize::Large`. For instance, you may make the text larger using `size(TextSize::Large)`:

```
use Filament\Infolists\Components\TextEntry;
use Filament\Support\Enums\TextSize;

TextEntry::make('title')
    ->size(TextSize::Large)
```

## [​](#customizing-the-font-weight)Customizing the font weight

Text entries have regular font weight by default, but you may change this to any of the following options: `FontWeight::Thin`, `FontWeight::ExtraLight`, `FontWeight::Light`, `FontWeight::Medium`, `FontWeight::SemiBold`, `FontWeight::Bold`, `FontWeight::ExtraBold` or `FontWeight::Black`. For instance, you may make the font bold using `weight(FontWeight::Bold)`:

```
use Filament\Infolists\Components\TextEntry;
use Filament\Support\Enums\FontWeight;

TextEntry::make('title')
    ->weight(FontWeight::Bold)
```

## [​](#customizing-the-font-family)Customizing the font family

You can change the text font family to any of the following options: `FontFamily::Sans`, `FontFamily::Serif` or `FontFamily::Mono`. For instance, you may make the font monospaced using `fontFamily(FontFamily::Mono)`:

```
use Filament\Support\Enums\FontFamily;
use Filament\Infolists\Components\TextEntry;

TextEntry::make('apiKey')
    ->label('API key')
    ->fontFamily(FontFamily::Mono)
```

## [​](#handling-long-text)Handling long text

### [​](#limiting-text-length)Limiting text length

You may `limit()` the length of the entry’s value:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->limit(50)
```

By default, when text is truncated, an ellipsis (`...`) is appended to the end of the text. You may customize this by passing a custom string to the `end` argument:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->limit(50, end: ' (more)')
```

You may also reuse the value that is being passed to `limit()` in a function, by getting it using the `getCharacterLimit()` method:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->limit(50)
    ->tooltip(function (TextEntry $component): ?string {
        $state = $component->getState();

        if (strlen($state) <= $component->getCharacterLimit()) {
            return null;
        }

        // Only render the tooltip if the entry contents exceeds the length limit.
        return $state;
    })
```

### [​](#limiting-word-count)Limiting word count

You may limit the number of `words()` displayed in the entry:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->words(10)
```

By default, when text is truncated, an ellipsis (`...`) is appended to the end of the text. You may customize this by passing a custom string to the `end` argument:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->words(10, end: ' (more)')
```

### [​](#limiting-text-to-a-specific-number-of-lines)Limiting text to a specific number of lines

You may want to limit text to a specific number of lines instead of limiting it to a fixed length. Clamping text to a number of lines is useful in responsive interfaces where you want to ensure a consistent experience across all screen sizes. This can be achieved using the `lineClamp()` method:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->lineClamp(2)
```

### [​](#preventing-text-wrapping)Preventing text wrapping

By default, text will wrap to the next line if it exceeds the width of the container. You can prevent this behavior using the `wrap(false)` method:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('description')
    ->wrap(false)
```

## [​](#allowing-the-text-to-be-copied-to-the-clipboard)Allowing the text to be copied to the clipboard

You may make the text copyable, such that clicking on the entry copies the text to the clipboard, and optionally specify a custom confirmation message and duration in milliseconds:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('apiKey')
    ->label('API key')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
```

Optionally, you may pass a boolean value to control if the text should be copyable or not:

```
use Filament\Infolists\Components\TextEntry;

TextEntry::make('apiKey')
    ->label('API key')
    ->copyable(FeatureFlag::active())
```

This feature only works when SSL is enabled for the app.

## [​](#adding-suffix-and-prefix-actions)Adding suffix and prefix actions

You may place an [action](../actions) before and after the entry using the `prefixAction()` and `suffixAction()` methods:

```
use Filament\Actions\Action;
use Filament\Infolists\Components\TextEntry;
use Filament\Support\Icons\Heroicon;

TextEntry::make('cost')
    ->prefix('€')
    ->suffixAction(
        Action::make('copyCostToPrice')
            ->icon(Heroicon::Clipboard),
    )
```

[Overview](/docs/5.x/infolists/overview)[Icon entry](/docs/5.x/infolists/icon-entry)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
