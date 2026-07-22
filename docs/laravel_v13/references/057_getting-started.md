# Database: Getting Started

- [Introduction](#introduction)
  * [Configuration](#configuration)
  * [Read and Write Connections](#read-and-write-connections)
  * [Pooled PostgreSQL Connections](#pooled-postgresql-connections)
- [Running SQL Queries](#running-queries)
  * [Using Multiple Database Connections](#using-multiple-database-connections)
  * [Listening for Query Events](#listening-for-query-events)
  * [Monitoring Cumulative Query Time](#monitoring-cumulative-query-time)
- [Database Transactions](#database-transactions)
- [Connecting to the Database CLI](#connecting-to-the-database-cli)
- [Inspecting Your Databases](#inspecting-your-databases)
- [Monitoring Your Databases](#monitoring-your-databases)

## [Introduction](#introduction)

Almost every modern web application interacts with a database. Laravel makes interacting with databases extremely simple across a variety of supported databases using raw SQL, a [fluent query builder](/docs/13.x/queries), and the [Eloquent ORM](/docs/13.x/eloquent). Currently, Laravel provides first-party support for five databases:

- MariaDB 10.3+ ([Version Policy](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([Version Policy](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([Version Policy](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([Version Policy](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

Additionally, MongoDB is supported via the `mongodb/laravel-mongodb` package, which is officially maintained by MongoDB. Check out the [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) documentation for more information.

### [Configuration](#configuration)

The configuration for Laravel's database services is located in your application's `config/database.php` configuration file. In this file, you may define all of your database connections, as well as specify which connection should be used by default. Most of the configuration options within this file are driven by the values of your application's environment variables. Examples for most of Laravel's supported database systems are provided in this file.

By default, Laravel's sample [environment configuration](/docs/13.x/configuration#environment-configuration) is ready to use with [Laravel Sail](/docs/13.x/sail), which is a Docker configuration for developing Laravel applications on your local machine. However, you are free to modify your database configuration as needed for your local database.

#### [SQLite Configuration](#sqlite-configuration)

SQLite databases are contained within a single file on your filesystem. You can create a new SQLite database using the `touch` command in your terminal: `touch database/database.sqlite`. After the database has been created, you may easily configure your environment variables to point to this database by placing the absolute path to the database in the `DB_DATABASE` environment variable:

```
1DB_CONNECTION=sqlite

2DB_DATABASE=/absolute/path/to/database.sqlite
```

By default, foreign key constraints are enabled for SQLite connections. If you would like to disable them, you should set the `DB_FOREIGN_KEYS` environment variable to `false`:

```
1DB_FOREIGN_KEYS=false
```

If you use the [Laravel installer](/docs/13.x/installation#creating-a-laravel-project) to create your Laravel application and select SQLite as your database, Laravel will automatically create a `database/database.sqlite` file and run the default [database migrations](/docs/13.x/migrations) for you.

#### [Microsoft SQL Server Configuration](#mssql-configuration)

To use a Microsoft SQL Server database, you should ensure that you have the `sqlsrv` and `pdo_sqlsrv` PHP extensions installed as well as any dependencies they may require such as the Microsoft SQL ODBC driver.

#### [Configuration Using URLs](#configuration-using-urls)

Typically, database connections are configured using multiple configuration values such as `host`, `database`, `username`, `password`, etc. Each of these configuration values has its own corresponding environment variable. This means that when configuring your database connection information on a production server, you need to manage several environment variables.

Some managed database providers such as AWS and Heroku provide a single database "URL" that contains all of the connection information for the database in a single string. An example database URL may look something like the following:

```
1mysql://root:[[email protected]](/cdn-cgi/l/email-protection)/forge?charset=UTF-8
```

These URLs typically follow a standard schema convention:

```
1driver://username:password@host:port/database?options
```

For convenience, Laravel supports these URLs as an alternative to configuring your database with multiple configuration options. If the `url` (or corresponding `DB_URL` environment variable) configuration option is present, it will be used to extract the database connection and credential information.

### [Read and Write Connections](#read-and-write-connections)

Sometimes you may wish to use one database connection for SELECT statements, and another for INSERT, UPDATE, and DELETE statements. Laravel makes this a breeze, and the proper connections will always be used whether you are using raw queries, the query builder, or the Eloquent ORM.

To see how read / write connections should be configured, let's look at this example:

```
 1'mysql' => [

 2    'driver' => 'mysql',

 3 

 4    'read' => [

 5        'host' => [

 6            '192.168.1.1',

 7            '196.168.1.2',

 8        ],

 9    ],

10    'write' => [

11        'host' => [

12            '192.168.1.3',

13        ],

14    ],

15    'sticky' => true,

16 

17    'port' => env('DB_PORT', '3306'),

18    'database' => env('DB_DATABASE', 'laravel'),

19    'username' => env('DB_USERNAME', 'root'),

20    'password' => env('DB_PASSWORD', ''),

21    'unix_socket' => env('DB_SOCKET', ''),

22    'charset' => env('DB_CHARSET', 'utf8mb4'),

23    'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),

24    'prefix' => '',

25    'prefix_indexes' => true,

26    'strict' => true,

27    'engine' => null,

28    'options' => extension_loaded('pdo_mysql') ? array_filter([

29        (PHP_VERSION_ID >= 80500 ? \Pdo\Mysql::ATTR_SSL_CA : \PDO::MYSQL_ATTR_SSL_CA) => env('MYSQL_ATTR_SSL_CA'),

30    ]) : [],

31],
```

Note that three keys have been added to the configuration array: `read`, `write` and `sticky`. The `read` and `write` keys have array values containing a single key: `host`. The rest of the database options for the `read` and `write` connections will be merged from the main `mysql` configuration array.

You only need to place items in the `read` and `write` arrays if you wish to override the values from the main `mysql` array. So, in this case, `192.168.1.1` will be used as the host for the "read" connection, while `192.168.1.3` will be used for the "write" connection. The database credentials, prefix, character set, and all other options in the main `mysql` array will be shared across both connections. When multiple values exist in the `host` configuration array, a database host will be randomly chosen for each request.

#### [The `sticky` Option](#the-sticky-option)

The `sticky` option is an *optional* value that can be used to allow the immediate reading of records that have been written to the database during the current request cycle. If the `sticky` option is enabled and a "write" operation has been performed against the database during the current request cycle, any further "read" operations will use the "write" connection. This ensures that any data written during the request cycle can be immediately read back from the database during that same request. It is up to you to decide if this is the desired behavior for your application.

### [Pooled PostgreSQL Connections](#pooled-postgresql-connections)

Many managed PostgreSQL providers offer transaction-mode connection pooling through services such as PgBouncer or connection proxying. These poolers are ideal for application queries, but some schema operations, migrations, and maintenance commands require a direct database connection.

To use a transaction pooler with PostgreSQL, configure the pooled connection as usual and provide direct connection details via the `direct` configuration option:

```
 1'pgsql' => [

 2    'driver' => 'pgsql',

 3    // ...

 4    'pooled' => env('DB_POOLED', false),

 5    'direct' => array_filter([

 6        'host' => env('DB_DIRECT_HOST'),

 7        'port' => env('DB_DIRECT_PORT'),

 8        'username' => env('DB_DIRECT_USERNAME'),

 9        'password' => env('DB_DIRECT_PASSWORD'),

10        'sslmode' => env('DB_DIRECT_SSLMODE'),

11    ]),

12],
```

When a PostgreSQL connection is configured as pooled, Laravel automatically enables emulated prepares for the pooled connection. The direct connection inherits any options not explicitly defined in the `direct` configuration and uses native prepares by default.

Laravel automatically uses the direct connection for migrations, schema dumps and restores, `db:wipe`, `db:show`, and `db:table`. The `db` command also uses the direct connection by default when pooled mode is enabled and a direct connection is configured; you may pass the `--pooled` option to connect to the pooled connection instead:

```
1php artisan db --pooled
```

If you need to explicitly use the direct connection in your application, append the `::direct` suffix to the connection name:

```
1DB::connection('pgsql::direct')->statement('create extension if not exists "uuid-ossp"');
```

## [Running SQL Queries](#running-queries)

Once you have configured your database connection, you may run queries using the `DB` facade. The `DB` facade provides methods for each type of query: `select`, `update`, `insert`, `delete`, and `statement`.

#### [Running a Select Query](#running-a-select-query)

To run a basic SELECT query, you may use the `select` method on the `DB` facade:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Support\Facades\DB;

 6use Illuminate\View\View;

 7 

 8class UserController extends Controller

 9{

10    /**

11     * Show a list of all of the application's users.

12     */

13    public function index(): View

14    {

15        $users = DB::select('select * from users where active = ?', [1]);

16 

17        return view('user.index', ['users' => $users]);

18    }

19}
```

The first argument passed to the `select` method is the SQL query, while the second argument is any parameter bindings that need to be bound to the query. Typically, these are the values of the `where` clause constraints. Parameter binding provides protection against SQL injection.

The `select` method will always return an `array` of results. Each result within the array will be a PHP `stdClass` object representing a record from the database:

```
1use Illuminate\Support\Facades\DB;

2 

3$users = DB::select('select * from users');

4 

5foreach ($users as $user) {

6    echo $user->name;

7}
```

#### [Selecting Scalar Values](#selecting-scalar-values)

Sometimes your database query may result in a single, scalar value. Instead of being required to retrieve the query's scalar result from a record object, Laravel allows you to retrieve this value directly using the `scalar` method:

```
1$burgers = DB::scalar(

2    "select count(case when food = 'burger' then 1 end) as burgers from menu"

3);
```

#### [Selecting Multiple Result Sets](#selecting-multiple-result-sets)

If your application calls stored procedures that return multiple result sets, you may use the `selectResultSets` method to retrieve all of the result sets returned by the stored procedure:

```
1[$options, $notifications] = DB::selectResultSets(

2    "CALL get_user_options_and_notifications(?)", $request->user()->id

3);
```

#### [Using Named Bindings](#using-named-bindings)

Instead of using `?` to represent your parameter bindings, you may execute a query using named bindings:

```
1$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

#### [Running an Insert Statement](#running-an-insert-statement)

To execute an `insert` statement, you may use the `insert` method on the `DB` facade. Like `select`, this method accepts the SQL query as its first argument and bindings as its second argument:

```
1use Illuminate\Support\Facades\DB;

2 

3DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

#### [Running an Update Statement](#running-an-update-statement)

The `update` method should be used to update existing records in the database. The number of rows affected by the statement is returned by the method:

```
1use Illuminate\Support\Facades\DB;

2 

3$affected = DB::update(

4    'update users set votes = 100 where name = ?',

5    ['Anita']

6);
```

#### [Running a Delete Statement](#running-a-delete-statement)

The `delete` method should be used to delete records from the database. Like `update`, the number of rows affected will be returned by the method:

```
1use Illuminate\Support\Facades\DB;

2 

3$deleted = DB::delete('delete from users');
```

#### [Running a General Statement](#running-a-general-statement)

Some database statements do not return any value. For these types of operations, you may use the `statement` method on the `DB` facade:

```
1DB::statement('drop table users');
```

#### [Running an Unprepared Statement](#running-an-unprepared-statement)

Sometimes you may want to execute an SQL statement without binding any values. You may use the `DB` facade's `unprepared` method to accomplish this:

```
1DB::unprepared('update users set votes = 100 where name = "Dries"');
```

Since unprepared statements do not bind parameters, they may be vulnerable to SQL injection. You should never allow user controlled values within an unprepared statement.

#### [Implicit Commits](#implicit-commits-in-transactions)

When using the `DB` facade's `statement` and `unprepared` methods within transactions you must be careful to avoid statements that cause [implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). These statements will cause the database engine to indirectly commit the entire transaction, leaving Laravel unaware of the database's transaction level. An example of such a statement is creating a database table:

```
1DB::unprepared('create table a (col varchar(1) null)');
```

Please refer to the MySQL manual for [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) that trigger implicit commits.

### [Using Multiple Database Connections](#using-multiple-database-connections)

If your application defines multiple connections in your `config/database.php` configuration file, you may access each connection via the `connection` method provided by the `DB` facade. The connection name passed to the `connection` method should correspond to one of the connections listed in your `config/database.php` configuration file or configured at runtime using the `config` helper:

```
1use Illuminate\Support\Facades\DB;

2 

3$users = DB::connection('sqlite')->select(/* ... */);
```

You may access the raw, underlying PDO instance of a connection using the `getPdo` method on a connection instance:

```
1$pdo = DB::connection()->getPdo();
```

### [Listening for Query Events](#listening-for-query-events)

If you would like to specify a closure that is invoked for each SQL query executed by your application, you may use the `DB` facade's `listen` method. This method can be useful for logging queries or debugging. You may register your query listener closure in the `boot` method of a [service provider](/docs/13.x/providers):

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Database\Events\QueryExecuted;

 6use Illuminate\Support\Facades\DB;

 7use Illuminate\Support\ServiceProvider;

 8 

 9class AppServiceProvider extends ServiceProvider

10{

11    /**

12     * Register any application services.

13     */

14    public function register(): void

15    {

16        // ...

17    }

18 

19    /**

20     * Bootstrap any application services.

21     */

22    public function boot(): void

23    {

24        DB::listen(function (QueryExecuted $query) {

25            // $query->sql;

26            // $query->bindings;

27            // $query->time;

28            // $query->toRawSql();

29        });

30    }

31}
```

### [Monitoring Cumulative Query Time](#monitoring-cumulative-query-time)

A common performance bottleneck of modern web applications is the amount of time they spend querying databases. Thankfully, Laravel can invoke a closure or callback of your choice when it spends too much time querying the database during a single request. To get started, provide a query time threshold (in milliseconds) and closure to the `whenQueryingForLongerThan` method. You may invoke this method in the `boot` method of a [service provider](/docs/13.x/providers):

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Database\Connection;

 6use Illuminate\Support\Facades\DB;

 7use Illuminate\Support\ServiceProvider;

 8use Illuminate\Database\Events\QueryExecuted;

 9 

10class AppServiceProvider extends ServiceProvider

11{

12    /**

13     * Register any application services.

14     */

15    public function register(): void

16    {

17        // ...

18    }

19 

20    /**

21     * Bootstrap any application services.

22     */

23    public function boot(): void

24    {

25        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {

26            // Notify development team...

27        });

28    }

29}
```

## [Database Transactions](#database-transactions)

You may use the `transaction` method provided by the `DB` facade to run a set of operations within a database transaction. If an exception is thrown within the transaction closure, the transaction will automatically be rolled back and the exception is re-thrown. If the closure executes successfully, the transaction will automatically be committed. You don't need to worry about manually rolling back or committing while using the `transaction` method:

```
1use Illuminate\Support\Facades\DB;

2 

3DB::transaction(function () {

4    DB::update('update users set votes = 1');

5 

6    DB::delete('delete from posts');

7});
```

#### [Handling Deadlocks](#handling-deadlocks)

The `transaction` method accepts an optional second argument which defines the number of times a transaction should be retried when a deadlock occurs. Once these attempts have been exhausted, an exception will be thrown:

```
1use Illuminate\Support\Facades\DB;

2 

3DB::transaction(function () {

4    DB::update('update users set votes = 1');

5 

6    DB::delete('delete from posts');

7}, attempts: 5);
```

#### [Manually Using Transactions](#manually-using-transactions)

If you would like to begin a transaction manually and have complete control over rollbacks and commits, you may use the `beginTransaction` method provided by the `DB` facade:

```
1use Illuminate\Support\Facades\DB;

2 

3DB::beginTransaction();
```

You can rollback the transaction via the `rollBack` method:

```
1DB::rollBack();
```

Lastly, you can commit a transaction via the `commit` method:

```
1DB::commit();
```

The `DB` facade's transaction methods control the transactions for both the [query builder](/docs/13.x/queries) and [Eloquent ORM](/docs/13.x/eloquent).

## [Connecting to the Database CLI](#connecting-to-the-database-cli)

If you would like to connect to your database's CLI, you may use the `db` Artisan command:

```
1php artisan db
```

If needed, you may specify a database connection name to connect to a database connection that is not the default connection:

```
1php artisan db mysql
```

## [Inspecting Your Databases](#inspecting-your-databases)

Using the `db:show` and `db:table` Artisan commands, you can get valuable insight into your database and its associated tables. To see an overview of your database, including its size, type, number of open connections, and a summary of its tables, you may use the `db:show` command:

```
1php artisan db:show
```

You may specify which database connection should be inspected by providing the database connection name to the command via the `--database` option:

```
1php artisan db:show --database=pgsql
```

If you would like to include table row counts and database view details within the output of the command, you may provide the `--counts` and `--views` options, respectively. On large databases, retrieving row counts and view details can be slow:

```
1php artisan db:show --counts --views
```

In addition, you may use the following `Schema` methods to inspect your database:

```
1use Illuminate\Support\Facades\Schema;

2 

3$tables = Schema::getTables();

4$views = Schema::getViews();

5$columns = Schema::getColumns('users');

6$indexes = Schema::getIndexes('users');

7$foreignKeys = Schema::getForeignKeys('users');
```

If you would like to inspect a database connection that is not your application's default connection, you may use the `connection` method:

```
1$columns = Schema::connection('sqlite')->getColumns('users');
```

#### [Table Overview](#table-overview)

If you would like to get an overview of an individual table within your database, you may execute the `db:table` Artisan command. This command provides a general overview of a database table, including its columns, types, attributes, keys, and indexes:

```
1php artisan db:table users
```

## [Monitoring Your Databases](#monitoring-your-databases)

Using the `db:monitor` Artisan command, you can instruct Laravel to dispatch an `Illuminate\Database\Events\DatabaseBusy` event if your database is managing more than a specified number of open connections.

To get started, you should schedule the `db:monitor` command to [run every minute](/docs/13.x/scheduling). The command accepts the names of the database connection configurations that you wish to monitor as well as the maximum number of open connections that should be tolerated before dispatching an event:

```
1php artisan db:monitor --databases=mysql,pgsql --max=100
```

Scheduling this command alone is not enough to trigger a notification alerting you of the number of open connections. When the command encounters a database that has an open connection count that exceeds your threshold, a `DatabaseBusy` event will be dispatched. You should listen for this event within your application's `AppServiceProvider` in order to send a notification to you or your development team:

```
 1use App\Notifications\DatabaseApproachingMaxConnections;

 2use Illuminate\Database\Events\DatabaseBusy;

 3use Illuminate\Support\Facades\Event;

 4use Illuminate\Support\Facades\Notification;

 5 

 6/**

 7 * Bootstrap any application services.

 8 */

 9public function boot(): void

10{

11    Event::listen(function (DatabaseBusy $event) {

12        Notification::route('mail', '[[email protected]](/cdn-cgi/l/email-protection)')

13            ->notify(new DatabaseApproachingMaxConnections(

14                $event->connectionName,

15                $event->connections

16            ));

17    });

18}
```
