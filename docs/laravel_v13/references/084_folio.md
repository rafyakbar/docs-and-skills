# Laravel Folio

- [Introduction](#introduction)
- [Installation](#installation)
  * [Page Paths / URIs](#page-paths-uris)
  * [Subdomain Routing](#subdomain-routing)
- [Creating Routes](#creating-routes)
  * [Nested Routes](#nested-routes)
  * [Index Routes](#index-routes)
- [Route Parameters](#route-parameters)
- [Route Model Binding](#route-model-binding)
  * [Soft Deleted Models](#soft-deleted-models)
- [Render Hooks](#render-hooks)
- [Named Routes](#named-routes)
- [Middleware](#middleware)
- [Route Caching](#route-caching)

## [Introduction](#introduction)

[Laravel Folio](https://github.com/laravel/folio) is a powerful page based router designed to simplify routing in Laravel applications. With Laravel Folio, generating a route becomes as effortless as creating a Blade template within your application's `resources/views/pages` directory.

For example, to create a page that is accessible at the `/greeting` URL, just create a `greeting.blade.php` file in your application's `resources/views/pages` directory:

```
1<div>

2    Hello World

3</div>
```

## [Installation](#installation)

To get started, install Folio into your project using the Composer package manager:

```
1composer require laravel/folio
```

After installing Folio, you may execute the `folio:install` Artisan command, which will install Folio's service provider into your application. This service provider registers the directory where Folio will search for routes / pages:

```
1php artisan folio:install
```

### [Page Paths / URIs](#page-paths-uris)

By default, Folio serves pages from your application's `resources/views/pages` directory, but you may customize these directories in your Folio service provider's `boot` method.

For example, sometimes it may be convenient to specify multiple Folio paths in the same Laravel application. You may wish to have a separate directory of Folio pages for your application's "admin" area, while using another directory for the rest of your application's pages.

You may accomplish this using the `Folio::path` and `Folio::uri` methods. The `path` method registers a directory that Folio will scan for pages when routing incoming HTTP requests, while the `uri` method specifies the "base URI" for that directory of pages:

```
 1use Laravel\Folio\Folio;

 2 

 3Folio::path(resource_path('views/pages/guest'))->uri('/');

 4 

 5Folio::path(resource_path('views/pages/admin'))

 6    ->uri('/admin')

 7    ->middleware([

 8        '*' => [

 9            'auth',

10            'verified',

11 

12            // ...

13        ],

14    ]);
```

### [Subdomain Routing](#subdomain-routing)

You may also route to pages based on the incoming request's subdomain. For example, you may wish to route requests from `admin.example.com` to a different page directory than the rest of your Folio pages. You may accomplish this by invoking the `domain` method after invoking the `Folio::path` method:

```
1use Laravel\Folio\Folio;

2 

3Folio::domain('admin.example.com')

4    ->path(resource_path('views/pages/admin'));
```

The `domain` method also allows you to capture parts of the domain or subdomain as parameters. These parameters will be injected into your page template:

```
1use Laravel\Folio\Folio;

2 

3Folio::domain('{account}.example.com')

4    ->path(resource_path('views/pages/admin'));
```

## [Creating Routes](#creating-routes)

You may create a Folio route by placing a Blade template in any of your Folio mounted directories. By default, Folio mounts the `resources/views/pages` directory, but you may customize these directories in your Folio service provider's `boot` method.

Once a Blade template has been placed in a Folio mounted directory, you may immediately access it via your browser. For example, a page placed in `pages/schedule.blade.php` may be accessed in your browser at `http://example.com/schedule`.

To quickly view a list of all of your Folio pages / routes, you may invoke the `folio:list` Artisan command:

```
1php artisan folio:list
```

### [Nested Routes](#nested-routes)

You may create a nested route by creating one or more directories within one of Folio's directories. For instance, to create a page that is accessible via `/user/profile`, create a `profile.blade.php` template within the `pages/user` directory:

```
1php artisan folio:page user/profile

2 

3# pages/user/profile.blade.php → /user/profile
```

### [Index Routes](#index-routes)

Sometimes, you may wish to make a given page the "index" of a directory. By placing an `index.blade.php` template within a Folio directory, any requests to the root of that directory will be routed to that page:

```
1php artisan folio:page index

2# pages/index.blade.php → /

3 

4php artisan folio:page users/index

5# pages/users/index.blade.php → /users
```

## [Route Parameters](#route-parameters)

Often, you will need to have segments of the incoming request's URL injected into your page so that you can interact with them. For example, you may need to access the "ID" of the user whose profile is being displayed. To accomplish this, you may encapsulate a segment of the page's filename in square brackets:

```
1php artisan folio:page "users/[id]"

2 

3# pages/users/[id].blade.php → /users/1
```

Captured segments can be accessed as variables within your Blade template:

```
1<div>

2    User {{ $id }}

3</div>
```

To capture multiple segments, you can prefix the encapsulated segment with three dots `...`:

```
1php artisan folio:page "users/[...ids]"

2 

3# pages/users/[...ids].blade.php → /users/1/2/3
```

When capturing multiple segments, the captured segments will be injected into the page as an array:

```
1<ul>

2    @foreach ($ids as $id)

3        <li>User {{ $id }}</li>

4    @endforeach

5</ul>
```

## [Route Model Binding](#route-model-binding)

If a wildcard segment of your page template's filename corresponds one of your application's Eloquent models, Folio will automatically take advantage of Laravel's route model binding capabilities and attempt to inject the resolved model instance into your page:

```
1php artisan folio:page "users/[User]"

2 

3# pages/users/[User].blade.php → /users/1
```

Captured models can be accessed as variables within your Blade template. The model's variable name will be converted to "camel case":

```
1<div>

2    User {{ $user->id }}

3</div>
```

#### Customizing the Key

Sometimes you may wish to resolve bound Eloquent models using a column other than `id`. To do so, you may specify the column in the page's filename. For example, a page with the filename `[Post:slug].blade.php` will attempt to resolve the bound model via the `slug` column instead of the `id` column.

On Windows, you should use `-` to separate the model name from the key: `[Post-slug].blade.php`.

#### Model Location

By default, Folio will search for your model within your application's `app/Models` directory. However, if needed, you may specify the fully-qualified model class name in your template's filename:

```
1php artisan folio:page "users/[.App.Models.User]"

2 

3# pages/users/[.App.Models.User].blade.php → /users/1
```

### [Soft Deleted Models](#soft-deleted-models)

By default, models that have been soft deleted are not retrieved when resolving implicit model bindings. However, if you wish, you can instruct Folio to retrieve soft deleted models by invoking the `withTrashed` function within the page's template:

```
 1<?php

 2 

 3use function Laravel\Folio\{withTrashed};

 4 

 5withTrashed();

 6 

 7?>

 8 

 9<div>

10    User {{ $user->id }}

11</div>
```

## [Render Hooks](#render-hooks)

By default, Folio will return the content of the page's Blade template as the response to the incoming request. However, you may customize the response by invoking the `render` function within the page's template.

The `render` function accepts a closure which will receive the `View` instance being rendered by Folio, allowing you to add additional data to the view or customize the entire response. In addition to receiving the `View` instance, any additional route parameters or model bindings will also be provided to the `render` closure:

```
 1<?php

 2 

 3use App\Models\Post;

 4use Illuminate\Support\Facades\Auth;

 5use Illuminate\View\View;

 6 

 7use function Laravel\Folio\render;

 8 

 9render(function (View $view, Post $post) {

10    if (! Auth::user()->can('view', $post)) {

11        return response('Unauthorized', 403);

12    }

13 

14    return $view->with('photos', $post->author->photos);

15}); ?>

16 

17<div>

18    {{ $post->content }}

19</div>

20 

21<div>

22    This author has also taken {{ count($photos) }} photos.

23</div>
```

## [Named Routes](#named-routes)

You may specify a name for a given page's route using the `name` function:

```
1<?php

2 

3use function Laravel\Folio\name;

4 

5name('users.index');
```

Just like Laravel's named routes, you may use the `route` function to generate URLs to Folio pages that have been assigned a name:

```
1<a href="{{ route('users.index') }}">

2    All Users

3</a>
```

If the page has parameters, you may simply pass their values to the `route` function:

```
1route('users.show', ['user' => $user]);
```

## [Middleware](#middleware)

You can apply middleware to a specific page by invoking the `middleware` function within the page's template:

```
 1<?php

 2 

 3use function Laravel\Folio\{middleware};

 4 

 5middleware(['auth', 'verified']);

 6 

 7?>

 8 

 9<div>

10    Dashboard

11</div>
```

Or, to assign middleware to a group of pages, you may chain the `middleware` method after invoking the `Folio::path` method.

To specify which pages the middleware should be applied to, the array of middleware may be keyed using the corresponding URL patterns of the pages they should be applied to. The `*` character may be utilized as a wildcard character:

```
 1use Laravel\Folio\Folio;

 2 

 3Folio::path(resource_path('views/pages'))->middleware([

 4    'admin/*' => [

 5        'auth',

 6        'verified',

 7 

 8        // ...

 9    ],

10]);
```

You may include closures in the array of middleware to define inline, anonymous middleware:

```
 1use Closure;

 2use Illuminate\Http\Request;

 3use Laravel\Folio\Folio;

 4 

 5Folio::path(resource_path('views/pages'))->middleware([

 6    'admin/*' => [

 7        'auth',

 8        'verified',

 9 

10        function (Request $request, Closure $next) {

11            // ...

12 

13            return $next($request);

14        },

15    ],

16]);
```

## [Route Caching](#route-caching)

When using Folio, you should always take advantage of [Laravel's route caching capabilities](/docs/13.x/routing#route-caching). Folio listens for the `route:cache` Artisan command to ensure that Folio page definitions and route names are properly cached for maximum performance.
