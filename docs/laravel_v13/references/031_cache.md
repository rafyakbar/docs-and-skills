# Cache

- [Introduction](#introduction)
- [Configuration](#configuration)
  * [Driver Prerequisites](#driver-prerequisites)
- [Cache Usage](#cache-usage)
  * [Obtaining a Cache Instance](#obtaining-a-cache-instance)
  * [Retrieving Items From the Cache](#retrieving-items-from-the-cache)
  * [Storing Items in the Cache](#storing-items-in-the-cache)
  * [Extending Item Lifetime](#extending-item-lifetime)
  * [Removing Items From the Cache](#removing-items-from-the-cache)
  * [Cache Memoization](#cache-memoization)
  * [The Cache Helper](#the-cache-helper)
- [Cache Tags](#cache-tags)
- [Atomic Locks](#atomic-locks)
  * [Managing Locks](#managing-locks)
  * [Managing Locks Across Processes](#managing-locks-across-processes)
  * [Refreshing Locks](#refreshing-locks)
  * [Concurrency Limiting](#concurrency-limiting)
- [Cache Failover](#cache-failover)
- [Adding Custom Cache Drivers](#adding-custom-cache-drivers)
  * [Writing the Driver](#writing-the-driver)
  * [Registering the Driver](#registering-the-driver)
- [Events](#events)

## [Introduction](#introduction)

Some of the data retrieval or processing tasks performed by your application could be CPU intensive or take several seconds to complete. When this is the case, it is common to cache the retrieved data for a time so it can be retrieved quickly on subsequent requests for the same data. The cached data is usually stored in a very fast data store such as [Memcached](https://memcached.org) or [Redis](https://redis.io).

Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application.

## [Configuration](#configuration)

Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache store you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), relational databases, and filesystem disks out of the box. In addition, a file based cache driver is available, while `array` and `null` cache drivers provide convenient cache backends for your automated tests.

The cache configuration file also contains a variety of other options that you may review. By default, Laravel is configured to use the `database` cache driver, which stores the serialized, cached objects in your application's database.

### [Driver Prerequisites](#driver-prerequisites)

#### [Database](#prerequisites-database)

When using the `database` cache driver, you will need a database table to contain the cache data. Typically, this is included in Laravel's default `0001_01_01_000001_create_cache_table.php` [database migration](/docs/13.x/migrations); however, if your application does not contain this migration, you may use the `make:cache-table` Artisan command to create it:

```
1php artisan make:cache-table

2 

3php artisan migrate
```

#### [Memcached](#memcached)

Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started:

```
 1'memcached' => [

 2    // ...

 3 

 4    'servers' => [

 5        [

 6            'host' => env('MEMCACHED_HOST', '127.0.0.1'),

 7            'port' => env('MEMCACHED_PORT', 11211),

 8            'weight' => 100,

 9        ],

10    ],

11],
```

If needed, you may set the `host` option to a UNIX socket path. If you do this, the `port` option should be set to `0`:

```
 1'memcached' => [

 2    // ...

 3 

 4    'servers' => [

 5        [

 6            'host' => '/var/run/memcached/memcached.sock',

 7            'port' => 0,

 8            'weight' => 100

 9        ],

10    ],

11],
```

#### [Redis](#redis)

Before using a Redis cache with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~2.0) via Composer. [Laravel Sail](/docs/13.x/sail) already includes this extension. In addition, official Laravel application platforms such as [Laravel Cloud](https://cloud.laravel.com) and [Laravel Forge](https://forge.laravel.com) have the PhpRedis extension installed by default.

For more information on configuring Redis, consult its [Laravel documentation page](/docs/13.x/redis#configuration).

#### [Storage](#storage)

The `storage` cache driver allows you to store cached values on any of your application's configured [filesystem disks](/docs/13.x/filesystem). This can be useful when you want to use an existing disk, such as an S3 disk, as a key / value cache store:

```
1'storage' => [

2    'driver' => 'storage',

3    'disk' => env('CACHE_STORAGE_DISK'),

4    'path' => env('CACHE_STORAGE_PATH', 'framework/cache/data'),

5],
```

#### [DynamoDB](#dynamodb)

Before using the [DynamoDB](https://aws.amazon.com/dynamodb) cache driver, you must create a DynamoDB table to store all of the cached data. Typically, this table should be named `cache`. However, you should name the table based on the value of the `stores.dynamodb.table` configuration value within the `cache` configuration file. The table name may also be set via the `DYNAMODB_CACHE_TABLE` environment variable.

This table should also have a string partition key with a name that corresponds to the value of the `stores.dynamodb.attributes.key` configuration item within your application's `cache` configuration file. By default, the partition key should be named `key`.

Typically, DynamoDB will not proactively remove expired items from a table. Therefore, you should [enable Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) on the table. When configuring the table's TTL settings, you should set the TTL attribute name to `expires_at`.

Next, install the AWS SDK so that your Laravel application can communicate with DynamoDB:

```
1composer require aws/aws-sdk-php
```

In addition, you should ensure that values are provided for the DynamoDB cache store configuration options. Typically these options, such as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, should be defined in your application's `.env` configuration file:

```
1'dynamodb' => [

2    'driver' => 'dynamodb',

3    'key' => env('AWS_ACCESS_KEY_ID'),

4    'secret' => env('AWS_SECRET_ACCESS_KEY'),

5    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),

6    'table' => env('DYNAMODB_CACHE_TABLE', 'cache'),

7    'endpoint' => env('DYNAMODB_ENDPOINT'),

8],
```

#### [MongoDB](#mongodb)

If you are using MongoDB, a `mongodb` cache driver is provided by the official `mongodb/laravel-mongodb` package and can be configured using a `mongodb` database connection. MongoDB supports TTL indexes, which can be used to automatically clear expired cache items.

For more information on configuring MongoDB, please refer to the MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/).

## [Cache Usage](#cache-usage)

### [Obtaining a Cache Instance](#obtaining-a-cache-instance)

To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Support\Facades\Cache;

 6 

 7class UserController extends Controller

 8{

 9    /**

10     * Show a list of all users of the application.

11     */

12    public function index(): array

13    {

14        $value = Cache::get('key');

15 

16        return [

17            // ...

18        ];

19    }

20}
```

#### [Accessing Multiple Cache Stores](#accessing-multiple-cache-stores)

Using the `Cache` facade, you may access various cache stores via the `store` method. The key passed to the `store` method should correspond to one of the stores listed in the `stores` configuration array in your `cache` configuration file:

```
1$value = Cache::store('file')->get('foo');

2 

3Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

### [Retrieving Items From the Cache](#retrieving-items-from-the-cache)

The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist:

```
1$value = Cache::get('key');

2 

3$value = Cache::get('key', 'default');
```

You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service:

```
1$value = Cache::get('key', function () {

2    return DB::table(/* ... */)->get();

3});
```

#### [Determining Item Existence](#determining-item-existence)

The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`:

```
1if (Cache::has('key')) {

2    // ...

3}
```

#### [Incrementing / Decrementing Values](#incrementing-decrementing-values)

The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value:

```
1// Initialize the value if it does not exist...

2Cache::add('key', 0, now()->plus(hours: 4));

3 

4// Increment or decrement the value...

5Cache::increment('key');

6Cache::increment('key', $amount);

7Cache::decrement('key');

8Cache::decrement('key', $amount);
```

#### [Retrieve and Store](#retrieve-store)

Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. For example, you may wish to retrieve all users from the cache or, if they don't exist, retrieve them from the database and add them to the cache. You may do this using the `Cache::remember` method:

```
1$value = Cache::remember('users', $seconds, function () {

2    return DB::table('users')->get();

3});
```

If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache.

If you need to know whether the item was retrieved from the cache instead of by executing the given closure, you may use the `rememberWithWarmth` method. This method returns an array containing the cached value and a boolean indicating whether the item was "warm", meaning it was retrieved from the cache and not resolved from the closure:

```
1[$value, $warm] = Cache::rememberWithWarmth('users', $seconds, function () {

2    return DB::table('users')->get();

3});
```

You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist:

```
1$value = Cache::rememberForever('users', function () {

2    return DB::table('users')->get();

3});
```

#### [Stale While Revalidate](#swr)

When using the `Cache::remember` method, some users may experience slow response times if the cached value has expired. For certain types of data, it can be useful to allow partially stale data to be served while the cached value is recalculated in the background, preventing some users from experiencing slow response times while cached values are calculated. This is often referred to as the "stale-while-revalidate" pattern, and the `Cache::flexible` method provides an implementation of this pattern.

The flexible method accepts an array that specifies how long the cached value is considered "fresh" and when it becomes "stale". The first value in the array represents the number of seconds the cache is considered fresh, while the second value defines how long it can be served as stale data before recalculation is necessary.

If a request is made within the fresh period (before the first value), the cache is returned immediately without recalculation. If a request is made during the stale period (between the two values), the stale value is served to the user, and a [deferred function](/docs/13.x/helpers#deferred-functions) is registered to refresh the cached value after the response is sent to the user. If a request is made after the second value, the cache is considered expired, and the value is recalculated immediately, which may result in a slower response for the user:

```
1$value = Cache::flexible('users', [5, 10], function () {

2    return DB::table('users')->get();

3});
```

#### [Retrieve and Delete](#retrieve-delete)

If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache:

```
1$value = Cache::pull('key');

2 

3$value = Cache::pull('key', 'default');
```

### [Storing Items in the Cache](#storing-items-in-the-cache)

You may use the `put` method on the `Cache` facade to store items in the cache:

```
1Cache::put('key', 'value', $seconds = 10);
```

If the storage time is not passed to the `put` method, the item will be stored indefinitely:

```
1Cache::put('key', 'value');
```

Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item:

```
1Cache::put('key', 'value', now()->plus(minutes: 10));
```

#### [Store if Not Present](#store-if-not-present)

The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation:

```
1Cache::add('key', 'value', $seconds);
```

### [Extending Item Lifetime](#extending-item-lifetime)

The `touch` method allows you to extend the lifetime (TTL) of an existing cache item. The `touch` method will return `true` if the cache item exists and its expiration time was successfully extended. If the item does not exist in the cache, the method will return `false`:

```
1Cache::touch('key', 3600);
```

You may provide a `DateTimeInterface`, `DateInterval`, or `Carbon` instance to specify an exact expiration time:

```
1Cache::touch('key', now()->addHours(2));
```

#### [Storing Items Forever](#storing-items-forever)

The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method:

```
1Cache::forever('key', 'value');
```

If you are using the Memcached driver, items that are stored "forever" may be removed when the cache reaches its size limit.

### [Removing Items From the Cache](#removing-items-from-the-cache)

You may remove items from the cache using the `forget` method:

```
1Cache::forget('key');
```

You may also remove items by providing a zero or negative number of expiration seconds:

```
1Cache::put('key', 'value', 0);

2 

3Cache::put('key', 'value', -5);
```

You may clear the entire cache using the `flush` method:

```
1Cache::flush();
```

You may clear all atomic locks in the cache using the `flushLocks` method:

```
1Cache::flushLocks();
```

Flushing the cache does not respect your configured cache "prefix" and will remove all entries from the cache. Consider this carefully when clearing a cache which is shared by other applications.

### [Cache Memoization](#cache-memoization)

Laravel's `memo` cache driver allows you to temporarily store resolved cache values in memory during a single request or job execution. This prevents repeated cache hits within the same execution, significantly improving performance.

To use the memoized cache, invoke the `memo` method:

```
1use Illuminate\Support\Facades\Cache;

2 

3$value = Cache::memo()->get('key');
```

The `memo` method optionally accepts the name of a cache store, which specifies the underlying cache store the memoized driver will decorate:

```
1// Using the default cache store...

2$value = Cache::memo()->get('key');

3 

4// Using the Redis cache store...

5$value = Cache::memo('redis')->get('key');
```

The first `get` call for a given key retrieves the value from your cache store, but subsequent calls within the same request or job will retrieve the value from memory:

```
1// Hits the cache...

2$value = Cache::memo()->get('key');

3 

4// Does not hit the cache, returns memoized value...

5$value = Cache::memo()->get('key');
```

When calling methods that modify cache values (such as `put`, `increment`, `remember`, etc.), the memoized cache automatically forgets the memoized value and delegates the mutating method call to the underlying cache store:

```
1Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...

2Cache::memo()->get('name');           // Hits underlying cache...

3Cache::memo()->get('name');           // Memoized, does not hit cache...

4 

5Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...

6Cache::memo()->get('name');           // Hits underlying cache again...
```

### [The Cache Helper](#the-cache-helper)

In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key:

```
1$value = cache('key');
```

If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration:

```
1cache(['key' => 'value'], $seconds);

2 

3cache(['key' => 'value'], now()->plus(minutes: 10));
```

When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods:

```
1cache()->remember('users', $seconds, function () {

2    return DB::table('users')->get();

3});
```

When testing calls to the global `cache` function, you may use the `Cache::shouldReceive` method just as if you were [testing the facade](/docs/13.x/mocking#mocking-facades).

## [Cache Tags](#cache-tags)

Cache tags are not supported when using the `file`, `dynamodb`, `database`, or `storage` cache drivers.

### [Storing Tagged Cache Items](#storing-tagged-cache-items)

Cache tags allow you to tag related items in the cache and then flush all cached values that have been assigned a given tag. You may access a tagged cache by passing in an ordered array of tag names. For example, let's access a tagged cache and `put` a value into the cache:

```
1use Illuminate\Support\Facades\Cache;

2 

3Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

4Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

### [Accessing Tagged Cache Items](#accessing-tagged-cache-items)

Items stored via tags may not be accessed without also providing the tags that were used to store the value. To retrieve a tagged cache item, pass the same ordered list of tags to the `tags` method, then call the `get` method with the key you wish to retrieve:

```
1$john = Cache::tags(['people', 'artists'])->get('John');

2 

3$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

### [Removing Tagged Cache Items](#removing-tagged-cache-items)

You may flush all items that are assigned a tag or list of tags. For example, the following code would remove all caches tagged with either `people`, `authors`, or both. So, both `Anne` and `John` would be removed from the cache:

```
1Cache::tags(['people', 'authors'])->flush();
```

In contrast, the code below would remove only cached values tagged with `authors`, so `Anne` would be removed, but not `John`:

```
1Cache::tags('authors')->flush();
```

## [Atomic Locks](#atomic-locks)

To utilize this feature, your application must be using the `memcached`, `redis`, `dynamodb`, `database`, `file`, or `array` cache driver as your application's default cache driver. In addition, all servers must be communicating with the same central cache server.

### [Managing Locks](#managing-locks)

Atomic locks allow for the manipulation of distributed locks without worrying about race conditions. For example, [Laravel Cloud](https://cloud.laravel.com) uses atomic locks to ensure that only one remote task is being executed on a server at a time. You may create and manage locks using the `Cache::lock` method:

```
1use Illuminate\Support\Facades\Cache;

2 

3$lock = Cache::lock('foo', 10);

4 

5if ($lock->get()) {

6    // Lock acquired for 10 seconds...

7 

8    $lock->release();

9}
```

The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock:

```
1Cache::lock('foo', 10)->get(function () {

2    // Lock acquired for 10 seconds and automatically released...

3});
```

If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock cannot be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown:

```
 1use Illuminate\Contracts\Cache\LockTimeoutException;

 2 

 3$lock = Cache::lock('foo', 10);

 4 

 5try {

 6    $lock->block(5);

 7 

 8    // Lock acquired after waiting a maximum of 5 seconds...

 9} catch (LockTimeoutException $e) {

10    // Unable to acquire lock...

11} finally {

12    $lock->release();

13}
```

The example above may be simplified by passing a closure to the `block` method. When a closure is passed to this method, Laravel will attempt to acquire the lock for the specified number of seconds and will automatically release the lock once the closure has been executed:

```
1Cache::lock('foo', 10)->block(5, function () {

2    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...

3});
```

### [Managing Locks Across Processes](#managing-locks-across-processes)

Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token.

In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method:

```
1$podcast = Podcast::find($id);

2 

3$lock = Cache::lock('processing', 120);

4 

5if ($lock->get()) {

6    ProcessPodcast::dispatch($podcast, $lock->owner());

7}
```

Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token:

```
1Cache::restoreLock('processing', $this->owner)->release();
```

If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method:

```
1Cache::lock('processing')->forceRelease();
```

### [Refreshing Locks](#refreshing-locks)

If you need to extend the expiration of a lock that you currently own, you may use the `refresh` method. If no number of seconds is provided, the lock's original duration will be used. This is useful for long-running operations where you prefer to acquire a short lock and periodically extend it instead of acquiring a lock with a very long expiration time:

```
 1$lock = Cache::lock('generate-reports', 60);

 2 

 3if ($lock->get()) {

 4    foreach ($reports as $report) {

 5        $report->generate();

 6 

 7        // Extend the lock for another 60 seconds...

 8        $lock->refresh();

 9    }

10 

11    $lock->release();

12}
```

### [Concurrency Limiting](#concurrency-limiting)

Laravel's atomic lock functionality also provides a few ways to limit concurrent execution of closures. Use `withoutOverlapping` when you want to allow only one running instance across your infrastructure:

```
1Cache::withoutOverlapping('foo', function () {

2    // Lock acquired after waiting a maximum of 10 seconds...

3});
```

By default, the lock is held until the closure finishes executing, and the method waits up to 10 seconds to acquire the lock. You may customize these values using additional arguments:

```
1Cache::withoutOverlapping('foo', function () {

2    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...

3}, lockFor: 120, waitFor: 5);
```

If the lock cannot be acquired within the specified wait time, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown.

If you want controlled parallelism, use the `funnel` method to set a maximum number of concurrent executions. The `funnel` method works with any cache driver that supports locks:

```
1Cache::funnel('foo')

2    ->limit(3)

3    ->releaseAfter(60)

4    ->block(10)

5    ->then(function () {

6        // Concurrency lock acquired...

7    }, function () {

8        // Could not acquire concurrency lock...

9    });
```

The `funnel` key identifies the resource being limited. The `limit` method defines the maximum concurrent executions. The `releaseAfter` method sets a safety timeout in seconds before an acquired slot is automatically released. The `block` method sets how many seconds to wait for an available slot.

If you prefer to handle the timeout via exceptions instead of providing a failure closure, you may omit the second closure. An `Illuminate\Cache\Limiters\LimiterTimeoutException` will be thrown if the lock cannot be acquired within the specified wait time:

```
 1use Illuminate\Cache\Limiters\LimiterTimeoutException;

 2 

 3try {

 4    Cache::funnel('foo')

 5        ->limit(3)

 6        ->releaseAfter(60)

 7        ->block(10)

 8        ->then(function () {

 9            // Concurrency lock acquired...

10        });

11} catch (LimiterTimeoutException $e) {

12    // Unable to acquire concurrency lock...

13}
```

If you would like to use a specific cache store for the concurrency limiter, you may invoke the `funnel` method on the desired store:

```
1Cache::store('redis')->funnel('foo')

2    ->limit(3)

3    ->block(10)

4    ->then(function () {

5        // Concurrency lock acquired using the "redis" store...

6    });
```

The `funnel` method requires the cache store to implement the `Illuminate\Contracts\Cache\LockProvider` interface. If you attempt to use `funnel` with a cache store that does not support locks, a `BadMethodCallException` will be thrown.

## [Cache Failover](#cache-failover)

The `failover` cache driver provides automatic failover functionality when interacting with the cache. If the primary cache store of the `failover` store fails for any reason, Laravel will automatically attempt to use the next configured store in the list. This is particularly useful for ensuring high availability in production environments where cache reliability is critical.

To configure a failover cache store, specify the `failover` driver and provide an array of store names to attempt in order. By default, Laravel includes an example failover configuration in your application's `config/cache.php` configuration file:

```
1'failover' => [

2    'driver' => 'failover',

3    'stores' => [

4        'database',

5        'array',

6    ],

7],
```

Once you have configured a store that uses the `failover` driver, you will need to set the failover store as your default cache store in your application's `.env` file to make use of the failover functionality:

```
1CACHE_STORE=failover
```

When a cache store operation fails and failover is activated, Laravel will dispatch the `Illuminate\Cache\Events\CacheFailedOver` event, allowing you to report or log that a cache store has failed.

## [Adding Custom Cache Drivers](#adding-custom-cache-drivers)

### [Writing the Driver](#writing-the-driver)

To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/13.x/contracts). So, a MongoDB cache implementation might look something like this:

```
 1<?php

 2 

 3namespace App\Extensions;

 4 

 5use Illuminate\Contracts\Cache\Store;

 6 

 7class MongoStore implements Store

 8{

 9    public function get($key) {}

10    public function many(array $keys) {}

11    public function put($key, $value, $seconds) {}

12    public function putMany(array $values, $seconds) {}

13    public function increment($key, $value = 1) {}

14    public function decrement($key, $value = 1) {}

15    public function forever($key, $value) {}

16    public function forget($key) {}

17    public function flush() {}

18    public function getPrefix() {}

19}
```

We just need to implement each of these methods using a MongoDB connection. For an example of how to implement each of these methods, take a look at the `Illuminate\Cache\MemcachedStore` in the [Laravel framework source code](https://github.com/laravel/framework). Once our implementation is complete, we can finish our custom driver registration by calling the `Cache` facade's `extend` method:

```
1Cache::extend('mongo', function (Application $app) {

2    return Cache::repository(new MongoStore);

3});
```

If you're wondering where to put your custom cache driver code, you could create an `Extensions` namespace within your `app` directory. However, keep in mind that Laravel does not have a rigid application structure and you are free to organize your application according to your preferences.

### [Registering the Driver](#registering-the-driver)

To register the custom cache driver with Laravel, we will use the `extend` method on the `Cache` facade. Since other service providers may attempt to read cached values within their `boot` method, we will register our custom driver within a `booting` callback. By using the `booting` callback, we can ensure that the custom driver is registered just before the `boot` method is called on our application's service providers but after the `register` method is called on all of the service providers. We will register our `booting` callback within the `register` method of our application's `App\Providers\AppServiceProvider` class:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use App\Extensions\MongoStore;

 6use Illuminate\Contracts\Foundation\Application;

 7use Illuminate\Support\Facades\Cache;

 8use Illuminate\Support\ServiceProvider;

 9 

10class AppServiceProvider extends ServiceProvider

11{

12    /**

13     * Register any application services.

14     */

15    public function register(): void

16    {

17        $this->app->booting(function () {

18             Cache::extend('mongo', function (Application $app) {

19                 return Cache::repository(new MongoStore);

20             });

21         });

22    }

23 

24    /**

25     * Bootstrap any application services.

26     */

27    public function boot(): void

28    {

29        // ...

30    }

31}
```

The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/13.x/container).

Once your extension is registered, update the `CACHE_STORE` environment variable or `default` option within your application's `config/cache.php` configuration file to the name of your extension.

## [Events](#events)

To execute code on every cache operation, you may listen for various [events](/docs/13.x/events) dispatched by the cache:

| Event Name                                      |
| ----------------------------------------------- |
| `Illuminate\Cache\Events\CacheFlushed`          |
| `Illuminate\Cache\Events\CacheFlushing`         |
| `Illuminate\Cache\Events\CacheFlushFailed`      |
| `Illuminate\Cache\Events\CacheLocksFlushed`     |
| `Illuminate\Cache\Events\CacheLocksFlushing`    |
| `Illuminate\Cache\Events\CacheLocksFlushFailed` |
| `Illuminate\Cache\Events\CacheHit`              |
| `Illuminate\Cache\Events\CacheMissed`           |
| `Illuminate\Cache\Events\ForgettingKey`         |
| `Illuminate\Cache\Events\KeyForgetFailed`       |
| `Illuminate\Cache\Events\KeyForgotten`          |
| `Illuminate\Cache\Events\KeyWriteFailed`        |
| `Illuminate\Cache\Events\KeyWritten`            |
| `Illuminate\Cache\Events\RetrievingKey`         |
| `Illuminate\Cache\Events\RetrievingManyKeys`    |
| `Illuminate\Cache\Events\WritingKey`            |
| `Illuminate\Cache\Events\WritingManyKeys`       |

To increase performance, you may disable cache events by setting the `events` configuration option to `false` for a given cache store in your application's `config/cache.php` configuration file:

```
1'database' => [

2    'driver' => 'database',

3    // ...

4    'events' => false,

5],
```
