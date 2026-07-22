# Redis

- [Introduction](#introduction)
- [Configuration](#configuration)
  * [Clusters](#clusters)
  * [Predis](#predis)
  * [PhpRedis](#phpredis)
- [Interacting With Redis](#interacting-with-redis)
  * [Transactions](#transactions)
  * [Pipelining Commands](#pipelining-commands)
- [Pub / Sub](#pubsub)

## [Introduction](#introduction)

[Redis](https://redis.io) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain [strings](https://redis.io/docs/latest/develop/data-types/strings/), [hashes](https://redis.io/docs/latest/develop/data-types/hashes/), [lists](https://redis.io/docs/latest/develop/data-types/lists/), [sets](https://redis.io/docs/latest/develop/data-types/sets/), and [sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/).

Before using Redis with Laravel, we encourage you to install and use the [PhpRedis](https://github.com/phpredis/phpredis) PHP extension via PECL. The extension is more complex to install compared to "user-land" PHP packages but may yield better performance for applications that make heavy use of Redis. If you are using [Laravel Sail](/docs/13.x/sail), this extension is already installed in your application's Docker container.

If you are unable to install the PhpRedis extension, you may install the `predis/predis` package via Composer. Predis is a Redis client written entirely in PHP and does not require any additional extensions:

```
1composer require predis/predis
```

## [Configuration](#configuration)

You may configure your application's Redis settings via the `config/database.php` configuration file. Within this file, you will see a `redis` array containing the Redis servers utilized by your application:

```
 1'redis' => [

 2 

 3    'client' => env('REDIS_CLIENT', 'phpredis'),

 4 

 5    'options' => [

 6        'cluster' => env('REDIS_CLUSTER', 'redis'),

 7        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),

 8    ],

 9 

10    'default' => [

11        'url' => env('REDIS_URL'),

12        'host' => env('REDIS_HOST', '127.0.0.1'),

13        'username' => env('REDIS_USERNAME'),

14        'password' => env('REDIS_PASSWORD'),

15        'port' => env('REDIS_PORT', '6379'),

16        'database' => env('REDIS_DB', '0'),

17    ],

18 

19    'cache' => [

20        'url' => env('REDIS_URL'),

21        'host' => env('REDIS_HOST', '127.0.0.1'),

22        'username' => env('REDIS_USERNAME'),

23        'password' => env('REDIS_PASSWORD'),

24        'port' => env('REDIS_PORT', '6379'),

25        'database' => env('REDIS_CACHE_DB', '1'),

26    ],

27 

28],
```

Each Redis server defined in your configuration file is required to have a name, host, and a port unless you define a single URL to represent the Redis connection:

```
 1'redis' => [

 2 

 3    'client' => env('REDIS_CLIENT', 'phpredis'),

 4 

 5    'options' => [

 6        'cluster' => env('REDIS_CLUSTER', 'redis'),

 7        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),

 8    ],

 9 

10    'default' => [

11        'url' => 'tcp://127.0.0.1:6379?database=0',

12    ],

13 

14    'cache' => [

15        'url' => 'tls://user:[[email protected]](/cdn-cgi/l/email-protection):6380?database=1',

16    ],

17 

18],
```

#### [Configuring the Connection Scheme](#configuring-the-connection-scheme)

By default, Redis clients will use the `tcp` scheme when connecting to your Redis servers; however, you may use TLS / SSL encryption by specifying a `scheme` configuration option in your Redis server's configuration array:

```
1'default' => [

2    'scheme' => 'tls',

3    'url' => env('REDIS_URL'),

4    'host' => env('REDIS_HOST', '127.0.0.1'),

5    'username' => env('REDIS_USERNAME'),

6    'password' => env('REDIS_PASSWORD'),

7    'port' => env('REDIS_PORT', '6379'),

8    'database' => env('REDIS_DB', '0'),

9],
```

### [Clusters](#clusters)

If your application is utilizing a cluster of Redis servers, you should define these clusters within a `clusters` key of your Redis configuration. This configuration key does not exist by default so you will need to create it within your application's `config/database.php` configuration file:

```
 1'redis' => [

 2 

 3    'client' => env('REDIS_CLIENT', 'phpredis'),

 4 

 5    'options' => [

 6        'cluster' => env('REDIS_CLUSTER', 'redis'),

 7        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),

 8    ],

 9 

10    'clusters' => [

11        'default' => [

12            [

13                'url' => env('REDIS_URL'),

14                'host' => env('REDIS_HOST', '127.0.0.1'),

15                'username' => env('REDIS_USERNAME'),

16                'password' => env('REDIS_PASSWORD'),

17                'port' => env('REDIS_PORT', '6379'),

18                'database' => env('REDIS_DB', '0'),

19            ],

20        ],

21    ],

22 

23    // ...

24],
```

By default, Laravel will use native Redis clustering since the `options.cluster` configuration value is set to `redis`. Redis clustering is a great default option, as it gracefully handles failover.

Laravel also supports client-side sharding when using Predis. However, client-side sharding does not handle failover; therefore, it is primarily suited for transient cached data that is available from another primary data store.

If you would like to use client-side sharding instead of native Redis clustering, you may remove the `options.cluster` configuration value within your application's `config/database.php` configuration file:

```
 1'redis' => [

 2 

 3    'client' => env('REDIS_CLIENT', 'phpredis'),

 4 

 5    'clusters' => [

 6        // ...

 7    ],

 8 

 9    // ...

10],
```

### [Predis](#predis)

If you would like your application to interact with Redis via the Predis package, you should ensure the `REDIS_CLIENT` environment variable's value is `predis`:

```
1'redis' => [

2 

3    'client' => env('REDIS_CLIENT', 'predis'),

4 

5    // ...

6],
```

In addition to the default configuration options, Predis supports additional [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters) that may be defined for each of your Redis servers. To utilize these additional configuration options, add them to your Redis server configuration in your application's `config/database.php` configuration file:

```
1'default' => [

2    'url' => env('REDIS_URL'),

3    'host' => env('REDIS_HOST', '127.0.0.1'),

4    'username' => env('REDIS_USERNAME'),

5    'password' => env('REDIS_PASSWORD'),

6    'port' => env('REDIS_PORT', '6379'),

7    'database' => env('REDIS_DB', '0'),

8    'read_write_timeout' => 60,

9],
```

### [PhpRedis](#phpredis)

By default, Laravel will use the PhpRedis extension to communicate with Redis. The client that Laravel will use to communicate with Redis is dictated by the value of the `redis.client` configuration option, which typically reflects the value of the `REDIS_CLIENT` environment variable:

```
1'redis' => [

2 

3    'client' => env('REDIS_CLIENT', 'phpredis'),

4 

5    // ...

6],
```

In addition to the default configuration options, PhpRedis supports the following additional connection parameters: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, and `context`. You may add any of these options to your Redis server configuration in the `config/database.php` configuration file:

```
 1'default' => [

 2    'url' => env('REDIS_URL'),

 3    'host' => env('REDIS_HOST', '127.0.0.1'),

 4    'username' => env('REDIS_USERNAME'),

 5    'password' => env('REDIS_PASSWORD'),

 6    'port' => env('REDIS_PORT', '6379'),

 7    'database' => env('REDIS_DB', '0'),

 8    'read_timeout' => 60,

 9    'context' => [

10        // 'auth' => ['username', 'secret'],

11        // 'stream' => ['verify_peer' => false],

12    ],

13],
```

#### [Retry and Backoff Configuration](#retry-and-backoff-configuration)

The `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, and `backoff_cap` options may be used to configure how the PhpRedis client should attempt to reconnect to a Redis server. The following backoff algorithms are supported: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, and `constant`:

```
 1'default' => [

 2    'url' => env('REDIS_URL'),

 3    'host' => env('REDIS_HOST', '127.0.0.1'),

 4    'username' => env('REDIS_USERNAME'),

 5    'password' => env('REDIS_PASSWORD'),

 6    'port' => env('REDIS_PORT', '6379'),

 7    'database' => env('REDIS_DB', '0'),

 8    'max_retries' => env('REDIS_MAX_RETRIES', 3),

 9    'backoff_algorithm' => env('REDIS_BACKOFF_ALGORITHM', 'decorrelated_jitter'),

10    'backoff_base' => env('REDIS_BACKOFF_BASE', 100),

11    'backoff_cap' => env('REDIS_BACKOFF_CAP', 1000),

12],
```

Predis 3.4.0 and later supports built-in retry and backoff configuration via the `Retry` class. You may configure retries using the `max_retries` option and configure the backoff strategy using the `retry` option. The `retry` option should be an array keyed by one of the following strategy classes: `NoBackoff`, `EqualBackoff`, or `ExponentialBackoff`:

```
 1use Predis\Retry\Strategy\ExponentialBackoff;

 2 

 3'default' => [

 4    'url' => env('REDIS_URL'),

 5    // ...

 6    'retry' => [

 7        ExponentialBackoff::class => [

 8            env('REDIS_BACKOFF_BASE', 100),

 9            env('REDIS_BACKOFF_CAP', 1000),

10            true, // Enable jitter...

11        ],

12    ],

13    'max_retries' => env('REDIS_MAX_RETRIES', 3),

14],
```

When using Predis with a Redis cluster, you may define retry configuration in the `parameters` option of your cluster configuration:

```
 1use Predis\Retry\Strategy\NoBackoff;

 2 

 3'clusters' => [

 4    'default' => [

 5        // ...

 6    ],

 7],

 8 

 9'options' => [

10    'cluster' => env('REDIS_CLUSTER', 'redis'),

11    'parameters' => [

12        'retry' => [

13            NoBackoff::class => [],

14        ],

15        'max_retries' => env('REDIS_MAX_RETRIES', 3),

16    ],

17],
```

#### [Unix Socket Connections](#unix-socket-connections)

Redis connections can also be configured to use Unix sockets instead of TCP. This can offer improved performance by eliminating TCP overhead for connections to Redis instances on the same server as your application. To configure Redis to use a Unix socket, set your `REDIS_HOST` environment variable to the path of the Redis socket and the `REDIS_PORT` environment variable to `0`:

```
1REDIS_HOST=/run/redis/redis.sock

2REDIS_PORT=0
```

#### [PhpRedis Serialization and Compression](#phpredis-serialization)

The PhpRedis extension may also be configured to use a variety of serializers and compression algorithms. These algorithms can be configured via the `options` array of your Redis configuration:

```
 1'redis' => [

 2 

 3    'client' => env('REDIS_CLIENT', 'phpredis'),

 4 

 5    'options' => [

 6        'cluster' => env('REDIS_CLUSTER', 'redis'),

 7        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),

 8        'serializer' => Redis::SERIALIZER_MSGPACK,

 9        'compression' => Redis::COMPRESSION_LZ4,

10    ],

11 

12    // ...

13],
```

Currently supported serializers include: `Redis::SERIALIZER_NONE` (default), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, and `Redis::SERIALIZER_MSGPACK`.

Supported compression algorithms include: `Redis::COMPRESSION_NONE` (default), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, and `Redis::COMPRESSION_LZ4`.

## [Interacting With Redis](#interacting-with-redis)

You may interact with Redis by calling various methods on the `Redis` [facade](/docs/13.x/facades). The `Redis` facade supports dynamic methods, meaning you may call any [Redis command](https://redis.io/commands) on the facade and the command will be passed directly to Redis. In this example, we will call the Redis `GET` command by calling the `get` method on the `Redis` facade:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Support\Facades\Redis;

 6use Illuminate\View\View;

 7 

 8class UserController extends Controller

 9{

10    /**

11     * Show the profile for the given user.

12     */

13    public function show(string $id): View

14    {

15        return view('user.profile', [

16            'user' => Redis::get('user:profile:'.$id)

17        ]);

18    }

19}
```

As mentioned above, you may call any of Redis' commands on the `Redis` facade. Laravel uses magic methods to pass the commands to the Redis server. If a Redis command expects arguments, you should pass those to the facade's corresponding method:

```
1use Illuminate\Support\Facades\Redis;

2 

3Redis::set('name', 'Taylor');

4 

5$values = Redis::lrange('names', 5, 10);
```

Alternatively, you may pass commands to the server using the `Redis` facade's `command` method, which accepts the name of the command as its first argument and an array of values as its second argument:

```
1$values = Redis::command('lrange', ['name', 5, 10]);
```

#### [Using Multiple Redis Connections](#using-multiple-redis-connections)

Your application's `config/database.php` configuration file allows you to define multiple Redis connections / servers. You may obtain a connection to a specific Redis connection using the `Redis` facade's `connection` method:

```
1$redis = Redis::connection('connection-name');
```

To obtain an instance of the default Redis connection, you may call the `connection` method without any additional arguments:

```
1$redis = Redis::connection();
```

### [Transactions](#transactions)

The `Redis` facade's `transaction` method provides a convenient wrapper around Redis' native `MULTI` and `EXEC` commands. The `transaction` method accepts a closure as its only argument. This closure will receive a Redis connection instance and may issue any commands it would like to this instance. All of the Redis commands issued within the closure will be executed in a single, atomic transaction:

```
1use Redis;

2use Illuminate\Support\Facades;

3 

4Facades\Redis::transaction(function (Redis $redis) {

5    $redis->incr('user_visits', 1);

6    $redis->incr('total_visits', 1);

7});
```

When defining a Redis transaction, you may not retrieve any values from the Redis connection. Remember, your transaction is executed as a single, atomic operation and that operation is not executed until your entire closure has finished executing its commands.

#### Lua Scripts

The `eval` method provides another method of executing multiple Redis commands in a single, atomic operation. However, the `eval` method has the benefit of being able to interact with and inspect Redis key values during that operation. Redis scripts are written in the [Lua programming language](https://www.lua.org).

The `eval` method can be a bit scary at first, but we'll explore a basic example to break the ice. The `eval` method expects several arguments. First, you should pass the Lua script (as a string) to the method. Secondly, you should pass the number of keys (as an integer) that the script interacts with. Thirdly, you should pass the names of those keys. Finally, you may pass any other additional arguments that you need to access within your script.

In this example, we will increment a counter, inspect its new value, and increment a second counter if the first counter's value is greater than five. Finally, we will return the value of the first counter:

```
1$value = Redis::eval(<<<'LUA'

2    local counter = redis.call("incr", KEYS[1])

3 

4    if counter > 5 then

5        redis.call("incr", KEYS[2])

6    end

7 

8    return counter

9LUA, 2, 'first-counter', 'second-counter');
```

Please consult the [Redis documentation](https://redis.io/commands/eval) for more information on Redis scripting.

### [Pipelining Commands](#pipelining-commands)

Sometimes you may need to execute dozens of Redis commands. Instead of making a network trip to your Redis server for each command, you may use the `pipeline` method. The `pipeline` method accepts one argument: a closure that receives a Redis instance. You may issue all of your commands to this Redis instance and they will all be sent to the Redis server at the same time to reduce network trips to the server. The commands will still be executed in the order they were issued:

```
1use Redis;

2use Illuminate\Support\Facades;

3 

4Facades\Redis::pipeline(function (Redis $pipe) {

5    for ($i = 0; $i < 1000; $i++) {

6        $pipe->set("key:$i", $i);

7    }

8});
```

## [Pub / Sub](#pubsub)

Laravel provides a convenient interface to the Redis `publish` and `subscribe` commands. These Redis commands allow you to listen for messages on a given "channel". You may publish messages to the channel from another application, or even using another programming language, allowing easy communication between applications and processes.

First, let's set up a channel listener using the `subscribe` method. We'll place this method call within an [Artisan command](/docs/13.x/artisan) since calling the `subscribe` method begins a long-running process:

```
 1<?php

 2 

 3namespace App\Console\Commands;

 4 

 5use Illuminate\Console\Command;

 6use Illuminate\Support\Facades\Redis;

 7 

 8class RedisSubscribe extends Command

 9{

10    /**

11     * The name and signature of the console command.

12     *

13     * @var string

14     */

15    protected $signature = 'redis:subscribe';

16 

17    /**

18     * The console command description.

19     *

20     * @var string

21     */

22    protected $description = 'Subscribe to a Redis channel';

23 

24    /**

25     * Execute the console command.

26     */

27    public function handle(): void

28    {

29        Redis::subscribe(['test-channel'], function (string $message) {

30            echo $message;

31        });

32    }

33}
```

Now we may publish messages to the channel using the `publish` method:

```
1use Illuminate\Support\Facades\Redis;

2 

3Route::get('/publish', function () {

4    // ...

5 

6    Redis::publish('test-channel', json_encode([

7        'name' => 'Adam Wathan'

8    ]));

9});
```

#### [Wildcard Subscriptions](#wildcard-subscriptions)

Using the `psubscribe` method, you may subscribe to a wildcard channel, which may be useful for catching all messages on all channels. The channel name will be passed as the second argument to the provided closure:

```
1Redis::psubscribe(['*'], function (string $message, string $channel) {

2    echo $message;

3});

4 

5Redis::psubscribe(['users.*'], function (string $message, string $channel) {

6    echo $message;

7});
```
