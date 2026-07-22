# Service Providers

- [Introduction](#introduction)
- [Writing Service Providers](#writing-service-providers)
  * [The Register Method](#the-register-method)
  * [The Boot Method](#the-boot-method)
- [Registering Providers](#registering-providers)
- [Deferred Providers](#deferred-providers)

## [Introduction](#introduction)

Service providers are the central place of all Laravel application bootstrapping. Your own application, as well as all of Laravel's core services, are bootstrapped via service providers.

But, what do we mean by "bootstrapped"? In general, we mean **registering** things, including registering service container bindings, event listeners, middleware, and even routes. Service providers are the central place to configure your application.

Laravel uses dozens of service providers internally to bootstrap its core services, such as the mailer, queue, cache, and others. Many of these providers are "deferred" providers, meaning they will not be loaded on every request, but only when the services they provide are actually needed.

All user-defined service providers are registered in the `bootstrap/providers.php` file. In the following documentation, you will learn how to write your own service providers and register them with your Laravel application.

If you would like to learn more about how Laravel handles requests and works internally, check out our documentation on the Laravel [request lifecycle](/docs/13.x/lifecycle).

## [Writing Service Providers](#writing-service-providers)

All service providers extend the `Illuminate\Support\ServiceProvider` class. Most service providers contain a `register` and a `boot` method. Within the `register` method, you should **only bind things into the [service container](/docs/13.x/container)**. You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method.

The Artisan CLI can generate a new provider via the `make:provider` command. Laravel will automatically register your new provider in your application's `bootstrap/providers.php` file:

```
1php artisan make:provider RiakServiceProvider
```

### [The Register Method](#the-register-method)

As mentioned previously, within the `register` method, you should only bind things into the [service container](/docs/13.x/container). You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. Otherwise, you may accidentally use a service that is provided by a service provider which has not loaded yet.

Let's take a look at a basic service provider. Within any of your service provider methods, you always have access to the `$app` property which provides access to the service container:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use App\Services\Riak\Connection;

 6use Illuminate\Contracts\Foundation\Application;

 7use Illuminate\Support\ServiceProvider;

 8 

 9class RiakServiceProvider extends ServiceProvider

10{

11    /**

12     * Register any application services.

13     */

14    public function register(): void

15    {

16        $this->app->singleton(Connection::class, function (Application $app) {

17            return new Connection(config('riak'));

18        });

19    }

20}
```

This service provider only defines a `register` method, and uses that method to define an implementation of `App\Services\Riak\Connection` in the service container. If you're not yet familiar with Laravel's service container, check out [its documentation](/docs/13.x/container).

#### [The `bindings` and `singletons` Properties](#the-bindings-and-singletons-properties)

If your service provider registers many simple bindings, you may wish to use the `bindings` and `singletons` properties instead of manually registering each container binding. When the service provider is loaded by the framework, it will automatically check for these properties and register their bindings:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use App\Contracts\DowntimeNotifier;

 6use App\Contracts\ServerProvider;

 7use App\Services\DigitalOceanServerProvider;

 8use App\Services\PingdomDowntimeNotifier;

 9use App\Services\ServerToolsProvider;

10use Illuminate\Support\ServiceProvider;

11 

12class AppServiceProvider extends ServiceProvider

13{

14    /**

15     * All of the container bindings that should be registered.

16     *

17     * @var array

18     */

19    public $bindings = [

20        ServerProvider::class => DigitalOceanServerProvider::class,

21    ];

22 

23    /**

24     * All of the container singletons that should be registered.

25     *

26     * @var array

27     */

28    public $singletons = [

29        DowntimeNotifier::class => PingdomDowntimeNotifier::class,

30        ServerProvider::class => ServerToolsProvider::class,

31    ];

32}
```

### [The Boot Method](#the-boot-method)

So, what if we need to register a [view composer](/docs/13.x/views#view-composers) within our service provider? This should be done within the `boot` method. **This method is called after all other service providers have been registered**, meaning you have access to all other services that have been registered by the framework:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Support\Facades\View;

 6use Illuminate\Support\ServiceProvider;

 7 

 8class ComposerServiceProvider extends ServiceProvider

 9{

10    /**

11     * Bootstrap any application services.

12     */

13    public function boot(): void

14    {

15        View::composer('view', function () {

16            // ...

17        });

18    }

19}
```

#### [Boot Method Dependency Injection](#boot-method-dependency-injection)

You may type-hint dependencies for your service provider's `boot` method. The [service container](/docs/13.x/container) will automatically inject any dependencies you need:

```
 1use Illuminate\Contracts\Routing\ResponseFactory;

 2 

 3/**

 4 * Bootstrap any application services.

 5 */

 6public function boot(ResponseFactory $response): void

 7{

 8    $response->macro('serialized', function (mixed $value) {

 9        // ...

10    });

11}
```

## [Registering Providers](#registering-providers)

All service providers are registered in the `bootstrap/providers.php` configuration file. This file returns an array that contains the class names of your application's service providers:

```
1<?php

2 

3return [

4    App\Providers\AppServiceProvider::class,

5];
```

When you invoke the `make:provider` Artisan command, Laravel will automatically add the generated provider to the `bootstrap/providers.php` file. However, if you have manually created the provider class, you should manually add the provider class to the array:

```
1<?php

2 

3return [

4    App\Providers\AppServiceProvider::class,

5    App\Providers\ComposerServiceProvider::class,

6];
```

## [Deferred Providers](#deferred-providers)

If your provider is **only** registering bindings in the [service container](/docs/13.x/container), you may choose to defer its registration until one of the registered bindings is actually needed. Deferring the loading of such a provider will improve the performance of your application, since it is not loaded from the filesystem on every request.

Laravel compiles and stores a list of all of the services supplied by deferred service providers, along with the name of its service provider class. Then, only when you attempt to resolve one of these services does Laravel load the service provider.

To defer the loading of a provider, implement the `\Illuminate\Contracts\Support\DeferrableProvider` interface and define a `provides` method. The `provides` method should return the service container bindings registered by the provider:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use App\Services\Riak\Connection;

 6use Illuminate\Contracts\Foundation\Application;

 7use Illuminate\Contracts\Support\DeferrableProvider;

 8use Illuminate\Support\ServiceProvider;

 9 

10class RiakServiceProvider extends ServiceProvider implements DeferrableProvider

11{

12    /**

13     * Register any application services.

14     */

15    public function register(): void

16    {

17        $this->app->singleton(Connection::class, function (Application $app) {

18            return new Connection($app['config']['riak']);

19        });

20    }

21 

22    /**

23     * Get the services provided by the provider.

24     *

25     * @return array<int, string>

26     */

27    public function provides(): array

28    {

29        return [Connection::class];

30    }

31}
```
