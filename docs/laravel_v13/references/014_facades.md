# Facades

- [Introduction](#introduction)
- [When to Utilize Facades](#when-to-use-facades)
  * [Facades vs. Dependency Injection](#facades-vs-dependency-injection)
  * [Facades vs. Helper Functions](#facades-vs-helper-functions)
- [How Facades Work](#how-facades-work)
- [Real-Time Facades](#real-time-facades)
- [Facade Class Reference](#facade-class-reference)

## [Introduction](#introduction)

Throughout the Laravel documentation, you will see examples of code that interacts with Laravel's features via "facades". Facades provide a "static" interface to classes that are available in the application's [service container](/docs/13.x/container). Laravel ships with many facades which provide access to almost all of Laravel's features.

Laravel facades serve as "static proxies" to underlying classes in the service container, providing the benefit of a terse, expressive syntax while maintaining more testability and flexibility than traditional static methods. It's perfectly fine if you don't totally understand how facades work - just go with the flow and continue learning about Laravel.

All of Laravel's facades are defined in the `Illuminate\Support\Facades` namespace. So, we can easily access a facade like so:

```
1use Illuminate\Support\Facades\Cache;

2use Illuminate\Support\Facades\Route;

3 

4Route::get('/cache', function () {

5    return Cache::get('key');

6});
```

Throughout the Laravel documentation, many of the examples will use facades to demonstrate various features of the framework.

#### [Helper Functions](#helper-functions)

To complement facades, Laravel offers a variety of global "helper functions" that make it even easier to interact with common Laravel features. Some of the common helper functions you may interact with are `view`, `response`, `url`, `config`, and more. Each helper function offered by Laravel is documented with their corresponding feature; however, a complete list is available within the dedicated [helper documentation](/docs/13.x/helpers).

For example, instead of using the `Illuminate\Support\Facades\Response` facade to generate a JSON response, we may simply use the `response` function. Because helper functions are globally available, you do not need to import any classes in order to use them:

```
 1use Illuminate\Support\Facades\Response;

 2 

 3Route::get('/users', function () {

 4    return Response::json([

 5        // ...

 6    ]);

 7});

 8 

 9Route::get('/users', function () {

10    return response()->json([

11        // ...

12    ]);

13});
```

## [When to Utilize Facades](#when-to-use-facades)

Facades have many benefits. They provide a terse, memorable syntax that allows you to use Laravel's features without remembering long class names that must be injected or configured manually. Furthermore, because of their unique usage of PHP's dynamic methods, they are easy to test.

However, some care must be taken when using facades. The primary danger of facades is class "scope creep". Since facades are so easy to use and do not require injection, it can be easy to let your classes continue to grow and use many facades in a single class. Using dependency injection, this potential is mitigated by the visual feedback a large constructor gives you that your class is growing too large. So, when using facades, pay special attention to the size of your class so that its scope of responsibility stays narrow. If your class is getting too large, consider splitting it into multiple smaller classes.

### [Facades vs. Dependency Injection](#facades-vs-dependency-injection)

One of the primary benefits of dependency injection is the ability to swap implementations of the injected class. This is useful during testing since you can inject a mock or stub and assert that various methods were called on the stub.

Typically, it would not be possible to mock or stub a truly static class method. However, since facades use dynamic methods to proxy method calls to objects resolved from the service container, we actually can test facades just as we would test an injected class instance. For example, given the following route:

```
1use Illuminate\Support\Facades\Cache;

2 

3Route::get('/cache', function () {

4    return Cache::get('key');

5});
```

Using Laravel's facade testing methods, we can write the following test to verify that the `Cache::get` method was called with the argument we expected:

Pest

PHPUnit

```
 1use Illuminate\Support\Facades\Cache;

 2 

 3test('basic example', function () {

 4    Cache::shouldReceive('get')

 5        ->with('key')

 6        ->andReturn('value');

 7 

 8    $response = $this->get('/cache');

 9 

10    $response->assertSee('value');

11});
```

```
 1use Illuminate\Support\Facades\Cache;

 2 

 3/**

 4 * A basic functional test example.

 5 */

 6public function test_basic_example(): void

 7{

 8    Cache::shouldReceive('get')

 9        ->with('key')

10        ->andReturn('value');

11 

12    $response = $this->get('/cache');

13 

14    $response->assertSee('value');

15}
```

### [Facades vs. Helper Functions](#facades-vs-helper-functions)

In addition to facades, Laravel includes a variety of "helper" functions which can perform common tasks like generating views, firing events, dispatching jobs, or sending HTTP responses. Many of these helper functions perform the same function as a corresponding facade. For example, this facade call and helper call are equivalent:

```
1return Illuminate\Support\Facades\View::make('profile');

2 

3return view('profile');
```

There is absolutely no practical difference between facades and helper functions. When using helper functions, you may still test them exactly as you would the corresponding facade. For example, given the following route:

```
1Route::get('/cache', function () {

2    return cache('key');

3});
```

The `cache` helper is going to call the `get` method on the class underlying the `Cache` facade. So, even though we are using the helper function, we can write the following test to verify that the method was called with the argument we expected:

```
 1use Illuminate\Support\Facades\Cache;

 2 

 3/**

 4 * A basic functional test example.

 5 */

 6public function test_basic_example(): void

 7{

 8    Cache::shouldReceive('get')

 9        ->with('key')

10        ->andReturn('value');

11 

12    $response = $this->get('/cache');

13 

14    $response->assertSee('value');

15}
```

## [How Facades Work](#how-facades-work)

In a Laravel application, a facade is a class that provides access to an object from the container. The machinery that makes this work is in the `Facade` class. Laravel's facades, and any custom facades you create, will extend the base `Illuminate\Support\Facades\Facade` class.

The `Facade` base class makes use of the `__callStatic()` magic-method to defer calls from your facade to an object resolved from the container. In the example below, a call is made to the Laravel cache system. By glancing at this code, one might assume that the static `get` method is being called on the `Cache` class:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Support\Facades\Cache;

 6use Illuminate\View\View;

 7 

 8class UserController extends Controller

 9{

10    /**

11     * Show the profile for the given user.

12     */

13    public function showProfile(string $id): View

14    {

15        $user = Cache::get('user:'.$id);

16 

17        return view('profile', ['user' => $user]);

18    }

19}
```

Notice that near the top of the file we are "importing" the `Cache` facade. This facade serves as a proxy for accessing the underlying implementation of the `Illuminate\Contracts\Cache\Factory` interface. Any calls we make using the facade will be passed to the underlying instance of Laravel's cache service.

If we look at that `Illuminate\Support\Facades\Cache` class, you'll see that there is no static method `get`:

```
 1class Cache extends Facade

 2{

 3    /**

 4     * Get the registered name of the component.

 5     */

 6    protected static function getFacadeAccessor(): string

 7    {

 8        return 'cache';

 9    }

10}
```

Instead, the `Cache` facade extends the base `Facade` class and defines the method `getFacadeAccessor()`. This method's job is to return the name of a service container binding. When a user references any static method on the `Cache` facade, Laravel resolves the `cache` binding from the [service container](/docs/13.x/container) and runs the requested method (in this case, `get`) against that object.

## [Real-Time Facades](#real-time-facades)

Using real-time facades, you may treat any class in your application as if it was a facade. To illustrate how this can be used, let's first examine some code that does not use real-time facades. For example, let's assume our `Podcast` model has a `publish` method. However, in order to publish the podcast, we need to inject a `Publisher` instance:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use App\Contracts\Publisher;

 6use Illuminate\Database\Eloquent\Model;

 7 

 8class Podcast extends Model

 9{

10    /**

11     * Publish the podcast.

12     */

13    public function publish(Publisher $publisher): void

14    {

15        $this->update(['publishing' => now()]);

16 

17        $publisher->publish($this);

18    }

19}
```

Injecting a publisher implementation into the method allows us to easily test the method in isolation since we can mock the injected publisher. However, it requires us to always pass a publisher instance each time we call the `publish` method. Using real-time facades, we can maintain the same testability while not being required to explicitly pass a `Publisher` instance. To generate a real-time facade, prefix the namespace of the imported class with `Facades`:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use App\Contracts\Publisher;

 6use Facades\App\Contracts\Publisher;

 7use Illuminate\Database\Eloquent\Model;

 8 

 9class Podcast extends Model

10{

11    /**

12     * Publish the podcast.

13     */

14    public function publish(Publisher $publisher): void

15    public function publish(): void

16    {

17        $this->update(['publishing' => now()]);

18 

19        $publisher->publish($this);

20        Publisher::publish($this);

21    }

22}
```

When the real-time facade is used, the publisher implementation will be resolved out of the service container using the portion of the interface or class name that appears after the `Facades` prefix. When testing, we can use Laravel's built-in facade testing helpers to mock this method call:

Pest

PHPUnit

```
 1<?php

 2 

 3use App\Models\Podcast;

 4use Facades\App\Contracts\Publisher;

 5use Illuminate\Foundation\Testing\RefreshDatabase;

 6 

 7pest()->use(RefreshDatabase::class);

 8 

 9test('podcast can be published', function () {

10    $podcast = Podcast::factory()->create();

11 

12    Publisher::shouldReceive('publish')->once()->with($podcast);

13 

14    $podcast->publish();

15});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use App\Models\Podcast;

 6use Facades\App\Contracts\Publisher;

 7use Illuminate\Foundation\Testing\RefreshDatabase;

 8use Tests\TestCase;

 9 

10class PodcastTest extends TestCase

11{

12    use RefreshDatabase;

13 

14    /**

15     * A test example.

16     */

17    public function test_podcast_can_be_published(): void

18    {

19        $podcast = Podcast::factory()->create();

20 

21        Publisher::shouldReceive('publish')->once()->with($podcast);

22 

23        $podcast->publish();

24    }

25}
```

## [Facade Class Reference](#facade-class-reference)

Below you will find every facade and its underlying class. This is a useful tool for quickly digging into the API documentation for a given facade root. The [service container binding](/docs/13.x/container) key is also included where applicable.

| Facade                | Class                                                                                                                                     | Service Container Binding |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| App                   | [Illuminate\Foundation\Application](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Application.html)                             | `app`                     |
| Artisan               | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Console/Kernel.html)                         | `artisan`                 |
| Auth (Instance)       | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Auth/Guard.html)                                 | `auth.driver`             |
| Auth                  | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/13.x/Illuminate/Auth/AuthManager.html)                                         | `auth`                    |
| Blade                 | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/13.x/Illuminate/View/Compilers/BladeCompiler.html)                 | `blade.compiler`          |
| Broadcast (Instance)  | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Broadcaster.html)     |                           |
| Broadcast             | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Factory.html)             |                           |
| Bus                   | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Bus/Dispatcher.html)                         |                           |
| Cache (Instance)      | [Illuminate\Cache\Repository](https://api.laravel.com/docs/13.x/Illuminate/Cache/Repository.html)                                         | `cache.store`             |
| Cache                 | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/13.x/Illuminate/Cache/CacheManager.html)                                     | `cache`                   |
| Config                | [Illuminate\Config\Repository](https://api.laravel.com/docs/13.x/Illuminate/Config/Repository.html)                                       | `config`                  |
| Context               | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/13.x/Illuminate/Log/Context/Repository.html)                             |                           |
| Cookie                | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/13.x/Illuminate/Cookie/CookieJar.html)                                         | `cookie`                  |
| Crypt                 | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/13.x/Illuminate/Encryption/Encrypter.html)                                 | `encrypter`               |
| Date                  | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/13.x/Illuminate/Support/DateFactory.html)                                   | `date`                    |
| DB (Instance)         | [Illuminate\Database\Connection](https://api.laravel.com/docs/13.x/Illuminate/Database/Connection.html)                                   | `db.connection`           |
| DB                    | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/13.x/Illuminate/Database/DatabaseManager.html)                         | `db`                      |
| Event                 | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/13.x/Illuminate/Events/Dispatcher.html)                                       | `events`                  |
| Exceptions (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Debug/ExceptionHandler.html)         |                           |
| Exceptions            | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Exceptions/Handler.html)               |                           |
| File                  | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/13.x/Illuminate/Filesystem/Filesystem.html)                               | `files`                   |
| Gate                  | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Auth/Access/Gate.html)                     |                           |
| Hash                  | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Hashing/Hasher.html)                         | `hash`                    |
| Http                  | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/13.x/Illuminate/Http/Client/Factory.html)                                   |                           |
| Lang                  | [Illuminate\Translation\Translator](https://api.laravel.com/docs/13.x/Illuminate/Translation/Translator.html)                             | `translator`              |
| Log                   | [Illuminate\Log\LogManager](https://api.laravel.com/docs/13.x/Illuminate/Log/LogManager.html)                                             | `log`                     |
| Mail                  | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/13.x/Illuminate/Mail/Mailer.html)                                                   | `mailer`                  |
| Notification          | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/13.x/Illuminate/Notifications/ChannelManager.html)                 |                           |
| Password (Instance)   | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBroker.html)               | `auth.password.broker`    |
| Password              | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password`           |
| Pipeline (Instance)   | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/13.x/Illuminate/Pipeline/Pipeline.html)                                       |                           |
| Process               | [Illuminate\Process\Factory](https://api.laravel.com/docs/13.x/Illuminate/Process/Factory.html)                                           |                           |
| Queue (Base Class)    | [Illuminate\Queue\Queue](https://api.laravel.com/docs/13.x/Illuminate/Queue/Queue.html)                                                   |                           |
| Queue (Instance)      | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Queue/Queue.html)                               | `queue.connection`        |
| Queue                 | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/13.x/Illuminate/Queue/QueueManager.html)                                     | `queue`                   |
| RateLimiter           | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/13.x/Illuminate/Cache/RateLimiter.html)                                       |                           |
| Redirect              | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/13.x/Illuminate/Routing/Redirector.html)                                     | `redirect`                |
| Redis (Instance)      | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/13.x/Illuminate/Redis/Connections/Connection.html)                 | `redis.connection`        |
| Redis                 | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/13.x/Illuminate/Redis/RedisManager.html)                                     | `redis`                   |
| Request               | [Illuminate\Http\Request](https://api.laravel.com/docs/13.x/Illuminate/Http/Request.html)                                                 | `request`                 |
| Response (Instance)   | [Illuminate\Http\Response](https://api.laravel.com/docs/13.x/Illuminate/Http/Response.html)                                               |                           |
| Response              | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Routing/ResponseFactory.html)       |                           |
| Route                 | [Illuminate\Routing\Router](https://api.laravel.com/docs/13.x/Illuminate/Routing/Router.html)                                             | `router`                  |
| Schedule              | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/13.x/Illuminate/Console/Scheduling/Schedule.html)                   |                           |
| Schema                | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/13.x/Illuminate/Database/Schema/Builder.html)                           |                           |
| Session (Instance)    | [Illuminate\Session\Store](https://api.laravel.com/docs/13.x/Illuminate/Session/Store.html)                                               | `session.store`           |
| Session               | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/13.x/Illuminate/Session/SessionManager.html)                             | `session`                 |
| Storage (Instance)    | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Filesystem/Filesystem.html)           | `filesystem.disk`         |
| Storage               | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/13.x/Illuminate/Filesystem/FilesystemManager.html)                 | `filesystem`              |
| URL                   | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/13.x/Illuminate/Routing/UrlGenerator.html)                                 | `url`                     |
| Validator (Instance)  | [Illuminate\Validation\Validator](https://api.laravel.com/docs/13.x/Illuminate/Validation/Validator.html)                                 |                           |
| Validator             | [Illuminate\Validation\Factory](https://api.laravel.com/docs/13.x/Illuminate/Validation/Factory.html)                                     | `validator`               |
| View (Instance)       | [Illuminate\View\View](https://api.laravel.com/docs/13.x/Illuminate/View/View.html)                                                       |                           |
| View                  | [Illuminate\View\Factory](https://api.laravel.com/docs/13.x/Illuminate/View/Factory.html)                                                 | `view`                    |
| Vite                  | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Vite.html)                                           |                           |
