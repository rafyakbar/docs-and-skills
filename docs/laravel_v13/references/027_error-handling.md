# Error Handling

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Handling Exceptions](#handling-exceptions)
  * [Reporting Exceptions](#reporting-exceptions)
  * [Exception Log Levels](#exception-log-levels)
  * [Ignoring Exceptions by Type](#ignoring-exceptions-by-type)
  * [Rendering Exceptions](#rendering-exceptions)
  * [Reportable and Renderable Exceptions](#renderable-exceptions)
- [Throttling Reported Exceptions](#throttling-reported-exceptions)
- [HTTP Exceptions](#http-exceptions)
  * [Custom HTTP Error Pages](#custom-http-error-pages)

## [Introduction](#introduction)

When you start a new Laravel project, error and exception handling is already configured for you; however, at any point, you may use the `withExceptions` method in your application's `bootstrap/app.php` to manage how exceptions are reported and rendered by your application.

The `$exceptions` object provided to the `withExceptions` closure is an instance of `Illuminate\Foundation\Configuration\Exceptions` and is responsible for managing exception handling in your application. We'll dive deeper into this object throughout this documentation.

## [Configuration](#configuration)

The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file.

During local development, you should set the `APP_DEBUG` environment variable to `true`.

In your production environment, the value of `APP_DEBUG` should always be `false`. If the value is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.

## [Handling Exceptions](#handling-exceptions)

### [Reporting Exceptions](#reporting-exceptions)

In Laravel, exception reporting is used to log exceptions or send them to an external service like [Laravel Nightwatch](https://nightwatch.laravel.com), [Sentry](https://github.com/getsentry/sentry-laravel), or [Flare](https://flareapp.io). By default, exceptions will be logged based on your [logging](/docs/13.x/logging) configuration. However, you are free to log exceptions however you wish.

If you need to report different types of exceptions in different ways, you may use the `report` exception method in your application's `bootstrap/app.php` to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will determine what type of exception the closure reports by examining the type-hint of the closure:

```
1use App\Exceptions\InvalidOrderException;

2 

3->withExceptions(function (Exceptions $exceptions): void {

4    $exceptions->report(function (InvalidOrderException $e) {

5        // ...

6    });

7})
```

When you register a custom exception reporting callback using the `report` method, Laravel will still log the exception using the default logging configuration for the application. If you wish to stop the propagation of the exception to the default logging stack, you may use the `stop` method when defining your reporting callback or return `false` from the callback:

```
 1use App\Exceptions\InvalidOrderException;

 2 

 3->withExceptions(function (Exceptions $exceptions): void {

 4    $exceptions->report(function (InvalidOrderException $e) {

 5        // ...

 6    })->stop();

 7 

 8    $exceptions->report(function (InvalidOrderException $e) {

 9        return false;

10    });

11})
```

To customize the exception reporting for a given exception, you may also utilize [reportable exceptions](/docs/13.x/errors#renderable-exceptions).

#### [Global Log Context](#global-log-context)

If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data using the `context` exception method in your application's `bootstrap/app.php` file. This information will be included in every exception's log message written by your application:

```
1->withExceptions(function (Exceptions $exceptions): void {

2    $exceptions->context(fn () => [

3        'foo' => 'bar',

4    ]);

5})
```

#### [Exception Log Context](#exception-log-context)

While adding context to every log message can be useful, sometimes a particular exception may have unique context that you would like to include in your logs. By defining a `context` method on one of your application's exceptions, you may specify any data relevant to that exception that should be added to the exception's log entry:

```
 1<?php

 2 

 3namespace App\Exceptions;

 4 

 5use Exception;

 6 

 7class InvalidOrderException extends Exception

 8{

 9    // ...

10 

11    /**

12     * Get the exception's context information.

13     *

14     * @return array<string, mixed>

15     */

16    public function context(): array

17    {

18        return ['order_id' => $this->orderId];

19    }

20}
```

#### [The `report` Helper](#the-report-helper)

Sometimes you may need to report an exception but continue handling the current request. The `report` helper function allows you to quickly report an exception without rendering an error page to the user:

```
 1public function isValid(string $value): bool

 2{

 3    try {

 4        // Validate the value...

 5    } catch (Throwable $e) {

 6        report($e);

 7 

 8        return false;

 9    }

10}
```

#### [Deduplicating Reported Exceptions](#deduplicating-reported-exceptions)

If you are using the `report` function throughout your application, you may occasionally report the same exception multiple times, creating duplicate entries in your logs.

If you would like to ensure that a single instance of an exception is only ever reported once, you may invoke the `dontReportDuplicates` exception method in your application's `bootstrap/app.php` file:

```
1->withExceptions(function (Exceptions $exceptions): void {

2    $exceptions->dontReportDuplicates();

3})
```

Now, when the `report` helper is called with the same instance of an exception, only the first call will be reported:

```
 1$original = new RuntimeException('Whoops!');

 2 

 3report($original); // reported

 4 

 5try {

 6    throw $original;

 7} catch (Throwable $caught) {

 8    report($caught); // ignored

 9}

10 

11report($original); // ignored

12report($caught); // ignored
```

### [Exception Log Levels](#exception-log-levels)

When messages are written to your application's [logs](/docs/13.x/logging), the messages are written at a specified [log level](/docs/13.x/logging#log-levels), which indicates the severity or importance of the message being logged.

As noted above, even when you register a custom exception reporting callback using the `report` method, Laravel will still log the exception using the default logging configuration for the application; however, since the log level can sometimes influence the channels on which a message is logged, you may wish to configure the log level that certain exceptions are logged at.

To accomplish this, you may use the `level` exception method in your application's `bootstrap/app.php` file. This method receives the exception type as its first argument and the log level as its second argument:

```
1use PDOException;

2use Psr\Log\LogLevel;

3 

4->withExceptions(function (Exceptions $exceptions): void {

5    $exceptions->level(PDOException::class, LogLevel::CRITICAL);

6})
```

### [Ignoring Exceptions by Type](#ignoring-exceptions-by-type)

When building your application, there will be some types of exceptions you never want to report. To ignore these exceptions, you may use the `dontReport` exception method in your application's `bootstrap/app.php` file. Any class provided to this method will never be reported; however, they may still have custom rendering logic:

```
1use App\Exceptions\InvalidOrderException;

2 

3->withExceptions(function (Exceptions $exceptions): void {

4    $exceptions->dontReport([

5        InvalidOrderException::class,

6    ]);

7})
```

Alternatively, you may simply "mark" an exception class with the `Illuminate\Contracts\Debug\ShouldntReport` interface. When an exception is marked with this interface, it will never be reported by Laravel's exception handler:

```
 1<?php

 2 

 3namespace App\Exceptions;

 4 

 5use Exception;

 6use Illuminate\Contracts\Debug\ShouldntReport;

 7 

 8class PodcastProcessingException extends Exception implements ShouldntReport

 9{

10    //

11}
```

If you need even more control over when a particular type of exception is ignored, you may provide a closure to the `dontReportWhen` method:

```
1use App\Exceptions\InvalidOrderException;

2use Throwable;

3 

4->withExceptions(function (Exceptions $exceptions): void {

5    $exceptions->dontReportWhen(function (Throwable $e) {

6        return $e instanceof PodcastProcessingException &&

7               $e->reason() === 'Subscription expired';

8    });

9})
```

Internally, Laravel already ignores some types of errors for you, such as exceptions resulting from 404 HTTP errors, 403 HTTP responses generated by origin mismatches, or 419 HTTP responses generated by invalid CSRF tokens. If you would like to instruct Laravel to stop ignoring a given type of exception, you may use the `stopIgnoring` exception method in your application's `bootstrap/app.php` file:

```
1use Symfony\Component\HttpKernel\Exception\HttpException;

2 

3->withExceptions(function (Exceptions $exceptions): void {

4    $exceptions->stopIgnoring(HttpException::class);

5})
```

### [Rendering Exceptions](#rendering-exceptions)

By default, the Laravel exception handler will convert exceptions into an HTTP response for you. However, you are free to register a custom rendering closure for exceptions of a given type. You may accomplish this by using the `render` exception method in your application's `bootstrap/app.php` file.

The closure passed to the `render` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will determine what type of exception the closure renders by examining the type-hint of the closure:

```
1use App\Exceptions\InvalidOrderException;

2use Illuminate\Http\Request;

3 

4->withExceptions(function (Exceptions $exceptions): void {

5    $exceptions->render(function (InvalidOrderException $e, Request $request) {

6        return response()->view('errors.invalid-order', status: 500);

7    });

8})
```

You may also use the `render` method to override the rendering behavior for built-in Laravel or Symfony exceptions such as `NotFoundHttpException`. If the closure given to the `render` method does not return a value, Laravel's default exception rendering will be utilized:

```
 1use Illuminate\Http\Request;

 2use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

 3 

 4->withExceptions(function (Exceptions $exceptions): void {

 5    $exceptions->render(function (NotFoundHttpException $e, Request $request) {

 6        if ($request->is('api/*')) {

 7            return response()->json([

 8                'message' => 'Record not found.'

 9            ], 404);

10        }

11    });

12})
```

#### [Rendering Exceptions as JSON](#rendering-exceptions-as-json)

When rendering an exception, Laravel will automatically determine if the exception should be rendered as an HTML or JSON response based on the `Accept` header of the request. If you would like to customize how Laravel determines whether to render HTML or JSON exception responses, you may utilize the `shouldRenderJsonWhen` method:

```
 1use Illuminate\Http\Request;

 2use Throwable;

 3 

 4->withExceptions(function (Exceptions $exceptions): void {

 5    $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {

 6        if ($request->is('admin/*')) {

 7            return true;

 8        }

 9 

10        return $request->expectsJson();

11    });

12})
```

#### [Customizing the Exception Response](#customizing-the-exception-response)

Rarely, you may need to customize the entire HTTP response rendered by Laravel's exception handler. To accomplish this, you may register a response customization closure using the `respond` method:

```
 1use Symfony\Component\HttpFoundation\Response;

 2 

 3->withExceptions(function (Exceptions $exceptions): void {

 4    $exceptions->respond(function (Response $response) {

 5        if ($response->getStatusCode() === 419) {

 6            return back()->with([

 7                'message' => 'The page expired, please try again.',

 8            ]);

 9        }

10 

11        return $response;

12    });

13})
```

### [Reportable and Renderable Exceptions](#renderable-exceptions)

Instead of defining custom reporting and rendering behavior in your application's `bootstrap/app.php` file, you may define `report` and `render` methods directly on your application's exceptions. When these methods exist, they will automatically be called by the framework:

```
 1<?php

 2 

 3namespace App\Exceptions;

 4 

 5use Exception;

 6use Illuminate\Http\Request;

 7use Illuminate\Http\Response;

 8 

 9class InvalidOrderException extends Exception

10{

11    /**

12     * Report the exception.

13     */

14    public function report(): void

15    {

16        // ...

17    }

18 

19    /**

20     * Render the exception as an HTTP response.

21     */

22    public function render(Request $request): Response

23    {

24        return response(/* ... */);

25    }

26}
```

If your exception extends an exception that is already renderable, such as a built-in Laravel or Symfony exception, you may return `false` from the exception's `render` method to render the exception's default HTTP response:

```
 1/**

 2 * Render the exception as an HTTP response.

 3 */

 4public function render(Request $request): Response|bool

 5{

 6    if (/** Determine if the exception needs custom rendering */) {

 7 

 8        return response(/* ... */);

 9    }

10 

11    return false;

12}
```

If your exception contains custom reporting logic that is only necessary when certain conditions are met, you may need to instruct Laravel to sometimes report the exception using the default exception handling configuration. To accomplish this, you may return `false` from the exception's `report` method:

```
 1/**

 2 * Report the exception.

 3 */

 4public function report(): bool

 5{

 6    if (/** Determine if the exception needs custom reporting */) {

 7 

 8        // ...

 9 

10        return true;

11    }

12 

13    return false;

14}
```

You may type-hint any required dependencies of the `report` method and they will automatically be injected into the method by Laravel's [service container](/docs/13.x/container).

### [Throttling Reported Exceptions](#throttling-reported-exceptions)

If your application reports a very large number of exceptions, you may want to throttle how many exceptions are actually logged or sent to your application's external error tracking service.

To take a random sample rate of exceptions, you may use the `throttle` exception method in your application's `bootstrap/app.php` file. The `throttle` method receives a closure that should return a `Lottery` instance:

```
1use Illuminate\Support\Lottery;

2use Throwable;

3 

4->withExceptions(function (Exceptions $exceptions): void {

5    $exceptions->throttle(function (Throwable $e) {

6        return Lottery::odds(1, 1000);

7    });

8})
```

It is also possible to conditionally sample based on the exception type. If you would like to only sample instances of a specific exception class, you may return a `Lottery` instance only for that class:

```
 1use App\Exceptions\ApiMonitoringException;

 2use Illuminate\Support\Lottery;

 3use Throwable;

 4 

 5->withExceptions(function (Exceptions $exceptions): void {

 6    $exceptions->throttle(function (Throwable $e) {

 7        if ($e instanceof ApiMonitoringException) {

 8            return Lottery::odds(1, 1000);

 9        }

10    });

11})
```

You may also rate limit exceptions logged or sent to an external error tracking service by returning a `Limit` instance instead of a `Lottery`. This is useful if you want to protect against sudden bursts of exceptions flooding your logs, for example, when a third-party service used by your application is down:

```
 1use Illuminate\Broadcasting\BroadcastException;

 2use Illuminate\Cache\RateLimiting\Limit;

 3use Throwable;

 4 

 5->withExceptions(function (Exceptions $exceptions): void {

 6    $exceptions->throttle(function (Throwable $e) {

 7        if ($e instanceof BroadcastException) {

 8            return Limit::perMinute(300);

 9        }

10    });

11})
```

By default, limits will use the exception's class as the rate limit key. You can customize this by specifying your own key using the `by` method on the `Limit`:

```
 1use Illuminate\Broadcasting\BroadcastException;

 2use Illuminate\Cache\RateLimiting\Limit;

 3use Throwable;

 4 

 5->withExceptions(function (Exceptions $exceptions): void {

 6    $exceptions->throttle(function (Throwable $e) {

 7        if ($e instanceof BroadcastException) {

 8            return Limit::perMinute(300)->by($e->getMessage());

 9        }

10    });

11})
```

Of course, you may return a mixture of `Lottery` and `Limit` instances for different exceptions:

```
 1use App\Exceptions\ApiMonitoringException;

 2use Illuminate\Broadcasting\BroadcastException;

 3use Illuminate\Cache\RateLimiting\Limit;

 4use Illuminate\Support\Lottery;

 5use Throwable;

 6 

 7->withExceptions(function (Exceptions $exceptions): void {

 8    $exceptions->throttle(function (Throwable $e) {

 9        return match (true) {

10            $e instanceof BroadcastException => Limit::perMinute(300),

11            $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),

12            default => Limit::none(),

13        };

14    });

15})
```

## [HTTP Exceptions](#http-exceptions)

Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401), or even a developer generated 500 error. In order to generate such a response from anywhere in your application, you may use the `abort` helper:

```
1abort(404);
```

### [Custom HTTP Error Pages](#custom-http-error-pages)

Laravel makes it easy to display custom error pages for various HTTP status codes. For example, to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered for all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable:

```
1<h2>{{ $exception->getMessage() }}</h2>
```

You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking:

```
1php artisan vendor:publish --tag=laravel-errors
```

#### [Fallback HTTP Error Pages](#fallback-http-error-pages)

You may also define a "fallback" error page for a given series of HTTP status codes. This page will be rendered if there is not a corresponding page for the specific HTTP status code that occurred. To accomplish this, define a `4xx.blade.php` template and a `5xx.blade.php` template in your application's `resources/views/errors` directory.

When defining fallback error pages, the fallback pages will not affect `404`, `500`, and `503` error responses since Laravel has internal, dedicated pages for these status codes. To customize the pages rendered for these status codes, you should define a custom error page for each of them individually.
