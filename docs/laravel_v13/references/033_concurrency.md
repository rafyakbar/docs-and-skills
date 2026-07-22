# Concurrency

- [Introduction](#introduction)
- [Running Concurrent Tasks](#running-concurrent-tasks)
  * [Named Results](#named-results)
  * [Task Timeouts](#task-timeouts)
- [Deferring Concurrent Tasks](#deferring-concurrent-tasks)

## [Introduction](#introduction)

Sometimes you may need to execute several slow tasks which do not depend on one another. In many cases, significant performance improvements can be realized by executing the tasks concurrently. Laravel's `Concurrency` facade provides a simple, convenient API for executing closures concurrently.

#### [How it Works](#how-it-works)

Laravel achieves concurrency by serializing the given closures and dispatching them to a hidden Artisan CLI command, which unserializes the closures and invokes it within its own PHP process. After the closure has been invoked, the resulting value is serialized back to the parent process.

The `Concurrency` facade supports three drivers: `process` (the default), `fork`, and `sync`.

The `fork` driver offers improved performance compared to the default `process` driver, but it may only be used within PHP's CLI context, as PHP does not support forking during web requests. Before using the `fork` driver, you need to install the `spatie/fork` package:

```
1composer require spatie/fork
```

The `sync` driver is primarily useful during testing when you want to disable all concurrency and simply execute the given closures in sequence within the parent process.

## [Running Concurrent Tasks](#running-concurrent-tasks)

To run concurrent tasks, you may invoke the `Concurrency` facade's `run` method. The `run` method accepts an array of closures which should be executed simultaneously in child PHP processes:

```
1use Illuminate\Support\Facades\Concurrency;

2use Illuminate\Support\Facades\DB;

3 

4[$userCount, $orderCount] = Concurrency::run([

5    fn () => DB::table('users')->count(),

6    fn () => DB::table('orders')->count(),

7]);
```

To use a specific driver, you may use the `driver` method:

```
1$results = Concurrency::driver('fork')->run(...);
```

Or, to change the default concurrency driver, you should publish the `concurrency` configuration file via the `config:publish` Artisan command and update the `default` option within the file:

```
1php artisan config:publish concurrency
```

### [Named Results](#named-results)

If you would like to access concurrent task results by name rather than by position, you may provide an associative array of closures. Each result will be returned using the same key as its corresponding closure:

```
 1use Illuminate\Support\Facades\Concurrency;

 2use Illuminate\Support\Facades\DB;

 3 

 4$results = Concurrency::run([

 5    'users' => fn () => DB::table('users')->count(),

 6    'orders' => fn () => DB::table('orders')->count(),

 7]);

 8 

 9$userCount = $results['users'];

10$orderCount = $results['orders'];
```

### [Task Timeouts](#task-timeouts)

When using the `process` driver (the default), you may specify a maximum number of seconds a concurrent task is allowed to run before it is terminated by providing a timeout to the `run` method:

```
1use Illuminate\Support\Facades\Concurrency;

2use Illuminate\Support\Facades\DB;

3 

4[$userCount, $orderCount] = Concurrency::run([

5    fn () => DB::table('users')->count(),

6    fn () => DB::table('orders')->count(),

7], timeout: 30);
```

You may also provide a `CarbonInterval` instance if you prefer a more expressive timeout definition:

```
1use Illuminate\Support\Facades\Concurrency;

2 

3use function Illuminate\Support\seconds;

4 

5Concurrency::run([...], timeout: seconds(30));
```

## [Deferring Concurrent Tasks](#deferring-concurrent-tasks)

If you would like to execute an array of closures concurrently, but are not interested in the results returned by those closures, you should consider using the `defer` method. When the `defer` method is invoked, the given closures are not executed immediately. Instead, Laravel will execute the closures concurrently after the HTTP response has been sent to the user:

```
1use App\Services\Metrics;

2use Illuminate\Support\Facades\Concurrency;

3 

4Concurrency::defer([

5    fn () => Metrics::report('users'),

6    fn () => Metrics::report('orders'),

7]);
```
