# Eloquent: Collections

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Custom Collections](#custom-collections)

## [Introduction](#introduction)

All Eloquent methods that return more than one model result will return instances of the `Illuminate\Database\Eloquent\Collection` class, including results retrieved via the `get` method or accessed via a relationship. The Eloquent collection object extends Laravel's [base collection](/docs/13.x/collections), so it naturally inherits dozens of methods used to fluently work with the underlying array of Eloquent models. Be sure to review the Laravel collection documentation to learn all about these helpful methods!

All collections also serve as iterators, allowing you to loop over them as if they were simple PHP arrays:

```
1use App\Models\User;

2 

3$users = User::where('active', 1)->get();

4 

5foreach ($users as $user) {

6    echo $user->name;

7}
```

However, as previously mentioned, collections are much more powerful than arrays and expose a variety of map / reduce operations that may be chained using an intuitive interface. For example, we may remove all inactive models and then gather the first name for each remaining user:

```
1$names = User::all()->reject(function (User $user) {

2    return $user->active === false;

3})->map(function (User $user) {

4    return $user->name;

5});
```

#### [Eloquent Collection Conversion](#eloquent-collection-conversion)

While most Eloquent collection methods return a new instance of an Eloquent collection, the `collapse`, `flatten`, `flip`, `keys`, `pluck`, and `zip` methods return a [base collection](/docs/13.x/collections) instance. Likewise, if a `map` operation returns a collection that does not contain any Eloquent models, it will be converted to a base collection instance.

## [Available Methods](#available-methods)

All Eloquent collections extend the base [Laravel collection](/docs/13.x/collections#available-methods) object; therefore, they inherit all of the powerful methods provided by the base collection class.

In addition, the `Illuminate\Database\Eloquent\Collection` class provides a superset of methods to aid with managing your model collections. Most methods return `Illuminate\Database\Eloquent\Collection` instances; however, some methods, like `modelKeys`, return an `Illuminate\Support\Collection` instance.

[append](#method-append) [contains](#method-contains) [diff](#method-diff) [except](#method-except) [find](#method-find) [findOrFail](#method-find-or-fail) [fresh](#method-fresh) [intersect](#method-intersect) [load](#method-load) [loadMissing](#method-loadMissing) [modelKeys](#method-modelKeys) [makeVisible](#method-makeVisible) [makeHidden](#method-makeHidden) [mergeVisible](#method-mergeVisible) [mergeHidden](#method-mergeHidden) [only](#method-only) [partition](#method-partition) [setAppends](#method-setAppends) [setVisible](#method-setVisible) [setHidden](#method-setHidden) [toQuery](#method-toquery) [unique](#method-unique) [withoutAppends](#method-withoutAppends)

#### [`append($attributes)`](#method-append)

The `append` method may be used to indicate that an attribute should be [appended](/docs/13.x/eloquent-serialization#appending-values-to-json) for every model in the collection. This method accepts an array of attributes or a single attribute:

```
1$users->append('team');

2 

3$users->append(['team', 'is_admin']);
```

#### [`contains($key, $operator = null, $value = null)`](#method-contains)

The `contains` method may be used to determine if a given model instance is contained by the collection. This method accepts a primary key or a model instance:

```
1$users->contains(1);

2 

3$users->contains(User::find(1));
```

#### [`diff($items)`](#method-diff)

The `diff` method returns all of the models that are not present in the given collection:

```
1use App\Models\User;

2 

3$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

#### [`except($keys)`](#method-except)

The `except` method returns all of the models that do not have the given primary keys:

```
1$users = $users->except([1, 2, 3]);
```

#### [`find($key)`](#method-find)

The `find` method returns the model that has a primary key matching the given key. If `$key` is a model instance, `find` will attempt to return a model matching the primary key. If `$key` is an array of keys, `find` will return all models which have a primary key in the given array:

```
1$users = User::all();

2 

3$user = $users->find(1);
```

#### [`findOrFail($key)`](#method-find-or-fail)

The `findOrFail` method returns the model that has a primary key matching the given key or throws an `Illuminate\Database\Eloquent\ModelNotFoundException` exception if no matching model can be found in the collection:

```
1$users = User::all();

2 

3$user = $users->findOrFail(1);
```

#### [`fresh($with = [])`](#method-fresh)

The `fresh` method retrieves a fresh instance of each model in the collection from the database. In addition, any specified relationships will be eager loaded:

```
1$users = $users->fresh();

2 

3$users = $users->fresh('comments');
```

#### [`intersect($items)`](#method-intersect)

The `intersect` method returns all of the models that are also present in the given collection:

```
1use App\Models\User;

2 

3$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

#### [`load($relations)`](#method-load)

The `load` method eager loads the given relationships for all models in the collection:

```
1$users->load(['comments', 'posts']);

2 

3$users->load('comments.author');

4 

5$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

#### [`loadMissing($relations)`](#method-loadMissing)

The `loadMissing` method eager loads the given relationships for all models in the collection if the relationships are not already loaded:

```
1$users->loadMissing(['comments', 'posts']);

2 

3$users->loadMissing('comments.author');

4 

5$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

#### [`modelKeys()`](#method-modelKeys)

The `modelKeys` method returns the primary keys for all models in the collection:

```
1$users->modelKeys();

2 

3// [1, 2, 3, 4, 5]
```

#### [`makeVisible($attributes)`](#method-makeVisible)

The `makeVisible` method [makes attributes visible](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) that are typically "hidden" on each model in the collection:

```
1$users = $users->makeVisible(['address', 'phone_number']);
```

#### [`makeHidden($attributes)`](#method-makeHidden)

The `makeHidden` method [hides attributes](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) that are typically "visible" on each model in the collection:

```
1$users = $users->makeHidden(['address', 'phone_number']);
```

#### [`mergeVisible($attributes)`](#method-mergeVisible)

The `mergeVisible` method [makes additional attributes visible](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) while retaining existing visible attributes:

```
1$users = $users->mergeVisible(['middle_name']);
```

#### [`mergeHidden($attributes)`](#method-mergeHidden)

The `mergeHidden` method [hides additional attributes](/docs/13.x/eloquent-serialization#hiding-attributes-from-json) while retaining existing hidden attributes:

```
1$users = $users->mergeHidden(['last_login_at']);
```

#### [`only($keys)`](#method-only)

The `only` method returns all of the models that have the given primary keys:

```
1$users = $users->only([1, 2, 3]);
```

#### [`partition`](#method-partition)

The `partition` method returns an instance of `Illuminate\Support\Collection` containing `Illuminate\Database\Eloquent\Collection` collection instances:

```
1$partition = $users->partition(fn ($user) => $user->age > 18);

2 

3dump($partition::class);    // Illuminate\Support\Collection

4dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection

5dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

#### [`setAppends($attributes)`](#method-setAppends)

The `setAppends` method temporarily overrides all of the [appended attributes](/docs/13.x/eloquent-serialization#appending-values-to-json) on each model in the collection:

```
1$users = $users->setAppends(['is_admin']);
```

#### [`setVisible($attributes)`](#method-setVisible)

The `setVisible` method [temporarily overrides](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the visible attributes on each model in the collection:

```
1$users = $users->setVisible(['id', 'name']);
```

#### [`setHidden($attributes)`](#method-setHidden)

The `setHidden` method [temporarily overrides](/docs/13.x/eloquent-serialization#temporarily-modifying-attribute-visibility) all of the hidden attributes on each model in the collection:

```
1$users = $users->setHidden(['email', 'password', 'remember_token']);
```

#### [`toQuery()`](#method-toquery)

The `toQuery` method returns an Eloquent query builder instance containing a `whereIn` constraint on the collection model's primary keys:

```
1use App\Models\User;

2 

3$users = User::where('status', 'VIP')->get();

4 

5$users->toQuery()->update([

6    'status' => 'Administrator',

7]);
```

#### [`unique($key = null, $strict = false)`](#method-unique)

The `unique` method returns all of the unique models in the collection. Any models with the same primary key as another model in the collection are removed:

```
1$users = $users->unique();
```

#### [`withoutAppends()`](#method-withoutAppends)

The `withoutAppends` method temporarily removes all of the [appended attributes](/docs/13.x/eloquent-serialization#appending-values-to-json) on each model in the collection:

```
1$users = $users->withoutAppends();
```

## [Custom Collections](#custom-collections)

If you would like to use a custom `Collection` object when interacting with a given model, you may add the `CollectedBy` attribute to your model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use App\Support\UserCollection;

 6use Illuminate\Database\Eloquent\Attributes\CollectedBy;

 7use Illuminate\Database\Eloquent\Model;

 8 

 9#[CollectedBy(UserCollection::class)]

10class User extends Model

11{

12    // ...

13}
```

Alternatively, you may define a `newCollection` method on your model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use App\Support\UserCollection;

 6use Illuminate\Database\Eloquent\Collection;

 7use Illuminate\Database\Eloquent\Model;

 8 

 9class User extends Model

10{

11    /**

12     * Create a new Eloquent Collection instance.

13     *

14     * @param  array<int, \Illuminate\Database\Eloquent\Model>  $models

15     * @return \Illuminate\Database\Eloquent\Collection<int, \Illuminate\Database\Eloquent\Model>

16     */

17    public function newCollection(array $models = []): Collection

18    {

19        $collection = new UserCollection($models);

20 

21        if (Model::isAutomaticallyEagerLoadingRelationships()) {

22            $collection->withRelationshipAutoloading();

23        }

24 

25        return $collection;

26    }

27}
```

Once you have defined a `newCollection` method or added the `CollectedBy` attribute to your model, you will receive an instance of your custom collection anytime Eloquent would normally return an `Illuminate\Database\Eloquent\Collection` instance.

If you would like to use a custom collection for every model in your application, you should define the `newCollection` method on a base model class that is extended by all of your application's models.
