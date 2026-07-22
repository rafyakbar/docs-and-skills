# Package Development

- [Introduction](#introduction)
  * [Creating a Package](#creating-a-package)
  * [A Note on Facades](#a-note-on-facades)
- [Package Discovery](#package-discovery)
- [Service Providers](#service-providers)
- [Resources](#resources)
  * [Configuration](#configuration)
  * [Routes](#routes)
  * [Migrations](#migrations)
  * [Language Files](#language-files)
  * [Views](#views)
  * [View Components](#view-components)
  * ["About" Artisan Command](#about-artisan-command)
- [Commands](#commands)
  * [Optimize Commands](#optimize-commands)
  * [Reload Commands](#reload-commands)
- [Public Assets](#public-assets)
- [Publishing File Groups](#publishing-file-groups)

## [Introduction](#introduction)

Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like [Carbon](https://github.com/briannesbitt/Carbon) or a package that allows you to associate files with Eloquent models like Spatie's [Laravel Media Library](https://github.com/spatie/laravel-medialibrary).

There are different types of packages. Some packages are stand-alone, meaning they work with any PHP framework. Carbon and Pest are examples of stand-alone packages. Any of these packages may be used with Laravel by requiring them in your `composer.json` file.

On the other hand, other packages are specifically intended for use with Laravel. These packages may have routes, controllers, views, and configuration specifically intended to enhance a Laravel application. This guide primarily covers the development of those packages that are Laravel specific.

### [Creating a Package](#creating-a-package)

The easiest way to start building a new Laravel package is the official [Laravel package skeleton](https://github.com/laravel/package-skeleton). The skeleton provides everything you need to build a Laravel package, including a service provider, testing via Pest, static analysis via Larastan, code formatting via Pint, and a workbench application for end-to-end package development. You can create a new package using the `package` command of the [Laravel installer CLI](/docs/13.x/installation#creating-a-laravel-project):

```
1laravel package my-package
```

An interactive configuration script will personalize the skeleton for your package, setting up your namespace, service provider, and only the features you need, such as configuration files, routes, views, translations, migrations, assets, commands, and a facade.

### [A Note on Facades](#a-note-on-facades)

When writing a Laravel application, it generally does not matter if you use contracts or facades since both provide essentially equal levels of testability. However, when writing packages, your package will not typically have access to all of Laravel's testing helpers. If you would like to be able to write your package tests as if the package were installed inside a typical Laravel application, you may use the [Orchestral Testbench](https://github.com/orchestral/testbench) package.

## [Package Discovery](#package-discovery)

A Laravel application's `bootstrap/providers.php` file contains the list of service providers that should be loaded by Laravel. However, instead of requiring users to manually add your service provider to the list, you may define the provider in the `extra` section of your package's `composer.json` file so that it is automatically loaded by Laravel. In addition to service providers, you may also list any [facades](/docs/13.x/facades) you would like to be registered:

```
 1"extra": {

 2    "laravel": {

 3        "providers": [

 4            "Barryvdh\\Debugbar\\ServiceProvider"

 5        ],

 6        "aliases": {

 7            "Debugbar": "Barryvdh\\Debugbar\\Facade"

 8        }

 9    }

10},
```

Once your package has been configured for discovery, Laravel will automatically register its service providers and facades when it is installed, creating a convenient installation experience for your package's users.

#### [Opting Out of Package Discovery](#opting-out-of-package-discovery)

If you are the consumer of a package and would like to disable package discovery for a package, you may list the package name in the `extra` section of your application's `composer.json` file:

```
1"extra": {

2    "laravel": {

3        "dont-discover": [

4            "barryvdh/laravel-debugbar"

5        ]

6    }

7},
```

You may disable package discovery for all packages using the `*` character inside of your application's `dont-discover` directive:

```
1"extra": {

2    "laravel": {

3        "dont-discover": [

4            "*"

5        ]

6    }

7},
```

## [Service Providers](#service-providers)

[Service providers](/docs/13.x/providers) are the connection point between your package and Laravel. A service provider is responsible for binding things into Laravel's [service container](/docs/13.x/container) and informing Laravel where to load package resources such as views, configuration, and language files.

A service provider extends the `Illuminate\Support\ServiceProvider` class and contains two methods: `register` and `boot`. The base `ServiceProvider` class is located in the `illuminate/support` Composer package, which you should add to your own package's dependencies. To learn more about the structure and purpose of service providers, check out [their documentation](/docs/13.x/providers).

## [Resources](#resources)

### [Configuration](#configuration)

Typically, you will need to publish your package's configuration file to the application's `config` directory. This will allow users of your package to easily override your default configuration options. To allow your configuration files to be published, call the `publishes` method from the `boot` method of your service provider:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    $this->publishes([

7        __DIR__.'/../config/courier.php' => config_path('courier.php'),

8    ]);

9}
```

Now, when users of your package execute Laravel's `vendor:publish` command, your file will be copied to the specified publish location. Once your configuration has been published, its values may be accessed like any other configuration file:

```
1$value = config('courier.option');
```

You should not define closures in your configuration files. They cannot be serialized correctly when users execute the `config:cache` Artisan command.

#### [Default Package Configuration](#default-package-configuration)

You may also merge your own package configuration file with the application's published copy. This will allow your users to define only the options they actually want to override in the published copy of the configuration file. To merge the configuration file values, use the `mergeConfigFrom` method within your service provider's `register` method.

The `mergeConfigFrom` method accepts the path to your package's configuration file as its first argument and the name of the application's copy of the configuration file as its second argument:

```
1/**

2 * Register any package services.

3 */

4public function register(): void

5{

6    $this->mergeConfigFrom(

7        __DIR__.'/../config/courier.php', 'courier'

8    );

9}
```

This method only merges the first level of the configuration array. If your users partially define a multi-dimensional configuration array, the missing options will not be merged.

### [Routes](#routes)

If your package contains routes, you may load them using the `loadRoutesFrom` method. This method will automatically determine if the application's routes are cached and will not load your routes file if the routes have already been cached:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');

7}
```

### [Migrations](#migrations)

If your package contains [database migrations](/docs/13.x/migrations), you may use the `publishesMigrations` method to inform Laravel that the given directory or file contains migrations. When Laravel publishes the migrations, it will automatically update the timestamp within their filename to reflect the current date and time:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    $this->publishesMigrations([

7        __DIR__.'/../database/migrations' => database_path('migrations'),

8    ]);

9}
```

### [Language Files](#language-files)

If your package contains [language files](/docs/13.x/localization), you may use the `loadTranslationsFrom` method to inform Laravel how to load them. For example, if your package is named `courier`, you should add the following to your service provider's `boot` method:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

7}
```

Package translation lines are referenced using the `package::file.line` syntax convention. So, you may load the `courier` package's `welcome` line from the `messages` file like so:

```
1echo trans('courier::messages.welcome');
```

You can register JSON translation files for your package using the `loadJsonTranslationsFrom` method. This method accepts the path to the directory that contains your package's JSON translation files:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');

7}
```

#### [Publishing Language Files](#publishing-language-files)

If you would like to publish your package's language files to the application's `lang/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package paths and their desired publish locations. For example, to publish the language files for the `courier` package, you may do the following:

```
 1/**

 2 * Bootstrap any package services.

 3 */

 4public function boot(): void

 5{

 6    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

 7 

 8    $this->publishes([

 9        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),

10    ]);

11}
```

Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's language files will be published to the specified publish location.

### [Views](#views)

To register your package's [views](/docs/13.x/views) with Laravel, you need to tell Laravel where the views are located. You may do this using the service provider's `loadViewsFrom` method. The `loadViewsFrom` method accepts two arguments: the path to your view templates and your package's name. For example, if your package's name is `courier`, you would add the following to your service provider's `boot` method:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

7}
```

Package views are referenced using the `package::view` syntax convention. So, once your view path is registered in a service provider, you may load the `dashboard` view from the `courier` package like so:

```
1Route::get('/dashboard', function () {

2    return view('courier::dashboard');

3});
```

#### [Overriding Package Views](#overriding-package-views)

When you use the `loadViewsFrom` method, Laravel actually registers two locations for your views: the application's `resources/views/vendor` directory and the directory you specify. So, using the `courier` package as an example, Laravel will first check if a custom version of the view has been placed in the `resources/views/vendor/courier` directory by the developer. Then, if the view has not been customized, Laravel will search the package view directory you specified in your call to `loadViewsFrom`. This makes it easy for package users to customize / override your package's views.

#### [Publishing Views](#publishing-views)

If you would like to make your views available for publishing to the application's `resources/views/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package view paths and their desired publish locations:

```
 1/**

 2 * Bootstrap the package services.

 3 */

 4public function boot(): void

 5{

 6    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

 7 

 8    $this->publishes([

 9        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),

10    ]);

11}
```

Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's views will be copied to the specified publish location.

### [View Components](#view-components)

If you are building a package that utilizes Blade components or placing components in non-conventional directories, you will need to manually register your component class and its HTML tag alias so that Laravel knows where to find the component. You should typically register your components in the `boot` method of your package's service provider:

```
 1use Illuminate\Support\Facades\Blade;

 2use VendorPackage\View\Components\AlertComponent;

 3 

 4/**

 5 * Bootstrap your package's services.

 6 */

 7public function boot(): void

 8{

 9    Blade::component('package-alert', AlertComponent::class);

10}
```

Once your component has been registered, it may be rendered using its tag alias:

```
1<x-package-alert/>
```

#### [Autoloading Package Components](#autoloading-package-components)

Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Nightshade\Views\Components` namespace:

```
1use Illuminate\Support\Facades\Blade;

2 

3/**

4 * Bootstrap your package's services.

5 */

6public function boot(): void

7{

8    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');

9}
```

This will allow the usage of package components by their vendor namespace using the `package-name::` syntax:

```
1<x-nightshade::calendar />

2<x-nightshade::color-picker />
```

Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation.

#### [Anonymous Components](#anonymous-components)

If your package contains anonymous components, they must be placed within a `components` directory of your package's "views" directory (as specified by the [loadViewsFrom method](#views)). Then, you may render them by prefixing the component name with the package's view namespace:

```
1<x-courier::alert />
```

### ["About" Artisan Command](#about-artisan-command)

Laravel's built-in `about` Artisan command provides a synopsis of the application's environment and configuration. Packages may push additional information to this command's output via the `AboutCommand` class. Typically, this information may be added from your package service provider's `boot` method:

```
1use Illuminate\Foundation\Console\AboutCommand;

2 

3/**

4 * Bootstrap any package services.

5 */

6public function boot(): void

7{

8    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);

9}
```

## [Commands](#commands)

To register your package's Artisan commands with Laravel, you may use the `commands` method. This method expects an array of command class names. Once the commands have been registered, you may execute them using the [Artisan CLI](/docs/13.x/artisan):

```
 1use Courier\Console\Commands\InstallCommand;

 2use Courier\Console\Commands\NetworkCommand;

 3 

 4/**

 5 * Bootstrap any package services.

 6 */

 7public function boot(): void

 8{

 9    if ($this->app->runningInConsole()) {

10        $this->commands([

11            InstallCommand::class,

12            NetworkCommand::class,

13        ]);

14    }

15}
```

### [Optimize Commands](#optimize-commands)

Laravel's [optimize command](/docs/13.x/deployment#optimization) caches the application's configuration, events, routes, and views. Using the `optimizes` method, you may register your package's own Artisan commands that should be invoked when the `optimize` and `optimize:clear` commands are executed:

```
 1/**

 2 * Bootstrap any package services.

 3 */

 4public function boot(): void

 5{

 6    if ($this->app->runningInConsole()) {

 7        $this->optimizes(

 8            optimize: 'package:optimize',

 9            clear: 'package:clear-optimizations',

10        );

11    }

12}
```

### [Reload Commands](#reload-commands)

Laravel's [reload command](/docs/13.x/deployment#reloading-services) terminates any running services so they can be automatically restarted by a system process monitor. Using the `reloads` method, you may register your package's own Artisan commands that should be invoked when the `reload` command is executed:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    if ($this->app->runningInConsole()) {

7        $this->reloads('package:reload');

8    }

9}
```

## [Public Assets](#public-assets)

Your package may have assets such as JavaScript, CSS, and images. To publish these assets to the application's `public` directory, use the service provider's `publishes` method. In this example, we will also add a `public` asset group tag, which may be used to easily publish groups of related assets:

```
1/**

2 * Bootstrap any package services.

3 */

4public function boot(): void

5{

6    $this->publishes([

7        __DIR__.'/../public' => public_path('vendor/courier'),

8    ], 'public');

9}
```

Now, when your package's users execute the `vendor:publish` command, your assets will be copied to the specified publish location. Since users will typically need to overwrite the assets every time the package is updated, they may use the `--force` flag:

```
1php artisan vendor:publish --tag=public --force
```

## [Publishing File Groups](#publishing-file-groups)

You may want to publish groups of package assets and resources separately. For instance, you might want to allow your users to publish your package's configuration files without being forced to publish your package's assets. You may do this by "tagging" them when calling the `publishes` method from a package's service provider. For example, let's use tags to define two publish groups for the `courier` package (`courier-config` and `courier-migrations`) in the `boot` method of the package's service provider:

```
 1/**

 2 * Bootstrap any package services.

 3 */

 4public function boot(): void

 5{

 6    $this->publishes([

 7        __DIR__.'/../config/package.php' => config_path('package.php')

 8    ], 'courier-config');

 9 

10    $this->publishesMigrations([

11        __DIR__.'/../database/migrations/' => database_path('migrations')

12    ], 'courier-migrations');

13}
```

Now your users may publish these groups separately by referencing their tag when executing the `vendor:publish` command:

```
1php artisan vendor:publish --tag=courier-config
```

Your users can also publish all publishable files defined by your package's service provider using the `--provider` flag:

```
1php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```
