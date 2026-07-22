# URL Generation

- [Introduction](#introduction)
- [The Basics](#the-basics)
  * [Generating URLs](#generating-urls)
  * [Accessing the Current URL](#accessing-the-current-url)
- [URLs for Named Routes](#urls-for-named-routes)
  * [Signed URLs](#signed-urls)
- [URLs for Controller Actions](#urls-for-controller-actions)
- [Fluent URI Objects](#fluent-uri-objects)
- [Default Values](#default-values)

## [Introduction](#introduction)

Laravel provides several helpers to assist you in generating URLs for your application. These helpers are primarily helpful when building links in your templates and API responses, or when generating redirect responses to another part of your application.

## [The Basics](#the-basics)

### [Generating URLs](#generating-urls)

The `url` helper may be used to generate arbitrary URLs for your application. The generated URL will automatically use the scheme (HTTP or HTTPS) and host from the current request being handled by the application:

```
1$post = App\Models\Post::find(1);

2 

3echo url("/posts/{$post->id}");

4 

5// http://example.com/posts/1
```

To generate a URL with query string parameters, you may use the `query` method:

```
1echo url()->query('/posts', ['search' => 'Laravel']);

2 

3// https://example.com/posts?search=Laravel

4 

5echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

6 

7// http://example.com/posts?sort=latest&search=Laravel
```

Providing query string parameters that already exist in the path will overwrite their existing value:

```
1echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

2 

3// http://example.com/posts?sort=oldest
```

Arrays of values may also be passed as query parameters. These values will be properly keyed and encoded in the generated URL:

```
1echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

2 

3// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

4 

5echo urldecode($url);

6 

7// http://example.com/posts?columns[0]=title&columns[1]=body
```

### [Accessing the Current URL](#accessing-the-current-url)

If no path is provided to the `url` helper, an `Illuminate\Routing\UrlGenerator` instance is returned, allowing you to access information about the current URL:

```
1// Get the current URL without the query string...

2echo url()->current();

3 

4// Get the current URL including the query string...

5echo url()->full();
```

Each of these methods may also be accessed via the `URL` [facade](/docs/13.x/facades):

```
1use Illuminate\Support\Facades\URL;

2 

3echo URL::current();
```

#### [Accessing the Previous URL](#accessing-the-previous-url)

Sometimes it is helpful to know the previous URL that the user is visiting from. You can access the previous URL via the `url` helper's `previous` and `previousPath` methods:

```
1// Get the full URL for the previous request...

2echo url()->previous();

3 

4// Get the path for the previous request...

5echo url()->previousPath();
```

Or, via the [session](/docs/13.x/session), you may access the previous URL as a [fluent URI](#fluent-uri-objects) instance:

```
1use Illuminate\Http\Request;

2 

3Route::post('/users', function (Request $request) {

4    $previousUri = $request->session()->previousUri();

5 

6    // ...

7});
```

It is also possible to retrieve the route name for the previously visited URL via the session:

```
1$previousRoute = $request->session()->previousRoute();
```

## [URLs for Named Routes](#urls-for-named-routes)

The `route` helper may be used to generate URLs to [named routes](/docs/13.x/routing#named-routes). Named routes allow you to generate URLs without being coupled to the actual URL defined on the route. Therefore, if the route's URL changes, no changes need to be made to your calls to the `route` function. For example, imagine your application contains a route defined like the following:

```
1Route::get('/post/{post}', function (Post $post) {

2    // ...

3})->name('post.show');
```

To generate a URL to this route, you may use the `route` helper like so:

```
1echo route('post.show', ['post' => 1]);

2 

3// http://example.com/post/1
```

Of course, the `route` helper may also be used to generate URLs for routes with multiple parameters:

```
1Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {

2    // ...

3})->name('comment.show');

4 

5echo route('comment.show', ['post' => 1, 'comment' => 3]);

6 

7// http://example.com/post/1/comment/3
```

Any additional array elements that do not correspond to the route's definition parameters will be added to the URL's query string:

```
1echo route('post.show', ['post' => 1, 'search' => 'rocket']);

2 

3// http://example.com/post/1?search=rocket
```

#### [Eloquent Models](#eloquent-models)

You will often be generating URLs using the route key (typically the primary key) of [Eloquent models](/docs/13.x/eloquent). For this reason, you may pass Eloquent models as parameter values. The `route` helper will automatically extract the model's route key:

```
1echo route('post.show', ['post' => $post]);
```

### [Signed URLs](#signed-urls)

Laravel allows you to easily create "signed" URLs to named routes. These URLs have a "signature" hash appended to the query string which allows Laravel to verify that the URL has not been modified since it was created. Signed URLs are especially useful for routes that are publicly accessible yet need a layer of protection against URL manipulation.

For example, you might use signed URLs to implement a public "unsubscribe" link that is emailed to your customers. To create a signed URL to a named route, use the `signedRoute` method of the `URL` facade:

```
1use Illuminate\Support\Facades\URL;

2 

3return URL::signedRoute('unsubscribe', ['user' => 1]);
```

You may exclude the domain from the signed URL hash by providing the `absolute` argument to the `signedRoute` method:

```
1return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

If you would like to generate a temporary signed route URL that expires after a specified amount of time, you may use the `temporarySignedRoute` method. When Laravel validates a temporary signed route URL, it will ensure that the expiration timestamp that is encoded into the signed URL has not elapsed:

```
1use Illuminate\Support\Facades\URL;

2 

3return URL::temporarySignedRoute(

4    'unsubscribe', now()->plus(minutes: 30), ['user' => 1]

5);
```

#### [Validating Signed Route Requests](#validating-signed-route-requests)

To verify that an incoming request has a valid signature, you should call the `hasValidSignature` method on the incoming `Illuminate\Http\Request` instance:

```
1use Illuminate\Http\Request;

2 

3Route::get('/unsubscribe/{user}', function (Request $request) {

4    if (! $request->hasValidSignature()) {

5        abort(401);

6    }

7 

8    // ...

9})->name('unsubscribe');
```

Sometimes, you may need to allow your application's frontend to append data to a signed URL, such as when performing client-side pagination. Therefore, you can specify request query parameters that should be ignored when validating a signed URL using the `hasValidSignatureWhileIgnoring` method. Remember, ignoring parameters allows anyone to modify those parameters on the request:

```
1if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {

2    abort(401);

3}
```

Instead of validating signed URLs using the incoming request instance, you may assign the `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [middleware](/docs/13.x/middleware) to the route. If the incoming request does not have a valid signature, the middleware will automatically return a `403` HTTP response:

```
1Route::post('/unsubscribe/{user}', function (Request $request) {

2    // ...

3})->name('unsubscribe')->middleware('signed');
```

If your signed URLs do not include the domain in the URL hash, you should provide the `relative` argument to the middleware:

```
1Route::post('/unsubscribe/{user}', function (Request $request) {

2    // ...

3})->name('unsubscribe')->middleware('signed:relative');
```

#### [Responding to Invalid Signed Routes](#responding-to-invalid-signed-routes)

When someone visits a signed URL that has expired, they will receive a generic error page for the `403` HTTP status code. However, you can customize this behavior by defining a custom "render" closure for the `InvalidSignatureException` exception in your application's `bootstrap/app.php` file:

```
1use Illuminate\Routing\Exceptions\InvalidSignatureException;

2 

3->withExceptions(function (Exceptions $exceptions): void {

4    $exceptions->render(function (InvalidSignatureException $e) {

5        return response()->view('errors.link-expired', status: 403);

6    });

7})
```

## [URLs for Controller Actions](#urls-for-controller-actions)

The `action` function generates a URL for the given controller action:

```
1use App\Http\Controllers\HomeController;

2 

3$url = action([HomeController::class, 'index']);
```

If the controller method accepts route parameters, you may pass an associative array of route parameters as the second argument to the function:

```
1$url = action([UserController::class, 'profile'], ['id' => 1]);
```

## [Fluent URI Objects](#fluent-uri-objects)

Laravel's `Uri` class provides a convenient and fluent interface for creating and manipulating URIs via objects. This class wraps the functionality provided by the underlying League URI package and integrates seamlessly with Laravel's routing system.

You can create a `Uri` instance easily using static methods:

```
 1use App\Http\Controllers\UserController;

 2use App\Http\Controllers\InvokableController;

 3use Illuminate\Support\Uri;

 4 

 5// Generate a URI instance from the given string...

 6$uri = Uri::of('https://example.com/path');

 7 

 8// Generate URI instances to paths, named routes, or controller actions...

 9$uri = Uri::to('/dashboard');

10$uri = Uri::route('users.show', ['user' => 1]);

11$uri = Uri::signedRoute('users.show', ['user' => 1]);

12$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));

13$uri = Uri::action([UserController::class, 'index']);

14$uri = Uri::action(InvokableController::class);

15 

16// Generate a URI instance from the current request URL...

17$uri = $request->uri();

18 

19// Generate a URI instance from the previous request URL...

20$uri = $request->session()->previousUri();
```

Once you have a URI instance, you can fluently modify it:

```
1$uri = Uri::of('https://example.com')

2    ->withScheme('http')

3    ->withHost('test.com')

4    ->withPort(8000)

5    ->withPath('/users')

6    ->withQuery(['page' => 2])

7    ->withFragment('section-1');
```

For more information on working with fluent URI objects, consult the [URI documentation](/docs/13.x/helpers#uri).

## [Default Values](#default-values)

For some applications, you may wish to specify request-wide default values for certain URL parameters. For example, imagine many of your routes define a `{locale}` parameter:

```
1Route::get('/{locale}/posts', function () {

2    // ...

3})->name('post.index');
```

It is cumbersome to always pass the `locale` every time you call the `route` helper. So, you may use the `URL::defaults` method to define a default value for this parameter that will always be applied during the current request. You may wish to call this method from a [route middleware](/docs/13.x/middleware#assigning-middleware-to-routes) so that you have access to the current request:

```
 1<?php

 2 

 3namespace App\Http\Middleware;

 4 

 5use Closure;

 6use Illuminate\Http\Request;

 7use Illuminate\Support\Facades\URL;

 8use Symfony\Component\HttpFoundation\Response;

 9 

10class SetDefaultLocaleForUrls

11{

12    /**

13     * Handle an incoming request.

14     *

15     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next

16     */

17    public function handle(Request $request, Closure $next): Response

18    {

19        URL::defaults(['locale' => $request->user()->locale]);

20 

21        return $next($request);

22    }

23}
```

Once the default value for the `locale` parameter has been set, you are no longer required to pass its value when generating URLs via the `route` helper.

#### [URL Defaults and Middleware Priority](#url-defaults-middleware-priority)

Setting URL default values can interfere with Laravel's handling of implicit model bindings. Therefore, you should [prioritize your middleware](/docs/13.x/middleware#sorting-middleware) that set URL defaults to be executed before Laravel's own `SubstituteBindings` middleware. You can accomplish this using the `priority` middleware method in your application's `bootstrap/app.php` file:

```
1->withMiddleware(function (Middleware $middleware): void {

2    $middleware->prependToPriorityList(

3        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,

4        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,

5    );

6})
```
