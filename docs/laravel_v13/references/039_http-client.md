# HTTP Client

- [Introduction](#introduction)
- [Making Requests](#making-requests)
  * [Request Data](#request-data)
  * [Headers](#headers)
  * [Authentication](#authentication)
  * [Timeout](#timeout)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Guzzle Middleware](#guzzle-middleware)
  * [Guzzle Options](#guzzle-options)
- [Concurrent Requests](#concurrent-requests)
  * [Request Pooling](#request-pooling)
  * [Request Batching](#request-batching)
- [Macros](#macros)
- [Testing](#testing)
  * [Faking Responses](#faking-responses)
  * [Inspecting Requests](#inspecting-requests)
  * [Preventing Stray Requests](#preventing-stray-requests)
- [Events](#events)

## [Introduction](#introduction)

Laravel provides an expressive, minimal API around the [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/), allowing you to quickly make outgoing HTTP requests to communicate with other web applications. Laravel's wrapper around Guzzle is focused on its most common use cases and a wonderful developer experience.

## [Making Requests](#making-requests)

To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL:

```
1use Illuminate\Support\Facades\Http;

2 

3$response = Http::get('http://example.com');
```

The `get` method returns an instance of `Illuminate\Http\Client\Response`, which provides a variety of methods that may be used to inspect the response:

```
 1$response->body() : string;

 2$response->json($key = null, $default = null) : mixed;

 3$response->object() : object;

 4$response->collect($key = null) : Illuminate\Support\Collection;

 5$response->resource() : resource;

 6$response->status() : int;

 7$response->successful() : bool;

 8$response->redirect(): bool;

 9$response->failed() : bool;

10$response->clientError() : bool;

11$response->header($header) : string;

12$response->headers() : array;
```

The `Illuminate\Http\Client\Response` object also implements the PHP `ArrayAccess` interface, allowing you to access JSON response data directly on the response:

```
1return Http::get('http://example.com/users/1')['name'];
```

In addition to the response methods listed above, the following methods may be used to determine if the response has a specific status code:

```
 1$response->ok() : bool;                  // 200 OK

 2$response->created() : bool;             // 201 Created

 3$response->accepted() : bool;            // 202 Accepted

 4$response->noContent() : bool;           // 204 No Content

 5$response->movedPermanently() : bool;    // 301 Moved Permanently

 6$response->found() : bool;               // 302 Found

 7$response->badRequest() : bool;          // 400 Bad Request

 8$response->unauthorized() : bool;        // 401 Unauthorized

 9$response->paymentRequired() : bool;     // 402 Payment Required

10$response->forbidden() : bool;           // 403 Forbidden

11$response->notFound() : bool;            // 404 Not Found

12$response->requestTimeout() : bool;      // 408 Request Timeout

13$response->conflict() : bool;            // 409 Conflict

14$response->unprocessableEntity() : bool; // 422 Unprocessable Entity

15$response->tooManyRequests() : bool;     // 429 Too Many Requests

16$response->serverError() : bool;         // 500 Internal Server Error
```

#### [URI Templates](#uri-templates)

The HTTP client also allows you to construct request URLs using the [URI template specification](https://www.rfc-editor.org/rfc/rfc6570). To define the URL parameters that can be expanded by your URI template, you may use the `withUrlParameters` method:

```
1Http::withUrlParameters([

2    'endpoint' => 'https://laravel.com',

3    'page' => 'docs',

4    'version' => '13.x',

5    'topic' => 'validation',

6])->get('{+endpoint}/{page}/{version}/{topic}');
```

#### [Dumping Requests](#dumping-requests)

If you would like to dump the outgoing request instance before it is sent and terminate the script's execution, you may add the `dd` method to the beginning of your request definition:

```
1return Http::dd()->get('http://example.com');
```

### [Request Data](#request-data)

Of course, it is common when making `POST`, `PUT`, and `PATCH` requests to send additional data with your request, so these methods accept an array of data as their second argument. By default, data will be sent using the `application/json` content type:

```
1use Illuminate\Support\Facades\Http;

2 

3$response = Http::post('http://example.com/users', [

4    'name' => 'Steve',

5    'role' => 'Network Administrator',

6]);
```

#### [GET Request Query Parameters](#get-request-query-parameters)

When making `GET` requests, you may either append a query string to the URL directly or pass an array of key / value pairs as the second argument to the `get` method:

```
1$response = Http::get('http://example.com/users', [

2    'name' => 'Taylor',

3    'page' => 1,

4]);
```

Alternatively, the `withQueryParameters` method may be used:

```
1Http::retry(3, 100)->withQueryParameters([

2    'name' => 'Taylor',

3    'page' => 1,

4])->get('http://example.com/users');
```

#### [Sending Form URL Encoded Requests](#sending-form-url-encoded-requests)

If you would like to send data using the `application/x-www-form-urlencoded` content type, you should call the `asForm` method before making your request:

```
1$response = Http::asForm()->post('http://example.com/users', [

2    'name' => 'Sara',

3    'role' => 'Privacy Consultant',

4]);
```

#### [Sending a Raw Request Body](#sending-a-raw-request-body)

You may use the `withBody` method if you would like to provide a raw request body when making a request. The content type may be provided via the method's second argument:

```
1$response = Http::withBody(

2    base64_encode($photo), 'image/jpeg'

3)->post('http://example.com/photo');
```

#### [Multi-Part Requests](#multi-part-requests)

If you would like to send files as multi-part requests, you should call the `attach` method before making your request. This method accepts the name of the file and its contents. If needed, you may provide a third argument which will be considered the file's filename, while a fourth argument may be used to provide headers associated with the file:

```
1$response = Http::attach(

2    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']

3)->post('http://example.com/attachments');
```

Instead of passing the raw contents of a file, you may pass a stream resource:

```
1$photo = fopen('photo.jpg', 'r');

2 

3$response = Http::attach(

4    'attachment', $photo, 'photo.jpg'

5)->post('http://example.com/attachments');
```

### [Headers](#headers)

Headers may be added to requests using the `withHeaders` method. This `withHeaders` method accepts an array of key / value pairs:

```
1$response = Http::withHeaders([

2    'X-First' => 'foo',

3    'X-Second' => 'bar'

4])->post('http://example.com/users', [

5    'name' => 'Taylor',

6]);
```

You may use the `accept` method to specify the content type that your application is expecting in response to your request:

```
1$response = Http::accept('application/json')->get('http://example.com/users');
```

For convenience, you may use the `acceptJson` method to quickly specify that your application expects the `application/json` content type in response to your request:

```
1$response = Http::acceptJson()->get('http://example.com/users');
```

The `withHeaders` method merges new headers into the request's existing headers. If needed, you may replace all of the headers entirely using the `replaceHeaders` method:

```
1$response = Http::withHeaders([

2    'X-Original' => 'foo',

3])->replaceHeaders([

4    'X-Replacement' => 'bar',

5])->post('http://example.com/users', [

6    'name' => 'Taylor',

7]);
```

### [Authentication](#authentication)

You may specify basic and digest authentication credentials using the `withBasicAuth` and `withDigestAuth` methods, respectively:

```
1// Basic authentication...

2$response = Http::withBasicAuth('[[email protected]](/cdn-cgi/l/email-protection)', 'secret')->post(/* ... */);

3 

4// Digest authentication...

5$response = Http::withDigestAuth('[[email protected]](/cdn-cgi/l/email-protection)', 'secret')->post(/* ... */);
```

#### [Bearer Tokens](#bearer-tokens)

If you would like to quickly add a bearer token to the request's `Authorization` header, you may use the `withToken` method:

```
1$response = Http::withToken('token')->post(/* ... */);
```

### [Timeout](#timeout)

The `timeout` method may be used to specify the maximum number of seconds to wait for a response. By default, the HTTP client will timeout after 30 seconds:

```
1$response = Http::timeout(3)->get(/* ... */);
```

If the given timeout is exceeded, an instance of `Illuminate\Http\Client\ConnectionException` will be thrown.

You may specify the maximum number of seconds to wait while trying to connect to a server using the `connectTimeout` method. The default is 10 seconds:

```
1$response = Http::connectTimeout(3)->get(/* ... */);
```

### [Retries](#retries)

If you would like the HTTP client to automatically retry the request if a client or server error occurs, you may use the `retry` method. The `retry` method accepts the maximum number of times the request should be attempted and the number of milliseconds that Laravel should wait in between attempts:

```
1$response = Http::retry(3, 100)->post(/* ... */);
```

If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the second argument to the `retry` method:

```
1use Exception;

2 

3$response = Http::retry(3, function (int $attempt, Exception $exception) {

4    return $attempt * 100;

5})->post(/* ... */);
```

For convenience, you may also provide an array as the first argument to the `retry` method. This array will be used to determine how many milliseconds to sleep between subsequent attempts:

```
1$response = Http::retry([100, 200])->post(/* ... */);
```

If needed, you may pass a third argument to the `retry` method. The third argument should be a callable that determines if the retries should actually be attempted. For example, you may wish to only retry the request if the initial request encounters an `ConnectionException`:

```
1use Illuminate\Http\Client\PendingRequest;

2use Throwable;

3 

4$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {

5    return $exception instanceof ConnectionException;

6})->post(/* ... */);
```

If a request attempt fails, you may wish to make a change to the request before a new attempt is made. You can achieve this by modifying the request argument provided to the callable you provided to the `retry` method. For example, you might want to retry the request with a new authorization token if the first attempt returned an authentication error:

```
 1use Illuminate\Http\Client\PendingRequest;

 2use Illuminate\Http\Client\RequestException;

 3use Throwable;

 4 

 5$response = Http::withToken($this->getToken())->retry(2, 0, function (Throwable $exception, PendingRequest $request) {

 6    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {

 7        return false;

 8    }

 9 

10    $request->withToken($this->getNewToken());

11 

12    return true;

13})->post(/* ... */);
```

If all of the requests fail, an instance of `Illuminate\Http\Client\RequestException` will be thrown. If you would like to disable this behavior, you may provide a `throw` argument with a value of `false`. When disabled, the last response received by the client will be returned after all retries have been attempted:

```
1$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

If all of the requests fail because of a connection issue, a `Illuminate\Http\Client\ConnectionException` will still be thrown even when the `throw` argument is set to `false`.

### [Error Handling](#error-handling)

Unlike Guzzle's default behavior, Laravel's HTTP client wrapper does not throw exceptions on client or server errors (`400` and `500` level responses from servers). You may determine if one of these errors was returned using the `successful`, `clientError`, or `serverError` methods:

```
 1// Determine if the status code is >= 200 and < 300...

 2$response->successful();

 3 

 4// Determine if the status code is >= 400...

 5$response->failed();

 6 

 7// Determine if the response has a 400 level status code...

 8$response->clientError();

 9 

10// Determine if the response has a 500 level status code...

11$response->serverError();

12 

13// Immediately execute the given callback if there was a client or server error...

14$response->onError(callable $callback);
```

#### [Throwing Exceptions](#throwing-exceptions)

If you have a response instance and would like to throw an instance of `Illuminate\Http\Client\RequestException` if the response status code indicates a client or server error, you may use the `throw` or `throwIf` methods:

```
 1use Illuminate\Http\Client\Response;

 2 

 3$response = Http::post(/* ... */);

 4 

 5// Throw an exception if a client or server error occurred...

 6$response->throw();

 7 

 8// Throw an exception if an error occurred and the given condition is true...

 9$response->throwIf($condition);

10 

11// Throw an exception if an error occurred and the given closure resolves to true...

12$response->throwIf(fn (Response $response) => true);

13 

14// Throw an exception if an error occurred and the given condition is false...

15$response->throwUnless($condition);

16 

17// Throw an exception if an error occurred and the given closure resolves to false...

18$response->throwUnless(fn (Response $response) => false);

19 

20// Throw an exception if the response has a specific status code...

21$response->throwIfStatus(403);

22 

23// Throw an exception unless the response has a specific status code...

24$response->throwUnlessStatus(200);

25 

26// Throw an exception if a server error occurred (status >500)...

27$response->throwIfServerError();

28 

29// Throw an exception if a client error occurred (status >400 and <500)...

30$response->throwIfClientError();

31 

32return $response['user']['id'];
```

The `Illuminate\Http\Client\RequestException` instance has a public `$response` property which will allow you to inspect the returned response.

The `throw` method returns the response instance if no error occurred, allowing you to chain other operations onto the `throw` method:

```
1return Http::post(/* ... */)->throw()->json();
```

If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw` method. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure:

```
1use Illuminate\Http\Client\Response;

2use Illuminate\Http\Client\RequestException;

3 

4return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {

5    // ...

6})->json();
```

By default, `RequestException` messages are truncated to 120 characters when logged or reported. To customize or disable this behavior, you may utilize the `truncateAt` and `dontTruncate` methods when configuring your application's registered behavior in your `bootstrap/app.php` file:

```
1use Illuminate\Http\Client\RequestException;

2 

3->registered(function (): void {

4    // Truncate request exception messages to 240 characters...

5    RequestException::truncateAt(240);

6 

7    // Disable request exception message truncation...

8    RequestException::dontTruncate();

9})
```

Alternatively, you may customize the exception truncation behavior per request using the `truncateExceptionsAt` method:

```
1return Http::truncateExceptionsAt(240)->post(/* ... */);
```

### [Guzzle Middleware](#guzzle-middleware)

Since Laravel's HTTP client is powered by Guzzle, you may take advantage of [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) to manipulate the outgoing request or inspect the incoming response. To manipulate the outgoing request, register a Guzzle middleware via the `withRequestMiddleware` method:

```
1use Illuminate\Support\Facades\Http;

2use Psr\Http\Message\RequestInterface;

3 

4$response = Http::withRequestMiddleware(

5    function (RequestInterface $request) {

6        return $request->withHeader('X-Example', 'Value');

7    }

8)->get('http://example.com');
```

Likewise, you can inspect the incoming HTTP response by registering a middleware via the `withResponseMiddleware` method:

```
 1use Illuminate\Support\Facades\Http;

 2use Psr\Http\Message\ResponseInterface;

 3 

 4$response = Http::withResponseMiddleware(

 5    function (ResponseInterface $response) {

 6        $header = $response->getHeader('X-Example');

 7 

 8        // ...

 9 

10        return $response;

11    }

12)->get('http://example.com');
```

#### [Global Middleware](#global-middleware)

Sometimes, you may want to register a middleware that applies to every outgoing request and incoming response. To accomplish this, you may use the `globalRequestMiddleware` and `globalResponseMiddleware` methods. Typically, these methods should be invoked in the `boot` method of your application's `AppServiceProvider`:

```
1use Illuminate\Support\Facades\Http;

2 

3Http::globalRequestMiddleware(fn ($request) => $request->withHeader(

4    'User-Agent', 'Example Application/1.0'

5));

6 

7Http::globalResponseMiddleware(fn ($response) => $response->withHeader(

8    'X-Finished-At', now()->toDateTimeString()

9));
```

### [Guzzle Options](#guzzle-options)

You may specify additional [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) for an outgoing request using the `withOptions` method. The `withOptions` method accepts an array of key / value pairs:

```
1$response = Http::withOptions([

2    'debug' => true,

3])->get('http://example.com/users');
```

#### [Global Options](#global-options)

To configure default options for every outgoing request, you may utilize the `globalOptions` method. Typically, this method should be invoked from the `boot` method of your application's `AppServiceProvider`:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3/**

 4 * Bootstrap any application services.

 5 */

 6public function boot(): void

 7{

 8    Http::globalOptions([

 9        'allow_redirects' => false,

10    ]);

11}
```

## [Concurrent Requests](#concurrent-requests)

Sometimes, you may wish to make multiple HTTP requests concurrently. In other words, you want several requests to be dispatched at the same time instead of issuing the requests sequentially. This can lead to substantial performance improvements when interacting with slow HTTP APIs.

### [Request Pooling](#request-pooling)

Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Http\Client\Pool` instance, allowing you to easily add requests to the request pool for dispatching:

```
 1use Illuminate\Http\Client\Pool;

 2use Illuminate\Support\Facades\Http;

 3 

 4$responses = Http::pool(fn (Pool $pool) => [

 5    $pool->get('http://localhost/first'),

 6    $pool->get('http://localhost/second'),

 7    $pool->get('http://localhost/third'),

 8]);

 9 

10return $responses[0]->ok() &&

11       $responses[1]->ok() &&

12       $responses[2]->ok();
```

As you can see, each response instance can be accessed based on the order it was added to the pool. If you wish, you can name the requests using the `as` method, which allows you to access the corresponding responses by name:

```
 1use Illuminate\Http\Client\Pool;

 2use Illuminate\Support\Facades\Http;

 3 

 4$responses = Http::pool(fn (Pool $pool) => [

 5    $pool->as('first')->get('http://localhost/first'),

 6    $pool->as('second')->get('http://localhost/second'),

 7    $pool->as('third')->get('http://localhost/third'),

 8]);

 9 

10return $responses['first']->ok();
```

The maximum concurrency of the request pool may be controlled by providing the `concurrency` argument to the `pool` method. This value determines the maximum number of HTTP requests that may be concurrently in-flight while processing the request pool:

```
1$responses = Http::pool(fn (Pool $pool) => [

2    // ...

3], concurrency: 5);
```

#### [Customizing Concurrent Requests](#customizing-concurrent-requests)

The `pool` method cannot be chained with other HTTP client methods such as the `withHeaders` or `middleware` methods. If you want to apply custom headers or middleware to pooled requests, you should configure those options on each request in the pool:

```
 1use Illuminate\Http\Client\Pool;

 2use Illuminate\Support\Facades\Http;

 3 

 4$headers = [

 5    'X-Example' => 'example',

 6];

 7 

 8$responses = Http::pool(fn (Pool $pool) => [

 9    $pool->withHeaders($headers)->get('http://laravel.test/test'),

10    $pool->withHeaders($headers)->get('http://laravel.test/test'),

11    $pool->withHeaders($headers)->get('http://laravel.test/test'),

12]);
```

### [Request Batching](#request-batching)

Another way of working with concurrent requests in Laravel is to use the `batch` method. Like the `pool` method, it accepts a closure which receives an `Illuminate\Http\Client\Batch` instance, allowing you to easily add requests to the request pool for dispatching, but it also allows you to define completion callbacks:

```
 1use Illuminate\Http\Client\Batch;

 2use Illuminate\Http\Client\ConnectionException;

 3use Illuminate\Http\Client\RequestException;

 4use Illuminate\Http\Client\Response;

 5use Illuminate\Support\Facades\Http;

 6 

 7$responses = Http::batch(fn (Batch $batch) => [

 8    $batch->get('http://localhost/first'),

 9    $batch->get('http://localhost/second'),

10    $batch->get('http://localhost/third'),

11])->before(function (Batch $batch) {

12    // The batch has been created but no requests have been initialized...

13})->progress(function (Batch $batch, int|string $key, Response $response) {

14    // An individual request has completed successfully...

15})->then(function (Batch $batch, array $results) {

16    // All requests completed successfully...

17})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {

18    // Batch request failure detected...

19})->finally(function (Batch $batch, array $results) {

20    // The batch has finished executing...

21})->send();
```

Like the `pool` method, you can use the `as` method to name your requests:

```
1$responses = Http::batch(fn (Batch $batch) => [

2    $batch->as('first')->get('http://localhost/first'),

3    $batch->as('second')->get('http://localhost/second'),

4    $batch->as('third')->get('http://localhost/third'),

5])->send();
```

After a `batch` is started by calling the `send` method, you can't add new requests to it. Trying to do so will result in a `Illuminate\Http\Client\BatchInProgressException` exception being thrown.

The maximum concurrency of the request batch may be controlled via the `concurrency` method. This value determines the maximum number of HTTP requests that may be concurrently in-flight while processing the request batch:

```
1$responses = Http::batch(fn (Batch $batch) => [

2    // ...

3])->concurrency(5)->send();
```

#### [Inspecting Batches](#inspecting-batches)

The `Illuminate\Http\Client\Batch` instance that is provided to batch completion callbacks has a variety of properties and methods to assist you in interacting with and inspecting a given batch of requests:

```
 1// The number of requests assigned to the batch...

 2$batch->totalRequests;

 3 

 4// The number of requests that have not been processed yet...

 5$batch->pendingRequests;

 6 

 7// The number of requests that have failed...

 8$batch->failedRequests;

 9 

10// The number of requests that have been processed thus far...

11$batch->processedRequests();

12 

13// Indicates if the batch has finished executing...

14$batch->finished();

15 

16// Indicates if the batch has request failures...

17$batch->hasFailures();
```

#### [Deferring Batches](#deferring-batches)

When the `defer` method is invoked, the batch of requests is not executed immediately. Instead, Laravel will execute the batch after the current application request's HTTP response has been sent to the user, keeping your application feeling fast and responsive:

```
 1use Illuminate\Http\Client\Batch;

 2use Illuminate\Support\Facades\Http;

 3 

 4$responses = Http::batch(fn (Batch $batch) => [

 5    $batch->get('http://localhost/first'),

 6    $batch->get('http://localhost/second'),

 7    $batch->get('http://localhost/third'),

 8])->then(function (Batch $batch, array $results) {

 9    // All requests completed successfully...

10})->defer();
```

## [Macros](#macros)

The Laravel HTTP client allows you to define "macros", which can serve as a fluent, expressive mechanism to configure common request paths and headers when interacting with services throughout your application. To get started, you may define the macro within the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3/**

 4 * Bootstrap any application services.

 5 */

 6public function boot(): void

 7{

 8    Http::macro('github', function () {

 9        return Http::withHeaders([

10            'X-Example' => 'example',

11        ])->baseUrl('https://github.com');

12    });

13}
```

Once your macro has been configured, you may invoke it from anywhere in your application to create a pending request with the specified configuration:

```
1$response = Http::github()->get('/');
```

## [Testing](#testing)

Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's HTTP client is no exception. The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made.

### [Faking Responses](#faking-responses)

For example, to instruct the HTTP client to return empty, `200` status code responses for every request, you may call the `fake` method with no arguments:

```
1use Illuminate\Support\Facades\Http;

2 

3Http::fake();

4 

5$response = Http::post(/* ... */);
```

#### [Faking Specific URLs](#faking-specific-urls)

Alternatively, you may pass an array to the `fake` method. The array's keys should represent URL patterns that you wish to fake and their associated responses. The `*` character may be used as a wildcard character. You may use the `Http` facade's `response` method to construct stub / fake responses for these endpoints:

```
1Http::fake([

2    // Stub a JSON response for GitHub endpoints...

3    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

4 

5    // Stub a string response for Google endpoints...

6    'google.com/*' => Http::response('Hello World', 200, $headers),

7]);
```

Any requests made to URLs that have not been faked will actually be executed. If you would like to specify a fallback URL pattern that will stub all unmatched URLs, you may use a single `*` character:

```
1Http::fake([

2    // Stub a JSON response for GitHub endpoints...

3    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

4 

5    // Stub a string response for all other endpoints...

6    '*' => Http::response('Hello World', 200, ['Headers']),

7]);
```

For convenience, simple string, JSON, and empty responses may be generated by providing a string, array, or integer as the response:

```
1Http::fake([

2    'google.com/*' => 'Hello World',

3    'github.com/*' => ['foo' => 'bar'],

4    'chatgpt.com/*' => 200,

5]);
```

#### [Faking Exceptions](#faking-connection-exceptions)

Sometimes you may need to test your application's behavior if the HTTP client encounters an `Illuminate\Http\Client\ConnectionException` when attempting to make a request. You can instruct the HTTP client to throw a connection exception using the `failedConnection` method:

```
1Http::fake([

2    'github.com/*' => Http::failedConnection(),

3]);
```

To test your application's behavior if a `Illuminate\Http\Client\RequestException` is thrown, you may use the `failedRequest` method:

```
1$this->mock(GithubService::class);

2    ->shouldReceive('getUser')

3    ->andThrow(

4        Http::failedRequest(['code' => 'not_found'], 404)

5    );
```

#### [Faking Response Sequences](#faking-response-sequences)

Sometimes you may need to specify that a single URL should return a series of fake responses in a specific order. You may accomplish this using the `Http::sequence` method to build the responses:

```
1Http::fake([

2    // Stub a series of responses for GitHub endpoints...

3    'github.com/*' => Http::sequence()

4        ->push('Hello World', 200)

5        ->push(['foo' => 'bar'], 200)

6        ->pushStatus(404),

7]);
```

When all the responses in a response sequence have been consumed, any further requests will cause the response sequence to throw an exception. If you would like to specify a default response that should be returned when a sequence is empty, you may use the `whenEmpty` method:

```
1Http::fake([

2    // Stub a series of responses for GitHub endpoints...

3    'github.com/*' => Http::sequence()

4        ->push('Hello World', 200)

5        ->push(['foo' => 'bar'], 200)

6        ->whenEmpty(Http::response()),

7]);
```

If you would like to fake a sequence of responses but do not need to specify a specific URL pattern that should be faked, you may use the `Http::fakeSequence` method:

```
1Http::fakeSequence()

2    ->push('Hello World', 200)

3    ->whenEmpty(Http::response());
```

#### [Fake Callback](#fake-callback)

If you require more complicated logic to determine what responses to return for certain endpoints, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Http\Client\Request` and should return a response instance. Within your closure, you may perform whatever logic is necessary to determine what type of response to return:

```
1use Illuminate\Http\Client\Request;

2 

3Http::fake(function (Request $request) {

4    return Http::response('Hello World', 200);

5});
```

### [Inspecting Requests](#inspecting-requests)

When faking responses, you may occasionally wish to inspect the requests the client receives in order to make sure your application is sending the correct data or headers. You may accomplish this by calling the `Http::assertSent` method after calling `Http::fake`.

The `assertSent` method accepts a closure which will receive an `Illuminate\Http\Client\Request` instance and should return a boolean value indicating if the request matches your expectations. In order for the test to pass, at least one request must have been issued matching the given expectations:

```
 1use Illuminate\Http\Client\Request;

 2use Illuminate\Support\Facades\Http;

 3 

 4Http::fake();

 5 

 6Http::withHeaders([

 7    'X-First' => 'foo',

 8])->post('http://example.com/users', [

 9    'name' => 'Taylor',

10    'role' => 'Developer',

11]);

12 

13Http::assertSent(function (Request $request) {

14    return $request->hasHeader('X-First', 'foo') &&

15           $request->url() == 'http://example.com/users' &&

16           $request['name'] == 'Taylor' &&

17           $request['role'] == 'Developer';

18});
```

If needed, you may assert that a specific request was not sent using the `assertNotSent` method:

```
 1use Illuminate\Http\Client\Request;

 2use Illuminate\Support\Facades\Http;

 3 

 4Http::fake();

 5 

 6Http::post('http://example.com/users', [

 7    'name' => 'Taylor',

 8    'role' => 'Developer',

 9]);

10 

11Http::assertNotSent(function (Request $request) {

12    return $request->url() === 'http://example.com/posts';

13});
```

You may use the `assertSentCount` method to assert how many requests were "sent" during the test:

```
1Http::fake();

2 

3Http::assertSentCount(5);
```

Or, you may use the `assertNothingSent` method to assert that no requests were sent during the test:

```
1Http::fake();

2 

3Http::assertNothingSent();
```

#### [Recording Requests / Responses](#recording-requests-and-responses)

You may use the `recorded` method to gather all requests and their corresponding responses. The `recorded` method returns a collection of arrays that contains instances of `Illuminate\Http\Client\Request` and `Illuminate\Http\Client\Response`:

```
 1Http::fake([

 2    'https://laravel.com' => Http::response(status: 500),

 3    'https://nova.laravel.com/' => Http::response(),

 4]);

 5 

 6Http::get('https://laravel.com');

 7Http::get('https://nova.laravel.com/');

 8 

 9$recorded = Http::recorded();

10 

11[$request, $response] = $recorded[0];
```

Additionally, the `recorded` method accepts a closure which will receive an instance of `Illuminate\Http\Client\Request` and `Illuminate\Http\Client\Response` and may be used to filter request / response pairs based on your expectations:

```
 1use Illuminate\Http\Client\Request;

 2use Illuminate\Http\Client\Response;

 3 

 4Http::fake([

 5    'https://laravel.com' => Http::response(status: 500),

 6    'https://nova.laravel.com/' => Http::response(),

 7]);

 8 

 9Http::get('https://laravel.com');

10Http::get('https://nova.laravel.com/');

11 

12$recorded = Http::recorded(function (Request $request, Response $response) {

13    return $request->url() !== 'https://laravel.com' &&

14           $response->successful();

15});
```

### [Preventing Stray Requests](#preventing-stray-requests)

If you would like to ensure that all requests sent via the HTTP client have been faked throughout your individual test or complete test suite, you can call the `preventStrayRequests` method. After calling this method, any requests that do not have a corresponding fake response will throw an exception rather than making the actual HTTP request:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3Http::preventStrayRequests();

 4 

 5Http::fake([

 6    'github.com/*' => Http::response('ok'),

 7]);

 8 

 9// An "ok" response is returned...

10Http::get('https://github.com/laravel/framework');

11 

12// An exception is thrown...

13Http::get('https://laravel.com');
```

Sometimes, you may wish to prevent most stray requests while still allowing specific requests to execute. To accomplish this, you may pass an array of URL patterns to the `allowStrayRequests` method. Any request matching one of the given patterns will be allowed, while all other requests will continue to throw an exception:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3Http::preventStrayRequests();

 4 

 5Http::allowStrayRequests([

 6    'http://127.0.0.1:5000/*',

 7]);

 8 

 9// This request is executed...

10Http::get('http://127.0.0.1:5000/generate');

11 

12// An exception is thrown...

13Http::get('https://laravel.com');
```

## [Events](#events)

Laravel fires three events during the process of sending HTTP requests. The `RequestSending` event is fired prior to a request being sent, while the `ResponseReceived` event is fired after a response is received for a given request. The `ConnectionFailed` event is fired if no response is received for a given request.

The `RequestSending` and `ConnectionFailed` events both contain a public `$request` property that you may use to inspect the `Illuminate\Http\Client\Request` instance. Likewise, the `ResponseReceived` event contains a `$request` property as well as a `$response` property which may be used to inspect the `Illuminate\Http\Client\Response` instance. You may create [event listeners](/docs/13.x/events) for these events within your application:

```
 1use Illuminate\Http\Client\Events\RequestSending;

 2 

 3class LogRequest

 4{

 5    /**

 6     * Handle the event.

 7     */

 8    public function handle(RequestSending $event): void

 9    {

10        // $event->request ...

11    }

12}
```
