# Routing

- [Basic Routing](#basic-routing)
  * [The Default Route Files](#the-default-route-files)
  * [Redirect Routes](#redirect-routes)
  * [View Routes](#view-routes)
  * [Listing Your Routes](#listing-your-routes)
  * [Routing Customization](#routing-customization)
- [Route Parameters](#route-parameters)
  * [Required Parameters](#required-parameters)
  * [Optional Parameters](#parameters-optional-parameters)
  * [Regular Expression Constraints](#parameters-regular-expression-constraints)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
  * [Middleware](#route-group-middleware)
  * [Controllers](#route-group-controllers)
  * [Subdomain Routing](#route-group-subdomain-routing)
  * [Route Prefixes](#route-group-prefixes)
  * [Route Name Prefixes](#route-group-name-prefixes)
- [Route Model Binding](#route-model-binding)
  * [Implicit Binding](#implicit-binding)
  * [Implicit Enum Binding](#implicit-enum-binding)
  * [Explicit Binding](#explicit-binding)
- [Fallback Routes](#fallback-routes)
- [Rate Limiting](#rate-limiting)
  * [Defining Rate Limiters](#defining-rate-limiters)
  * [Attaching Rate Limiters to Routes](#attaching-rate-limiters-to-routes)
- [Form Method Spoofing](#form-method-spoofing)
- [Accessing the Current Route](#accessing-the-current-route)
- [Cross-Origin Resource Sharing (CORS)](#cors)
- [Route Caching](#route-caching)

## [Basic Routing](#basic-routing)

The most basic Laravel routes accept a URI and a closure, providing a very simple and expressive method of defining routes and behavior without complicated routing configuration files:

```
1use Illuminate\Support\Facades\Route;

2 

3Route::get('/greeting', function () {

4    return 'Hello World';

5});
```

### [The Default Route Files](#the-default-route-files)

All Laravel routes are defined in your route files, which are located in the `routes` directory. These files are automatically loaded by Laravel using the configuration specified in your application's `bootstrap/app.php` file. The `routes/web.php` file defines routes that are for your web interface. These routes are assigned the `web` [middleware group](/docs/13.x/middleware#laravels-default-middleware-groups), which provides features like session state and CSRF protection.

For most applications, you will begin by defining routes in your `routes/web.php` file. The routes defined in `routes/web.php` may be accessed by entering the defined route's URL in your browser. For example, you may access the following route by navigating to `http://example.com/user` in your browser:

```
1use App\Http\Controllers\UserController;

2 

3Route::get('/user', [UserController::class, 'index']);
```

#### [API Routes](#api-routes)

If your application will also offer a stateless API, you may enable API routing using the `install:api` Artisan command:

```
1php artisan install:api
```

The `install:api` command installs [Laravel Sanctum](/docs/13.x/sanctum), which provides a robust, yet simple API token authentication guard which can be used to authenticate third-party API consumers, SPAs, or mobile applications. In addition, the `install:api` command creates the `routes/api.php` file:

```
1Route::get('/user', function (Request $request) {

2    return $request->user();

3})->middleware('auth:sanctum');
```

Of course, you are free to omit the `auth:sanctum` middleware on routes that should be publicly accessible.

The routes in `routes/api.php` are stateless and are assigned to the `api` [middleware group](/docs/13.x/middleware#laravels-default-middleware-groups). Additionally, the `/api` URI prefix is automatically applied to these routes, so you do not need to manually apply it to every route in the file. You may change the prefix by modifying your application's `bootstrap/app.php` file:

```
1->withRouting(

2    api: __DIR__.'/../routes/api.php',

3    apiPrefix: 'api/admin',

4    // ...

5)
```

#### [Available Router Methods](#available-router-methods)

The router allows you to register routes that respond to any HTTP verb:

```
1Route::get($uri, $callback);

2Route::post($uri, $callback);

3Route::put($uri, $callback);

4Route::patch($uri, $callback);

5Route::delete($uri, $callback);

6Route::options($uri, $callback);
```

Sometimes you may need to register a route that responds to multiple HTTP verbs. You may do so using the `match` method. Or, you may even register a route that responds to all HTTP verbs using the `any` method:

```
1Route::match(['get', 'post'], '/', function () {

2    // ...

3});

4 

5Route::any('/', function () {

6    // ...

7});
```

When defining multiple routes that share the same URI, routes using the `get`, `post`, `put`, `patch`, `delete`, and `options` methods should be defined before routes using the `any`, `match`, and `redirect` methods. This ensures the incoming request is matched with the correct route.

#### [Dependency Injection](#dependency-injection)

You may type-hint any dependencies required by your route in your route's callback signature. The declared dependencies will automatically be resolved and injected into the callback by the Laravel [service container](/docs/13.x/container). For example, you may type-hint the `Illuminate\Http\Request` class to have the current HTTP request automatically injected into your route callback:

```
1use Illuminate\Http\Request;

2 

3Route::get('/users', function (Request $request) {

4    // ...

5});
```

#### [CSRF Protection](#csrf-protection)

Remember, any HTML forms pointing to `POST`, `PUT`, `PATCH`, or `DELETE` routes that are defined in the `web` routes file should include a CSRF token field. Otherwise, the request will be rejected. You can read more about CSRF protection in the [CSRF documentation](/docs/13.x/csrf):

```
1<form method="POST" action="/profile">

2    @csrf

3    ...

4</form>
```

### [Redirect Routes](#redirect-routes)

If you are defining a route that redirects to another URI, you may use the `Route::redirect` method. This method provides a convenient shortcut so that you do not have to define a full route or controller for performing a simple redirect:

```
1Route::redirect('/here', '/there');
```

By default, `Route::redirect` returns a `302` status code. You may customize the status code using the optional third parameter:

```
1Route::redirect('/here', '/there', 301);
```

Or, you may use the `Route::permanentRedirect` method to return a `301` status code:

```
1Route::permanentRedirect('/here', '/there');
```

When using route parameters in redirect routes, the following parameters are reserved by Laravel and cannot be used: `destination` and `status`.

### [View Routes](#view-routes)

If your route only needs to return a [view](/docs/13.x/views), you may use the `Route::view` method. Like the `redirect` method, this method provides a simple shortcut so that you do not have to define a full route or controller. The `view` method accepts a URI as its first argument and a view name as its second argument. In addition, you may provide an array of data to pass to the view as an optional third argument:

```
1Route::view('/welcome', 'welcome');

2 

3Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

When using route parameters in view routes, the following parameters are reserved by Laravel and cannot be used: `view`, `data`, `status`, and `headers`.

### [Listing Your Routes](#listing-your-routes)

The `route:list` Artisan command can easily provide an overview of all of the routes that are defined by your application:

```
1php artisan route:list
```

By default, the route middleware that are assigned to each route will not be displayed in the `route:list` output; however, you can instruct Laravel to display the route middleware and middleware group names by adding the `-v` option to the command:

```
1php artisan route:list -v

2 

3# Expand middleware groups...

4php artisan route:list -vv
```

You may also instruct Laravel to only show routes that begin with a given URI:

```
1php artisan route:list --path=api
```

In addition, you may instruct Laravel to hide any routes that are defined by third-party packages by providing the `--except-vendor` option when executing the `route:list` command:

```
1php artisan route:list --except-vendor
```

Likewise, you may also instruct Laravel to only show routes that are defined by third-party packages by providing the `--only-vendor` option when executing the `route:list` command:

```
1php artisan route:list --only-vendor
```

### [Routing Customization](#routing-customization)

By default, your application's routes are configured and loaded by the `bootstrap/app.php` file:

```
 1<?php

 2 

 3use Illuminate\Foundation\Application;

 4 

 5return Application::configure(basePath: dirname(__DIR__))

 6    ->withRouting(

 7        web: __DIR__.'/../routes/web.php',

 8        commands: __DIR__.'/../routes/console.php',

 9        health: '/up',

10    )->create();
```

However, sometimes you may want to define an entirely new file to contain a subset of your application's routes. To accomplish this, you may provide a `then` closure to the `withRouting` method. Within this closure, you may register any additional routes that are necessary for your application:

```
 1use Illuminate\Support\Facades\Route;

 2 

 3->withRouting(

 4    web: __DIR__.'/../routes/web.php',

 5    commands: __DIR__.'/../routes/console.php',

 6    health: '/up',

 7    then: function () {

 8        Route::middleware('api')

 9            ->prefix('webhooks')

10            ->name('webhooks.')

11            ->group(base_path('routes/webhooks.php'));

12    },

13)
```

Or, you may even take complete control over route registration by providing a `using` closure to the `withRouting` method. When this argument is passed, no HTTP routes will be registered by the framework and you are responsible for manually registering all routes:

```
 1use Illuminate\Support\Facades\Route;

 2 

 3->withRouting(

 4    commands: __DIR__.'/../routes/console.php',

 5    using: function () {

 6        Route::middleware('api')

 7            ->prefix('api')

 8            ->group(base_path('routes/api.php'));

 9 

10        Route::middleware('web')

11            ->group(base_path('routes/web.php'));

12    },

13)
```

## [Route Parameters](#route-parameters)

### [Required Parameters](#required-parameters)

Sometimes you will need to capture segments of the URI within your route. For example, you may need to capture a user's ID from the URL. You may do so by defining route parameters:

```
1Route::get('/user/{id}', function (string $id) {

2    return 'User '.$id;

3});
```

You may define as many route parameters as required by your route:

```
1Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {

2    // ...

3});
```

Route parameters are always encased within `{}` braces and should consist of alphabetic characters. Underscores (`_`) are also acceptable within route parameter names. Route parameters are injected into route callbacks / controllers based on their order - the names of the route callback / controller arguments do not matter.

#### [Parameters and Dependency Injection](#parameters-and-dependency-injection)

If your route has dependencies that you would like the Laravel service container to automatically inject into your route's callback, you should list your route parameters after your dependencies:

```
1use Illuminate\Http\Request;

2 

3Route::get('/user/{id}', function (Request $request, string $id) {

4    return 'User '.$id;

5});
```

### [Optional Parameters](#parameters-optional-parameters)

Occasionally you may need to specify a route parameter that may not always be present in the URI. You may do so by placing a `?` mark after the parameter name. Make sure to give the route's corresponding variable a default value:

```
1Route::get('/user/{name?}', function (?string $name = null) {

2    return $name;

3});

4 

5Route::get('/user/{name?}', function (?string $name = 'John') {

6    return $name;

7});
```

### [Regular Expression Constraints](#parameters-regular-expression-constraints)

You may constrain the format of your route parameters using the `where` method on a route instance. The `where` method accepts the name of the parameter and a regular expression defining how the parameter should be constrained:

```
 1Route::get('/user/{name}', function (string $name) {

 2    // ...

 3})->where('name', '[A-Za-z]+');

 4 

 5Route::get('/user/{id}', function (string $id) {

 6    // ...

 7})->where('id', '[0-9]+');

 8 

 9Route::get('/user/{id}/{name}', function (string $id, string $name) {

10    // ...

11})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

For convenience, some commonly used regular expression patterns have helper methods that allow you to quickly add pattern constraints to your routes:

```
 1Route::get('/user/{id}/{name}', function (string $id, string $name) {

 2    // ...

 3})->whereNumber('id')->whereAlpha('name');

 4 

 5Route::get('/user/{name}', function (string $name) {

 6    // ...

 7})->whereAlphaNumeric('name');

 8 

 9Route::get('/user/{id}', function (string $id) {

10    // ...

11})->whereUuid('id');

12 

13Route::get('/user/{id}', function (string $id) {

14    // ...

15})->whereUlid('id');

16 

17Route::get('/category/{category}', function (string $category) {

18    // ...

19})->whereIn('category', ['movie', 'song', 'painting']);

20 

21Route::get('/category/{category}', function (string $category) {

22    // ...

23})->whereIn('category', CategoryEnum::cases());
```

If the incoming request does not match the route pattern constraints, a 404 HTTP response will be returned.

#### [Global Constraints](#parameters-global-constraints)

If you would like a route parameter to always be constrained by a given regular expression, you may use the `pattern` method. You should define these patterns in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
1use Illuminate\Support\Facades\Route;

2 

3/**

4 * Bootstrap any application services.

5 */

6public function boot(): void

7{

8    Route::pattern('id', '[0-9]+');

9}
```

Once the pattern has been defined, it is automatically applied to all routes using that parameter name:

```
1Route::get('/user/{id}', function (string $id) {

2    // Only executed if {id} is numeric...

3});
```

#### [Encoded Forward Slashes](#parameters-encoded-forward-slashes)

The Laravel routing component allows all characters except `/` to be present within route parameter values. You must explicitly allow `/` to be part of your placeholder using a `where` condition regular expression:

```
1Route::get('/search/{search}', function (string $search) {

2    return $search;

3})->where('search', '.*');
```

Encoded forward slashes are only supported within the last route segment.

## [Named Routes](#named-routes)

Named routes allow the convenient generation of URLs or redirects for specific routes. You may specify a name for a route by chaining the `name` method onto the route definition:

```
1Route::get('/user/profile', function () {

2    // ...

3})->name('profile');
```

You may also specify route names for controller actions:

```
1Route::get(

2    '/user/profile',

3    [UserProfileController::class, 'show']

4)->name('profile');
```

Route names should always be unique.

#### [Generating URLs to Named Routes](#generating-urls-to-named-routes)

Once you have assigned a name to a given route, you may use the route's name when generating URLs or redirects via Laravel's `route` and `redirect` helper functions:

```
1// Generating URLs...

2$url = route('profile');

3 

4// Generating Redirects...

5return redirect()->route('profile');

6 

7return to_route('profile');
```

If the named route defines parameters, you may pass the parameters as the second argument to the `route` function. The given parameters will automatically be inserted into the generated URL in their correct positions:

```
1Route::get('/user/{id}/profile', function (string $id) {

2    // ...

3})->name('profile');

4 

5$url = route('profile', ['id' => 1]);
```

If you pass additional parameters in the array, those key / value pairs will automatically be added to the generated URL's query string:

```
1Route::get('/user/{id}/profile', function (string $id) {

2    // ...

3})->name('profile');

4 

5$url = route('profile', ['id' => 1, 'photos' => 'yes']);

6 

7// http://example.com/user/1/profile?photos=yes
```

Sometimes, you may wish to specify request-wide default values for URL parameters, such as the current locale. To accomplish this, you may use the [URL::defaults method](/docs/13.x/urls#default-values).

#### [Inspecting the Current Route](#inspecting-the-current-route)

If you would like to determine if the current request was routed to a given named route, you may use the `named` method on a Route instance. For example, you may check the current route name from a route middleware:

```
 1use Closure;

 2use Illuminate\Http\Request;

 3use Symfony\Component\HttpFoundation\Response;

 4 

 5/**

 6 * Handle an incoming request.

 7 *

 8 * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next

 9 */

10public function handle(Request $request, Closure $next): Response

11{

12    if ($request->route()->named('profile')) {

13        // ...

14    }

15 

16    return $next($request);

17}
```

## [Route Groups](#route-groups)

Route groups allow you to share route attributes, such as middleware, across a large number of routes without needing to define those attributes on each individual route.

Nested groups attempt to intelligently "merge" attributes with their parent group. Middleware and `where` conditions are merged while names and prefixes are appended. Namespace delimiters and slashes in URI prefixes are automatically added where appropriate.

### [Middleware](#route-group-middleware)

To assign [middleware](/docs/13.x/middleware) to all routes within a group, you may use the `middleware` method before defining the group. Middleware are executed in the order they are listed in the array:

```
1Route::middleware(['first', 'second'])->group(function () {

2    Route::get('/', function () {

3        // Uses first & second middleware...

4    });

5 

6    Route::get('/user/profile', function () {

7        // Uses first & second middleware...

8    });

9});
```

### [Controllers](#route-group-controllers)

If a group of routes all utilize the same [controller](/docs/13.x/controllers), you may use the `controller` method to define the common controller for all of the routes within the group. Then, when defining the routes, you only need to provide the controller method that they invoke:

```
1use App\Http\Controllers\OrderController;

2 

3Route::controller(OrderController::class)->group(function () {

4    Route::get('/orders/{id}', 'show');

5    Route::post('/orders', 'store');

6});
```

### [Subdomain Routing](#route-group-subdomain-routing)

Route groups may also be used to handle subdomain routing. Subdomains may be assigned route parameters just like route URIs, allowing you to capture a portion of the subdomain for usage in your route or controller. The subdomain may be specified by calling the `domain` method before defining the group:

```
1Route::domain('{account}.example.com')->group(function () {

2    Route::get('/user/{id}', function (string $account, string $id) {

3        // ...

4    });

5});
```

### [Route Prefixes](#route-group-prefixes)

The `prefix` method may be used to prefix each route in the group with a given URI. For example, you may want to prefix all route URIs within the group with `admin`:

```
1Route::prefix('admin')->group(function () {

2    Route::get('/users', function () {

3        // Matches The "/admin/users" URL

4    });

5});
```

### [Route Name Prefixes](#route-group-name-prefixes)

The `name` method may be used to prefix each route name in the group with a given string. For example, you may want to prefix the names of all of the routes in the group with `admin`. The given string is prefixed to the route name exactly as it is specified, so we will be sure to provide the trailing `.` character in the prefix:

```
1Route::name('admin.')->group(function () {

2    Route::get('/users', function () {

3        // Route assigned name "admin.users"...

4    })->name('users');

5});
```

## [Route Model Binding](#route-model-binding)

When injecting a model ID to a route or controller action, you will often query the database to retrieve the model that corresponds to that ID. Laravel route model binding provides a convenient way to automatically inject the model instances directly into your routes. For example, instead of injecting a user's ID, you can inject the entire `User` model instance that matches the given ID.

### [Implicit Binding](#implicit-binding)

Laravel automatically resolves Eloquent models defined in routes or controller actions whose type-hinted variable names match a route segment name. For example:

```
1use App\Models\User;

2 

3Route::get('/users/{user}', function (User $user) {

4    return $user->email;

5});
```

Since the `$user` variable is type-hinted as the `App\Models\User` Eloquent model and the variable name matches the `{user}` URI segment, Laravel will automatically inject the model instance that has an ID matching the corresponding value from the request URI. If a matching model instance is not found in the database, a 404 HTTP response will automatically be generated.

Of course, implicit binding is also possible when using controller methods. Again, note the `{user}` URI segment matches the `$user` variable in the controller which contains an `App\Models\User` type-hint:

```
 1use App\Http\Controllers\UserController;

 2use App\Models\User;

 3 

 4// Route definition...

 5Route::get('/users/{user}', [UserController::class, 'show']);

 6 

 7// Controller method definition...

 8public function show(User $user)

 9{

10    return view('user.profile', ['user' => $user]);

11}
```

#### [Soft Deleted Models](#implicit-soft-deleted-models)

Typically, implicit model binding will not retrieve models that have been [soft deleted](/docs/13.x/eloquent#soft-deleting). However, you may instruct the implicit binding to retrieve these models by chaining the `withTrashed` method onto your route's definition:

```
1use App\Models\User;

2 

3Route::get('/users/{user}', function (User $user) {

4    return $user->email;

5})->withTrashed();
```

#### [Customizing the Key](#customizing-the-default-key-name)

Sometimes you may wish to resolve Eloquent models using a column other than `id`. To do so, you may specify the column in the route parameter definition:

```
1use App\Models\Post;

2 

3Route::get('/posts/{post:slug}', function (Post $post) {

4    return $post;

5});
```

If you would like model binding to always use a database column other than `id` when retrieving a given model class, you may apply the `RouteKey` attribute to the Eloquent model:

```
1use Illuminate\Database\Eloquent\Attributes\RouteKey;

2use Illuminate\Database\Eloquent\Model;

3 

4#[RouteKey('slug')]

5class Post extends Model

6{

7    // ...

8}
```

#### [Custom Keys and Scoping](#implicit-model-binding-scoping)

When implicitly binding multiple Eloquent models in a single route definition, you may wish to scope the second Eloquent model such that it must be a child of the previous Eloquent model. For example, consider this route definition that retrieves a blog post by slug for a specific user:

```
1use App\Models\Post;

2use App\Models\User;

3 

4Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {

5    return $post;

6});
```

When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `User` model has a relationship named `posts` (the plural form of the route parameter name) which can be used to retrieve the `Post` model.

If you wish, you may instruct Laravel to scope "child" bindings even when a custom key is not provided. To do so, you may invoke the `scopeBindings` method when defining your route:

```
1use App\Models\Post;

2use App\Models\User;

3 

4Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {

5    return $post;

6})->scopeBindings();
```

Or, you may instruct an entire group of route definitions to use scoped bindings:

```
1Route::scopeBindings()->group(function () {

2    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {

3        return $post;

4    });

5});
```

Similarly, you may explicitly instruct Laravel to not scope bindings by invoking the `withoutScopedBindings` method:

```
1Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {

2    return $post;

3})->withoutScopedBindings();
```

#### [Customizing Missing Model Behavior](#customizing-missing-model-behavior)

Typically, a 404 HTTP response will be generated if an implicitly bound model is not found. However, you may customize this behavior by calling the `missing` method when defining your route. The `missing` method accepts a closure that will be invoked if an implicitly bound model cannot be found:

```
1use App\Http\Controllers\LocationsController;

2use Illuminate\Http\Request;

3use Illuminate\Support\Facades\Redirect;

4 

5Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])

6    ->name('locations.view')

7    ->missing(function (Request $request) {

8        return Redirect::route('locations.index');

9    });
```

### [Implicit Enum Binding](#implicit-enum-binding)

PHP 8.1 introduced support for [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To complement this feature, Laravel allows you to type-hint a [string-backed Enum](https://www.php.net/manual/en/language.enumerations.backed.php) on your route definition and Laravel will only invoke the route if that route segment corresponds to a valid Enum value. Otherwise, a 404 HTTP response will be returned automatically. For example, given the following Enum:

```
1<?php

2 

3namespace App\Enums;

4 

5enum Category: string

6{

7    case Fruits = 'fruits';

8    case People = 'people';

9}
```

You may define a route that will only be invoked if the `{category}` route segment is `fruits` or `people`. Otherwise, Laravel will return a 404 HTTP response:

```
1use App\Enums\Category;

2use Illuminate\Support\Facades\Route;

3 

4Route::get('/categories/{category}', function (Category $category) {

5    return $category->value;

6});
```

### [Explicit Binding](#explicit-binding)

You are not required to use Laravel's implicit, convention based model resolution in order to use model binding. You can also explicitly define how route parameters correspond to models. To register an explicit binding, use the router's `model` method to specify the class for a given parameter. You should define your explicit model bindings at the beginning of the `boot` method of your `AppServiceProvider` class:

```
 1use App\Models\User;

 2use Illuminate\Support\Facades\Route;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Route::model('user', User::class);

10}
```

Next, define a route that contains a `{user}` parameter:

```
1use App\Models\User;

2 

3Route::get('/users/{user}', function (User $user) {

4    // ...

5});
```

Since we have bound all `{user}` parameters to the `App\Models\User` model, an instance of that class will be injected into the route. So, for example, a request to `users/1` will inject the `User` instance from the database which has an ID of `1`.

If a matching model instance is not found in the database, a 404 HTTP response will be automatically generated.

#### [Customizing the Resolution Logic](#customizing-the-resolution-logic)

If you wish to define your own model binding resolution logic, you may use the `Route::bind` method. The closure you pass to the `bind` method will receive the value of the URI segment and should return the instance of the class that should be injected into the route. Again, this customization should take place in the `boot` method of your application's `AppServiceProvider`:

```
 1use App\Models\User;

 2use Illuminate\Support\Facades\Route;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Route::bind('user', function (string $value) {

10        return User::where('name', $value)->firstOrFail();

11    });

12}
```

Alternatively, you may override the `resolveRouteBinding` method on your Eloquent model. This method will receive the value of the URI segment and should return the instance of the class that should be injected into the route:

```
 1/**

 2 * Retrieve the model for a bound value.

 3 *

 4 * @param  mixed  $value

 5 * @param  string|null  $field

 6 * @return \Illuminate\Database\Eloquent\Model|null

 7 */

 8public function resolveRouteBinding($value, $field = null)

 9{

10    return $this->where('name', $value)->firstOrFail();

11}
```

If a route is utilizing [implicit binding scoping](#implicit-model-binding-scoping), the `resolveChildRouteBinding` method will be used to resolve the child binding of the parent model:

```
 1/**

 2 * Retrieve the child model for a bound value.

 3 *

 4 * @param  string  $childType

 5 * @param  mixed  $value

 6 * @param  string|null  $field

 7 * @return \Illuminate\Database\Eloquent\Model|null

 8 */

 9public function resolveChildRouteBinding($childType, $value, $field)

10{

11    return parent::resolveChildRouteBinding($childType, $value, $field);

12}
```

## [Fallback Routes](#fallback-routes)

Using the `Route::fallback` method, you may define a route that will be executed when no other route matches the incoming request. Typically, unhandled requests will automatically render a "404" page via your application's exception handler. However, since you would typically define the `fallback` route within your `routes/web.php` file, all middleware in the `web` middleware group will apply to the route. You are free to add additional middleware to this route as needed:

```
1Route::fallback(function () {

2    // ...

3});
```

## [Rate Limiting](#rate-limiting)

### [Defining Rate Limiters](#defining-rate-limiters)

Laravel includes powerful and customizable rate limiting services that you may utilize to restrict the amount of traffic for a given route or group of routes. To get started, you should define rate limiter configurations that meet your application's needs.

Rate limiters may be defined within the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use Illuminate\Cache\RateLimiting\Limit;

 2use Illuminate\Http\Request;

 3use Illuminate\Support\Facades\RateLimiter;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    RateLimiter::for('api', function (Request $request) {

11        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());

12    });

13}
```

Rate limiters are defined using the `RateLimiter` facade's `for` method. The `for` method accepts a rate limiter name and a closure that returns the limit configuration that should apply to routes that are assigned to the rate limiter. Limit configuration are instances of the `Illuminate\Cache\RateLimiting\Limit` class. This class contains helpful "builder" methods so that you can quickly define your limit. The rate limiter name may be any string you wish:

```
 1use Illuminate\Cache\RateLimiting\Limit;

 2use Illuminate\Http\Request;

 3use Illuminate\Support\Facades\RateLimiter;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    RateLimiter::for('global', function (Request $request) {

11        return Limit::perMinute(1000);

12    });

13}
```

If the incoming request exceeds the specified rate limit, a response with a 429 HTTP status code will automatically be returned by Laravel. If you would like to define your own response that should be returned by a rate limit, you may use the `response` method:

```
1RateLimiter::for('global', function (Request $request) {

2    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {

3        return response('Custom response...', 429, $headers);

4    });

5});
```

Since rate limiter callbacks receive the incoming HTTP request instance, you may build the appropriate rate limit dynamically based on the incoming request or authenticated user:

```
1RateLimiter::for('uploads', function (Request $request) {

2    return $request->user()?->vipCustomer()

3        ? Limit::none()

4        : Limit::perHour(10);

5});
```

#### [Segmenting Rate Limits](#segmenting-rate-limits)

Sometimes you may wish to segment rate limits by some arbitrary value. For example, you may wish to allow users to access a given route 100 times per minute per IP address. To accomplish this, you may use the `by` method when building your rate limit:

```
1RateLimiter::for('uploads', function (Request $request) {

2    return $request->user()->vipCustomer()

3        ? Limit::none()

4        : Limit::perMinute(100)->by($request->ip());

5});
```

To illustrate this feature using another example, we can limit access to the route to 100 times per minute per authenticated user ID or 10 times per minute per IP address for guests:

```
1RateLimiter::for('uploads', function (Request $request) {

2    return $request->user()

3        ? Limit::perMinute(100)->by($request->user()->id)

4        : Limit::perMinute(10)->by($request->ip());

5});
```

#### [Multiple Rate Limits](#multiple-rate-limits)

If needed, you may return an array of rate limits for a given rate limiter configuration. Each rate limit will be evaluated for the route based on the order they are placed within the array:

```
1RateLimiter::for('login', function (Request $request) {

2    return [

3        Limit::perMinute(500),

4        Limit::perMinute(3)->by($request->input('email')),

5    ];

6});
```

If you're assigning multiple rate limits segmented by identical `by` values, you should ensure that each `by` value is unique. The easiest way to achieve this is to prefix the values given to the `by` method:

```
1RateLimiter::for('uploads', function (Request $request) {

2    return [

3        Limit::perMinute(10)->by('minute:'.$request->user()->id),

4        Limit::perDay(1000)->by('day:'.$request->user()->id),

5    ];

6});
```

#### [Response-Based Rate Limiting](#response-base-rate-limiting)

In addition to rate limiting incoming requests, Laravel allows you to rate limit based on the response using the `after` method. This is useful when you only want to count certain responses toward the rate limit, such as validation errors, 404 responses, or other specific HTTP status codes.

The `after` method accepts a closure that receives the response and should return `true` if the response should be counted toward the rate limit, or `false` if it should be ignored. This is particularly useful for preventing enumeration attacks by limiting consecutive 404 responses, or allowing users to retry requests that fail validation without exhausting their rate limit on an endpoint that should only throttle successful operations:

```
 1use Illuminate\Cache\RateLimiting\Limit;

 2use Illuminate\Http\Request;

 3use Illuminate\Support\Facades\RateLimiter;

 4use Symfony\Component\HttpFoundation\Response;

 5 

 6RateLimiter::for('resource-not-found', function (Request $request) {

 7    return Limit::perMinute(10)

 8        ->by($request->user()?->id ?: $request->ip())

 9        ->after(function (Response $response) {

10            // Only count 404 responses toward the rate limit to prevent enumeration...

11            return $response->status() === 404;

12        });

13});
```

### [Attaching Rate Limiters to Routes](#attaching-rate-limiters-to-routes)

Rate limiters may be attached to routes or route groups using the `throttle` [middleware](/docs/13.x/middleware). The throttle middleware accepts the name of the rate limiter you wish to assign to the route:

```
1Route::middleware(['throttle:uploads'])->group(function () {

2    Route::post('/audio', function () {

3        // ...

4    });

5 

6    Route::post('/video', function () {

7        // ...

8    });

9});
```

#### [Throttling With Redis](#throttling-with-redis)

By default, the `throttle` middleware is mapped to the `Illuminate\Routing\Middleware\ThrottleRequests` class. However, if you are using Redis as your application's cache driver, you may wish to instruct Laravel to use Redis to manage rate limiting. To do so, you should use the `throttleWithRedis` method in your application's `bootstrap/app.php` file. This method maps the `throttle` middleware to the `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` middleware class:

```
1->withMiddleware(function (Middleware $middleware): void {

2    $middleware->throttleWithRedis();

3    // ...

4})
```

## [Form Method Spoofing](#form-method-spoofing)

HTML forms do not support `PUT`, `PATCH`, or `DELETE` actions. So, when defining `PUT`, `PATCH`, or `DELETE` routes that are called from an HTML form, you will need to add a hidden `_method` field to the form. The value sent with the `_method` field will be used as the HTTP request method:

```
1<form action="/example" method="POST">

2    <input type="hidden" name="_method" value="PUT">

3    <input type="hidden" name="_token" value="{{ csrf_token() }}">

4</form>
```

For convenience, you may use the `@method` [Blade directive](/docs/13.x/blade) to generate the `_method` input field:

```
1<form action="/example" method="POST">

2    @method('PUT')

3    @csrf

4</form>
```

## [Accessing the Current Route](#accessing-the-current-route)

You may use the `current`, `currentRouteName`, and `currentRouteAction` methods on the `Route` facade to access information about the route handling the incoming request:

```
1use Illuminate\Support\Facades\Route;

2 

3$route = Route::current(); // Illuminate\Routing\Route

4$name = Route::currentRouteName(); // string

5$action = Route::currentRouteAction(); // string
```

You may refer to the API documentation for both the [underlying class of the Route facade](https://api.laravel.com/docs/13.x/Illuminate/Routing/Router.html) and [Route instance](https://api.laravel.com/docs/13.x/Illuminate/Routing/Route.html) to review all of the methods that are available on the router and route classes.

## [Cross-Origin Resource Sharing (CORS)](#cors)

Laravel can automatically respond to CORS `OPTIONS` HTTP requests with values that you configure. The `OPTIONS` requests will automatically be handled by the `HandleCors` [middleware](/docs/13.x/middleware) that is automatically included in your application's global middleware stack.

Sometimes, you may need to customize the CORS configuration values for your application. You may do so by publishing the `cors` configuration file using the `config:publish` Artisan command:

```
1php artisan config:publish cors
```

This command will place a `cors.php` configuration file within your application's `config` directory.

For more information on CORS and CORS headers, please consult the [MDN web documentation on CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers).

## [Route Caching](#route-caching)

When deploying your application to production, you should take advantage of Laravel's route cache. Using the route cache will drastically decrease the amount of time it takes to register all of your application's routes. To generate a route cache, execute the `route:cache` Artisan command:

```
1php artisan route:cache
```

After running this command, your cached routes file will be loaded on every request. Remember, if you add any new routes you will need to generate a fresh route cache. Because of this, you should only run the `route:cache` command during your project's deployment.

You may use the `route:clear` command to clear the route cache:

```
1php artisan route:clear
```
