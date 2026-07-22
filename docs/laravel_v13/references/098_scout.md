# Laravel Scout

- [Introduction](#introduction)
- [Installation](#installation)
  * [Queueing](#queueing)
- [Driver Prerequisites](#driver-prerequisites)
- [Configuration](#configuration)
  * [Configuring Searchable Data](#configuring-searchable-data)
- [Database / Collection Engines](#database-and-collection-engines)
  * [Database Engine](#database-engine)
  * [Collection Engine](#collection-engine)
- [Third-Party Engine Configuration](#third-party-engine-configuration)
  * [Configuring Model Indexes](#configuring-model-indexes)
  * [Algolia](#algolia-configuration)
  * [Meilisearch](#meilisearch-configuration)
  * [Typesense](#typesense-configuration)
- [Third-Party Engine Indexing](#indexing)
  * [Batch Import](#batch-import)
  * [Adding Records](#adding-records)
  * [Updating Records](#updating-records)
  * [Removing Records](#removing-records)
  * [Pausing Indexing](#pausing-indexing)
  * [Conditionally Searchable Model Instances](#conditionally-searchable-model-instances)
- [Searching](#searching)
  * [Where Clauses](#where-clauses)
  * [Pagination](#pagination)
  * [Soft Deleting](#soft-deleting)
  * [Customizing Engine Searches](#customizing-engine-searches)
- [Custom Engines](#custom-engines)

## [Introduction](#introduction)

[Laravel Scout](https://github.com/laravel/scout) provides a simple, driver-based solution for adding full-text search to your [Eloquent models](/docs/13.x/eloquent). Using model observers, Scout will automatically keep your search indexes in sync with your Eloquent records.

Scout ships with a built-in `database` engine that uses MySQL / PostgreSQL full-text indexes and `LIKE` clauses to search your existing database — no external service required. For most applications, this is all you need. For an overview of all search options available in Laravel, consult the [search documentation](/docs/13.x/search).

Scout also includes drivers for [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), and [Typesense](https://typesense.org) when you need features like typo tolerance, faceted filtering, or geo-search at massive scale. A "collection" driver is also available for local development, and you are free to write [custom engines](#custom-engines) as well.

## [Installation](#installation)

First, install Scout via the Composer package manager:

```
1composer require laravel/scout
```

After installing Scout, you should publish the Scout configuration file using the `vendor:publish` Artisan command. This command will publish the `scout.php` configuration file to your application's `config` directory:

```
1php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

Finally, add the `Laravel\Scout\Searchable` trait to the model you would like to make searchable. This trait will register a model observer that will automatically keep the model in sync with your search driver:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Database\Eloquent\Model;

 6use Laravel\Scout\Searchable;

 7 

 8class Post extends Model

 9{

10    use Searchable;

11}
```

### [Queueing](#queueing)

When using an engine that is not the `database` or `collection` engine, you should strongly consider configuring a [queue driver](/docs/13.x/queues) before using the library. Running a queue worker will allow Scout to queue all operations that sync your model information to your search indexes, providing much better response times for your application's web interface.

Once you have configured a queue driver, set the value of the `queue` option in your `config/scout.php` configuration file to `true`:

```
1'queue' => true,
```

Even when the `queue` option is set to `false`, it's important to remember that some Scout drivers like Algolia and Meilisearch always index records asynchronously. In other words, even though the index operation has completed within your Laravel application, the search engine itself may not reflect the new and updated records immediately.

To specify the connection and queue that your Scout jobs utilize, you may define the `queue` configuration option as an array:

```
1'queue' => [

2    'connection' => 'redis',

3    'queue' => 'scout'

4],
```

Of course, if you customize the connection and queue that Scout jobs utilize, you should run a queue worker to process jobs on that connection and queue:

```
1php artisan queue:work redis --queue=scout
```

#### [Unique Jobs](#unique-jobs)

In write-heavy applications, you may wish to prevent Scout from queueing duplicate jobs for the same model records. You may opt into unique indexing jobs by registering the `MakeSearchableUniquely` and `RemoveFromSearchUniquely` job classes, typically within the `boot` method of a service provider:

```
1use Laravel\Scout\Jobs\MakeSearchableUniquely;

2use Laravel\Scout\Jobs\RemoveFromSearchUniquely;

3use Laravel\Scout\Scout;

4 

5Scout::makeSearchableUsing(MakeSearchableUniquely::class);

6Scout::removeFromSearchUsing(RemoveFromSearchUniquely::class);
```

These jobs use Laravel's [unique job locks](/docs/13.x/queues#unique-jobs) to avoid dispatching duplicate queued indexing operations for the same searchable model records while a matching job is already queued.

## [Driver Prerequisites](#driver-prerequisites)

### [Algolia](#algolia)

When using the Algolia driver, you should configure your Algolia `id` and `secret` credentials in your `config/scout.php` configuration file. Once your credentials have been configured, you will also need to install the Algolia PHP SDK via the Composer package manager:

```
1composer require algolia/algoliasearch-client-php
```

### [Meilisearch](#meilisearch)

[Meilisearch](https://www.meilisearch.com) is a fast, open source search engine. If you aren't sure how to install Meilisearch on your local machine, you may use [Laravel Sail](/docs/13.x/sail#meilisearch), Laravel's officially supported Docker development environment.

When using the Meilisearch driver you will need to install the Meilisearch PHP SDK via the Composer package manager:

```
1composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```

Then, set the `SCOUT_DRIVER` environment variable as well as your Meilisearch `host` and `key` credentials within your application's `.env` file:

```
1SCOUT_DRIVER=meilisearch

2MEILISEARCH_HOST=http://127.0.0.1:7700

3MEILISEARCH_KEY=masterKey
```

For more information regarding Meilisearch, please consult the [Meilisearch documentation](https://docs.meilisearch.com/learn/getting_started/quick_start.html).

In addition, you should ensure that you install a version of `meilisearch/meilisearch-php` that is compatible with your Meilisearch binary version by reviewing [Meilisearch's documentation regarding binary compatibility](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch).

When upgrading Scout on an application that utilizes Meilisearch, you should always [review any additional breaking changes](https://github.com/meilisearch/Meilisearch/releases) to the Meilisearch service itself.

### [Typesense](#typesense)

[Typesense](https://typesense.org) is a lightning-fast, open source search engine and supports keyword search, semantic search, geo search, and vector search.

You can [self-host](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting) Typesense or use [Typesense Cloud](https://cloud.typesense.org).

To get started using Typesense with Scout, install the Typesense PHP SDK via the Composer package manager:

```
1composer require typesense/typesense-php
```

Then, set the `SCOUT_DRIVER` environment variable as well as your Typesense host and API key credentials within your application's .env file:

```
1SCOUT_DRIVER=typesense

2TYPESENSE_API_KEY=masterKey

3TYPESENSE_HOST=localhost
```

If you are using [Laravel Sail](/docs/13.x/sail), you may need to adjust the `TYPESENSE_HOST` environment variable to match the Docker container name. You may also optionally specify your installation's port, path, and protocol:

```
1TYPESENSE_PORT=8108

2TYPESENSE_PATH=

3TYPESENSE_PROTOCOL=http
```

Additional settings and schema definitions for your Typesense collections can be found within your application's `config/scout.php` configuration file. For more information regarding Typesense, please consult the [Typesense documentation](https://typesense.org/docs/guide/#quick-start).

## [Configuration](#configuration)

### [Configuring Searchable Data](#configuring-searchable-data)

By default, the entire `toArray` form of a given model will be persisted to its search index. If you would like to customize the data that is synchronized to the search index, you may override the `toSearchableArray` method on the model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Database\Eloquent\Model;

 6use Laravel\Scout\Searchable;

 7 

 8class Post extends Model

 9{

10    use Searchable;

11 

12    /**

13     * Get the indexable data array for the model.

14     *

15     * @return array<string, mixed>

16     */

17    public function toSearchableArray(): array

18    {

19        $array = $this->toArray();

20 

21        // Customize the data array...

22 

23        return $array;

24    }

25}
```

#### [Configuring Model Engines](#configuring-search-engines-per-model)

When searching, Scout will typically use the default search engine specified in your application's `scout` configuration file. However, the search engine for a particular model can be changed by overriding the `searchableUsing` method on the model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Database\Eloquent\Model;

 6use Laravel\Scout\Engines\Engine;

 7use Laravel\Scout\Scout;

 8use Laravel\Scout\Searchable;

 9 

10class User extends Model

11{

12    use Searchable;

13 

14    /**

15     * Get the engine used to index the model.

16     */

17    public function searchableUsing(): Engine

18    {

19        return Scout::engine('meilisearch');

20    }

21}
```

## [Database / Collection Engines](#database-and-collection-engines)

### [Database Engine](#database-engine)

The database engine currently supports MySQL and PostgreSQL, both of which provide support for fast, full-text column indexing.

The `database` engine uses MySQL / PostgreSQL full-text indexes and `LIKE` clauses to search your existing database directly. For many applications, this is the simplest and most practical way to add search — no external service or additional infrastructure required.

To use the database engine, set the `SCOUT_DRIVER` environment variable to `database`:

```
1SCOUT_DRIVER=database
```

Once configured, you may [define your searchable data](#configuring-searchable-data) and start [executing search queries](#searching) against your models. Unlike third-party engines, the database engine requires no separate indexing step — it searches your database tables directly.

#### Customizing Database Searching Strategies

By default, the database engine will execute a `LIKE` query against every model attribute that you have [configured as searchable](#configuring-searchable-data). However, you can assign more efficient search strategies to specific columns. The `SearchUsingFullText` attribute will use your database's full-text index for that column, while `SearchUsingPrefix` will only match the beginning of strings (`example%`) instead of searching within the entire string (`%example%`).

To define this behavior, assign PHP attributes to your model's `toSearchableArray` method. Any columns without an attribute will continue to use the default `LIKE` strategy:

```
 1use Laravel\Scout\Attributes\SearchUsingFullText;

 2use Laravel\Scout\Attributes\SearchUsingPrefix;

 3 

 4/**

 5 * Get the indexable data array for the model.

 6 *

 7 * @return array<string, mixed>

 8 */

 9#[SearchUsingPrefix(['id', 'email'])]

10#[SearchUsingFullText(['bio'])]

11public function toSearchableArray(): array

12{

13    return [

14        'id' => $this->id,

15        'name' => $this->name,

16        'email' => $this->email,

17        'bio' => $this->bio,

18    ];

19}
```

Before specifying that a column should use full text query constraints, ensure that the column has been assigned a [full text index](/docs/13.x/migrations#available-index-types).

### [Collection Engine](#collection-engine)

The "collection" engine is intended for quick prototypes, extremely small datasets (a few hundred records), or running tests. It retrieves all possible records from your database and uses Laravel's `Str::is` helper to filter them in PHP, so it does not require any indexing or database-specific features. For anything beyond trivial use cases, you should use the [database engine](#database-engine) instead.

To use the collection engine, you may simply set the value of the `SCOUT_DRIVER` environment variable to `collection`, or specify the `collection` driver directly in your application's `scout` configuration file:

```
1SCOUT_DRIVER=collection
```

Once you have specified the collection driver as your preferred driver, you may start [executing search queries](#searching) against your models. Search engine indexing, such as the indexing needed to seed Algolia, Meilisearch, or Typesense indexes, is unnecessary when using the collection engine.

#### Differences From Database Engine

While the database engine uses full-text indexes and `LIKE` clauses to find matching records efficiently, the collection engine pulls all records and filters them in PHP. The collection engine is the most portable option as it works across all relational databases supported by Laravel (including SQLite and SQL Server); however, it is significantly less efficient than the database engine and should not be used with large datasets.

## [Third-Party Engine Configuration](#third-party-engine-configuration)

The following configuration options are only relevant when using a third-party search engine such as Algolia, Meilisearch, or Typesense. If you are using the [database engine](#database-engine), you may skip this section.

### [Configuring Model Indexes](#configuring-model-indexes)

When using a third-party engine, each Eloquent model is synced with a given search "index", which contains all of the searchable records for that model. By default, each model will be persisted to an index matching the model's typical "table" name. Typically, this is the plural form of the model name; however, you are free to customize the model's index by overriding the `searchableAs` method on the model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Database\Eloquent\Model;

 6use Laravel\Scout\Searchable;

 7 

 8class Post extends Model

 9{

10    use Searchable;

11 

12    /**

13     * Get the name of the index associated with the model.

14     */

15    public function searchableAs(): string

16    {

17        return 'posts_index';

18    }

19}
```

The `searchableAs` method has no effect when using the database engine, which always searches the model's database table directly.

#### [Configuring the Model ID](#configuring-the-model-id)

By default, Scout will use the primary key of the model as the model's unique ID / key that is stored in the search index. If you need to customize this behavior when using a third-party engine, you may override the `getScoutKey` and the `getScoutKeyName` methods on the model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Database\Eloquent\Model;

 6use Laravel\Scout\Searchable;

 7 

 8class User extends Model

 9{

10    use Searchable;

11 

12    /**

13     * Get the value used to index the model.

14     */

15    public function getScoutKey(): mixed

16    {

17        return $this->email;

18    }

19 

20    /**

21     * Get the key name used to index the model.

22     */

23    public function getScoutKeyName(): mixed

24    {

25        return 'email';

26    }

27}
```

The `getScoutKey` and `getScoutKeyName` methods have no effect when using the database engine, which always uses the model's primary key.

### [Algolia](#algolia-configuration)

#### [Index Settings](#algolia-index-settings)

Sometimes you may want to configure additional settings on your Algolia indexes. While you can manage these settings via the Algolia UI, it is sometimes more efficient to manage the desired state of your index configuration directly from your application's `config/scout.php` configuration file.

This approach allows you to deploy these settings through your application's automated deployment pipeline, avoiding manual configuration and ensuring consistency across multiple environments. You may configure filterable attributes, ranking, faceting, or [any other supported settings](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings).

To get started, add settings for each index in your application's `config/scout.php` configuration file:

```
 1use App\Models\User;

 2use App\Models\Flight;

 3 

 4'algolia' => [

 5    'id' => env('ALGOLIA_APP_ID', ''),

 6    'secret' => env('ALGOLIA_SECRET', ''),

 7    'index-settings' => [

 8        User::class => [

 9            'searchableAttributes' => ['id', 'name', 'email'],

10            'attributesForFaceting'=> ['filterOnly(email)'],

11            // Other settings fields...

12        ],

13        Flight::class => [

14            'searchableAttributes'=> ['id', 'destination'],

15        ],

16    ],

17],
```

If the model underlying a given index is soft deletable and is included in the `index-settings` array, Scout will automatically include support for faceting on soft deleted models on that index. If you have no other faceting attributes to define for a soft deletable model index, you may simply add an empty entry to the `index-settings` array for that model:

```
1'index-settings' => [

2    Flight::class => []

3],
```

After configuring your application's index settings, you must invoke the `scout:sync-index-settings` Artisan command. This command will inform Algolia of your currently configured index settings. For convenience, you may wish to make this command part of your deployment process:

```
1php artisan scout:sync-index-settings
```

#### [Identifying Users](#algolia-identifying-users)

Scout allows you to auto identify users when using Algolia. Associating the authenticated user with search operations may be helpful when viewing your search analytics within Algolia's dashboard. You can enable user identification by defining a `SCOUT_IDENTIFY` environment variable as `true` in your application's `.env` file:

```
1SCOUT_IDENTIFY=true
```

Enabling this feature will also pass the request's IP address and your authenticated user's primary identifier to Algolia so this data is associated with any search request that is made by the user.

### [Meilisearch](#meilisearch-configuration)

#### [Index Settings](#meilisearch-index-settings)

Meilisearch requires you to pre-define index search settings such as filterable attributes, sortable attributes, and [other supported settings fields](https://docs.meilisearch.com/reference/api/settings.html).

Filterable attributes are any attributes you plan to filter on when invoking Scout's `where` method, while sortable attributes are any attributes you plan to sort by when invoking Scout's `orderBy` method. To define your index settings, adjust the `index-settings` portion of your `meilisearch` configuration entry in your application's `scout` configuration file:

```
 1use App\Models\User;

 2use App\Models\Flight;

 3 

 4'meilisearch' => [

 5    'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),

 6    'key' => env('MEILISEARCH_KEY', null),

 7    'index-settings' => [

 8        User::class => [

 9            'filterableAttributes'=> ['id', 'name', 'email'],

10            'sortableAttributes' => ['created_at'],

11            // Other settings fields...

12        ],

13        Flight::class => [

14            'filterableAttributes'=> ['id', 'destination'],

15            'sortableAttributes' => ['updated_at'],

16        ],

17    ],

18],
```

If the model underlying a given index is soft deletable and is included in the `index-settings` array, Scout will automatically include support for filtering on soft deleted models on that index. If you have no other filterable or sortable attributes to define for a soft deletable model index, you may simply add an empty entry to the `index-settings` array for that model:

```
1'index-settings' => [

2    Flight::class => []

3],
```

After configuring your application's index settings, you must invoke the `scout:sync-index-settings` Artisan command. This command will inform Meilisearch of your currently configured index settings. For convenience, you may wish to make this command part of your deployment process:

```
1php artisan scout:sync-index-settings
```

#### [Searchable Data Types](#meilisearch-data-types)

Meilisearch will only perform filter operations (`>`, `<`, etc.) on data of the correct type. When customizing your searchable data, you should ensure that numeric values are cast to their correct type:

```
1public function toSearchableArray()

2{

3    return [

4        'id' => (int) $this->id,

5        'name' => $this->name,

6        'price' => (float) $this->price,

7    ];

8}
```

### [Typesense](#typesense-configuration)

#### [Preparing Searchable Data](#typesense-searchable-data)

When utilizing Typesense, your searchable models must define a `toSearchableArray` method that casts your model's primary key to a string and creation date to a UNIX timestamp:

```
 1/**

 2 * Get the indexable data array for the model.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toSearchableArray(): array

 7{

 8    return array_merge($this->toArray(),[

 9        'id' => (string) $this->id,

10        'created_at' => $this->created_at->timestamp,

11    ]);

12}
```

You should also define your Typesense collection schemas in your application's `config/scout.php` file. A collection schema describes the data types of each field that is searchable via Typesense. For more information on all available schema options, please consult the [Typesense documentation](https://typesense.org/docs/latest/api/collections.html#schema-parameters).

If you need to change your Typesense collection's schema after it has been defined, you may either run `scout:flush` and `scout:import`, which will delete all existing indexed data and recreate the schema. Or, you may use Typesense's API to modify the collection's schema without removing any indexed data.

If your searchable model is soft deletable, you should define a `__soft_deleted` field in the model's corresponding Typesense schema within your application's `config/scout.php` configuration file:

```
 1User::class => [

 2    'collection-schema' => [

 3        'fields' => [

 4            // ...

 5            [

 6                'name' => '__soft_deleted',

 7                'type' => 'int32',

 8                'optional' => true,

 9            ],

10        ],

11    ],

12],
```

#### [Dynamic Search Parameters](#typesense-dynamic-search-parameters)

Typesense allows you to modify your [search parameters](https://typesense.org/docs/latest/api/search.html#search-parameters) dynamically when performing a search operation via the `options` method:

```
1use App\Models\Todo;

2 

3Todo::search('Groceries')->options([

4    'query_by' => 'title, description'

5])->get();
```

## [Third-Party Engine Indexing](#indexing)

The indexing features described in this section are primarily relevant when using a third-party engine (Algolia, Meilisearch, or Typesense). The database engine searches your database tables directly, so it does not require manual index management.

### [Batch Import](#batch-import)

If you are installing Scout into an existing project, you may already have database records you need to import into your indexes. Scout provides a `scout:import` Artisan command that you may use to import all of your existing records into your search indexes:

```
1php artisan scout:import "App\Models\Post"
```

The `scout:queue-import` command may be used to import all of your existing records using [queued jobs](/docs/13.x/queues):

```
1php artisan scout:queue-import "App\Models\Post" --chunk=500
```

The `flush` command may be used to remove all of a model's records from your search indexes:

```
1php artisan scout:flush "App\Models\Post"
```

#### [Modifying the Import Query](#modifying-the-import-query)

If you would like to modify the query that is used to retrieve all of your models for batch importing, you may define a `makeAllSearchableUsing` method on your model. This is a great place to add any eager relationship loading that may be necessary before importing your models:

```
1use Illuminate\Database\Eloquent\Builder;

2 

3/**

4 * Modify the query used to retrieve models when making all of the models searchable.

5 */

6protected function makeAllSearchableUsing(Builder $query): Builder

7{

8    return $query->with('author');

9}
```

The `makeAllSearchableUsing` method may not be applicable when using a queue to batch import models. Relationships are [not restored](/docs/13.x/queues#handling-relationships) when model collections are processed by jobs.

### [Adding Records](#adding-records)

Once you have added the `Laravel\Scout\Searchable` trait to a model, all you need to do is `save` or `create` a model instance and it will automatically be added to your search index. If you have configured Scout to [use queues](#queueing) this operation will be performed in the background by your queue worker:

```
1use App\Models\Order;

2 

3$order = new Order;

4 

5// ...

6 

7$order->save();
```

#### [Adding Records via Query](#adding-records-via-query)

If you would like to add a collection of models to your search index via an Eloquent query, you may chain the `searchable` method onto the Eloquent query. The `searchable` method will [chunk the results](/docs/13.x/eloquent#chunking-results) of the query and add the records to your search index. Again, if you have configured Scout to use queues, all of the chunks will be imported in the background by your queue workers:

```
1use App\Models\Order;

2 

3Order::where('price', '>', 100)->searchable();
```

You may also call the `searchable` method on an Eloquent relationship instance:

```
1$user->orders()->searchable();
```

Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to add the model instances to their corresponding index:

```
1$orders->searchable();
```

The `searchable` method can be considered an "upsert" operation. In other words, if the model record is already in your index, it will be updated. If it does not exist in the search index, it will be added to the index.

### [Updating Records](#updating-records)

To update a searchable model, you only need to update the model instance's properties and `save` the model to your database. Scout will automatically persist the changes to your search index:

```
1use App\Models\Order;

2 

3$order = Order::find(1);

4 

5// Update the order...

6 

7$order->save();
```

You may also invoke the `searchable` method on an Eloquent query instance to update a collection of models. If the models do not exist in your search index, they will be created:

```
1Order::where('price', '>', 100)->searchable();
```

If you would like to update the search index records for all of the models in a relationship, you may invoke the `searchable` on the relationship instance:

```
1$user->orders()->searchable();
```

Or, if you already have a collection of Eloquent models in memory, you may call the `searchable` method on the collection instance to update the model instances in their corresponding index:

```
1$orders->searchable();
```

#### [Modifying Records Before Importing](#modifying-records-before-importing)

Sometimes you may need to prepare the collection of models before they are made searchable. For instance, you may want to eager load a relationship so that the relationship data can be efficiently added to your search index. To accomplish this, define a `makeSearchableUsing` method on the corresponding model:

```
1use Illuminate\Database\Eloquent\Collection;

2 

3/**

4 * Modify the collection of models being made searchable.

5 */

6public function makeSearchableUsing(Collection $models): Collection

7{

8    return $models->load('author');

9}
```

#### [Conditionally Updating the Search Index](#conditionally-updating-the-search-index)

By default, Scout will reindex an updated model regardless of which attributes were modified. If you would like to customize this behavior, you may define a `searchIndexShouldBeUpdated` method on your model:

```
1/**

2 * Determine if the search index should be updated.

3 */

4public function searchIndexShouldBeUpdated(): bool

5{

6    return $this->wasRecentlyCreated || $this->wasChanged(['title', 'body']);

7}
```

### [Removing Records](#removing-records)

To remove a record from your index you may simply `delete` the model from the database. This may be done even if you are using [soft deleted](/docs/13.x/eloquent#soft-deleting) models:

```
1use App\Models\Order;

2 

3$order = Order::find(1);

4 

5$order->delete();
```

If you do not want to retrieve the model before deleting the record, you may use the `unsearchable` method on an Eloquent query instance:

```
1Order::where('price', '>', 100)->unsearchable();
```

If you would like to remove the search index records for all of the models in a relationship, you may invoke the `unsearchable` on the relationship instance:

```
1$user->orders()->unsearchable();
```

Or, if you already have a collection of Eloquent models in memory, you may call the `unsearchable` method on the collection instance to remove the model instances from their corresponding index:

```
1$orders->unsearchable();
```

To remove all of the model records from their corresponding index, you may invoke the `removeAllFromSearch` method:

```
1Order::removeAllFromSearch();
```

### [Pausing Indexing](#pausing-indexing)

Sometimes you may need to perform a batch of Eloquent operations on a model without syncing the model data to your search index. You may do this using the `withoutSyncingToSearch` method. This method accepts a single closure which will be immediately executed. Any model operations that occur within the closure will not be synced to the model's index:

```
1use App\Models\Order;

2 

3Order::withoutSyncingToSearch(function () {

4    // Perform model actions...

5});
```

### [Conditionally Searchable Model Instances](#conditionally-searchable-model-instances)

Sometimes you may need to only make a model searchable under certain conditions. For example, imagine you have `App\Models\Post` model that may be in one of two states: "draft" and "published". You may only want to allow "published" posts to be searchable. To accomplish this, you may define a `shouldBeSearchable` method on your model:

```
1/**

2 * Determine if the model should be searchable.

3 */

4public function shouldBeSearchable(): bool

5{

6    return $this->isPublished();

7}
```

The `shouldBeSearchable` method is only applied when manipulating models through the `save` and `create` methods, queries, or relationships. Directly making models or collections searchable using the `searchable` method will override the result of the `shouldBeSearchable` method.

The `shouldBeSearchable` method is not applicable when using Scout's "database" engine, as all searchable data is always stored in the database. To achieve similar behavior when using the database engine, you should use [where clauses](#where-clauses) instead.

## [Searching](#searching)

You may begin searching a model using the `search` method. The search method accepts a single string that will be used to search your models. You should then chain the `get` method onto the search query to retrieve the Eloquent models that match the given search query:

```
1use App\Models\Order;

2 

3$orders = Order::search('Star Trek')->get();
```

Since Scout searches return a collection of Eloquent models, you may even return the results directly from a route or controller and they will automatically be converted to JSON:

```
1use App\Models\Order;

2use Illuminate\Http\Request;

3 

4Route::get('/search', function (Request $request) {

5    return Order::search($request->search)->get();

6});
```

If you would like to get the raw search results before they are converted to Eloquent models, you may use the `raw` method:

```
1$orders = Order::search('Star Trek')->raw();
```

#### [Custom Indexes](#custom-indexes)

When searching using third-party engines, search queries will typically be performed on the index specified by the model's [searchableAs](#configuring-model-indexes) method. However, you may use the `within` method to specify a custom index that should be searched instead:

```
1$orders = Order::search('Star Trek')

2    ->within('tv_shows_popularity_desc')

3    ->get();
```

### [Where Clauses](#where-clauses)

Scout allows you to add "where" clauses to your search queries. For example, basic equality checks are useful for scoping search queries by an owner ID:

```
1use App\Models\Order;

2 

3$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```

You may also use the `=`, `!=`, `<`, `>`, `>=`, `<=` comparison operators to build more advanced queries:

```
1Order::search('Star Trek')

2  ->where('status', '=', 'completed')

3  ->where('is_refunded', '!=', true)

4  ->where('total_price', '>', 100)

5  ->where('shipping_cost', '<', 20)

6  ->where('discount_percent', '>=', 10)

7  ->where('item_count', '<=', 5)

8  ->get();
```

In addition, the `whereIn` method may be used to verify that a given column's value is contained within the given array:

```
1$orders = Order::search('Star Trek')->whereIn(

2    'status', ['open', 'paid']

3)->get();
```

The `whereNotIn` method verifies that the given column's value is not contained in the given array:

```
1$orders = Order::search('Star Trek')->whereNotIn(

2    'status', ['closed']

3)->get();
```

If your application is using Meilisearch, you must configure your application's [filterable attributes](#meilisearch-index-settings) before utilizing Scout's "where" clauses.

#### [Customizing the Eloquent Results Query](#customizing-the-eloquent-results-query)

After Scout retrieves a list of matching Eloquent models from your application's search engine, Eloquent is used to retrieve all of the matching models by their primary keys. You may customize this query by invoking the `query` method. The `query` method accepts a closure that will receive the Eloquent query builder instance as an argument:

```
1use App\Models\Order;

2use Illuminate\Database\Eloquent\Builder;

3 

4$orders = Order::search('Star Trek')

5    ->query(fn (Builder $query) => $query->with('invoices'))

6    ->get();
```

When using a third-party engine, this callback is invoked after the relevant models have already been retrieved from the search engine, so it should not be used for "filtering" results — use [Scout where clauses](#where-clauses) instead. However, when using the database engine, the `query` method's constraints are applied directly to the database query, so you may use it for filtering as well.

### [Pagination](#pagination)

In addition to retrieving a collection of models, you may paginate your search results using the `paginate` method. This method will return an `Illuminate\Pagination\LengthAwarePaginator` instance just as if you had [paginated a traditional Eloquent query](/docs/13.x/pagination):

```
1use App\Models\Order;

2 

3$orders = Order::search('Star Trek')->paginate();
```

You may specify how many models to retrieve per page by passing the amount as the first argument to the `paginate` method:

```
1$orders = Order::search('Star Trek')->paginate(15);
```

When using the database engine, you may also use the `simplePaginate` method. Unlike `paginate`, which retrieves the total number of matching records so it can display page numbers, `simplePaginate` only determines whether there are more results beyond the current page — making it more efficient for large datasets where you only need "previous" and "next" links:

```
1$orders = Order::search('Star Trek')->simplePaginate(15);
```

Once you have retrieved the results, you may display the results and render the page links using [Blade](/docs/13.x/blade) just as if you had paginated a traditional Eloquent query:

```
1<div class="container">

2    @foreach ($orders as $order)

3        {{ $order->price }}

4    @endforeach

5</div>

6 

7{{ $orders->links() }}
```

Of course, if you would like to retrieve the pagination results as JSON, you may return the paginator instance directly from a route or controller:

```
1use App\Models\Order;

2use Illuminate\Http\Request;

3 

4Route::get('/orders', function (Request $request) {

5    return Order::search($request->input('query'))->paginate(15);

6});
```

Since search engines are not aware of your Eloquent model's global scope definitions, you should not utilize global scopes in applications that utilize Scout pagination. Or, you should recreate the global scope's constraints when searching via Scout.

### [Soft Deleting](#soft-deleting)

If your indexed models are [soft deleting](/docs/13.x/eloquent#soft-deleting) and you need to search your soft deleted models, set the `soft_delete` option of the `config/scout.php` configuration file to `true`:

```
1'soft_delete' => true,
```

When this configuration option is `true`, Scout will not remove soft deleted models from the search index. Instead, it will set a hidden `__soft_deleted` attribute on the indexed record. Then, you may use the `withTrashed` or `onlyTrashed` methods to retrieve the soft deleted records when searching:

```
1use App\Models\Order;

2 

3// Include trashed records when retrieving results...

4$orders = Order::search('Star Trek')->withTrashed()->get();

5 

6// Only include trashed records when retrieving results...

7$orders = Order::search('Star Trek')->onlyTrashed()->get();
```

When a soft deleted model is permanently deleted using `forceDelete`, Scout will remove it from the search index automatically.

### [Customizing Engine Searches](#customizing-engine-searches)

If you need to perform advanced customization of the search behavior of an engine you may pass a closure as the second argument to the `search` method. For example, you could use this callback to add geo-location data to your search options before the search query is passed to Algolia:

```
 1use Algolia\AlgoliaSearch\SearchIndex;

 2use App\Models\Order;

 3 

 4Order::search(

 5    'Star Trek',

 6    function (SearchIndex $algolia, string $query, array $options) {

 7        $options['body']['query']['bool']['filter']['geo_distance'] = [

 8            'distance' => '1000km',

 9            'location' => ['lat' => 36, 'lon' => 111],

10        ];

11 

12        return $algolia->search($query, $options);

13    }

14)->get();
```

## [Custom Engines](#custom-engines)

#### [Writing the Engine](#writing-the-engine)

If one of the built-in Scout search engines doesn't fit your needs, you may write your own custom engine and register it with Scout. Your engine should extend the `Laravel\Scout\Engines\Engine` abstract class. This abstract class contains eight methods your custom engine must implement:

```
 1use Laravel\Scout\Builder;

 2 

 3abstract public function update($models);

 4abstract public function delete($models);

 5abstract public function search(Builder $builder);

 6abstract public function paginate(Builder $builder, $perPage, $page);

 7abstract public function mapIds($results);

 8abstract public function map(Builder $builder, $results, $model);

 9abstract public function getTotalCount($results);

10abstract public function flush($model);
```

You may find it helpful to review the implementations of these methods on the `Laravel\Scout\Engines\AlgoliaEngine` class. This class will provide you with a good starting point for learning how to implement each of these methods in your own engine.

#### [Registering the Engine](#registering-the-engine)

Once you have written your custom engine, you may register it with Scout using the `extend` method of the Scout engine manager. Scout's engine manager may be resolved from the Laravel service container. You should call the `extend` method from the `boot` method of your `App\Providers\AppServiceProvider` class or any other service provider used by your application:

```
 1use App\ScoutExtensions\MySqlSearchEngine;

 2use Laravel\Scout\EngineManager;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    resolve(EngineManager::class)->extend('mysql', function () {

10        return new MySqlSearchEngine;

11    });

12}
```

Once your engine has been registered, you may specify it as your default Scout `driver` in your application's `config/scout.php` configuration file:

```
1'driver' => 'mysql',
```
