# Search

- [Introduction](#introduction)
  * [Full-Text Search](#introduction-full-text-search)
  * [Semantic / Vector Search](#introduction-semantic-vector-search)
  * [Reranking](#introduction-reranking)
  * [Scout Search Engines](#introduction-scout-search-engines)
- [Full-Text Search](#full-text-search)
  * [Adding Full-Text Indexes](#adding-full-text-indexes)
  * [Running Full-Text Queries](#running-full-text-queries)
- [Semantic / Vector Search](#semantic-vector-search)
  * [Generating Embeddings](#generating-embeddings)
  * [Storing and Indexing Vectors](#storing-and-indexing-vectors)
  * [Querying by Similarity](#querying-by-similarity)
- [Reranking Results](#reranking-results)
- [Laravel Scout](#laravel-scout)
  * [Database Engine](#database-engine)
  * [Third-Party Engines](#third-party-engines)
- [Combining Techniques](#combining-techniques)

## [Introduction](#introduction)

Almost every application needs search. Whether your users are searching a knowledge base for relevant articles, exploring a product catalog, or asking natural-language questions against a corpus of documents, Laravel provides built-in tools to handle each of these scenarios — and you often don't need any external services to get there.

Most applications will find that the built-in database-powered options provided by Laravel are more than sufficient — external search services are only necessary when you need features like typo tolerance, faceted filtering, or geo-search at massive scale.

#### [Full-Text Search](#introduction-full-text-search)

When you need keyword relevance ranking — where the database scores and sorts results based on how well they match the search terms — Laravel's `whereFullText` query builder method leverages native full-text indexes on MariaDB, MySQL, and PostgreSQL. Full-text search understands word boundaries and stemming, so a search for "running" can match records containing "run". No external service is required.

#### [Semantic / Vector Search](#introduction-semantic-vector-search)

For AI-powered semantic search that matches results by *meaning* rather than exact keywords, the `whereVectorSimilarTo` query builder method uses vector embeddings stored in PostgreSQL with the `pgvector` extension. For example, a search for "best wineries in Napa Valley" can surface an article titled "Top Vineyards to Visit" — even though the words don't overlap. Vector search requires PostgreSQL with the `pgvector` extension and the [Laravel AI SDK](/docs/13.x/ai-sdk).

#### [Reranking](#introduction-reranking)

Laravel's [AI SDK](/docs/13.x/ai-sdk) provides reranking capabilities that use AI models to reorder any set of results by semantic relevance to a query. Reranking is especially powerful as a second stage after a fast initial retrieval step like full-text search — giving you both speed and semantic accuracy.

#### [Laravel Scout Search](#introduction-scout-search-engines)

For applications that want a `Searchable` trait that automatically keeps search indexes in sync with Eloquent models, [Laravel Scout](/docs/13.x/scout) offers both a built-in database engine and drivers for third-party services like Algolia, Meilisearch, and Typesense.

## [Full-Text Search](#full-text-search)

While `LIKE` queries work well for simple substring matching, they don't understand language. A `LIKE` search for "running" won't find a record containing "run", and results aren't ranked by relevance — they're simply returned in whatever order the database finds them. Full-text search solves both of these problems by using specialized indexes that understand word boundaries, stemming, and relevance scoring, allowing the database to return the most relevant results first.

Fast full-text search is built into MariaDB, MySQL, and PostgreSQL — no external search service is required. You only need to add a full-text index to the columns you want to search, and then use the `whereFullText` query builder method to search against them.

Full-text search is currently supported by MariaDB, MySQL, and PostgreSQL.

### [Adding Full-Text Indexes](#adding-full-text-indexes)

To use full-text search, first add a full-text index to the columns you want to search. You may add the index to a single column, or pass an array of columns to create a composite index that searches across multiple fields at once:

```
1Schema::create('articles', function (Blueprint $table) {

2    $table->id();

3    $table->string('title');

4    $table->text('body');

5    $table->timestamps();

6 

7    $table->fullText(['title', 'body']);

8});
```

On PostgreSQL, you may specify a language configuration for the index, which controls how words are stemmed:

```
1$table->fullText('body')->language('english');
```

For more information on creating indexes, consult the [migration documentation](/docs/13.x/migrations#available-index-types).

### [Running Full-Text Queries](#running-full-text-queries)

Once the index is in place, use the `whereFullText` query builder method to search against it. Laravel will generate the appropriate SQL for your database driver — for example, `MATCH(...) AGAINST(...)` on MariaDB and MySQL, and `to_tsvector(...) @@ plainto_tsquery(...)` on PostgreSQL:

```
1$articles = Article::whereFullText('body', 'web developer')->get();
```

When using MariaDB and MySQL, results are automatically ordered by relevance score. On PostgreSQL, `whereFullText` filters matching records but does not order them by relevance — if you need automatic relevance ordering on PostgreSQL, consider using [Scout's database engine](#database-engine), which handles this for you.

If you created a composite full-text index across multiple columns, you may search against all of them by passing the same array of columns to `whereFullText`:

```
1$articles = Article::whereFullText(

2    ['title', 'body'], 'web developer'

3)->get();
```

The `orWhereFullText` method may be used to add a full-text search clause as an "or" condition. For complete details, consult the [query builder documentation](/docs/13.x/queries#full-text-where-clauses).

## [Semantic / Vector Search](#semantic-vector-search)

Full-text search relies on matching keywords — the words in the query must appear (in some form) in the data. Semantic search takes a fundamentally different approach: it uses AI-generated vector embeddings to represent the *meaning* of text as arrays of numbers, and then finds results whose meaning is most similar to the query. For example, a search for "best wineries in Napa Valley" can surface an article titled "Top Vineyards to Visit" — even though the words don't overlap at all.

The basic workflow for vector search is: generate an embedding (a numeric array) for each piece of content and store it alongside your data, then at search time, generate an embedding for the user's query and find the stored embeddings that are closest to it in vector space.

Vector search requires the [Laravel AI SDK](/docs/13.x/ai-sdk) and is supported by PostgreSQL (requires the `pgvector` extension) and MongoDB (requires the [Laravel MongoDB package](https://laravel.com/docs/13.x/mongodb)). All Postgres databases on [Laravel Cloud](https://laravel.com/cloud) already have `pgvector` installed.

### [Generating Embeddings](#generating-embeddings)

An embedding is a high-dimensional numeric array (typically hundreds or thousands of numbers) that represents the semantic meaning of a piece of text. You may generate embeddings for a string using the `toEmbeddings` method available on Laravel's `Stringable` class:

```
1use Illuminate\Support\Str;

2 

3$embedding = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

To generate embeddings for multiple inputs at once — which is more efficient than generating them one at a time since it requires only a single API call to the embedding provider — use the `Embeddings` class:

```
1use Laravel\Ai\Embeddings;

2 

3$response = Embeddings::for([

4    'Napa Valley has great wine.',

5    'Laravel is a PHP framework.',

6])->generate();

7 

8$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

For more details on configuring embedding providers, customizing dimensions, and caching, consult the [AI SDK documentation](/docs/13.x/ai-sdk#embeddings).

### [Storing and Indexing Vectors](#storing-and-indexing-vectors)

To store vector embeddings, define a `vector` column in your migration, specifying the number of dimensions that matches your embedding provider's output (for example, 1536 for OpenAI's `text-embedding-3-small` model). You should also call `index` on the column to create an HNSW (Hierarchical Navigable Small World) index, which dramatically speeds up similarity searches on large datasets:

```
1Schema::ensureVectorExtensionExists();

2 

3Schema::create('documents', function (Blueprint $table) {

4    $table->id();

5    $table->string('title');

6    $table->text('content');

7    $table->vector('embedding', dimensions: 1536)->index();

8    $table->timestamps();

9});
```

The `Schema::ensureVectorExtensionExists` method ensures the `pgvector` extension is enabled on your PostgreSQL database before creating the table.

On your Eloquent model, cast the vector column to an `array` so that Laravel automatically handles the conversion between PHP arrays and the database's vector format:

```
1protected function casts(): array

2{

3    return [

4        'embedding' => 'array',

5    ];

6}
```

For more details on vector columns and indexes, consult the [migration documentation](/docs/13.x/migrations#available-column-types).

### [Querying by Similarity](#querying-by-similarity)

Once you have stored embeddings for your content, you can search for similar records using the `whereVectorSimilarTo` method. This method compares the given embedding against the stored vectors using cosine similarity, filters out results below the `minSimilarity` threshold, and automatically orders the results by relevance — with the most similar records first. The threshold should be a value between `0.0` and `1.0`, where `1.0` means the vectors are identical:

```
1$documents = Document::query()

2    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)

3    ->limit(10)

4    ->get();
```

As a convenience, when a plain string is given instead of an embedding array, Laravel will automatically generate the embedding for you using your configured embedding provider. This means you can pass the user's search query directly without manually converting it to an embedding first:

```
1$documents = Document::query()

2    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')

3    ->limit(10)

4    ->get();
```

For lower-level control over vector queries, the `whereVectorDistanceLessThan`, `selectVectorDistance`, and `orderByVectorDistance` methods are also available. These methods let you work directly with distance values rather than similarity scores, select the computed distance as a column in your results, or manually control the ordering. For complete details, consult the [query builder documentation](/docs/13.x/queries#vector-similarity-clauses) and the [AI SDK documentation](/docs/13.x/ai-sdk#querying-embeddings).

## [Reranking Results](#reranking-results)

Reranking is a technique where an AI model reorders a set of results by how semantically relevant each result is to a given query. Unlike vector search, which requires you to pre-compute and store embeddings, reranking works on any collection of text — it takes the raw content and the query as input and returns the items sorted by relevance.

Reranking is especially powerful as a second stage after a fast initial retrieval step. For example, you might use full-text search to quickly narrow thousands of records down to the top 50 candidates, and then use reranking to put the most relevant results at the top. This "retrieve then rerank" pattern gives you both speed and semantic accuracy.

You may rerank an array of strings using the `Reranking` class:

```
1use Laravel\Ai\Reranking;

2 

3$response = Reranking::of([

4    'Django is a Python web framework.',

5    'Laravel is a PHP web application framework.',

6    'React is a JavaScript library for building user interfaces.',

7])->rerank('PHP frameworks');

8 

9$response->first()->document; // "Laravel is a PHP web application framework."
```

Laravel collections also have a `rerank` macro that accepts a field name (or closure) and a query, making it easy to rerank Eloquent results:

```
1$articles = Article::all()

2    ->rerank('body', 'Laravel tutorials');
```

For complete details on configuring reranking providers and available options, consult the [AI SDK documentation](/docs/13.x/ai-sdk#reranking).

## [Laravel Scout](#laravel-scout)

The search techniques described above are all query builder methods that you call directly in your code. [Laravel Scout](/docs/13.x/scout) takes a different approach: it provides a `Searchable` trait that you add to your Eloquent models, and Scout automatically keeps your search indexes in sync as records are created, updated, and deleted. This is particularly convenient when you want your models to always be searchable without manually managing index updates.

### [Database Engine](#database-engine)

Scout's built-in database engine performs full-text and `LIKE` searches against your existing database — no external service or extra infrastructure required. Simply add the `Searchable` trait to your model and define a `toSearchableArray` method that returns the columns you want to be searchable.

You may use PHP attributes to control the search strategy for each column. `SearchUsingFullText` will use your database's full-text index, `SearchUsingPrefix` will only match from the beginning of the string (`example%`), and any columns without an attribute use a default `LIKE` strategy with wildcards on both sides (`%example%`):

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Database\Eloquent\Model;

 6use Laravel\Scout\Attributes\SearchUsingFullText;

 7use Laravel\Scout\Attributes\SearchUsingPrefix;

 8use Laravel\Scout\Searchable;

 9 

10class Article extends Model

11{

12    use Searchable;

13 

14    #[SearchUsingPrefix(['id'])]

15    #[SearchUsingFullText(['title', 'body'])]

16    public function toSearchableArray(): array

17    {

18        return [

19            'id' => $this->id,

20            'title' => $this->title,

21            'body' => $this->body,

22        ];

23    }

24}
```

Before specifying that a column should use full-text query constraints, ensure that the column has been assigned a [full-text index](/docs/13.x/migrations#available-index-types).

Once the trait is added, you may search your model using Scout's `search` method. Scout's database engine will automatically order results by relevance, even on PostgreSQL:

```
1$articles = Article::search('Laravel')->get();
```

The database engine is a great choice when your search needs are moderate and you want the convenience of Scout's automatic index syncing without deploying an external service. It handles the most common search use cases well, including filtering, pagination, and soft-deleted record handling. For complete details, consult the [Scout documentation](/docs/13.x/scout#database-engine).

### [Third-Party Engines](#third-party-engines)

Scout also supports third-party search engines such as [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), and [Typesense](https://typesense.org). These dedicated search services offer advanced features like typo tolerance, faceted filtering, geo-search, and custom ranking rules — features that become important at very large scale or when you need a highly polished search-as-you-type experience.

Since Scout provides a unified API across all of its drivers, switching from the database engine to a third-party engine later requires minimal code changes. You may start with the database engine and migrate to a third-party service only if your application's needs outgrow what the database can provide.

For complete details on configuring third-party engines, consult the [Scout documentation](/docs/13.x/scout).

Many applications never need an external search engine. The built-in techniques described on this page cover the vast majority of use cases.

## [Combining Techniques](#combining-techniques)

The search techniques described on this page are not mutually exclusive — combining them often produces the best results. Here are two common patterns that demonstrate how these tools work together.

**Full-Text Retrieval + Reranking**

Use full-text search to quickly narrow a large dataset down to a candidate set, then apply reranking to sort those candidates by semantic relevance. This gives you the speed of database-native full-text search with the accuracy of AI-powered relevance scoring:

```
1$articles = Article::query()

2    ->whereFullText('body', $request->input('query'))

3    ->limit(50)

4    ->get()

5    ->rerank('body', $request->input('query'), limit: 10);
```

**Vector Search + Traditional Filters**

Combine vector similarity with standard `where` clauses to scope semantic search to a subset of records. This is useful when you want meaning-based search but need to restrict results by ownership, category, or any other attribute:

```
1$documents = Document::query()

2    ->where('team_id', $user->team_id)

3    ->whereVectorSimilarTo('embedding', $request->input('query'))

4    ->limit(10)

5    ->get();
```
