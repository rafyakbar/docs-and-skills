# Collections

- [Introduction](#introduction)
  * [Creating Collections](#creating-collections)
  * [Extending Collections](#extending-collections)
- [Available Methods](#available-methods)
- [Higher Order Messages](#higher-order-messages)
- [Lazy Collections](#lazy-collections)
  * [Introduction](#lazy-collection-introduction)
  * [Creating Lazy Collections](#creating-lazy-collections)
  * [The Enumerable Contract](#the-enumerable-contract)
  * [Lazy Collection Methods](#lazy-collection-methods)

## [Introduction](#introduction)

The `Illuminate\Support\Collection` class provides a fluent, convenient wrapper for working with arrays of data. For example, check out the following code. We'll use the `collect` helper to create a new collection instance from the array, run the `strtoupper` function on each element, and then remove all empty elements:

```
1$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {

2    return strtoupper($name);

3})->reject(function (string $name) {

4    return empty($name);

5});
```

As you can see, the `Collection` class allows you to chain its methods to perform fluent mapping and reducing of the underlying array. In general, collections are immutable, meaning every `Collection` method returns an entirely new `Collection` instance.

### [Creating Collections](#creating-collections)

As mentioned above, the `collect` helper returns a new `Illuminate\Support\Collection` instance for the given array. So, creating a collection is as simple as:

```
1$collection = collect([1, 2, 3]);
```

You may also create a collection using the [make](#method-make) and [fromJson](#method-fromjson) methods.

The results of [Eloquent](/docs/13.x/eloquent) queries are always returned as `Collection` instances.

### [Extending Collections](#extending-collections)

Collections are "macroable", which allows you to add additional methods to the `Collection` class at run time. The `Illuminate\Support\Collection` class' `macro` method accepts a closure that will be executed when your macro is called. The macro closure may access the collection's other methods via `$this`, just as if it were a real method of the collection class. For example, the following code adds a `toUpper` method to the `Collection` class:

```
 1use Illuminate\Support\Collection;

 2use Illuminate\Support\Str;

 3 

 4Collection::macro('toUpper', function () {

 5    return $this->map(function (string $value) {

 6        return Str::upper($value);

 7    });

 8});

 9 

10$collection = collect(['first', 'second']);

11 

12$upper = $collection->toUpper();

13 

14// ['FIRST', 'SECOND']
```

Typically, you should declare collection macros in the `boot` method of a [service provider](/docs/13.x/providers).

#### [Macro Arguments](#macro-arguments)

If necessary, you may define macros that accept additional arguments:

```
 1use Illuminate\Support\Collection;

 2use Illuminate\Support\Facades\Lang;

 3 

 4Collection::macro('toLocale', function (string $locale) {

 5    return $this->map(function (string $value) use ($locale) {

 6        return Lang::get($value, [], $locale);

 7    });

 8});

 9 

10$collection = collect(['first', 'second']);

11 

12$translated = $collection->toLocale('es');

13 

14// ['primero', 'segundo'];
```

## [Available Methods](#available-methods)

For the majority of the remaining collection documentation, we'll discuss each method available on the `Collection` class. Remember, all of these methods may be chained to fluently manipulate the underlying array. Furthermore, almost every method returns a new `Collection` instance, allowing you to preserve the original copy of the collection when necessary:

[after](#method-after) [all](#method-all) [average](#method-average) [avg](#method-avg) [before](#method-before) [chunk](#method-chunk) [chunkWhile](#method-chunkwhile) [collapse](#method-collapse) [collapseWithKeys](#method-collapsewithkeys) [collect](#method-collect) [combine](#method-combine) [concat](#method-concat) [contains](#method-contains) [containsStrict](#method-containsstrict) [count](#method-count) [countBy](#method-countBy) [crossJoin](#method-crossjoin) [dd](#method-dd) [diff](#method-diff) [diffAssoc](#method-diffassoc) [diffAssocUsing](#method-diffassocusing) [diffKeys](#method-diffkeys) [doesntContain](#method-doesntcontain) [doesntContainStrict](#method-doesntcontainstrict) [dot](#method-dot) [dump](#method-dump) [duplicates](#method-duplicates) [duplicatesStrict](#method-duplicatesstrict) [each](#method-each) [eachSpread](#method-eachspread) [ensure](#method-ensure) [every](#method-every) [except](#method-except) [filter](#method-filter) [first](#method-first) [firstOrFail](#method-first-or-fail) [firstWhere](#method-first-where) [flatMap](#method-flatmap) [flatten](#method-flatten) [flip](#method-flip) [forget](#method-forget) [forPage](#method-forpage) [fromJson](#method-fromjson) [get](#method-get) [groupBy](#method-groupby) [has](#method-has) [hasAny](#method-hasany) [hasMany](#method-hasmany) [hasSole](#method-hassole) [implode](#method-implode) [intersect](#method-intersect) [intersectUsing](#method-intersectusing) [intersectAssoc](#method-intersectAssoc) [intersectAssocUsing](#method-intersectassocusing) [intersectByKeys](#method-intersectbykeys) [isEmpty](#method-isempty) [isNotEmpty](#method-isnotempty) [join](#method-join) [keyBy](#method-keyby) [keys](#method-keys) [last](#method-last) [lazy](#method-lazy) [macro](#method-macro) [make](#method-make) [map](#method-map) [mapInto](#method-mapinto) [mapSpread](#method-mapspread) [mapToGroups](#method-maptogroups) [mapWithKeys](#method-mapwithkeys) [max](#method-max) [median](#method-median) [merge](#method-merge) [mergeRecursive](#method-mergerecursive) [min](#method-min) [mode](#method-mode) [multiply](#method-multiply) [nth](#method-nth) [only](#method-only) [pad](#method-pad) [partition](#method-partition) [percentage](#method-percentage) [pipe](#method-pipe) [pipeInto](#method-pipeinto) [pipeThrough](#method-pipethrough) [pluck](#method-pluck) [pop](#method-pop) [prepend](#method-prepend) [pull](#method-pull) [push](#method-push) [put](#method-put) [random](#method-random) [range](#method-range) [reduce](#method-reduce) [reduceInto](#method-reduce-into) [reduceSpread](#method-reduce-spread) [reject](#method-reject) [replace](#method-replace) [replaceRecursive](#method-replacerecursive) [reverse](#method-reverse) [search](#method-search) [select](#method-select) [shift](#method-shift) [shuffle](#method-shuffle) [skip](#method-skip) [skipUntil](#method-skipuntil) [skipWhile](#method-skipwhile) [slice](#method-slice) [sliding](#method-sliding) [sole](#method-sole) [some](#method-some) [sort](#method-sort) [sortBy](#method-sortby) [sortByDesc](#method-sortbydesc) [sortDesc](#method-sortdesc) [sortKeys](#method-sortkeys) [sortKeysDesc](#method-sortkeysdesc) [sortKeysUsing](#method-sortkeysusing) [splice](#method-splice) [split](#method-split) [splitIn](#method-splitin) [sum](#method-sum) [take](#method-take) [takeUntil](#method-takeuntil) [takeWhile](#method-takewhile) [tap](#method-tap) [times](#method-times) [toArray](#method-toarray) [toJson](#method-tojson) [toPrettyJson](#method-to-pretty-json) [transform](#method-transform) [undot](#method-undot) [union](#method-union) [unique](#method-unique) [uniqueStrict](#method-uniquestrict) [unless](#method-unless) [unlessEmpty](#method-unlessempty) [unlessNotEmpty](#method-unlessnotempty) [unwrap](#method-unwrap) [value](#method-value) [values](#method-values) [when](#method-when) [whenEmpty](#method-whenempty) [whenNotEmpty](#method-whennotempty) [where](#method-where) [whereStrict](#method-wherestrict) [whereBetween](#method-wherebetween) [whereIn](#method-wherein) [whereInStrict](#method-whereinstrict) [whereInstanceOf](#method-whereinstanceof) [whereNotBetween](#method-wherenotbetween) [whereNotIn](#method-wherenotin) [whereNotInStrict](#method-wherenotinstrict) [whereNotNull](#method-wherenotnull) [whereNull](#method-wherenull) [wrap](#method-wrap) [zip](#method-zip)

## [Method Listing](#method-listing)

#### [`after()`](#method-after)

The `after` method returns the item after the given item. `null` is returned if the given item is not found or is the last item:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->after(3);

4 

5// 4

6 

7$collection->after(5);

8 

9// null
```

This method searches for the given item using "loose" comparison, meaning a string containing an integer value will be considered equal to an integer of the same value. To use "strict" comparison, you may provide the `strict` argument to the method:

```
1collect([2, 4, 6, 8])->after('4', strict: true);

2 

3// null
```

Alternatively, you may provide your own closure to search for the first item that passes a given truth test:

```
1collect([2, 4, 6, 8])->after(function (int $item, int $key) {

2    return $item > 5;

3});

4 

5// 8
```

#### [`all()`](#method-all)

The `all` method returns the underlying array represented by the collection:

```
1collect([1, 2, 3])->all();

2 

3// [1, 2, 3]
```

#### [`average()`](#method-average)

Alias for the [avg](#method-avg) method.

#### [`avg()`](#method-avg)

The `avg` method returns the [average value](https://en.wikipedia.org/wiki/Average) of a given key:

```
 1$average = collect([

 2    ['foo' => 10],

 3    ['foo' => 10],

 4    ['foo' => 20],

 5    ['foo' => 40]

 6])->avg('foo');

 7 

 8// 20

 9 

10$average = collect([1, 1, 2, 4])->avg();

11 

12// 2
```

#### [`before()`](#method-before)

The `before` method is the opposite of the [after](#method-after) method. It returns the item before the given item. `null` is returned if the given item is not found or is the first item:

```
 1$collection = collect([1, 2, 3, 4, 5]);

 2 

 3$collection->before(3);

 4 

 5// 2

 6 

 7$collection->before(1);

 8 

 9// null

10 

11collect([2, 4, 6, 8])->before('4', strict: true);

12 

13// null

14 

15collect([2, 4, 6, 8])->before(function (int $item, int $key) {

16    return $item > 5;

17});

18 

19// 4
```

#### [`chunk()`](#method-chunk)

The `chunk` method breaks the collection into multiple, smaller collections of a given size:

```
1$collection = collect([1, 2, 3, 4, 5, 6, 7]);

2 

3$chunks = $collection->chunk(4);

4 

5$chunks->all();

6 

7// [[1, 2, 3, 4], [5, 6, 7]]
```

This method is especially useful in [views](/docs/13.x/views) when working with a grid system such as [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/). For example, imagine you have a collection of [Eloquent](/docs/13.x/eloquent) models you want to display in a grid:

```
1@foreach ($products->chunk(3) as $chunk)

2    <div class="row">

3        @foreach ($chunk as $product)

4            <div class="col-xs-4">{{ $product->name }}</div>

5        @endforeach

6    </div>

7@endforeach
```

#### [`chunkWhile()`](#method-chunkwhile)

The `chunkWhile` method breaks the collection into multiple, smaller collections based on the evaluation of the given callback. The `$chunk` variable passed to the closure may be used to inspect the previous element:

```
1$collection = collect(str_split('AABBCCCD'));

2 

3$chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {

4    return $value === $chunk->last();

5});

6 

7$chunks->all();

8 

9// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

#### [`collapse()`](#method-collapse)

The `collapse` method collapses a collection of arrays or collections into a single, flat collection:

```
 1$collection = collect([

 2    [1, 2, 3],

 3    [4, 5, 6],

 4    [7, 8, 9],

 5]);

 6 

 7$collapsed = $collection->collapse();

 8 

 9$collapsed->all();

10 

11// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### [`collapseWithKeys()`](#method-collapsewithkeys)

The `collapseWithKeys` method flattens a collection of arrays or collections into a single collection, keeping the original keys intact. If the collection is already flat, it will return an empty collection:

```
 1$collection = collect([

 2    ['first'  => collect([1, 2, 3])],

 3    ['second' => [4, 5, 6]],

 4    ['third'  => collect([7, 8, 9])]

 5]);

 6 

 7$collapsed = $collection->collapseWithKeys();

 8 

 9$collapsed->all();

10 

11// [

12//     'first'  => [1, 2, 3],

13//     'second' => [4, 5, 6],

14//     'third'  => [7, 8, 9],

15// ]
```

#### [`collect()`](#method-collect)

The `collect` method returns a new `Collection` instance with the items currently in the collection:

```
1$collectionA = collect([1, 2, 3]);

2 

3$collectionB = $collectionA->collect();

4 

5$collectionB->all();

6 

7// [1, 2, 3]
```

The `collect` method is primarily useful for converting [lazy collections](#lazy-collections) into standard `Collection` instances:

```
 1$lazyCollection = LazyCollection::make(function () {

 2    yield 1;

 3    yield 2;

 4    yield 3;

 5});

 6 

 7$collection = $lazyCollection->collect();

 8 

 9$collection::class;

10 

11// 'Illuminate\Support\Collection'

12 

13$collection->all();

14 

15// [1, 2, 3]
```

The `collect` method is especially useful when you have an instance of `Enumerable` and need a non-lazy collection instance. Since `collect()` is part of the `Enumerable` contract, you can safely use it to get a `Collection` instance.

#### [`combine()`](#method-combine)

The `combine` method combines the values of the collection, as keys, with the values of another array or collection:

```
1$collection = collect(['name', 'age']);

2 

3$combined = $collection->combine(['George', 29]);

4 

5$combined->all();

6 

7// ['name' => 'George', 'age' => 29]
```

#### [`concat()`](#method-concat)

The `concat` method appends the given array or collection's values onto the end of another collection:

```
1$collection = collect(['John Doe']);

2 

3$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

4 

5$concatenated->all();

6 

7// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

The `concat` method numerically reindexes keys for items concatenated onto the original collection. To maintain keys in associative collections, see the [merge](#method-merge) method.

#### [`contains()`](#method-contains)

The `contains` method determines whether the collection contains a given item. You may pass a closure to the `contains` method to determine if an element exists in the collection matching a given truth test:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->contains(function (int $value, int $key) {

4    return $value > 5;

5});

6 

7// false
```

Alternatively, you may pass a string to the `contains` method to determine whether the collection contains a given item value:

```
1$collection = collect(['name' => 'Desk', 'price' => 100]);

2 

3$collection->contains('Desk');

4 

5// true

6 

7$collection->contains('New York');

8 

9// false
```

You may also pass a key / value pair to the `contains` method, which will determine if the given pair exists in the collection:

```
1$collection = collect([

2    ['product' => 'Desk', 'price' => 200],

3    ['product' => 'Chair', 'price' => 100],

4]);

5 

6$collection->contains('product', 'Bookcase');

7 

8// false
```

The `contains` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [containsStrict](#method-containsstrict) method to filter using "strict" comparisons.

For the inverse of `contains`, see the [doesntContain](#method-doesntcontain) method.

#### [`containsStrict()`](#method-containsstrict)

This method has the same signature as the [contains](#method-contains) method; however, all values are compared using "strict" comparisons.

This method's behavior is modified when using [Eloquent Collections](/docs/13.x/eloquent-collections#method-contains).

#### [`count()`](#method-count)

The `count` method returns the total number of items in the collection:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$collection->count();

4 

5// 4
```

#### [`countBy()`](#method-countBy)

The `countBy` method counts the occurrences of values in the collection. By default, the method counts the occurrences of every element, allowing you to count certain "types" of elements in the collection:

```
1$collection = collect([1, 2, 2, 2, 3]);

2 

3$counted = $collection->countBy();

4 

5$counted->all();

6 

7// [1 => 1, 2 => 3, 3 => 1]
```

You may pass a closure to the `countBy` method to count all items by a custom value:

```
1$collection = collect(['[[email protected]](/cdn-cgi/l/email-protection)', '[[email protected]](/cdn-cgi/l/email-protection)', '[[email protected]](/cdn-cgi/l/email-protection)']);

2 

3$counted = $collection->countBy(function (string $email) {

4    return substr(strrchr($email, '@'), 1);

5});

6 

7$counted->all();

8 

9// ['gmail.com' => 2, 'yahoo.com' => 1]
```

#### [`crossJoin()`](#method-crossjoin)

The `crossJoin` method cross joins the collection's values among the given arrays or collections, returning a Cartesian product with all possible permutations:

```
 1$collection = collect([1, 2]);

 2 

 3$matrix = $collection->crossJoin(['a', 'b']);

 4 

 5$matrix->all();

 6 

 7/*

 8    [

 9        [1, 'a'],

10        [1, 'b'],

11        [2, 'a'],

12        [2, 'b'],

13    ]

14*/

15 

16$collection = collect([1, 2]);

17 

18$matrix = $collection->crossJoin(['a', 'b'], ['I', 'II']);

19 

20$matrix->all();

21 

22/*

23    [

24        [1, 'a', 'I'],

25        [1, 'a', 'II'],

26        [1, 'b', 'I'],

27        [1, 'b', 'II'],

28        [2, 'a', 'I'],

29        [2, 'a', 'II'],

30        [2, 'b', 'I'],

31        [2, 'b', 'II'],

32    ]

33*/
```

#### [`dd()`](#method-dd)

The `dd` method dumps the collection's items and ends execution of the script:

```
 1$collection = collect(['John Doe', 'Jane Doe']);

 2 

 3$collection->dd();

 4 

 5/*

 6    array:2 [

 7        0 => "John Doe"

 8        1 => "Jane Doe"

 9    ]

10*/
```

If you do not want to stop executing the script, use the [dump](#method-dump) method instead.

#### [`diff()`](#method-diff)

The `diff` method compares the collection against another collection or a plain PHP `array` based on its values. This method will return the values in the original collection that are not present in the given collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$diff = $collection->diff([2, 4, 6, 8]);

4 

5$diff->all();

6 

7// [1, 3, 5]
```

This method's behavior is modified when using [Eloquent Collections](/docs/13.x/eloquent-collections#method-diff).

#### [`diffAssoc()`](#method-diffassoc)

The `diffAssoc` method compares the collection against another collection or a plain PHP `array` based on its keys and values. This method will return the key / value pairs in the original collection that are not present in the given collection:

```
 1$collection = collect([

 2    'color' => 'orange',

 3    'type' => 'fruit',

 4    'remain' => 6,

 5]);

 6 

 7$diff = $collection->diffAssoc([

 8    'color' => 'yellow',

 9    'type' => 'fruit',

10    'remain' => 3,

11    'used' => 6,

12]);

13 

14$diff->all();

15 

16// ['color' => 'orange', 'remain' => 6]
```

#### [`diffAssocUsing()`](#method-diffassocusing)

Unlike `diffAssoc`, `diffAssocUsing` accepts a user supplied callback function for the indices comparison:

```
 1$collection = collect([

 2    'color' => 'orange',

 3    'type' => 'fruit',

 4    'remain' => 6,

 5]);

 6 

 7$diff = $collection->diffAssocUsing([

 8    'Color' => 'yellow',

 9    'Type' => 'fruit',

10    'Remain' => 3,

11], 'strnatcasecmp');

12 

13$diff->all();

14 

15// ['color' => 'orange', 'remain' => 6]
```

The callback must be a comparison function that returns an integer less than, equal to, or greater than zero. For more information, refer to the PHP documentation on [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters), which is the PHP function that the `diffAssocUsing` method utilizes internally.

#### [`diffKeys()`](#method-diffkeys)

The `diffKeys` method compares the collection against another collection or a plain PHP `array` based on its keys. This method will return the key / value pairs in the original collection that are not present in the given collection:

```
 1$collection = collect([

 2    'one' => 10,

 3    'two' => 20,

 4    'three' => 30,

 5    'four' => 40,

 6    'five' => 50,

 7]);

 8 

 9$diff = $collection->diffKeys([

10    'two' => 2,

11    'four' => 4,

12    'six' => 6,

13    'eight' => 8,

14]);

15 

16$diff->all();

17 

18// ['one' => 10, 'three' => 30, 'five' => 50]
```

#### [`doesntContain()`](#method-doesntcontain)

The `doesntContain` method determines whether the collection does not contain a given item. You may pass a closure to the `doesntContain` method to determine if an element does not exist in the collection matching a given truth test:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->doesntContain(function (int $value, int $key) {

4    return $value < 5;

5});

6 

7// false
```

Alternatively, you may pass a string to the `doesntContain` method to determine whether the collection does not contain a given item value:

```
1$collection = collect(['name' => 'Desk', 'price' => 100]);

2 

3$collection->doesntContain('Table');

4 

5// true

6 

7$collection->doesntContain('Desk');

8 

9// false
```

You may also pass a key / value pair to the `doesntContain` method, which will determine if the given pair does not exist in the collection:

```
1$collection = collect([

2    ['product' => 'Desk', 'price' => 200],

3    ['product' => 'Chair', 'price' => 100],

4]);

5 

6$collection->doesntContain('product', 'Bookcase');

7 

8// true
```

The `doesntContain` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value.

#### [`doesntContainStrict()`](#method-doesntcontainstrict)

This method has the same signature as the [doesntContain](#method-doesntcontain) method; however, all values are compared using "strict" comparisons.

#### [`dot()`](#method-dot)

The `dot` method flattens a multi-dimensional collection into a single level collection that uses "dot" notation to indicate depth:

```
1$collection = collect(['products' => ['desk' => ['price' => 100]]]);

2 

3$flattened = $collection->dot();

4 

5$flattened->all();

6 

7// ['products.desk.price' => 100]
```

#### [`dump()`](#method-dump)

The `dump` method dumps the collection's items:

```
 1$collection = collect(['John Doe', 'Jane Doe']);

 2 

 3$collection->dump();

 4 

 5/*

 6    array:2 [

 7        0 => "John Doe"

 8        1 => "Jane Doe"

 9    ]

10*/
```

If you want to stop executing the script after dumping the collection, use the [dd](#method-dd) method instead.

#### [`duplicates()`](#method-duplicates)

The `duplicates` method retrieves and returns duplicate values from the collection:

```
1$collection = collect(['a', 'b', 'a', 'c', 'b']);

2 

3$collection->duplicates();

4 

5// [2 => 'a', 4 => 'b']
```

If the collection contains arrays or objects, you can pass the key of the attributes that you wish to check for duplicate values:

```
1$employees = collect([

2    ['email' => '[[email protected]](/cdn-cgi/l/email-protection)', 'position' => 'Developer'],

3    ['email' => '[[email protected]](/cdn-cgi/l/email-protection)', 'position' => 'Designer'],

4    ['email' => '[[email protected]](/cdn-cgi/l/email-protection)', 'position' => 'Developer'],

5]);

6 

7$employees->duplicates('position');

8 

9// [2 => 'Developer']
```

#### [`duplicatesStrict()`](#method-duplicatesstrict)

This method has the same signature as the [duplicates](#method-duplicates) method; however, all values are compared using "strict" comparisons.

#### [`each()`](#method-each)

The `each` method iterates over the items in the collection and passes each item to a closure:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$collection->each(function (int $item, int $key) {

4    // ...

5});
```

If you would like to stop iterating through the items, you may return `false` from your closure:

```
1$collection->each(function (int $item, int $key) {

2    if (/* condition */) {

3        return false;

4    }

5});
```

#### [`eachSpread()`](#method-eachspread)

The `eachSpread` method iterates over the collection's items, passing each nested item value into the given callback:

```
1$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

2 

3$collection->eachSpread(function (string $name, int $age) {

4    // ...

5});
```

You may stop iterating through the items by returning `false` from the callback:

```
1$collection->eachSpread(function (string $name, int $age) {

2    return false;

3});
```

#### [`ensure()`](#method-ensure)

The `ensure` method may be used to verify that all elements of a collection are of a given type or list of types. Otherwise, an `UnexpectedValueException` will be thrown:

```
1return $collection->ensure(User::class);

2 

3return $collection->ensure([User::class, Customer::class]);
```

Primitive types such as `string`, `int`, `float`, `bool`, and `array` may also be specified:

```
1return $collection->ensure('int');
```

The `ensure` method does not guarantee that elements of different types will not be added to the collection at a later time.

#### [`every()`](#method-every)

The `every` method may be used to verify that all elements of a collection pass a given truth test:

```
1collect([1, 2, 3, 4])->every(function (int $value, int $key) {

2    return $value > 2;

3});

4 

5// false
```

If the collection is empty, the `every` method will return true:

```
1$collection = collect([]);

2 

3$collection->every(function (int $value, int $key) {

4    return $value > 2;

5});

6 

7// true
```

#### [`except()`](#method-except)

The `except` method returns all items in the collection except for those with the specified keys:

```
1$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

2 

3$filtered = $collection->except(['price', 'discount']);

4 

5$filtered->all();

6 

7// ['product_id' => 1]
```

For the inverse of `except`, see the [only](#method-only) method.

This method's behavior is modified when using [Eloquent Collections](/docs/13.x/eloquent-collections#method-except).

#### [`filter()`](#method-filter)

The `filter` method filters the collection using the given callback, keeping only those items that pass a given truth test:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$filtered = $collection->filter(function (int $value, int $key) {

4    return $value > 2;

5});

6 

7$filtered->all();

8 

9// [3, 4]
```

If no callback is supplied, all entries of the collection that are equivalent to `false` will be removed:

```
1$collection = collect([1, 2, 3, null, false, '', 0, []]);

2 

3$collection->filter()->all();

4 

5// [1, 2, 3]
```

For the inverse of `filter`, see the [reject](#method-reject) method.

#### [`first()`](#method-first)

The `first` method returns the first element in the collection that passes a given truth test:

```
1collect([1, 2, 3, 4])->first(function (int $value, int $key) {

2    return $value > 2;

3});

4 

5// 3
```

You may also call the `first` method with no arguments to get the first element in the collection. If the collection is empty, `null` is returned:

```
1collect([1, 2, 3, 4])->first();

2 

3// 1
```

#### [`firstOrFail()`](#method-first-or-fail)

The `firstOrFail` method is identical to the `first` method; however, if no result is found, an `Illuminate\Support\ItemNotFoundException` exception will be thrown:

```
1collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {

2    return $value > 5;

3});

4 

5// Throws ItemNotFoundException...
```

You may also call the `firstOrFail` method with no arguments to get the first element in the collection. If the collection is empty, an `Illuminate\Support\ItemNotFoundException` exception will be thrown:

```
1collect([])->firstOrFail();

2 

3// Throws ItemNotFoundException...
```

#### [`firstWhere()`](#method-first-where)

The `firstWhere` method returns the first element in the collection with the given key / value pair:

```
 1$collection = collect([

 2    ['name' => 'Regena', 'age' => null],

 3    ['name' => 'Linda', 'age' => 14],

 4    ['name' => 'Diego', 'age' => 23],

 5    ['name' => 'Linda', 'age' => 84],

 6]);

 7 

 8$collection->firstWhere('name', 'Linda');

 9 

10// ['name' => 'Linda', 'age' => 14]
```

You may also call the `firstWhere` method with a comparison operator:

```
1$collection->firstWhere('age', '>=', 18);

2 

3// ['name' => 'Diego', 'age' => 23]
```

Like the [where](#method-where) method, you may pass one argument to the `firstWhere` method. In this scenario, the `firstWhere` method will return the first item where the given item key's value is "truthy":

```
1$collection->firstWhere('age');

2 

3// ['name' => 'Linda', 'age' => 14]
```

#### [`flatMap()`](#method-flatmap)

The `flatMap` method iterates through the collection and passes each value to the given closure. The closure is free to modify the item and return it, thus forming a new collection of modified items. Then, the array is flattened by one level:

```
 1$collection = collect([

 2    ['name' => 'Sally'],

 3    ['school' => 'Arkansas'],

 4    ['age' => 28]

 5]);

 6 

 7$flattened = $collection->flatMap(function (array $values) {

 8    return array_map('strtoupper', $values);

 9});

10 

11$flattened->all();

12 

13// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];
```

#### [`flatten()`](#method-flatten)

The `flatten` method flattens a multi-dimensional collection into a single dimension:

```
 1$collection = collect([

 2    'name' => 'Taylor',

 3    'languages' => [

 4        'PHP', 'JavaScript'

 5    ]

 6]);

 7 

 8$flattened = $collection->flatten();

 9 

10$flattened->all();

11 

12// ['Taylor', 'PHP', 'JavaScript'];
```

If necessary, you may pass the `flatten` method a "depth" argument:

```
 1$collection = collect([

 2    'Apple' => [

 3        [

 4            'name' => 'iPhone 6S',

 5            'brand' => 'Apple'

 6        ],

 7    ],

 8    'Samsung' => [

 9        [

10            'name' => 'Galaxy S7',

11            'brand' => 'Samsung'

12        ],

13    ],

14]);

15 

16$products = $collection->flatten(1);

17 

18$products->values()->all();

19 

20/*

21    [

22        ['name' => 'iPhone 6S', 'brand' => 'Apple'],

23        ['name' => 'Galaxy S7', 'brand' => 'Samsung'],

24    ]

25*/
```

In this example, calling `flatten` without providing the depth would have also flattened the nested arrays, resulting in `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`. Providing a depth allows you to specify the number of levels nested arrays will be flattened.

#### [`flip()`](#method-flip)

The `flip` method swaps the collection's keys with their corresponding values:

```
1$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

2 

3$flipped = $collection->flip();

4 

5$flipped->all();

6 

7// ['Taylor' => 'name', 'Laravel' => 'framework']
```

#### [`forget()`](#method-forget)

The `forget` method removes an item from the collection by its key:

```
 1$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

 2 

 3// Forget a single key...

 4$collection->forget('name');

 5 

 6// ['framework' => 'Laravel']

 7 

 8// Forget multiple keys...

 9$collection->forget(['name', 'framework']);

10 

11// []
```

Unlike most other collection methods, `forget` does not return a new modified collection; it modifies and returns the collection it is called on.

#### [`forPage()`](#method-forpage)

The `forPage` method returns a new collection containing the items that would be present on a given page number. The method accepts the page number as its first argument and the number of items to show per page as its second argument:

```
1$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

2 

3$chunk = $collection->forPage(2, 3);

4 

5$chunk->all();

6 

7// [4, 5, 6]
```

#### [`fromJson()`](#method-fromjson)

The static `fromJson` method creates a new collection instance by decoding a given JSON string using the `json_decode` PHP function:

```
1use Illuminate\Support\Collection;

2 

3$json = json_encode([

4    'name' => 'Taylor Otwell',

5    'role' => 'Developer',

6    'status' => 'Active',

7]);

8 

9$collection = Collection::fromJson($json);
```

#### [`get()`](#method-get)

The `get` method returns the item at a given key. If the key does not exist, `null` is returned:

```
1$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

2 

3$value = $collection->get('name');

4 

5// Taylor
```

You may optionally pass a default value as the second argument:

```
1$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

2 

3$value = $collection->get('age', 34);

4 

5// 34
```

You may even pass a callback as the method's default value. The result of the callback will be returned if the specified key does not exist:

```
1$collection->get('email', function () {

2    return '[[email protected]](/cdn-cgi/l/email-protection)';

3});

4 

5// [[email protected]](/cdn-cgi/l/email-protection)
```

#### [`groupBy()`](#method-groupby)

The `groupBy` method groups the collection's items by a given key:

```
 1$collection = collect([

 2    ['account_id' => 'account-x10', 'product' => 'Chair'],

 3    ['account_id' => 'account-x10', 'product' => 'Bookcase'],

 4    ['account_id' => 'account-x11', 'product' => 'Desk'],

 5]);

 6 

 7$grouped = $collection->groupBy('account_id');

 8 

 9$grouped->all();

10 

11/*

12    [

13        'account-x10' => [

14            ['account_id' => 'account-x10', 'product' => 'Chair'],

15            ['account_id' => 'account-x10', 'product' => 'Bookcase'],

16        ],

17        'account-x11' => [

18            ['account_id' => 'account-x11', 'product' => 'Desk'],

19        ],

20    ]

21*/
```

Instead of passing a string `key`, you may pass a callback. The callback should return the value you wish to key the group by:

```
 1$grouped = $collection->groupBy(function (array $item, int $key) {

 2    return substr($item['account_id'], -3);

 3});

 4 

 5$grouped->all();

 6 

 7/*

 8    [

 9        'x10' => [

10            ['account_id' => 'account-x10', 'product' => 'Chair'],

11            ['account_id' => 'account-x10', 'product' => 'Bookcase'],

12        ],

13        'x11' => [

14            ['account_id' => 'account-x11', 'product' => 'Desk'],

15        ],

16    ]

17*/
```

Multiple grouping criteria may be passed as an array. Each array element will be applied to the corresponding level within a multi-dimensional array:

```
 1$data = new Collection([

 2    10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],

 3    20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],

 4    30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],

 5    40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],

 6]);

 7 

 8$result = $data->groupBy(['skill', function (array $item) {

 9    return $item['roles'];

10}], preserveKeys: true);

11 

12/*

13[

14    1 => [

15        'Role_1' => [

16            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],

17            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],

18        ],

19        'Role_2' => [

20            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],

21        ],

22        'Role_3' => [

23            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],

24        ],

25    ],

26    2 => [

27        'Role_1' => [

28            30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],

29        ],

30        'Role_2' => [

31            40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],

32        ],

33    ],

34];

35*/
```

#### [`has()`](#method-has)

The `has` method determines if a given key exists in the collection:

```
 1$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

 2 

 3$collection->has('product');

 4 

 5// true

 6 

 7$collection->has(['product', 'amount']);

 8 

 9// true

10 

11$collection->has(['amount', 'price']);

12 

13// false
```

#### [`hasAny()`](#method-hasany)

The `hasAny` method determines whether any of the given keys exist in the collection:

```
1$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

2 

3$collection->hasAny(['product', 'price']);

4 

5// true

6 

7$collection->hasAny(['name', 'price']);

8 

9// false
```

#### [`hasMany()`](#method-hasmany)

The `hasMany` method determines whether the collection contains multiple items:

```
 1collect([])->hasMany();

 2 

 3// false

 4 

 5collect(['1'])->hasMany();

 6 

 7// false

 8 

 9collect([1, 2, 3])->hasMany();

10 

11// true

12 

13collect([

14    ['age' => 2],

15    ['age' => 3],

16])->hasMany(fn ($item) => $item['age'] === 2)

17 

18// false
```

#### [`hasSole()`](#method-hassole)

The `hasSole` method determines if the collection contains a single item, optionally matching the given criteria:

```
 1collect([])->hasSole();

 2 

 3// false

 4 

 5collect(['1'])->hasSole();

 6 

 7// true

 8 

 9collect([1, 2, 3])->hasSole(fn (int $item) => $item === 2);

10 

11// true
```

#### [`implode()`](#method-implode)

The `implode` method joins items in a collection. Its arguments depend on the type of items in the collection. If the collection contains arrays or objects, you should pass the key of the attributes you wish to join, and the "glue" string you wish to place between the values:

```
1$collection = collect([

2    ['account_id' => 1, 'product' => 'Desk'],

3    ['account_id' => 2, 'product' => 'Chair'],

4]);

5 

6$collection->implode('product', ', ');

7 

8// 'Desk, Chair'
```

If the collection contains simple strings or numeric values, you should pass the "glue" as the only argument to the method:

```
1collect([1, 2, 3, 4, 5])->implode('-');

2 

3// '1-2-3-4-5'
```

You may pass a closure to the `implode` method if you would like to format the values being imploded:

```
1$collection->implode(function (array $item, int $key) {

2    return strtoupper($item['product']);

3}, ', ');

4 

5// 'DESK, CHAIR'
```

#### [`intersect()`](#method-intersect)

The `intersect` method removes any values from the original collection that are not present in the given array or collection. The resulting collection will preserve the original collection's keys:

```
1$collection = collect(['Desk', 'Sofa', 'Chair']);

2 

3$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

4 

5$intersect->all();

6 

7// [0 => 'Desk', 2 => 'Chair']
```

This method's behavior is modified when using [Eloquent Collections](/docs/13.x/eloquent-collections#method-intersect).

#### [`intersectUsing()`](#method-intersectusing)

The `intersectUsing` method removes any values from the original collection that are not present in the given array or collection, using a custom callback to compare the values. The resulting collection will preserve the original collection's keys:

```
1$collection = collect(['Desk', 'Sofa', 'Chair']);

2 

3$intersect = $collection->intersectUsing(['desk', 'chair', 'bookcase'], function (string $a, string $b) {

4    return strcasecmp($a, $b);

5});

6 

7$intersect->all();

8 

9// [0 => 'Desk', 2 => 'Chair']
```

#### [`intersectAssoc()`](#method-intersectAssoc)

The `intersectAssoc` method compares the original collection against another collection or array, returning the key / value pairs that are present in all of the given collections:

```
 1$collection = collect([

 2    'color' => 'red',

 3    'size' => 'M',

 4    'material' => 'cotton'

 5]);

 6 

 7$intersect = $collection->intersectAssoc([

 8    'color' => 'blue',

 9    'size' => 'M',

10    'material' => 'polyester'

11]);

12 

13$intersect->all();

14 

15// ['size' => 'M']
```

#### [`intersectAssocUsing()`](#method-intersectassocusing)

The `intersectAssocUsing` method compares the original collection against another collection or array, returning the key / value pairs that are present in both, using a custom comparison callback to determine equality for both keys and values:

```
 1$collection = collect([

 2    'color' => 'red',

 3    'Size' => 'M',

 4    'material' => 'cotton',

 5]);

 6 

 7$intersect = $collection->intersectAssocUsing([

 8    'color' => 'blue',

 9    'size' => 'M',

10    'material' => 'polyester',

11], function (string $a, string $b) {

12    return strcasecmp($a, $b);

13});

14 

15$intersect->all();

16 

17// ['Size' => 'M']
```

#### [`intersectByKeys()`](#method-intersectbykeys)

The `intersectByKeys` method removes any keys and their corresponding values from the original collection that are not present in the given array or collection:

```
 1$collection = collect([

 2    'serial' => 'UX301', 'type' => 'screen', 'year' => 2009,

 3]);

 4 

 5$intersect = $collection->intersectByKeys([

 6    'reference' => 'UX404', 'type' => 'tab', 'year' => 2011,

 7]);

 8 

 9$intersect->all();

10 

11// ['type' => 'screen', 'year' => 2009]
```

#### [`isEmpty()`](#method-isempty)

The `isEmpty` method returns `true` if the collection is empty; otherwise, `false` is returned:

```
1collect([])->isEmpty();

2 

3// true
```

#### [`isNotEmpty()`](#method-isnotempty)

The `isNotEmpty` method returns `true` if the collection is not empty; otherwise, `false` is returned:

```
1collect([])->isNotEmpty();

2 

3// false
```

#### [`join()`](#method-join)

The `join` method joins the collection's values with a string. Using this method's second argument, you may also specify how the final element should be appended to the string:

```
1collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'

2collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'

3collect(['a', 'b'])->join(', ', ' and '); // 'a and b'

4collect(['a'])->join(', ', ' and '); // 'a'

5collect([])->join(', ', ' and '); // ''
```

#### [`keyBy()`](#method-keyby)

The `keyBy` method keys the collection by the given key. If multiple items have the same key, only the last one will appear in the new collection:

```
 1$collection = collect([

 2    ['product_id' => 'prod-100', 'name' => 'Desk'],

 3    ['product_id' => 'prod-200', 'name' => 'Chair'],

 4]);

 5 

 6$keyed = $collection->keyBy('product_id');

 7 

 8$keyed->all();

 9 

10/*

11    [

12        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],

13        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],

14    ]

15*/
```

You may also pass a callback to the method. The callback should return the value to key the collection by:

```
 1$keyed = $collection->keyBy(function (array $item, int $key) {

 2    return strtoupper($item['product_id']);

 3});

 4 

 5$keyed->all();

 6 

 7/*

 8    [

 9        'PROD-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],

10        'PROD-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],

11    ]

12*/
```

#### [`keys()`](#method-keys)

The `keys` method returns all of the collection's keys:

```
 1$collection = collect([

 2    'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],

 3    'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],

 4]);

 5 

 6$keys = $collection->keys();

 7 

 8$keys->all();

 9 

10// ['prod-100', 'prod-200']
```

#### [`last()`](#method-last)

The `last` method returns the last element in the collection that passes a given truth test:

```
1collect([1, 2, 3, 4])->last(function (int $value, int $key) {

2    return $value < 3;

3});

4 

5// 2
```

You may also call the `last` method with no arguments to get the last element in the collection. If the collection is empty, `null` is returned:

```
1collect([1, 2, 3, 4])->last();

2 

3// 4
```

#### [`lazy()`](#method-lazy)

The `lazy` method returns a new [LazyCollection](#lazy-collections) instance from the underlying array of items:

```
1$lazyCollection = collect([1, 2, 3, 4])->lazy();

2 

3$lazyCollection::class;

4 

5// Illuminate\Support\LazyCollection

6 

7$lazyCollection->all();

8 

9// [1, 2, 3, 4]
```

This is especially useful when you need to perform transformations on a huge `Collection` that contains many items:

```
1$count = $hugeCollection

2    ->lazy()

3    ->where('country', 'FR')

4    ->where('balance', '>', '100')

5    ->count();
```

By converting the collection to a `LazyCollection`, we avoid having to allocate a ton of additional memory. Though the original collection still keeps *its* values in memory, the subsequent filters will not. Therefore, virtually no additional memory will be allocated when filtering the collection's results.

#### [`macro()`](#method-macro)

The static `macro` method allows you to add methods to the `Collection` class at run time. Refer to the documentation on [extending collections](#extending-collections) for more information.

#### [`make()`](#method-make)

The static `make` method creates a new collection instance. See the [Creating Collections](#creating-collections) section.

```
1use Illuminate\Support\Collection;

2 

3$collection = Collection::make([1, 2, 3]);
```

#### [`map()`](#method-map)

The `map` method iterates through the collection and passes each value to the given callback. The callback is free to modify the item and return it, thus forming a new collection of modified items:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$multiplied = $collection->map(function (int $item, int $key) {

4    return $item * 2;

5});

6 

7$multiplied->all();

8 

9// [2, 4, 6, 8, 10]
```

Like most other collection methods, `map` returns a new collection instance; it does not modify the collection it is called on. If you want to transform the original collection, use the [transform](#method-transform) method.

#### [`mapInto()`](#method-mapinto)

The `mapInto()` method iterates over the collection, creating a new instance of the given class by passing the value into the constructor:

```
 1class Currency

 2{

 3    /**

 4     * Create a new currency instance.

 5     */

 6    function __construct(

 7        public string $code,

 8    ) {}

 9}

10 

11$collection = collect(['USD', 'EUR', 'GBP']);

12 

13$currencies = $collection->mapInto(Currency::class);

14 

15$currencies->all();

16 

17// [Currency('USD'), Currency('EUR'), Currency('GBP')]
```

#### [`mapSpread()`](#method-mapspread)

The `mapSpread` method iterates over the collection's items, passing each nested item value into the given closure. The closure is free to modify the item and return it, thus forming a new collection of modified items:

```
 1$collection = collect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);

 2 

 3$chunks = $collection->chunk(2);

 4 

 5$sequence = $chunks->mapSpread(function (int $even, int $odd) {

 6    return $even + $odd;

 7});

 8 

 9$sequence->all();

10 

11// [1, 5, 9, 13, 17]
```

#### [`mapToGroups()`](#method-maptogroups)

The `mapToGroups` method groups the collection's items by the given closure. The closure should return an associative array containing a single key / value pair, thus forming a new collection of grouped values:

```
 1$collection = collect([

 2    [

 3        'name' => 'John Doe',

 4        'department' => 'Sales',

 5    ],

 6    [

 7        'name' => 'Jane Doe',

 8        'department' => 'Sales',

 9    ],

10    [

11        'name' => 'Johnny Doe',

12        'department' => 'Marketing',

13    ]

14]);

15 

16$grouped = $collection->mapToGroups(function (array $item, int $key) {

17    return [$item['department'] => $item['name']];

18});

19 

20$grouped->all();

21 

22/*

23    [

24        'Sales' => ['John Doe', 'Jane Doe'],

25        'Marketing' => ['Johnny Doe'],

26    ]

27*/

28 

29$grouped->get('Sales')->all();

30 

31// ['John Doe', 'Jane Doe']
```

#### [`mapWithKeys()`](#method-mapwithkeys)

The `mapWithKeys` method iterates through the collection and passes each value to the given callback. The callback should return an associative array containing a single key / value pair:

```
 1$collection = collect([

 2    [

 3        'name' => 'John',

 4        'department' => 'Sales',

 5        'email' => '[[email protected]](/cdn-cgi/l/email-protection)',

 6    ],

 7    [

 8        'name' => 'Jane',

 9        'department' => 'Marketing',

10        'email' => '[[email protected]](/cdn-cgi/l/email-protection)',

11    ]

12]);

13 

14$keyed = $collection->mapWithKeys(function (array $item, int $key) {

15    return [$item['email'] => $item['name']];

16});

17 

18$keyed->all();

19 

20/*

21    [

22        '[[email protected]](/cdn-cgi/l/email-protection)' => 'John',

23        '[[email protected]](/cdn-cgi/l/email-protection)' => 'Jane',

24    ]

25*/
```

#### [`max()`](#method-max)

The `max` method returns the maximum value of a given key:

```
 1$max = collect([

 2    ['foo' => 10],

 3    ['foo' => 20]

 4])->max('foo');

 5 

 6// 20

 7 

 8$max = collect([1, 2, 3, 4, 5])->max();

 9 

10// 5
```

#### [`median()`](#method-median)

The `median` method returns the [median value](https://en.wikipedia.org/wiki/Median) of a given key:

```
 1$median = collect([

 2    ['foo' => 10],

 3    ['foo' => 10],

 4    ['foo' => 20],

 5    ['foo' => 40]

 6])->median('foo');

 7 

 8// 15

 9 

10$median = collect([1, 1, 2, 4])->median();

11 

12// 1.5
```

#### [`merge()`](#method-merge)

The `merge` method merges the given array or collection with the original collection. If a string key in the given items matches a string key in the original collection, the given item's value will overwrite the value in the original collection:

```
1$collection = collect(['product_id' => 1, 'price' => 100]);

2 

3$merged = $collection->merge(['price' => 200, 'discount' => false]);

4 

5$merged->all();

6 

7// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

If the given item's keys are numeric, the values will be appended to the end of the collection:

```
1$collection = collect(['Desk', 'Chair']);

2 

3$merged = $collection->merge(['Bookcase', 'Door']);

4 

5$merged->all();

6 

7// ['Desk', 'Chair', 'Bookcase', 'Door']
```

#### [`mergeRecursive()`](#method-mergerecursive)

The `mergeRecursive` method merges the given array or collection recursively with the original collection. If a string key in the given items matches a string key in the original collection, then the values for these keys are merged together into an array, and this is done recursively:

```
 1$collection = collect(['product_id' => 1, 'price' => 100]);

 2 

 3$merged = $collection->mergeRecursive([

 4    'product_id' => 2,

 5    'price' => 200,

 6    'discount' => false

 7]);

 8 

 9$merged->all();

10 

11// ['product_id' => [1, 2], 'price' => [100, 200], 'discount' => false]
```

#### [`min()`](#method-min)

The `min` method returns the minimum value of a given key:

```
 1$min = collect([

 2    ['foo' => 10],

 3    ['foo' => 20]

 4])->min('foo');

 5 

 6// 10

 7 

 8$min = collect([1, 2, 3, 4, 5])->min();

 9 

10// 1
```

#### [`mode()`](#method-mode)

The `mode` method returns the [mode value](https://en.wikipedia.org/wiki/Mode_(statistics)) of a given key:

```
 1$mode = collect([

 2    ['foo' => 10],

 3    ['foo' => 10],

 4    ['foo' => 20],

 5    ['foo' => 40]

 6])->mode('foo');

 7 

 8// [10]

 9 

10$mode = collect([1, 1, 2, 4])->mode();

11 

12// [1]

13 

14$mode = collect([1, 1, 2, 2])->mode();

15 

16// [1, 2]
```

#### [`multiply()`](#method-multiply)

The `multiply` method creates the specified number of copies of all items in the collection:

```
 1$users = collect([

 2    ['name' => 'User #1', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

 3    ['name' => 'User #2', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

 4])->multiply(3);

 5 

 6/*

 7    [

 8        ['name' => 'User #1', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

 9        ['name' => 'User #2', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

10        ['name' => 'User #1', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

11        ['name' => 'User #2', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

12        ['name' => 'User #1', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

13        ['name' => 'User #2', 'email' => '[[email protected]](/cdn-cgi/l/email-protection)'],

14    ]

15*/
```

#### [`nth()`](#method-nth)

The `nth` method creates a new collection consisting of every n-th element:

```
1$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

2 

3$collection->nth(4);

4 

5// ['a', 'e']
```

You may optionally pass a starting offset as the second argument:

```
1$collection->nth(4, 1);

2 

3// ['b', 'f']
```

#### [`only()`](#method-only)

The `only` method returns the items in the collection with the specified keys:

```
 1$collection = collect([

 2    'product_id' => 1,

 3    'name' => 'Desk',

 4    'price' => 100,

 5    'discount' => false

 6]);

 7 

 8$filtered = $collection->only(['product_id', 'name']);

 9 

10$filtered->all();

11 

12// ['product_id' => 1, 'name' => 'Desk']
```

For the inverse of `only`, see the [except](#method-except) method.

This method's behavior is modified when using [Eloquent Collections](/docs/13.x/eloquent-collections#method-only).

#### [`pad()`](#method-pad)

The `pad` method will fill the array with the given value until the array reaches the specified size. This method behaves like the [array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP function.

To pad to the left, you should specify a negative size. No padding will take place if the absolute value of the given size is less than or equal to the length of the array:

```
 1$collection = collect(['A', 'B', 'C']);

 2 

 3$filtered = $collection->pad(5, 0);

 4 

 5$filtered->all();

 6 

 7// ['A', 'B', 'C', 0, 0]

 8 

 9$filtered = $collection->pad(-5, 0);

10 

11$filtered->all();

12 

13// [0, 0, 'A', 'B', 'C']
```

#### [`partition()`](#method-partition)

The `partition` method may be combined with PHP array destructuring to separate elements that pass a given truth test from those that do not:

```
 1$collection = collect([1, 2, 3, 4, 5, 6]);

 2 

 3[$underThree, $equalOrAboveThree] = $collection->partition(function (int $i) {

 4    return $i < 3;

 5});

 6 

 7$underThree->all();

 8 

 9// [1, 2]

10 

11$equalOrAboveThree->all();

12 

13// [3, 4, 5, 6]
```

This method's behavior is modified when interacting with [Eloquent collections](/docs/13.x/eloquent-collections#method-partition).

#### [`percentage()`](#method-percentage)

The `percentage` method may be used to quickly determine the percentage of items in the collection that pass a given truth test:

```
1$collection = collect([1, 1, 2, 2, 2, 3]);

2 

3$percentage = $collection->percentage(fn (int $value) => $value === 1);

4 

5// 33.33
```

By default, the percentage will be rounded to two decimal places. However, you may customize this behavior by providing a second argument to the method:

```
1$percentage = $collection->percentage(fn (int $value) => $value === 1, precision: 3);

2 

3// 33.333
```

#### [`pipe()`](#method-pipe)

The `pipe` method passes the collection to the given closure and returns the result of the executed closure:

```
1$collection = collect([1, 2, 3]);

2 

3$piped = $collection->pipe(function (Collection $collection) {

4    return $collection->sum();

5});

6 

7// 6
```

#### [`pipeInto()`](#method-pipeinto)

The `pipeInto` method creates a new instance of the given class and passes the collection into the constructor:

```
 1class ResourceCollection

 2{

 3    /**

 4     * Create a new ResourceCollection instance.

 5     */

 6    public function __construct(

 7        public Collection $collection,

 8    ) {}

 9}

10 

11$collection = collect([1, 2, 3]);

12 

13$resource = $collection->pipeInto(ResourceCollection::class);

14 

15$resource->collection->all();

16 

17// [1, 2, 3]
```

#### [`pipeThrough()`](#method-pipethrough)

The `pipeThrough` method passes the collection to the given array of closures and returns the result of the executed closures:

```
 1use Illuminate\Support\Collection;

 2 

 3$collection = collect([1, 2, 3]);

 4 

 5$result = $collection->pipeThrough([

 6    function (Collection $collection) {

 7        return $collection->merge([4, 5]);

 8    },

 9    function (Collection $collection) {

10        return $collection->sum();

11    },

12]);

13 

14// 15
```

#### [`pluck()`](#method-pluck)

The `pluck` method retrieves all of the values for a given key:

```
 1$collection = collect([

 2    ['product_id' => 'prod-100', 'name' => 'Desk'],

 3    ['product_id' => 'prod-200', 'name' => 'Chair'],

 4]);

 5 

 6$plucked = $collection->pluck('name');

 7 

 8$plucked->all();

 9 

10// ['Desk', 'Chair']
```

You may also specify how you wish the resulting collection to be keyed:

```
1$plucked = $collection->pluck('name', 'product_id');

2 

3$plucked->all();

4 

5// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

The `pluck` method also supports retrieving nested values using "dot" notation:

```
 1$collection = collect([

 2    [

 3        'name' => 'Laracon',

 4        'speakers' => [

 5            'first_day' => ['Rosa', 'Judith'],

 6        ],

 7    ],

 8    [

 9        'name' => 'VueConf',

10        'speakers' => [

11            'first_day' => ['Abigail', 'Joey'],

12        ],

13    ],

14]);

15 

16$plucked = $collection->pluck('speakers.first_day');

17 

18$plucked->all();

19 

20// [['Rosa', 'Judith'], ['Abigail', 'Joey']]
```

If duplicate keys exist, the last matching element will be inserted into the plucked collection:

```
 1$collection = collect([

 2    ['brand' => 'Tesla',  'color' => 'red'],

 3    ['brand' => 'Pagani', 'color' => 'white'],

 4    ['brand' => 'Tesla',  'color' => 'black'],

 5    ['brand' => 'Pagani', 'color' => 'orange'],

 6]);

 7 

 8$plucked = $collection->pluck('color', 'brand');

 9 

10$plucked->all();

11 

12// ['Tesla' => 'black', 'Pagani' => 'orange']
```

#### [`pop()`](#method-pop)

The `pop` method removes and returns the last item from the collection. If the collection is empty, `null` will be returned:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->pop();

4 

5// 5

6 

7$collection->all();

8 

9// [1, 2, 3, 4]
```

You may pass an integer to the `pop` method to remove and return multiple items from the end of a collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->pop(3);

4 

5// collect([5, 4, 3])

6 

7$collection->all();

8 

9// [1, 2]
```

#### [`prepend()`](#method-prepend)

The `prepend` method adds an item to the beginning of the collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->prepend(0);

4 

5$collection->all();

6 

7// [0, 1, 2, 3, 4, 5]
```

You may also pass a second argument to specify the key of the prepended item:

```
1$collection = collect(['one' => 1, 'two' => 2]);

2 

3$collection->prepend(0, 'zero');

4 

5$collection->all();

6 

7// ['zero' => 0, 'one' => 1, 'two' => 2]
```

#### [`pull()`](#method-pull)

The `pull` method removes and returns an item from the collection by its key:

```
1$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

2 

3$collection->pull('name');

4 

5// 'Desk'

6 

7$collection->all();

8 

9// ['product_id' => 'prod-100']
```

#### [`push()`](#method-push)

The `push` method appends an item to the end of the collection:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$collection->push(5);

4 

5$collection->all();

6 

7// [1, 2, 3, 4, 5]
```

You may also provide multiple items to append to the end of the collection:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$collection->push(5, 6, 7);

4 

5$collection->all();

6 

7// [1, 2, 3, 4, 5, 6, 7]
```

#### [`put()`](#method-put)

The `put` method sets the given key and value in the collection:

```
1$collection = collect(['product_id' => 1, 'name' => 'Desk']);

2 

3$collection->put('price', 100);

4 

5$collection->all();

6 

7// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

#### [`random()`](#method-random)

The `random` method returns a random item from the collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->random();

4 

5// 4 - (retrieved randomly)
```

You may pass an integer to `random` to specify how many items you would like to randomly retrieve. A collection of items is always returned when explicitly passing the number of items you wish to receive:

```
1$random = $collection->random(3);

2 

3$random->all();

4 

5// [2, 4, 5] - (retrieved randomly)
```

If the collection instance has fewer items than requested, the `random` method will throw an `InvalidArgumentException`.

The `random` method also accepts a closure, which will receive the current collection instance:

```
1use Illuminate\Support\Collection;

2 

3$random = $collection->random(fn (Collection $items) => min(10, count($items)));

4 

5$random->all();

6 

7// [1, 2, 3, 4, 5] - (retrieved randomly)
```

#### [`range()`](#method-range)

The `range` method returns a collection containing integers between the specified range:

```
1$collection = collect()->range(3, 6);

2 

3$collection->all();

4 

5// [3, 4, 5, 6]
```

#### [`reduce()`](#method-reduce)

The `reduce` method reduces the collection to a single value, passing the result of each iteration into the subsequent iteration:

```
1$collection = collect([1, 2, 3]);

2 

3$total = $collection->reduce(function (?int $carry, int $item) {

4    return $carry + $item;

5});

6 

7// 6
```

The value for `$carry` on the first iteration is `null`; however, you may specify its initial value by passing a second argument to `reduce`:

```
1$collection->reduce(function (int $carry, int $item) {

2    return $carry + $item;

3}, 4);

4 

5// 10
```

The `reduce` method also passes array keys to the given callback:

```
 1$collection = collect([

 2    'usd' => 1400,

 3    'gbp' => 1200,

 4    'eur' => 1000,

 5]);

 6 

 7$ratio = [

 8    'usd' => 1,

 9    'gbp' => 1.37,

10    'eur' => 1.22,

11];

12 

13$collection->reduce(function (int $carry, int $value, string $key) use ($ratio) {

14    return $carry + ($value * $ratio[$key]);

15}, 0);

16 

17// 4264
```

#### [`reduceInto()`](#method-reduce-into)

The `reduceInto` method reduces the collection to a single value by mutating the given initial value. Unlike the `reduce` method, the given callback does not need to return the accumulated value:

```
 1class OrderStats

 2{

 3    public int $total = 0;

 4 

 5    public int $count = 0;

 6}

 7 

 8$orders = collect([

 9    ['amount' => 100],

10    ['amount' => 250],

11    ['amount' => 50],

12]);

13 

14$stats = $orders->reduceInto(new OrderStats, function (OrderStats $stats, array $order) {

15    $stats->total += $order['amount'];

16    $stats->count++;

17});

18 

19$stats->total;

20 

21// 400
```

When reducing into a scalar or array, you should accept it by reference in the callback so that your mutations are applied to the original value:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$even = $collection->reduceInto([], function (array &$result, int $value) {

4    if ($value % 2 === 0) {

5        $result[] = $value;

6    }

7});

8 

9// [2, 4]
```

#### [`reduceSpread()`](#method-reduce-spread)

The `reduceSpread` method reduces the collection to an array of values, passing the results of each iteration into the subsequent iteration. This method is similar to the `reduce` method; however, it can accept multiple initial values:

```
 1[$creditsRemaining, $batch] = Image::where('status', 'unprocessed')

 2    ->get()

 3    ->reduceSpread(function (int $creditsRemaining, Collection $batch, Image $image) {

 4        if ($creditsRemaining >= $image->creditsRequired()) {

 5            $batch->push($image);

 6 

 7            $creditsRemaining -= $image->creditsRequired();

 8        }

 9 

10        return [$creditsRemaining, $batch];

11    }, $creditsAvailable, collect());
```

#### [`reject()`](#method-reject)

The `reject` method filters the collection using the given closure. The closure should return `true` if the item should be removed from the resulting collection:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$filtered = $collection->reject(function (int $value, int $key) {

4    return $value > 2;

5});

6 

7$filtered->all();

8 

9// [1, 2]
```

For the inverse of the `reject` method, see the [filter](#method-filter) method.

#### [`replace()`](#method-replace)

The `replace` method behaves similarly to `merge`; however, in addition to overwriting matching items that have string keys, the `replace` method will also overwrite items in the collection that have matching numeric keys:

```
1$collection = collect(['Taylor', 'Abigail', 'James']);

2 

3$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

4 

5$replaced->all();

6 

7// ['Taylor', 'Victoria', 'James', 'Finn']
```

#### [`replaceRecursive()`](#method-replacerecursive)

The `replaceRecursive` method behaves similarly to `replace`, but it will recur into arrays and apply the same replacement process to the inner values:

```
 1$collection = collect([

 2    'Taylor',

 3    'Abigail',

 4    [

 5        'James',

 6        'Victoria',

 7        'Finn'

 8    ]

 9]);

10 

11$replaced = $collection->replaceRecursive([

12    'Charlie',

13    2 => [1 => 'King']

14]);

15 

16$replaced->all();

17 

18// ['Charlie', 'Abigail', ['James', 'King', 'Finn']]
```

#### [`reverse()`](#method-reverse)

The `reverse` method reverses the order of the collection's items, preserving the original keys:

```
 1$collection = collect(['a', 'b', 'c', 'd', 'e']);

 2 

 3$reversed = $collection->reverse();

 4 

 5$reversed->all();

 6 

 7/*

 8    [

 9        4 => 'e',

10        3 => 'd',

11        2 => 'c',

12        1 => 'b',

13        0 => 'a',

14    ]

15*/
```

#### [`search()`](#method-search)

The `search` method searches the collection for the given value and returns its key if found. If the item is not found, `false` is returned:

```
1$collection = collect([2, 4, 6, 8]);

2 

3$collection->search(4);

4 

5// 1
```

The search is done using a "loose" comparison, meaning a string with an integer value will be considered equal to an integer of the same value. To use "strict" comparison, pass `true` as the second argument to the method:

```
1collect([2, 4, 6, 8])->search('4', strict: true);

2 

3// false
```

Alternatively, you may provide your own closure to search for the first item that passes a given truth test:

```
1collect([2, 4, 6, 8])->search(function (int $item, int $key) {

2    return $item > 5;

3});

4 

5// 2
```

#### [`select()`](#method-select)

The `select` method selects the given keys from the collection, similar to an SQL `SELECT` statement:

```
 1$users = collect([

 2    ['name' => 'Taylor Otwell', 'role' => 'Developer', 'status' => 'active'],

 3    ['name' => 'Victoria Faith', 'role' => 'Researcher', 'status' => 'active'],

 4]);

 5 

 6$users->select(['name', 'role']);

 7 

 8/*

 9    [

10        ['name' => 'Taylor Otwell', 'role' => 'Developer'],

11        ['name' => 'Victoria Faith', 'role' => 'Researcher'],

12    ],

13*/
```

#### [`shift()`](#method-shift)

The `shift` method removes and returns the first item from the collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->shift();

4 

5// 1

6 

7$collection->all();

8 

9// [2, 3, 4, 5]
```

You may pass an integer to the `shift` method to remove and return multiple items from the beginning of a collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->shift(3);

4 

5// collect([1, 2, 3])

6 

7$collection->all();

8 

9// [4, 5]
```

#### [`shuffle()`](#method-shuffle)

The `shuffle` method randomly shuffles the items in the collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$shuffled = $collection->shuffle();

4 

5$shuffled->all();

6 

7// [3, 2, 5, 1, 4] - (generated randomly)
```

#### [`skip()`](#method-skip)

The `skip` method returns a new collection, with the given number of elements removed from the beginning of the collection:

```
1$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

2 

3$collection = $collection->skip(4);

4 

5$collection->all();

6 

7// [5, 6, 7, 8, 9, 10]
```

#### [`skipUntil()`](#method-skipuntil)

The `skipUntil` method skips over items from the collection while the given callback returns `false`. Once the callback returns `true` all of the remaining items in the collection will be returned as a new collection:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$subset = $collection->skipUntil(function (int $item) {

4    return $item >= 3;

5});

6 

7$subset->all();

8 

9// [3, 4]
```

You may also pass a simple value to the `skipUntil` method to skip all items until the given value is found:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$subset = $collection->skipUntil(3);

4 

5$subset->all();

6 

7// [3, 4]
```

If the given value is not found or the callback never returns `true`, the `skipUntil` method will return an empty collection.

#### [`skipWhile()`](#method-skipwhile)

The `skipWhile` method skips over items from the collection while the given callback returns `true`. Once the callback returns `false` all of the remaining items in the collection will be returned as a new collection:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$subset = $collection->skipWhile(function (int $item) {

4    return $item <= 3;

5});

6 

7$subset->all();

8 

9// [4]
```

If the callback never returns `false`, the `skipWhile` method will return an empty collection.

#### [`slice()`](#method-slice)

The `slice` method returns a slice of the collection starting at the given index:

```
1$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

2 

3$slice = $collection->slice(4);

4 

5$slice->all();

6 

7// [5, 6, 7, 8, 9, 10]
```

If you would like to limit the size of the returned slice, pass the desired size as the second argument to the method:

```
1$slice = $collection->slice(4, 2);

2 

3$slice->all();

4 

5// [5, 6]
```

The returned slice will preserve keys by default. If you do not wish to preserve the original keys, you can use the [values](#method-values) method to reindex them.

#### [`sliding()`](#method-sliding)

The `sliding` method returns a new collection of chunks representing a "sliding window" view of the items in the collection:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$chunks = $collection->sliding(2);

4 

5$chunks->toArray();

6 

7// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

This is especially useful in conjunction with the [eachSpread](#method-eachspread) method:

```
1$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {

2    $current->total = $previous->total + $current->amount;

3});
```

You may optionally pass a second "step" value, which determines the distance between the first item of every chunk:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$chunks = $collection->sliding(3, step: 2);

4 

5$chunks->toArray();

6 

7// [[1, 2, 3], [3, 4, 5]]
```

#### [`sole()`](#method-sole)

The `sole` method returns the first element in the collection that passes a given truth test, but only if the truth test matches exactly one element:

```
1collect([1, 2, 3, 4])->sole(function (int $value, int $key) {

2    return $value === 2;

3});

4 

5// 2
```

You may also pass a key / value pair to the `sole` method, which will return the first element in the collection that matches the given pair, but only if it exactly one element matches:

```
1$collection = collect([

2    ['product' => 'Desk', 'price' => 200],

3    ['product' => 'Chair', 'price' => 100],

4]);

5 

6$collection->sole('product', 'Chair');

7 

8// ['product' => 'Chair', 'price' => 100]
```

Alternatively, you may also call the `sole` method with no argument to get the first element in the collection if there is only one element:

```
1$collection = collect([

2    ['product' => 'Desk', 'price' => 200],

3]);

4 

5$collection->sole();

6 

7// ['product' => 'Desk', 'price' => 200]
```

If there are no elements in the collection that should be returned by the `sole` method, an `\Illuminate\Collections\ItemNotFoundException` exception will be thrown. If there is more than one element that should be returned, an `\Illuminate\Collections\MultipleItemsFoundException` will be thrown.

#### [`some()`](#method-some)

Alias for the [contains](#method-contains) method.

#### [`sort()`](#method-sort)

The `sort` method sorts the collection. The sorted collection keeps the original array keys, so in the following example we will use the [values](#method-values) method to reset the keys to consecutively numbered indexes:

```
1$collection = collect([5, 3, 1, 2, 4]);

2 

3$sorted = $collection->sort();

4 

5$sorted->values()->all();

6 

7// [1, 2, 3, 4, 5]
```

If your sorting needs are more advanced, you may pass a callback to `sort` with your own algorithm. Refer to the PHP documentation on [uasort](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters), which is what the collection's `sort` method calls utilizes internally.

If you need to sort a collection of nested arrays or objects, see the [sortBy](#method-sortby) and [sortByDesc](#method-sortbydesc) methods.

#### [`sortBy()`](#method-sortby)

The `sortBy` method sorts the collection by the given key. The sorted collection keeps the original array keys, so in the following example we will use the [values](#method-values) method to reset the keys to consecutively numbered indexes:

```
 1$collection = collect([

 2    ['name' => 'Desk', 'price' => 200],

 3    ['name' => 'Chair', 'price' => 100],

 4    ['name' => 'Bookcase', 'price' => 150],

 5]);

 6 

 7$sorted = $collection->sortBy('price');

 8 

 9$sorted->values()->all();

10 

11/*

12    [

13        ['name' => 'Chair', 'price' => 100],

14        ['name' => 'Bookcase', 'price' => 150],

15        ['name' => 'Desk', 'price' => 200],

16    ]

17*/
```

The `sortBy` method accepts [sort flags](https://www.php.net/manual/en/function.sort.php) as its second argument:

```
 1$collection = collect([

 2    ['title' => 'Item 1'],

 3    ['title' => 'Item 12'],

 4    ['title' => 'Item 3'],

 5]);

 6 

 7$sorted = $collection->sortBy('title', SORT_NATURAL);

 8 

 9$sorted->values()->all();

10 

11/*

12    [

13        ['title' => 'Item 1'],

14        ['title' => 'Item 3'],

15        ['title' => 'Item 12'],

16    ]

17*/
```

Alternatively, you may pass your own closure to determine how to sort the collection's values:

```
 1$collection = collect([

 2    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],

 3    ['name' => 'Chair', 'colors' => ['Black']],

 4    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],

 5]);

 6 

 7$sorted = $collection->sortBy(function (array $product, int $key) {

 8    return count($product['colors']);

 9});

10 

11$sorted->values()->all();

12 

13/*

14    [

15        ['name' => 'Chair', 'colors' => ['Black']],

16        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],

17        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],

18    ]

19*/
```

If you would like to sort your collection by multiple attributes, you may pass an array of sort operations to the `sortBy` method. Each sort operation should be an array consisting of the attribute that you wish to sort by and the direction of the desired sort:

```
 1$collection = collect([

 2    ['name' => 'Taylor Otwell', 'age' => 34],

 3    ['name' => 'Abigail Otwell', 'age' => 30],

 4    ['name' => 'Taylor Otwell', 'age' => 36],

 5    ['name' => 'Abigail Otwell', 'age' => 32],

 6]);

 7 

 8$sorted = $collection->sortBy([

 9    ['name', 'asc'],

10    ['age', 'desc'],

11]);

12 

13$sorted->values()->all();

14 

15/*

16    [

17        ['name' => 'Abigail Otwell', 'age' => 32],

18        ['name' => 'Abigail Otwell', 'age' => 30],

19        ['name' => 'Taylor Otwell', 'age' => 36],

20        ['name' => 'Taylor Otwell', 'age' => 34],

21    ]

22*/
```

When sorting a collection by multiple attributes, you may also provide closures that define each sort operation:

```
 1$collection = collect([

 2    ['name' => 'Taylor Otwell', 'age' => 34],

 3    ['name' => 'Abigail Otwell', 'age' => 30],

 4    ['name' => 'Taylor Otwell', 'age' => 36],

 5    ['name' => 'Abigail Otwell', 'age' => 32],

 6]);

 7 

 8$sorted = $collection->sortBy([

 9    fn (array $a, array $b) => $a['name'] <=> $b['name'],

10    fn (array $a, array $b) => $b['age'] <=> $a['age'],

11]);

12 

13$sorted->values()->all();

14 

15/*

16    [

17        ['name' => 'Abigail Otwell', 'age' => 32],

18        ['name' => 'Abigail Otwell', 'age' => 30],

19        ['name' => 'Taylor Otwell', 'age' => 36],

20        ['name' => 'Taylor Otwell', 'age' => 34],

21    ]

22*/
```

#### [`sortByDesc()`](#method-sortbydesc)

This method has the same signature as the [sortBy](#method-sortby) method, but will sort the collection in the opposite order.

#### [`sortDesc()`](#method-sortdesc)

This method will sort the collection in the opposite order as the [sort](#method-sort) method:

```
1$collection = collect([5, 3, 1, 2, 4]);

2 

3$sorted = $collection->sortDesc();

4 

5$sorted->values()->all();

6 

7// [5, 4, 3, 2, 1]
```

Unlike `sort`, you may not pass a closure to `sortDesc`. Instead, you should use the [sort](#method-sort) method and invert your comparison.

#### [`sortKeys()`](#method-sortkeys)

The `sortKeys` method sorts the collection by the keys of the underlying associative array:

```
 1$collection = collect([

 2    'id' => 22345,

 3    'first' => 'John',

 4    'last' => 'Doe',

 5]);

 6 

 7$sorted = $collection->sortKeys();

 8 

 9$sorted->all();

10 

11/*

12    [

13        'first' => 'John',

14        'id' => 22345,

15        'last' => 'Doe',

16    ]

17*/
```

#### [`sortKeysDesc()`](#method-sortkeysdesc)

This method has the same signature as the [sortKeys](#method-sortkeys) method, but will sort the collection in the opposite order.

#### [`sortKeysUsing()`](#method-sortkeysusing)

The `sortKeysUsing` method sorts the collection by the keys of the underlying associative array using a callback:

```
 1$collection = collect([

 2    'ID' => 22345,

 3    'first' => 'John',

 4    'last' => 'Doe',

 5]);

 6 

 7$sorted = $collection->sortKeysUsing('strnatcasecmp');

 8 

 9$sorted->all();

10 

11/*

12    [

13        'first' => 'John',

14        'ID' => 22345,

15        'last' => 'Doe',

16    ]

17*/
```

The callback must be a comparison function that returns an integer less than, equal to, or greater than zero. For more information, refer to the PHP documentation on [uksort](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters), which is the PHP function that `sortKeysUsing` method utilizes internally.

#### [`splice()`](#method-splice)

The `splice` method removes and returns a slice of items starting at the specified index:

```
 1$collection = collect([1, 2, 3, 4, 5]);

 2 

 3$chunk = $collection->splice(2);

 4 

 5$chunk->all();

 6 

 7// [3, 4, 5]

 8 

 9$collection->all();

10 

11// [1, 2]
```

You may pass a second argument to limit the size of the resulting collection:

```
 1$collection = collect([1, 2, 3, 4, 5]);

 2 

 3$chunk = $collection->splice(2, 1);

 4 

 5$chunk->all();

 6 

 7// [3]

 8 

 9$collection->all();

10 

11// [1, 2, 4, 5]
```

In addition, you may pass a third argument containing the new items to replace the items removed from the collection:

```
 1$collection = collect([1, 2, 3, 4, 5]);

 2 

 3$chunk = $collection->splice(2, 1, [10, 11]);

 4 

 5$chunk->all();

 6 

 7// [3]

 8 

 9$collection->all();

10 

11// [1, 2, 10, 11, 4, 5]
```

#### [`split()`](#method-split)

The `split` method breaks a collection into the given number of groups:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$groups = $collection->split(3);

4 

5$groups->all();

6 

7// [[1, 2], [3, 4], [5]]
```

#### [`splitIn()`](#method-splitin)

The `splitIn` method breaks a collection into the given number of groups, filling non-terminal groups completely before allocating the remainder to the final group:

```
1$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

2 

3$groups = $collection->splitIn(3);

4 

5$groups->all();

6 

7// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

#### [`sum()`](#method-sum)

The `sum` method returns the sum of all items in the collection:

```
1collect([1, 2, 3, 4, 5])->sum();

2 

3// 15
```

If the collection contains nested arrays or objects, you should pass a key that will be used to determine which values to sum:

```
1$collection = collect([

2    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],

3    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],

4]);

5 

6$collection->sum('pages');

7 

8// 1272
```

In addition, you may pass your own closure to determine which values of the collection to sum:

```
 1$collection = collect([

 2    ['name' => 'Chair', 'colors' => ['Black']],

 3    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],

 4    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],

 5]);

 6 

 7$collection->sum(function (array $product) {

 8    return count($product['colors']);

 9});

10 

11// 6
```

#### [`take()`](#method-take)

The `take` method returns a new collection with the specified number of items:

```
1$collection = collect([0, 1, 2, 3, 4, 5]);

2 

3$chunk = $collection->take(3);

4 

5$chunk->all();

6 

7// [0, 1, 2]
```

You may also pass a negative integer to take the specified number of items from the end of the collection:

```
1$collection = collect([0, 1, 2, 3, 4, 5]);

2 

3$chunk = $collection->take(-2);

4 

5$chunk->all();

6 

7// [4, 5]
```

#### [`takeUntil()`](#method-takeuntil)

The `takeUntil` method returns items in the collection until the given callback returns `true`:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$subset = $collection->takeUntil(function (int $item) {

4    return $item >= 3;

5});

6 

7$subset->all();

8 

9// [1, 2]
```

You may also pass a simple value to the `takeUntil` method to get the items until the given value is found:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$subset = $collection->takeUntil(3);

4 

5$subset->all();

6 

7// [1, 2]
```

If the given value is not found or the callback never returns `true`, the `takeUntil` method will return all items in the collection.

#### [`takeWhile()`](#method-takewhile)

The `takeWhile` method returns items in the collection until the given callback returns `false`:

```
1$collection = collect([1, 2, 3, 4]);

2 

3$subset = $collection->takeWhile(function (int $item) {

4    return $item < 3;

5});

6 

7$subset->all();

8 

9// [1, 2]
```

If the callback never returns `false`, the `takeWhile` method will return all items in the collection.

#### [`tap()`](#method-tap)

The `tap` method passes the collection to the given callback, allowing you to "tap" into the collection at a specific point and do something with the items while not affecting the collection itself. The collection is then returned by the `tap` method:

```
1collect([2, 4, 3, 1, 5])

2    ->sort()

3    ->tap(function (Collection $collection) {

4        Log::debug('Values after sorting', $collection->values()->all());

5    })

6    ->shift();

7 

8// 1
```

#### [`times()`](#method-times)

The static `times` method creates a new collection by invoking the given closure a specified number of times:

```
1$collection = Collection::times(10, function (int $number) {

2    return $number * 9;

3});

4 

5$collection->all();

6 

7// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

#### [`toArray()`](#method-toarray)

The `toArray` method converts the collection into a plain PHP `array`. If the collection's values are [Eloquent](/docs/13.x/eloquent) models, the models will also be converted to arrays:

```
1$collection = collect(['name' => 'Desk', 'price' => 200]);

2 

3$collection->toArray();

4 

5/*

6    [

7        ['name' => 'Desk', 'price' => 200],

8    ]

9*/
```

`toArray` also converts all of the collection's nested objects that are an instance of `Arrayable` to an array. If you want to get the raw array underlying the collection, use the [all](#method-all) method instead.

#### [`toJson()`](#method-tojson)

The `toJson` method converts the collection into a JSON serialized string:

```
1$collection = collect(['name' => 'Desk', 'price' => 200]);

2 

3$collection->toJson();

4 

5// '{"name":"Desk", "price":200}'
```

#### [`toPrettyJson()`](#method-to-pretty-json)

The `toPrettyJson` method converts the collection into a formatted JSON string using the `JSON_PRETTY_PRINT` option:

```
1$collection = collect(['name' => 'Desk', 'price' => 200]);

2 

3$collection->toPrettyJson();
```

#### [`transform()`](#method-transform)

The `transform` method iterates over the collection and calls the given callback with each item in the collection. The items in the collection will be replaced by the values returned by the callback:

```
1$collection = collect([1, 2, 3, 4, 5]);

2 

3$collection->transform(function (int $item, int $key) {

4    return $item * 2;

5});

6 

7$collection->all();

8 

9// [2, 4, 6, 8, 10]
```

Unlike most other collection methods, `transform` modifies the collection itself. If you wish to create a new collection instead, use the [map](#method-map) method.

#### [`undot()`](#method-undot)

The `undot` method expands a single-dimensional collection that uses "dot" notation into a multi-dimensional collection:

```
 1$person = collect([

 2    'name.first_name' => 'Marie',

 3    'name.last_name' => 'Valentine',

 4    'address.line_1' => '2992 Eagle Drive',

 5    'address.line_2' => '',

 6    'address.suburb' => 'Detroit',

 7    'address.state' => 'MI',

 8    'address.postcode' => '48219'

 9]);

10 

11$person = $person->undot();

12 

13$person->toArray();

14 

15/*

16    [

17        "name" => [

18            "first_name" => "Marie",

19            "last_name" => "Valentine",

20        ],

21        "address" => [

22            "line_1" => "2992 Eagle Drive",

23            "line_2" => "",

24            "suburb" => "Detroit",

25            "state" => "MI",

26            "postcode" => "48219",

27        ],

28    ]

29*/
```

#### [`union()`](#method-union)

The `union` method adds the given array to the collection. If the given array contains keys that are already in the original collection, the original collection's values will be preferred:

```
1$collection = collect([1 => ['a'], 2 => ['b']]);

2 

3$union = $collection->union([3 => ['c'], 1 => ['d']]);

4 

5$union->all();

6 

7// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

#### [`unique()`](#method-unique)

The `unique` method returns all of the unique items in the collection. The returned collection keeps the original array keys, so in the following example we will use the [values](#method-values) method to reset the keys to consecutively numbered indexes:

```
1$collection = collect([1, 1, 2, 2, 3, 4, 2]);

2 

3$unique = $collection->unique();

4 

5$unique->values()->all();

6 

7// [1, 2, 3, 4]
```

When dealing with nested arrays or objects, you may specify the key used to determine uniqueness:

```
 1$collection = collect([

 2    ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],

 3    ['name' => 'iPhone 5', 'brand' => 'Apple', 'type' => 'phone'],

 4    ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],

 5    ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],

 6    ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],

 7]);

 8 

 9$unique = $collection->unique('brand');

10 

11$unique->values()->all();

12 

13/*

14    [

15        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],

16        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],

17    ]

18*/
```

Finally, you may also pass your own closure to the `unique` method to specify which value should determine an item's uniqueness:

```
 1$unique = $collection->unique(function (array $item) {

 2    return $item['brand'].$item['type'];

 3});

 4 

 5$unique->values()->all();

 6 

 7/*

 8    [

 9        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],

10        ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],

11        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],

12        ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],

13    ]

14*/
```

The `unique` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [uniqueStrict](#method-uniquestrict) method to filter using "strict" comparisons.

This method's behavior is modified when using [Eloquent Collections](/docs/13.x/eloquent-collections#method-unique).

#### [`uniqueStrict()`](#method-uniquestrict)

This method has the same signature as the [unique](#method-unique) method; however, all values are compared using "strict" comparisons.

#### [`unless()`](#method-unless)

The `unless` method will execute the given callback unless the first argument given to the method evaluates to `true`. The collection instance and the first argument given to the `unless` method will be provided to the closure:

```
 1$collection = collect([1, 2, 3]);

 2 

 3$collection->unless(true, function (Collection $collection, bool $value) {

 4    return $collection->push(4);

 5});

 6 

 7$collection->unless(false, function (Collection $collection, bool $value) {

 8    return $collection->push(5);

 9});

10 

11$collection->all();

12 

13// [1, 2, 3, 5]
```

A second callback may be passed to the `unless` method. The second callback will be executed when the first argument given to the `unless` method evaluates to `true`:

```
 1$collection = collect([1, 2, 3]);

 2 

 3$collection->unless(true, function (Collection $collection, bool $value) {

 4    return $collection->push(4);

 5}, function (Collection $collection, bool $value) {

 6    return $collection->push(5);

 7});

 8 

 9$collection->all();

10 

11// [1, 2, 3, 5]
```

For the inverse of `unless`, see the [when](#method-when) method.

#### [`unlessEmpty()`](#method-unlessempty)

Alias for the [whenNotEmpty](#method-whennotempty) method.

#### [`unlessNotEmpty()`](#method-unlessnotempty)

Alias for the [whenEmpty](#method-whenempty) method.

#### [`unwrap()`](#method-unwrap)

The static `unwrap` method returns the collection's underlying items from the given value when applicable:

```
 1Collection::unwrap(collect('John Doe'));

 2 

 3// ['John Doe']

 4 

 5Collection::unwrap(['John Doe']);

 6 

 7// ['John Doe']

 8 

 9Collection::unwrap('John Doe');

10 

11// 'John Doe'
```

#### [`value()`](#method-value)

The `value` method retrieves a given value from the first element of the collection:

```
1$collection = collect([

2    ['product' => 'Desk', 'price' => 200],

3    ['product' => 'Speaker', 'price' => 400],

4]);

5 

6$value = $collection->value('price');

7 

8// 200
```

#### [`values()`](#method-values)

The `values` method returns a new collection with the keys reset to consecutive integers:

```
 1$collection = collect([

 2    10 => ['product' => 'Desk', 'price' => 200],

 3    11 => ['product' => 'Speaker', 'price' => 400],

 4]);

 5 

 6$values = $collection->values();

 7 

 8$values->all();

 9 

10/*

11    [

12        0 => ['product' => 'Desk', 'price' => 200],

13        1 => ['product' => 'Speaker', 'price' => 400],

14    ]

15*/
```

#### [`when()`](#method-when)

The `when` method will execute the given callback when the first argument given to the method evaluates to `true`. The collection instance and the first argument given to the `when` method will be provided to the closure:

```
 1$collection = collect([1, 2, 3]);

 2 

 3$collection->when(true, function (Collection $collection, bool $value) {

 4    return $collection->push(4);

 5});

 6 

 7$collection->when(false, function (Collection $collection, bool $value) {

 8    return $collection->push(5);

 9});

10 

11$collection->all();

12 

13// [1, 2, 3, 4]
```

A second callback may be passed to the `when` method. The second callback will be executed when the first argument given to the `when` method evaluates to `false`:

```
 1$collection = collect([1, 2, 3]);

 2 

 3$collection->when(false, function (Collection $collection, bool $value) {

 4    return $collection->push(4);

 5}, function (Collection $collection, bool $value) {

 6    return $collection->push(5);

 7});

 8 

 9$collection->all();

10 

11// [1, 2, 3, 5]
```

For the inverse of `when`, see the [unless](#method-unless) method.

#### [`whenEmpty()`](#method-whenempty)

The `whenEmpty` method will execute the given callback when the collection is empty:

```
 1$collection = collect(['Michael', 'Tom']);

 2 

 3$collection->whenEmpty(function (Collection $collection) {

 4    return $collection->push('Adam');

 5});

 6 

 7$collection->all();

 8 

 9// ['Michael', 'Tom']

10 

11$collection = collect();

12 

13$collection->whenEmpty(function (Collection $collection) {

14    return $collection->push('Adam');

15});

16 

17$collection->all();

18 

19// ['Adam']
```

A second closure may be passed to the `whenEmpty` method that will be executed when the collection is not empty:

```
 1$collection = collect(['Michael', 'Tom']);

 2 

 3$collection->whenEmpty(function (Collection $collection) {

 4    return $collection->push('Adam');

 5}, function (Collection $collection) {

 6    return $collection->push('Taylor');

 7});

 8 

 9$collection->all();

10 

11// ['Michael', 'Tom', 'Taylor']
```

For the inverse of `whenEmpty`, see the [whenNotEmpty](#method-whennotempty) method.

#### [`whenNotEmpty()`](#method-whennotempty)

The `whenNotEmpty` method will execute the given callback when the collection is not empty:

```
 1$collection = collect(['Michael', 'Tom']);

 2 

 3$collection->whenNotEmpty(function (Collection $collection) {

 4    return $collection->push('Adam');

 5});

 6 

 7$collection->all();

 8 

 9// ['Michael', 'Tom', 'Adam']

10 

11$collection = collect();

12 

13$collection->whenNotEmpty(function (Collection $collection) {

14    return $collection->push('Adam');

15});

16 

17$collection->all();

18 

19// []
```

A second closure may be passed to the `whenNotEmpty` method that will be executed when the collection is empty:

```
 1$collection = collect();

 2 

 3$collection->whenNotEmpty(function (Collection $collection) {

 4    return $collection->push('Adam');

 5}, function (Collection $collection) {

 6    return $collection->push('Taylor');

 7});

 8 

 9$collection->all();

10 

11// ['Taylor']
```

For the inverse of `whenNotEmpty`, see the [whenEmpty](#method-whenempty) method.

#### [`where()`](#method-where)

The `where` method filters the collection by a given key / value pair:

```
 1$collection = collect([

 2    ['product' => 'Desk', 'price' => 200],

 3    ['product' => 'Chair', 'price' => 100],

 4    ['product' => 'Bookcase', 'price' => 150],

 5    ['product' => 'Door', 'price' => 100],

 6]);

 7 

 8$filtered = $collection->where('price', 100);

 9 

10$filtered->all();

11 

12/*

13    [

14        ['product' => 'Chair', 'price' => 100],

15        ['product' => 'Door', 'price' => 100],

16    ]

17*/
```

The `where` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [whereStrict](#method-wherestrict) method to filter using "strict" comparisons, or the [whereNull](#method-wherenull) and [whereNotNull](#method-wherenotnull) methods to filter for `null` values.

Optionally, you may pass a comparison operator as the second parameter. Supported operators are: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', and '<=':

```
 1$collection = collect([

 2    ['name' => 'Jim', 'platform' => 'Mac'],

 3    ['name' => 'Sally', 'platform' => 'Mac'],

 4    ['name' => 'Sue', 'platform' => 'Linux'],

 5]);

 6 

 7$filtered = $collection->where('platform', '!=', 'Linux');

 8 

 9$filtered->all();

10 

11/*

12    [

13        ['name' => 'Jim', 'platform' => 'Mac'],

14        ['name' => 'Sally', 'platform' => 'Mac'],

15    ]

16*/
```

#### [`whereStrict()`](#method-wherestrict)

This method has the same signature as the [where](#method-where) method; however, all values are compared using "strict" comparisons.

#### [`whereBetween()`](#method-wherebetween)

The `whereBetween` method filters the collection by determining if a specified item value is within a given range:

```
 1$collection = collect([

 2    ['product' => 'Desk', 'price' => 200],

 3    ['product' => 'Chair', 'price' => 80],

 4    ['product' => 'Bookcase', 'price' => 150],

 5    ['product' => 'Pencil', 'price' => 30],

 6    ['product' => 'Door', 'price' => 100],

 7]);

 8 

 9$filtered = $collection->whereBetween('price', [100, 200]);

10 

11$filtered->all();

12 

13/*

14    [

15        ['product' => 'Desk', 'price' => 200],

16        ['product' => 'Bookcase', 'price' => 150],

17        ['product' => 'Door', 'price' => 100],

18    ]

19*/
```

#### [`whereIn()`](#method-wherein)

The `whereIn` method removes elements from the collection that do not have a specified item value that is contained within the given array:

```
 1$collection = collect([

 2    ['product' => 'Desk', 'price' => 200],

 3    ['product' => 'Chair', 'price' => 100],

 4    ['product' => 'Bookcase', 'price' => 150],

 5    ['product' => 'Door', 'price' => 100],

 6]);

 7 

 8$filtered = $collection->whereIn('price', [150, 200]);

 9 

10$filtered->all();

11 

12/*

13    [

14        ['product' => 'Desk', 'price' => 200],

15        ['product' => 'Bookcase', 'price' => 150],

16    ]

17*/
```

The `whereIn` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [whereInStrict](#method-whereinstrict) method to filter using "strict" comparisons.

#### [`whereInStrict()`](#method-whereinstrict)

This method has the same signature as the [whereIn](#method-wherein) method; however, all values are compared using "strict" comparisons.

#### [`whereInstanceOf()`](#method-whereinstanceof)

The `whereInstanceOf` method filters the collection by a given class type:

```
 1use App\Models\User;

 2use App\Models\Post;

 3 

 4$collection = collect([

 5    new User,

 6    new User,

 7    new Post,

 8]);

 9 

10$filtered = $collection->whereInstanceOf(User::class);

11 

12$filtered->all();

13 

14// [App\Models\User, App\Models\User]
```

#### [`whereNotBetween()`](#method-wherenotbetween)

The `whereNotBetween` method filters the collection by determining if a specified item value is outside of a given range:

```
 1$collection = collect([

 2    ['product' => 'Desk', 'price' => 200],

 3    ['product' => 'Chair', 'price' => 80],

 4    ['product' => 'Bookcase', 'price' => 150],

 5    ['product' => 'Pencil', 'price' => 30],

 6    ['product' => 'Door', 'price' => 100],

 7]);

 8 

 9$filtered = $collection->whereNotBetween('price', [100, 200]);

10 

11$filtered->all();

12 

13/*

14    [

15        ['product' => 'Chair', 'price' => 80],

16        ['product' => 'Pencil', 'price' => 30],

17    ]

18*/
```

#### [`whereNotIn()`](#method-wherenotin)

The `whereNotIn` method removes elements from the collection that have a specified item value that is contained within the given array:

```
 1$collection = collect([

 2    ['product' => 'Desk', 'price' => 200],

 3    ['product' => 'Chair', 'price' => 100],

 4    ['product' => 'Bookcase', 'price' => 150],

 5    ['product' => 'Door', 'price' => 100],

 6]);

 7 

 8$filtered = $collection->whereNotIn('price', [150, 200]);

 9 

10$filtered->all();

11 

12/*

13    [

14        ['product' => 'Chair', 'price' => 100],

15        ['product' => 'Door', 'price' => 100],

16    ]

17*/
```

The `whereNotIn` method uses "loose" comparisons when checking item values, meaning a string with an integer value will be considered equal to an integer of the same value. Use the [whereNotInStrict](#method-wherenotinstrict) method to filter using "strict" comparisons.

#### [`whereNotInStrict()`](#method-wherenotinstrict)

This method has the same signature as the [whereNotIn](#method-wherenotin) method; however, all values are compared using "strict" comparisons.

#### [`whereNotNull()`](#method-wherenotnull)

The `whereNotNull` method returns items from the collection where the given key is not `null`:

```
 1$collection = collect([

 2    ['name' => 'Desk'],

 3    ['name' => null],

 4    ['name' => 'Bookcase'],

 5    ['name' => 0],

 6    ['name' => ''],

 7]);

 8 

 9$filtered = $collection->whereNotNull('name');

10 

11$filtered->all();

12 

13/*

14    [

15        ['name' => 'Desk'],

16        ['name' => 'Bookcase'],

17        ['name' => 0],

18        ['name' => ''],

19    ]

20*/
```

#### [`whereNull()`](#method-wherenull)

The `whereNull` method returns items from the collection where the given key is `null`:

```
 1$collection = collect([

 2    ['name' => 'Desk'],

 3    ['name' => null],

 4    ['name' => 'Bookcase'],

 5    ['name' => 0],

 6    ['name' => ''],

 7]);

 8 

 9$filtered = $collection->whereNull('name');

10 

11$filtered->all();

12 

13/*

14    [

15        ['name' => null],

16    ]

17*/
```

#### [`wrap()`](#method-wrap)

The static `wrap` method wraps the given value in a collection when applicable:

```
 1use Illuminate\Support\Collection;

 2 

 3$collection = Collection::wrap('John Doe');

 4 

 5$collection->all();

 6 

 7// ['John Doe']

 8 

 9$collection = Collection::wrap(['John Doe']);

10 

11$collection->all();

12 

13// ['John Doe']

14 

15$collection = Collection::wrap(collect('John Doe'));

16 

17$collection->all();

18 

19// ['John Doe']
```

#### [`zip()`](#method-zip)

The `zip` method merges together the values of the given array with the values of the original collection at their corresponding index:

```
1$collection = collect(['Chair', 'Desk']);

2 

3$zipped = $collection->zip([100, 200]);

4 

5$zipped->all();

6 

7// [['Chair', 100], ['Desk', 200]]
```

## [Higher Order Messages](#higher-order-messages)

Collections also provide support for "higher order messages", which are short-cuts for performing common actions on collections. The collection methods that provide higher order messages are: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), and [unique](#method-unique).

Each higher order message can be accessed as a dynamic property on a collection instance. For instance, let's use the `each` higher order message to call a method on each object within a collection:

```
1use App\Models\User;

2 

3$users = User::where('votes', '>', 500)->get();

4 

5$users->each->markAsVip();
```

Likewise, we can use the `sum` higher order message to gather the total number of "votes" for a collection of users:

```
1$users = User::where('group', 'Development')->get();

2 

3return $users->sum->votes;
```

## [Lazy Collections](#lazy-collections)

### [Introduction](#lazy-collection-introduction)

Before learning more about Laravel's lazy collections, take some time to familiarize yourself with [PHP generators](https://www.php.net/manual/en/language.generators.overview.php).

To supplement the already powerful `Collection` class, the `LazyCollection` class leverages PHP's [generators](https://www.php.net/manual/en/language.generators.overview.php) to allow you to work with very large datasets while keeping memory usage low.

For example, imagine your application needs to process a multi-gigabyte log file while taking advantage of Laravel's collection methods to parse the logs. Instead of reading the entire file into memory at once, lazy collections may be used to keep only a small part of the file in memory at a given time:

```
 1use App\Models\LogEntry;

 2use Illuminate\Support\LazyCollection;

 3 

 4LazyCollection::make(function () {

 5    $handle = fopen('log.txt', 'r');

 6 

 7    while (($line = fgets($handle)) !== false) {

 8        yield $line;

 9    }

10 

11    fclose($handle);

12})->chunk(4)->map(function (array $lines) {

13    return LogEntry::fromLines($lines);

14})->each(function (LogEntry $logEntry) {

15    // Process the log entry...

16});
```

Or, imagine you need to iterate through 10,000 Eloquent models. When using traditional Laravel collections, all 10,000 Eloquent models must be loaded into memory at the same time:

```
1use App\Models\User;

2 

3$users = User::all()->filter(function (User $user) {

4    return $user->id > 500;

5});
```

However, the query builder's `cursor` method returns a `LazyCollection` instance. This allows you to still only run a single query against the database but also only keep one Eloquent model loaded in memory at a time. In this example, the `filter` callback is not executed until we actually iterate over each user individually, allowing for a drastic reduction in memory usage:

```
1use App\Models\User;

2 

3$users = User::cursor()->filter(function (User $user) {

4    return $user->id > 500;

5});

6 

7foreach ($users as $user) {

8    echo $user->id;

9}
```

### [Creating Lazy Collections](#creating-lazy-collections)

To create a lazy collection instance, you should pass a PHP generator function to the collection's `make` method:

```
 1use Illuminate\Support\LazyCollection;

 2 

 3LazyCollection::make(function () {

 4    $handle = fopen('log.txt', 'r');

 5 

 6    while (($line = fgets($handle)) !== false) {

 7        yield $line;

 8    }

 9 

10    fclose($handle);

11});
```

### [The Enumerable Contract](#the-enumerable-contract)

Almost all methods available on the `Collection` class are also available on the `LazyCollection` class. Both of these classes implement the `Illuminate\Support\Enumerable` contract, which defines the following methods:

[all](#method-all) [average](#method-average) [avg](#method-avg) [chunk](#method-chunk) [chunkWhile](#method-chunkwhile) [collapse](#method-collapse) [collect](#method-collect) [combine](#method-combine) [concat](#method-concat) [contains](#method-contains) [containsStrict](#method-containsstrict) [count](#method-count) [countBy](#method-countBy) [crossJoin](#method-crossjoin) [dd](#method-dd) [diff](#method-diff) [diffAssoc](#method-diffassoc) [diffKeys](#method-diffkeys) [dump](#method-dump) [duplicates](#method-duplicates) [duplicatesStrict](#method-duplicatesstrict) [each](#method-each) [eachSpread](#method-eachspread) [every](#method-every) [except](#method-except) [filter](#method-filter) [first](#method-first) [firstOrFail](#method-first-or-fail) [firstWhere](#method-first-where) [flatMap](#method-flatmap) [flatten](#method-flatten) [flip](#method-flip) [forPage](#method-forpage) [get](#method-get) [groupBy](#method-groupby) [has](#method-has) [implode](#method-implode) [intersect](#method-intersect) [intersectAssoc](#method-intersectAssoc) [intersectByKeys](#method-intersectbykeys) [isEmpty](#method-isempty) [isNotEmpty](#method-isnotempty) [join](#method-join) [keyBy](#method-keyby) [keys](#method-keys) [last](#method-last) [macro](#method-macro) [make](#method-make) [map](#method-map) [mapInto](#method-mapinto) [mapSpread](#method-mapspread) [mapToGroups](#method-maptogroups) [mapWithKeys](#method-mapwithkeys) [max](#method-max) [median](#method-median) [merge](#method-merge) [mergeRecursive](#method-mergerecursive) [min](#method-min) [mode](#method-mode) [nth](#method-nth) [only](#method-only) [pad](#method-pad) [partition](#method-partition) [pipe](#method-pipe) [pluck](#method-pluck) [random](#method-random) [reduce](#method-reduce) [reduceInto](#method-reduce-into) [reject](#method-reject) [replace](#method-replace) [replaceRecursive](#method-replacerecursive) [reverse](#method-reverse) [search](#method-search) [shuffle](#method-shuffle) [skip](#method-skip) [slice](#method-slice) [sole](#method-sole) [some](#method-some) [sort](#method-sort) [sortBy](#method-sortby) [sortByDesc](#method-sortbydesc) [sortKeys](#method-sortkeys) [sortKeysDesc](#method-sortkeysdesc) [split](#method-split) [sum](#method-sum) [take](#method-take) [tap](#method-tap) [times](#method-times) [toArray](#method-toarray) [toJson](#method-tojson) [union](#method-union) [unique](#method-unique) [uniqueStrict](#method-uniquestrict) [unless](#method-unless) [unlessEmpty](#method-unlessempty) [unlessNotEmpty](#method-unlessnotempty) [unwrap](#method-unwrap) [values](#method-values) [when](#method-when) [whenEmpty](#method-whenempty) [whenNotEmpty](#method-whennotempty) [where](#method-where) [whereStrict](#method-wherestrict) [whereBetween](#method-wherebetween) [whereIn](#method-wherein) [whereInStrict](#method-whereinstrict) [whereInstanceOf](#method-whereinstanceof) [whereNotBetween](#method-wherenotbetween) [whereNotIn](#method-wherenotin) [whereNotInStrict](#method-wherenotinstrict) [wrap](#method-wrap) [zip](#method-zip)

Methods that mutate the collection (such as `shift`, `pop`, `prepend` etc.) are **not** available on the `LazyCollection` class.

### [Lazy Collection Methods](#lazy-collection-methods)

In addition to the methods defined in the `Enumerable` contract, the `LazyCollection` class contains the following methods:

#### [`takeUntilTimeout()`](#method-takeUntilTimeout)

The `takeUntilTimeout` method returns a new lazy collection that will enumerate values until the specified time. After that time, the collection will then stop enumerating:

```
 1$lazyCollection = LazyCollection::times(INF)

 2    ->takeUntilTimeout(now()->plus(minutes: 1));

 3 

 4$lazyCollection->each(function (int $number) {

 5    dump($number);

 6 

 7    sleep(1);

 8});

 9 

10// 1

11// 2

12// ...

13// 58

14// 59
```

To illustrate the usage of this method, imagine an application that submits invoices from the database using a cursor. You could define a [scheduled task](/docs/13.x/scheduling) that runs every 15 minutes and only processes invoices for a maximum of 14 minutes:

```
1use App\Models\Invoice;

2use Illuminate\Support\Carbon;

3 

4Invoice::pending()->cursor()

5    ->takeUntilTimeout(

6        Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')

7    )

8    ->each(fn (Invoice $invoice) => $invoice->submit());
```

#### [`tapEach()`](#method-tapEach)

While the `each` method calls the given callback for each item in the collection right away, the `tapEach` method only calls the given callback as the items are being pulled out of the list one by one:

```
 1// Nothing has been dumped so far...

 2$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {

 3    dump($value);

 4});

 5 

 6// Three items are dumped...

 7$array = $lazyCollection->take(3)->all();

 8 

 9// 1

10// 2

11// 3
```

#### [`throttle()`](#method-throttle)

The `throttle` method will throttle the lazy collection such that each value is returned after the specified number of seconds. This method is especially useful for situations where you may be interacting with external APIs that rate limit incoming requests:

```
1use App\Models\User;

2 

3User::where('vip', true)

4    ->cursor()

5    ->throttle(seconds: 1)

6    ->each(function (User $user) {

7        // Call external API...

8    });
```

#### [`remember()`](#method-remember)

The `remember` method returns a new lazy collection that will remember any values that have already been enumerated and will not retrieve them again on subsequent collection enumerations:

```
 1// No query has been executed yet...

 2$users = User::cursor()->remember();

 3 

 4// The query is executed...

 5// The first 5 users are hydrated from the database...

 6$users->take(5)->all();

 7 

 8// First 5 users come from the collection's cache...

 9// The rest are hydrated from the database...

10$users->take(20)->all();
```

#### [`withHeartbeat()`](#method-with-heartbeat)

The `withHeartbeat` method allows you to execute a callback at regular time intervals while a lazy collection is being enumerated. This is particularly useful for long-running operations that require periodic maintenance tasks, such as extending locks or sending progress updates:

```
 1use Carbon\CarbonInterval;

 2use Illuminate\Support\Facades\Cache;

 3 

 4$lock = Cache::lock('generate-reports', seconds: 60 * 5);

 5 

 6if ($lock->get()) {

 7    try {

 8        Report::where('status', 'pending')

 9            ->lazy()

10            ->withHeartbeat(

11                CarbonInterval::minutes(4),

12                fn () => $lock->extend(CarbonInterval::minutes(5))

13            )

14            ->each(fn ($report) => $report->process());

15    } finally {

16        $lock->release();

17    }

18}
```
