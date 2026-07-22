# Eloquent: API Resources

- [Introduction](#introduction)
- [Generating Resources](#generating-resources)
- [Concept Overview](#concept-overview)
  * [Resource Collections](#resource-collections)
- [Writing Resources](#writing-resources)
  * [Data Wrapping](#data-wrapping)
  * [Pagination](#pagination)
  * [Conditional Attributes](#conditional-attributes)
  * [Conditional Relationships](#conditional-relationships)
  * [Adding Meta Data](#adding-meta-data)
- [JSON:API Resources](#jsonapi-resources)
  * [Generating JSON:API Resources](#generating-jsonapi-resources)
  * [Defining Attributes](#defining-jsonapi-attributes)
  * [Defining Relationships](#defining-jsonapi-relationships)
  * [Resource Type and ID](#jsonapi-resource-type-and-id)
  * [Sparse Fieldsets and Includes](#jsonapi-sparse-fieldsets-and-includes)
  * [Links and Meta](#jsonapi-links-and-meta)
- [Resource Responses](#resource-responses)

## [Introduction](#introduction)

When building an API, you may need a transformation layer that sits between your Eloquent models and the JSON responses that are actually returned to your application's users. For example, you may wish to display certain attributes for a subset of users and not others, or you may wish to always include certain relationships in the JSON representation of your models. Eloquent's resource classes allow you to expressively and easily transform your models and model collections into JSON.

Of course, you may always convert Eloquent models or collections to JSON using their `toJson` methods; however, Eloquent resources provide more granular and robust control over the JSON serialization of your models and their relationships.

## [Generating Resources](#generating-resources)

To generate a resource class, you may use the `make:resource` Artisan command. By default, resources will be placed in the `app/Http/Resources` directory of your application. Resources extend the `Illuminate\Http\Resources\Json\JsonResource` class:

```
1php artisan make:resource UserResource
```

#### [Resource Collections](#generating-resource-collections)

In addition to generating resources that transform individual models, you may generate resources that are responsible for transforming collections of models. This allows your JSON responses to include links and other meta information that is relevant to an entire collection of a given resource.

To create a resource collection, you should use the `--collection` flag when creating the resource. Or, including the word `Collection` in the resource name will indicate to Laravel that it should create a collection resource. Collection resources extend the `Illuminate\Http\Resources\Json\ResourceCollection` class:

```
1php artisan make:resource User --collection

2 

3php artisan make:resource UserCollection
```

## [Concept Overview](#concept-overview)

This is a high-level overview of resources and resource collections. You are highly encouraged to read the other sections of this documentation to gain a deeper understanding of the customization and power offered to you by resources.

Before diving into all of the options available to you when writing resources, let's first take a high-level look at how resources are used within Laravel. A resource class represents a single model that needs to be transformed into a JSON structure. For example, here is a simple `UserResource` resource class:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Request;

 6use Illuminate\Http\Resources\Json\JsonResource;

 7 

 8class UserResource extends JsonResource

 9{

10    /**

11     * Transform the resource into an array.

12     *

13     * @return array<string, mixed>

14     */

15    public function toArray(Request $request): array

16    {

17        return [

18            'id' => $this->id,

19            'name' => $this->name,

20            'email' => $this->email,

21            'created_at' => $this->created_at,

22            'updated_at' => $this->updated_at,

23        ];

24    }

25}
```

Every resource class defines a `toArray` method which returns the array of attributes that should be converted to JSON when the resource is returned as a response from a route or controller method.

Note that we can access model properties directly from the `$this` variable. This is because a resource class will automatically proxy property and method access down to the underlying model for convenient access. Once the resource is defined, it may be returned from a route or controller. The resource accepts the underlying model instance via its constructor:

```
1use App\Http\Resources\UserResource;

2use App\Models\User;

3 

4Route::get('/user/{id}', function (string $id) {

5    return new UserResource(User::findOrFail($id));

6});
```

For convenience, you may use the model's `toResource` method, which will use framework conventions to automatically discover the model's underlying resource:

```
1return User::findOrFail($id)->toResource();
```

When invoking the `toResource` method, Laravel will attempt to locate a resource that matches the model's name and is optionally suffixed with `Resource` within the `Http\Resources` namespace closest to the model's namespace.

If your resource class doesn't follow this naming convention or is located in a different namespace, you may specify the default resource for the model using the `UseResource` attribute:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use App\Http\Resources\CustomUserResource;

 6use Illuminate\Database\Eloquent\Model;

 7use Illuminate\Database\Eloquent\Attributes\UseResource;

 8 

 9#[UseResource(CustomUserResource::class)]

10class User extends Model

11{

12    // ...

13}
```

Alternatively, you may specify resource class by passing it to the `toResource` method:

```
1return User::findOrFail($id)->toResource(CustomUserResource::class);
```

### [Resource Collections](#resource-collections)

If you are returning a collection of resources or a paginated response, you should use the `collection` method provided by your resource class when creating the resource instance in your route or controller:

```
1use App\Http\Resources\UserResource;

2use App\Models\User;

3 

4Route::get('/users', function () {

5    return UserResource::collection(User::all());

6});
```

Or, for convenience, you may use the Eloquent collection's `toResourceCollection` method, which will use framework conventions to automatically discover the model's underlying resource collection:

```
1return User::all()->toResourceCollection();
```

When invoking the `toResourceCollection` method, Laravel will attempt to locate a resource collection that matches the model's name and is suffixed with `Collection` within the `Http\Resources` namespace closest to the model's namespace.

If your resource collection class doesn't follow this naming convention or is located in a different namespace, you may specify the default resource collection for the model using the `UseResourceCollection` attribute:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use App\Http\Resources\CustomUserCollection;

 6use Illuminate\Database\Eloquent\Model;

 7use Illuminate\Database\Eloquent\Attributes\UseResourceCollection;

 8 

 9#[UseResourceCollection(CustomUserCollection::class)]

10class User extends Model

11{

12    // ...

13}
```

Alternatively, you may specify the resource collection class by passing it to the `toResourceCollection` method:

```
1return User::all()->toResourceCollection(CustomUserCollection::class);
```

#### [Custom Resource Collections](#custom-resource-collections)

By default, resource collections do not allow any addition of custom meta data that may need to be returned with your collection. If you would like to customize the resource collection response, you may create a dedicated resource to represent the collection:

```
1php artisan make:resource UserCollection
```

Once the resource collection class has been generated, you may easily define any meta data that should be included with the response:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Request;

 6use Illuminate\Http\Resources\Json\ResourceCollection;

 7 

 8class UserCollection extends ResourceCollection

 9{

10    /**

11     * Transform the resource collection into an array.

12     *

13     * @return array<int|string, mixed>

14     */

15    public function toArray(Request $request): array

16    {

17        return [

18            'data' => $this->collection,

19            'links' => [

20                'self' => 'link-value',

21            ],

22        ];

23    }

24}
```

After defining your resource collection, it may be returned from a route or controller:

```
1use App\Http\Resources\UserCollection;

2use App\Models\User;

3 

4Route::get('/users', function () {

5    return new UserCollection(User::all());

6});
```

Or, for convenience, you may use the Eloquent collection's `toResourceCollection` method, which will use framework conventions to automatically discover the model's underlying resource collection:

```
1return User::all()->toResourceCollection();
```

When invoking the `toResourceCollection` method, Laravel will attempt to locate a resource collection that matches the model's name and is suffixed with `Collection` within the `Http\Resources` namespace closest to the model's namespace.

#### [Preserving Collection Keys](#preserving-collection-keys)

When returning a resource collection from a route, Laravel resets the collection's keys so that they are in numerical order. However, you may use the `PreserveKeys` attribute on your resource class indicating whether a collection's original keys should be preserved:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Resources\Attributes\PreserveKeys;

 6use Illuminate\Http\Resources\Json\JsonResource;

 7 

 8#[PreserveKeys]

 9class UserResource extends JsonResource

10{

11    // ...

12}
```

When the `preserveKeys` property is set to `true`, collection keys will be preserved when the collection is returned from a route or controller:

```
1use App\Http\Resources\UserResource;

2use App\Models\User;

3 

4Route::get('/users', function () {

5    return UserResource::collection(User::all()->keyBy->id);

6});
```

#### [Customizing the Underlying Resource Class](#customizing-the-underlying-resource-class)

Typically, the `$this->collection` property of a resource collection is automatically populated with the result of mapping each item of the collection to its singular resource class. The singular resource class is assumed to be the collection's class name without the trailing `Collection` portion of the class name. In addition, depending on your personal preference, the singular resource class may or may not be suffixed with `Resource`.

For example, `UserCollection` will attempt to map the given user instances into the `UserResource` resource. To customize this behavior, you may use the `Collects` attribute on your resource collection:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Resources\Attributes\Collects;

 6use Illuminate\Http\Resources\Json\ResourceCollection;

 7 

 8#[Collects(Member::class)]

 9class UserCollection extends ResourceCollection

10{

11    // ...

12}
```

## [Writing Resources](#writing-resources)

If you have not read the [concept overview](#concept-overview), you are highly encouraged to do so before proceeding with this documentation.

Resources only need to transform a given model into an array. So, each resource contains a `toArray` method which translates your model's attributes into an API friendly array that can be returned from your application's routes or controllers:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Request;

 6use Illuminate\Http\Resources\Json\JsonResource;

 7 

 8class UserResource extends JsonResource

 9{

10    /**

11     * Transform the resource into an array.

12     *

13     * @return array<string, mixed>

14     */

15    public function toArray(Request $request): array

16    {

17        return [

18            'id' => $this->id,

19            'name' => $this->name,

20            'email' => $this->email,

21            'created_at' => $this->created_at,

22            'updated_at' => $this->updated_at,

23        ];

24    }

25}
```

Once a resource has been defined, it may be returned directly from a route or controller:

```
1use App\Models\User;

2 

3Route::get('/user/{id}', function (string $id) {

4    return User::findOrFail($id)->toUserResource();

5});
```

#### [Relationships](#relationships)

If you would like to include related resources in your response, you may add them to the array returned by your resource's `toArray` method. In this example, we will use the `PostResource` resource's `collection` method to add the user's blog posts to the resource response:

```
 1use App\Http\Resources\PostResource;

 2use Illuminate\Http\Request;

 3 

 4/**

 5 * Transform the resource into an array.

 6 *

 7 * @return array<string, mixed>

 8 */

 9public function toArray(Request $request): array

10{

11    return [

12        'id' => $this->id,

13        'name' => $this->name,

14        'email' => $this->email,

15        'posts' => PostResource::collection($this->posts),

16        'created_at' => $this->created_at,

17        'updated_at' => $this->updated_at,

18    ];

19}
```

If you would like to include relationships only when they have already been loaded, check out the documentation on [conditional relationships](#conditional-relationships).

#### [Resource Collections](#writing-resource-collections)

While resources transform a single model into an array, resource collections transform a collection of models into an array. However, it is not absolutely necessary to define a resource collection class for each one of your models since all Eloquent model collections provide a `toResourceCollection` method to generate an "ad-hoc" resource collection on the fly:

```
1use App\Models\User;

2 

3Route::get('/users', function () {

4    return User::all()->toResourceCollection();

5});
```

However, if you need to customize the meta data returned with the collection, it is necessary to define your own resource collection:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Request;

 6use Illuminate\Http\Resources\Json\ResourceCollection;

 7 

 8class UserCollection extends ResourceCollection

 9{

10    /**

11     * Transform the resource collection into an array.

12     *

13     * @return array<string, mixed>

14     */

15    public function toArray(Request $request): array

16    {

17        return [

18            'data' => $this->collection,

19            'links' => [

20                'self' => 'link-value',

21            ],

22        ];

23    }

24}
```

Like singular resources, resource collections may be returned directly from routes or controllers:

```
1use App\Http\Resources\UserCollection;

2use App\Models\User;

3 

4Route::get('/users', function () {

5    return new UserCollection(User::all());

6});
```

Or, for convenience, you may use the Eloquent collection's `toResourceCollection` method, which will use framework conventions to automatically discover the model's underlying resource collection:

```
1return User::all()->toResourceCollection();
```

When invoking the `toResourceCollection` method, Laravel will attempt to locate a resource collection that matches the model's name and is suffixed with `Collection` within the `Http\Resources` namespace closest to the model's namespace.

### [Data Wrapping](#data-wrapping)

By default, your outermost resource is wrapped in a `data` key when the resource response is converted to JSON. So, for example, a typical resource collection response looks like the following:

```
 1{

 2    "data": [

 3        {

 4            "id": 1,

 5            "name": "Eladio Schroeder Sr.",

 6            "email": "[[email protected]](/cdn-cgi/l/email-protection)"

 7        },

 8        {

 9            "id": 2,

10            "name": "Liliana Mayert",

11            "email": "[[email protected]](/cdn-cgi/l/email-protection)"

12        }

13    ]

14}
```

If you would like to disable the wrapping of the outermost resource, you should invoke the `withoutWrapping` method on the base `Illuminate\Http\Resources\Json\JsonResource` class. Typically, you should call this method from your `AppServiceProvider` or another [service provider](/docs/13.x/providers) that is loaded on every request to your application:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Http\Resources\Json\JsonResource;

 6use Illuminate\Support\ServiceProvider;

 7 

 8class AppServiceProvider extends ServiceProvider

 9{

10    /**

11     * Register any application services.

12     */

13    public function register(): void

14    {

15        // ...

16    }

17 

18    /**

19     * Bootstrap any application services.

20     */

21    public function boot(): void

22    {

23        JsonResource::withoutWrapping();

24    }

25}
```

The `withoutWrapping` method only affects the outermost response and will not remove `data` keys that you manually add to your own resource collections.

#### [Wrapping Nested Resources](#wrapping-nested-resources)

You have total freedom to determine how your resource's relationships are wrapped. If you would like all resource collections to be wrapped in a `data` key, regardless of their nesting, you should define a resource collection class for each resource and return the collection within a `data` key.

You may be wondering if this will cause your outermost resource to be wrapped in two `data` keys. Don't worry, Laravel will never let your resources be accidentally double-wrapped, so you don't have to be concerned about the nesting level of the resource collection you are transforming:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Resources\Json\ResourceCollection;

 6 

 7class CommentsCollection extends ResourceCollection

 8{

 9    /**

10     * Transform the resource collection into an array.

11     *

12     * @return array<string, mixed>

13     */

14    public function toArray(Request $request): array

15    {

16        return ['data' => $this->collection];

17    }

18}
```

#### [Data Wrapping and Pagination](#data-wrapping-and-pagination)

When returning paginated collections via a resource response, Laravel will wrap your resource data in a `data` key even if the `withoutWrapping` method has been called. This is because paginated responses always contain `meta` and `links` keys with information about the paginator's state:

```
 1{

 2    "data": [

 3        {

 4            "id": 1,

 5            "name": "Eladio Schroeder Sr.",

 6            "email": "[[email protected]](/cdn-cgi/l/email-protection)"

 7        },

 8        {

 9            "id": 2,

10            "name": "Liliana Mayert",

11            "email": "[[email protected]](/cdn-cgi/l/email-protection)"

12        }

13    ],

14    "links":{

15        "first": "http://example.com/users?page=1",

16        "last": "http://example.com/users?page=1",

17        "prev": null,

18        "next": null

19    },

20    "meta":{

21        "current_page": 1,

22        "from": 1,

23        "last_page": 1,

24        "path": "http://example.com/users",

25        "per_page": 15,

26        "to": 10,

27        "total": 10

28    }

29}
```

### [Pagination](#pagination)

You may pass a Laravel paginator instance to the `collection` method of a resource or to a custom resource collection:

```
1use App\Http\Resources\UserCollection;

2use App\Models\User;

3 

4Route::get('/users', function () {

5    return new UserCollection(User::paginate());

6});
```

Or, for convenience, you may use the paginator's `toResourceCollection` method, which will use framework conventions to automatically discover the paginated model's underlying resource collection:

```
1return User::paginate()->toResourceCollection();
```

Paginated responses always contain `meta` and `links` keys with information about the paginator's state:

```
 1{

 2    "data": [

 3        {

 4            "id": 1,

 5            "name": "Eladio Schroeder Sr.",

 6            "email": "[[email protected]](/cdn-cgi/l/email-protection)"

 7        },

 8        {

 9            "id": 2,

10            "name": "Liliana Mayert",

11            "email": "[[email protected]](/cdn-cgi/l/email-protection)"

12        }

13    ],

14    "links":{

15        "first": "http://example.com/users?page=1",

16        "last": "http://example.com/users?page=1",

17        "prev": null,

18        "next": null

19    },

20    "meta":{

21        "current_page": 1,

22        "from": 1,

23        "last_page": 1,

24        "path": "http://example.com/users",

25        "per_page": 15,

26        "to": 10,

27        "total": 10

28    }

29}
```

#### [Customizing the Pagination Information](#customizing-the-pagination-information)

If you would like to customize the information included in the `links` or `meta` keys of the pagination response, you may define a `paginationInformation` method on the resource. This method will receive the `$paginated` data and the array of `$default` information, which is an array containing the `links` and `meta` keys:

```
 1/**

 2 * Customize the pagination information for the resource.

 3 *

 4 * @param  \Illuminate\Http\Request  $request

 5 * @param  array  $paginated

 6 * @param  array  $default

 7 * @return array

 8 */

 9public function paginationInformation($request, $paginated, $default)

10{

11    $default['links']['custom'] = 'https://example.com';

12 

13    return $default;

14}
```

### [Conditional Attributes](#conditional-attributes)

Sometimes you may wish to only include an attribute in a resource response if a given condition is met. For example, you may wish to only include a value if the current user is an "administrator". Laravel provides a variety of helper methods to assist you in this situation. The `when` method may be used to conditionally add an attribute to a resource response:

```
 1/**

 2 * Transform the resource into an array.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toArray(Request $request): array

 7{

 8    return [

 9        'id' => $this->id,

10        'name' => $this->name,

11        'email' => $this->email,

12        'secret' => $this->when($request->user()->isAdmin(), 'secret-value'),

13        'created_at' => $this->created_at,

14        'updated_at' => $this->updated_at,

15    ];

16}
```

In this example, the `secret` key will only be returned in the final resource response if the authenticated user's `isAdmin` method returns `true`. If the method returns `false`, the `secret` key will be removed from the resource response before it is sent to the client. The `when` method allows you to expressively define your resources without resorting to conditional statements when building the array.

The `when` method also accepts a closure as its second argument, allowing you to calculate the resulting value only if the given condition is `true`:

```
1'secret' => $this->when($request->user()->isAdmin(), function () {

2    return 'secret-value';

3}),
```

The `whenHas` method may be used to include an attribute if it is actually present on the underlying model:

```
1'name' => $this->whenHas('name'),
```

Additionally, the `whenNotNull` method may be used to include an attribute in the resource response if the attribute is not null:

```
1'name' => $this->whenNotNull($this->name),
```

#### [Merging Conditional Attributes](#merging-conditional-attributes)

Sometimes you may have several attributes that should only be included in the resource response based on the same condition. In this case, you may use the `mergeWhen` method to include the attributes in the response only when the given condition is `true`:

```
 1/**

 2 * Transform the resource into an array.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toArray(Request $request): array

 7{

 8    return [

 9        'id' => $this->id,

10        'name' => $this->name,

11        'email' => $this->email,

12        $this->mergeWhen($request->user()->isAdmin(), [

13            'first-secret' => 'value',

14            'second-secret' => 'value',

15        ]),

16        'created_at' => $this->created_at,

17        'updated_at' => $this->updated_at,

18    ];

19}
```

Again, if the given condition is `false`, these attributes will be removed from the resource response before it is sent to the client.

The `mergeWhen` method should not be used within arrays that mix string and numeric keys. Furthermore, it should not be used within arrays with numeric keys that are not ordered sequentially.

### [Conditional Relationships](#conditional-relationships)

In addition to conditionally loading attributes, you may conditionally include relationships on your resource responses based on if the relationship has already been loaded on the model. This allows your controller to decide which relationships should be loaded on the model and your resource can easily include them only when they have actually been loaded. Ultimately, this makes it easier to avoid "N+1" query problems within your resources.

The `whenLoaded` method may be used to conditionally load a relationship. In order to avoid unnecessarily loading relationships, this method accepts the name of the relationship instead of the relationship itself:

```
 1use App\Http\Resources\PostResource;

 2 

 3/**

 4 * Transform the resource into an array.

 5 *

 6 * @return array<string, mixed>

 7 */

 8public function toArray(Request $request): array

 9{

10    return [

11        'id' => $this->id,

12        'name' => $this->name,

13        'email' => $this->email,

14        'posts' => PostResource::collection($this->whenLoaded('posts')),

15        'created_at' => $this->created_at,

16        'updated_at' => $this->updated_at,

17    ];

18}
```

In this example, if the relationship has not been loaded, the `posts` key will be removed from the resource response before it is sent to the client.

#### [Conditional Relationship Counts](#conditional-relationship-counts)

In addition to conditionally including relationships, you may conditionally include relationship "counts" on your resource responses based on if the relationship's count has been loaded on the model:

```
1new UserResource($user->loadCount('posts'));
```

The `whenCounted` method may be used to conditionally include a relationship's count in your resource response. This method avoids unnecessarily including the attribute if the relationships' count is not present:

```
 1/**

 2 * Transform the resource into an array.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toArray(Request $request): array

 7{

 8    return [

 9        'id' => $this->id,

10        'name' => $this->name,

11        'email' => $this->email,

12        'posts_count' => $this->whenCounted('posts'),

13        'created_at' => $this->created_at,

14        'updated_at' => $this->updated_at,

15    ];

16}
```

In this example, if the `posts` relationship's count has not been loaded, the `posts_count` key will be removed from the resource response before it is sent to the client.

Other types of aggregates, such as `avg`, `sum`, `min`, and `max` may also be conditionally loaded using the `whenAggregated` method:

```
1'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),

2'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),

3'words_min' => $this->whenAggregated('posts', 'words', 'min'),

4'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```

#### [Conditional Pivot Information](#conditional-pivot-information)

In addition to conditionally including relationship information in your resource responses, you may conditionally include data from the intermediate tables of many-to-many relationships using the `whenPivotLoaded` method. The `whenPivotLoaded` method accepts the name of the pivot table as its first argument. The second argument should be a closure that returns the value to be returned if the pivot information is available on the model:

```
 1/**

 2 * Transform the resource into an array.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toArray(Request $request): array

 7{

 8    return [

 9        'id' => $this->id,

10        'name' => $this->name,

11        'expires_at' => $this->whenPivotLoaded('role_user', function () {

12            return $this->pivot->expires_at;

13        }),

14    ];

15}
```

If your relationship is using a [custom intermediate table model](/docs/13.x/eloquent-relationships#defining-custom-intermediate-table-models), you may pass an instance of the intermediate table model as the first argument to the `whenPivotLoaded` method:

```
1'expires_at' => $this->whenPivotLoaded(new Membership, function () {

2    return $this->pivot->expires_at;

3}),
```

If your intermediate table is using an accessor other than `pivot`, you may use the `whenPivotLoadedAs` method:

```
 1/**

 2 * Transform the resource into an array.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toArray(Request $request): array

 7{

 8    return [

 9        'id' => $this->id,

10        'name' => $this->name,

11        'expires_at' => $this->whenPivotLoadedAs('subscription', 'role_user', function () {

12            return $this->subscription->expires_at;

13        }),

14    ];

15}
```

### [Adding Meta Data](#adding-meta-data)

Some JSON API standards require the addition of meta data to your resource and resource collections responses. This often includes things like `links` to the resource or related resources, or meta data about the resource itself. If you need to return additional meta data about a resource, include it in your `toArray` method. For example, you might include `links` information when transforming a resource collection:

```
 1/**

 2 * Transform the resource into an array.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toArray(Request $request): array

 7{

 8    return [

 9        'data' => $this->collection,

10        'links' => [

11            'self' => 'link-value',

12        ],

13    ];

14}
```

When returning additional meta data from your resources, you never have to worry about accidentally overriding the `links` or `meta` keys that are automatically added by Laravel when returning paginated responses. Any additional `links` you define will be merged with the links provided by the paginator.

#### [Top Level Meta Data](#top-level-meta-data)

Sometimes you may wish to only include certain meta data with a resource response if the resource is the outermost resource being returned. Typically, this includes meta information about the response as a whole. To define this meta data, add a `with` method to your resource class. This method should return an array of meta data to be included with the resource response only when the resource is the outermost resource being transformed:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Resources\Json\ResourceCollection;

 6 

 7class UserCollection extends ResourceCollection

 8{

 9    /**

10     * Transform the resource collection into an array.

11     *

12     * @return array<string, mixed>

13     */

14    public function toArray(Request $request): array

15    {

16        return parent::toArray($request);

17    }

18 

19    /**

20     * Get additional data that should be returned with the resource array.

21     *

22     * @return array<string, mixed>

23     */

24    public function with(Request $request): array

25    {

26        return [

27            'meta' => [

28                'key' => 'value',

29            ],

30        ];

31    }

32}
```

#### [Adding Meta Data When Constructing Resources](#adding-meta-data-when-constructing-resources)

You may also add top-level data when constructing resource instances in your route or controller. The `additional` method, which is available on all resources, accepts an array of data that should be added to the resource response:

```
1return User::all()

2    ->load('roles')

3    ->toResourceCollection()

4    ->additional(['meta' => [

5        'key' => 'value',

6    ]]);
```

## [JSON:API Resources](#jsonapi-resources)

Laravel ships with `JsonApiResource`, a resource class that produces responses compliant with the [JSON:API specification](https://jsonapi.org/). It extends the standard `JsonResource` class and automatically handles resource object structure, relationships, sparse fieldsets, includes, lazy attribute evaluation, and sets the `Content-Type` header to `application/vnd.api+json`.

Laravel's JSON:API resources handle the serialization of your responses. If you also need to parse incoming JSON:API query parameters such as filters and sorts, [Spatie's Laravel Query Builder](https://spatie.be/docs/laravel-query-builder) is a great companion package.

### [Generating JSON:API Resources](#generating-jsonapi-resources)

To generate a JSON:API resource, use the `make:resource` Artisan command with the `--json-api` flag:

```
1php artisan make:resource PostResource --json-api
```

The generated class will extend `Illuminate\Http\Resources\JsonApi\JsonApiResource` and include `$attributes` and `$relationships` properties for you to define:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\Request;

 6use Illuminate\Http\Resources\JsonApi\JsonApiResource;

 7 

 8class PostResource extends JsonApiResource

 9{

10    /**

11     * The resource's attributes.

12     */

13    public $attributes = [

14        // ...

15    ];

16 

17    /**

18     * The resource's relationships.

19     */

20    public $relationships = [

21        // ...

22    ];

23}
```

JSON:API resources may be returned from routes and controllers just like standard resources:

```
1use App\Http\Resources\PostResource;

2use App\Models\Post;

3 

4Route::get('/api/posts/{post}', function (Post $post) {

5    return new PostResource($post);

6});
```

Or, for convenience, you may use the model's `toResource` method:

```
1Route::get('/api/posts/{post}', function (Post $post) {

2    return $post->toResource();

3});
```

This will produce a JSON:API compliant response:

```
 1{

 2    "data": {

 3        "id": "1",

 4        "type": "posts",

 5        "attributes": {

 6            "title": "Hello World",

 7            "body": "This is my first post."

 8        }

 9    }

10}
```

To return a collection of JSON:API resources, use the `collection` method or the `toResourceCollection` convenience method:

```
1return PostResource::collection(Post::all());

2 

3return Post::all()->toResourceCollection();
```

### [Defining Attributes](#defining-jsonapi-attributes)

There are two ways to define which attributes are included in your JSON:API resource.

The simplest approach is to define an `$attributes` property on your resource. You may list attribute names as values, which will be read directly from the underlying model:

```
1public $attributes = [

2    'title',

3    'body',

4    'created_at',

5];
```

If an attribute is expensive to calculate, you may return it from `toAttributes` as a closure so it is only evaluated when the attribute is actually needed in the response.

Or, for full control over the resource's attributes, you may override the `toAttributes` method on the resource:

```
 1/**

 2 * Get the resource's attributes.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function toAttributes(Request $request): array

 7{

 8    return [

 9        'title' => $this->title,

10        'body' => $this->body,

11        'is_published' => fn () => $this->published_at !== null,

12        'created_at' => $this->created_at,

13        'updated_at' => $this->updated_at,

14    ];

15}
```

### [Defining Relationships](#defining-jsonapi-relationships)

JSON:API resources support defining relationships that follow the JSON:API specification. Relationships are only serialized when requested by the client via the `include` query parameter.

#### The `$relationships` Property

You may define your resource's includable relationships via the `$relationships` property on your resource:

```
1public $relationships = [

2    'author',

3    'comments',

4];
```

When listing a relationship name as a value, Laravel will resolve the corresponding Eloquent relationship and automatically discover the appropriate resource class. If you need to specify the resource class explicitly, you may define the relationship as a key / class pair:

```
1use App\Http\Resources\UserResource;

2 

3public $relationships = [

4    'author' => UserResource::class,

5    'comments',

6];
```

Alternatively, you may override the `toRelationships` method on the resource:

```
 1/**

 2 * Get the resource's relationships.

 3 */

 4public function toRelationships(Request $request): array

 5{

 6    return [

 7        'author' => UserResource::class,

 8        'comments' => fn () => CommentResource::collection(

 9            $request->user()->is($this->resource)

10                ? $this->comments

11                : $this->comments->where('is_public', true),

12        ),

13    ];

14}
```

Using closures gives you more control over the relationship payload, while still only resolving the relationship when the client requests it.

#### Including Relationships

Clients may request related resources using the `include` query parameter:

```
1GET /api/posts/1?include=author,comments
```

This produces a response with resource identifier objects in the `relationships` key and full resource objects in the top-level `included` array:

```
 1{

 2    "data": {

 3        "id": "1",

 4        "type": "posts",

 5        "attributes": {

 6            "title": "Hello World"

 7        },

 8        "relationships": {

 9            "author": {

10                "data": {

11                    "id": "1",

12                    "type": "users"

13                }

14            },

15            "comments": {

16                "data": [

17                    {

18                        "id": "1",

19                        "type": "comments"

20                    }

21                ]

22            }

23        }

24    },

25    "included": [

26        {

27            "id": "1",

28            "type": "users",

29            "attributes": {

30                "name": "Taylor Otwell"

31            }

32        },

33        {

34            "id": "1",

35            "type": "comments",

36            "attributes": {

37                "body": "Great post!"

38            }

39        }

40    ]

41}
```

Nested relationships may be included using dot notation:

```
1GET /api/posts/1?include=comments.author
```

#### [Relationship Depth](#jsonapi-relationship-depth)

By default, nested relationship includes are limited to a maximum depth. You may customize this limit using the `maxRelationshipDepth` method, typically in one of you application's service provider:

```
1use Illuminate\Http\Resources\JsonApi\JsonApiResource;

2 

3JsonApiResource::maxRelationshipDepth(3);
```

### [Resource Type and ID](#jsonapi-resource-type-and-id)

By default, the resource's `type` is derived from the resource class name. For example, `PostResource` produces the type `posts` and `BlogPostResource` produces `blog-posts`. The resource's `id` is resolved from the model's primary key.

If you need to customize these values, you may override the `toType` and `toId` methods on your resource:

```
 1/**

 2 * Get the resource's type.

 3 */

 4public function toType(Request $request): string

 5{

 6    return 'articles';

 7}

 8 

 9/**

10 * Get the resource's ID.

11 */

12public function toId(Request $request): string

13{

14    return (string) $this->uuid;

15}
```

This is particularly useful when a resource's type should differ from its class name, such as when an `AuthorResource` wraps a `User` model and should output the type `authors`.

### [Sparse Fieldsets and Includes](#jsonapi-sparse-fieldsets-and-includes)

JSON:API resources support [sparse fieldsets](https://jsonapi.org/format/#fetching-sparse-fieldsets), allowing clients to request only specific attributes for each resource type using the `fields` query parameter:

```
1GET /api/posts?fields[posts]=title,created_at&fields[users]=name
```

This will only include the `title` and `created_at` attributes for `posts` resources, and the `name` attribute for `users` resources.

#### [Ignoring the Query String](#jsonapi-ignoring-query-string)

If you would like to disable sparse fieldset filtering for a given resource response, you may call the `ignoreFieldsAndIncludesInQueryString` method:

```
1return $post->toResource()

2    ->ignoreFieldsAndIncludesInQueryString();
```

#### [Including Previously Loaded Relationships](#jsonapi-including-previously-loaded-relationships)

By default, relationships are only included in the response when requested via the `include` query parameter. If you would like to include all previously eager-loaded relationships regardless of the query string, you may call the `includePreviouslyLoadedRelationships` method:

```
1return $post->load('author', 'comments')

2    ->toResource()

3    ->includePreviouslyLoadedRelationships();
```

### [Links and Meta](#jsonapi-links-and-meta)

You may add links and meta information to your JSON:API resource objects by overriding the `toLinks` and `toMeta` methods on the resource:

```
 1/**

 2 * Get the resource's links.

 3 */

 4public function toLinks(Request $request): array

 5{

 6    return [

 7        'self' => route('api.posts.show', $this->resource),

 8    ];

 9}

10 

11/**

12 * Get the resource's meta information.

13 */

14public function toMeta(Request $request): array

15{

16    return [

17        'readable_created_at' => $this->created_at->diffForHumans(),

18    ];

19}
```

This will add `links` and `meta` keys to the resource object in the response:

```
 1{

 2    "data": {

 3        "id": "1",

 4        "type": "posts",

 5        "attributes": {

 6            "title": "Hello World"

 7        },

 8        "links": {

 9            "self": "https://example.com/api/posts/1"

10        },

11        "meta": {

12            "readable_created_at": "2 hours ago"

13        }

14    }

15}
```

## [Resource Responses](#resource-responses)

As you have already read, resources may be returned directly from routes and controllers:

```
1use App\Models\User;

2 

3Route::get('/user/{id}', function (string $id) {

4    return User::findOrFail($id)->toResource();

5});
```

However, sometimes you may need to customize the outgoing HTTP response before it is sent to the client. There are two ways to accomplish this. First, you may chain the `response` method onto the resource. This method will return an `Illuminate\Http\JsonResponse` instance, giving you full control over the response's headers:

```
1use App\Http\Resources\UserResource;

2use App\Models\User;

3 

4Route::get('/user', function () {

5    return User::find(1)

6        ->toResource()

7        ->response()

8        ->header('X-Value', 'True');

9});
```

Alternatively, you may define a `withResponse` method within the resource itself. This method will be called when the resource is returned as the outermost resource in a response:

```
 1<?php

 2 

 3namespace App\Http\Resources;

 4 

 5use Illuminate\Http\JsonResponse;

 6use Illuminate\Http\Request;

 7use Illuminate\Http\Resources\Json\JsonResource;

 8 

 9class UserResource extends JsonResource

10{

11    /**

12     * Transform the resource into an array.

13     *

14     * @return array<string, mixed>

15     */

16    public function toArray(Request $request): array

17    {

18        return [

19            'id' => $this->id,

20        ];

21    }

22 

23    /**

24     * Customize the outgoing response for the resource.

25     */

26    public function withResponse(Request $request, JsonResponse $response): void

27    {

28        $response->header('X-Value', 'True');

29    }

30}
```
