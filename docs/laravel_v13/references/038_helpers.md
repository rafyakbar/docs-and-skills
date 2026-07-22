# Helpers

- [Introduction](#introduction)
- [Available Methods](#available-methods)
- [Other Utilities](#other-utilities)
  * [Benchmarking](#benchmarking)
  * [Dates and Time](#dates)
  * [Deferred Functions](#deferred-functions)
  * [Lottery](#lottery)
  * [Pipeline](#pipeline)
  * [Sleep](#sleep)
  * [Timebox](#timebox)
  * [URI](#uri)

## [Introduction](#introduction)

Laravel includes a variety of global "helper" PHP functions. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient.

## [Available Methods](#available-methods)

### [Arrays & Objects](#arrays-and-objects-method-list)

[Arr::accessible](#method-array-accessible) [Arr::add](#method-array-add) [Arr::array](#method-array-array) [Arr::boolean](#method-array-boolean) [Arr::collapse](#method-array-collapse) [Arr::crossJoin](#method-array-crossjoin) [Arr::divide](#method-array-divide) [Arr::dot](#method-array-dot) [Arr::every](#method-array-every) [Arr::except](#method-array-except) [Arr::exceptValues](#method-array-except-values) [Arr::exists](#method-array-exists) [Arr::first](#method-array-first) [Arr::flatten](#method-array-flatten) [Arr::float](#method-array-float) [Arr::forget](#method-array-forget) [Arr::from](#method-array-from) [Arr::get](#method-array-get) [Arr::has](#method-array-has) [Arr::hasAll](#method-array-hasall) [Arr::hasAny](#method-array-hasany) [Arr::integer](#method-array-integer) [Arr::isAssoc](#method-array-isassoc) [Arr::isList](#method-array-islist) [Arr::join](#method-array-join) [Arr::keyBy](#method-array-keyby) [Arr::last](#method-array-last) [Arr::map](#method-array-map) [Arr::mapSpread](#method-array-map-spread) [Arr::mapWithKeys](#method-array-map-with-keys) [Arr::only](#method-array-only) [Arr::onlyValues](#method-array-only-values) [Arr::partition](#method-array-partition) [Arr::pluck](#method-array-pluck) [Arr::prepend](#method-array-prepend) [Arr::prependKeysWith](#method-array-prependkeyswith) [Arr::pull](#method-array-pull) [Arr::push](#method-array-push) [Arr::query](#method-array-query) [Arr::random](#method-array-random) [Arr::reject](#method-array-reject) [Arr::select](#method-array-select) [Arr::set](#method-array-set) [Arr::shuffle](#method-array-shuffle) [Arr::sole](#method-array-sole) [Arr::some](#method-array-some) [Arr::sort](#method-array-sort) [Arr::sortDesc](#method-array-sort-desc) [Arr::sortRecursive](#method-array-sort-recursive) [Arr::string](#method-array-string) [Arr::take](#method-array-take) [Arr::toCssClasses](#method-array-to-css-classes) [Arr::toCssStyles](#method-array-to-css-styles) [Arr::undot](#method-array-undot) [Arr::where](#method-array-where) [Arr::whereNotNull](#method-array-where-not-null) [Arr::wrap](#method-array-wrap) [data_fill](#method-data-fill) [data_get](#method-data-get) [data_set](#method-data-set) [data_forget](#method-data-forget) [head](#method-head) [last](#method-last)

### [Numbers](#numbers-method-list)

[Number::abbreviate](#method-number-abbreviate) [Number::clamp](#method-number-clamp) [Number::currency](#method-number-currency) [Number::defaultCurrency](#method-default-currency) [Number::defaultLocale](#method-default-locale) [Number::fileSize](#method-number-file-size) [Number::forHumans](#method-number-for-humans) [Number::format](#method-number-format) [Number::ordinal](#method-number-ordinal) [Number::pairs](#method-number-pairs) [Number::parse](#method-number-parse) [Number::parseInt](#method-number-parse-int) [Number::parseFloat](#method-number-parse-float) [Number::percentage](#method-number-percentage) [Number::spell](#method-number-spell) [Number::spellOrdinal](#method-number-spell-ordinal) [Number::trim](#method-number-trim) [Number::useLocale](#method-number-use-locale) [Number::withLocale](#method-number-with-locale) [Number::useCurrency](#method-number-use-currency) [Number::withCurrency](#method-number-with-currency)

### [Paths](#paths-method-list)

[app_path](#method-app-path) [base_path](#method-base-path) [config_path](#method-config-path) [database_path](#method-database-path) [lang_path](#method-lang-path) [public_path](#method-public-path) [resource_path](#method-resource-path) [storage_path](#method-storage-path)

### [URLs](#urls-method-list)

[action](#method-action) [asset](#method-asset) [route](#method-route) [secure_asset](#method-secure-asset) [secure_url](#method-secure-url) [to_action](#method-to-action) [to_route](#method-to-route) [uri](#method-uri) [url](#method-url)

### [Miscellaneous](#miscellaneous-method-list)

[abort](#method-abort) [abort_if](#method-abort-if) [abort_unless](#method-abort-unless) [app](#method-app) [auth](#method-auth) [back](#method-back) [bcrypt](#method-bcrypt) [blank](#method-blank) [broadcast](#method-broadcast) [broadcast_if](#method-broadcast-if) [broadcast_unless](#method-broadcast-unless) [cache](#method-cache) [class_uses_recursive](#method-class-uses-recursive) [collect](#method-collect) [config](#method-config) [context](#method-context) [cookie](#method-cookie) [csrf_field](#method-csrf-field) [csrf_token](#method-csrf-token) [decrypt](#method-decrypt) [dd](#method-dd) [dispatch](#method-dispatch) [dispatch_sync](#method-dispatch-sync) [dump](#method-dump) [encrypt](#method-encrypt) [env](#method-env) [event](#method-event) [fake](#method-fake) [filled](#method-filled) [info](#method-info) [literal](#method-literal) [logger](#method-logger) [method_field](#method-method-field) [now](#method-now) [old](#method-old) [once](#method-once) [optional](#method-optional) [policy](#method-policy) [redirect](#method-redirect) [report](#method-report) [report_if](#method-report-if) [report_unless](#method-report-unless) [request](#method-request) [rescue](#method-rescue) [resolve](#method-resolve) [response](#method-response) [retry](#method-retry) [session](#method-session) [tap](#method-tap) [throw_if](#method-throw-if) [throw_unless](#method-throw-unless) [today](#method-today) [trait_uses_recursive](#method-trait-uses-recursive) [transform](#method-transform) [validator](#method-validator) [value](#method-value) [view](#method-view) [with](#method-with) [when](#method-when)

## [Arrays & Objects](#arrays)

#### [`Arr::accessible()`](#method-array-accessible)

The `Arr::accessible` method determines if the given value is array accessible:

```
 1use Illuminate\Support\Arr;

 2use Illuminate\Support\Collection;

 3 

 4$isAccessible = Arr::accessible(['a' => 1, 'b' => 2]);

 5 

 6// true

 7 

 8$isAccessible = Arr::accessible(new Collection);

 9 

10// true

11 

12$isAccessible = Arr::accessible('abc');

13 

14// false

15 

16$isAccessible = Arr::accessible(new stdClass);

17 

18// false
```

#### [`Arr::add()`](#method-array-add)

The `Arr::add` method adds a given key / value pair to an array if the given key doesn't already exist in the array or is set to `null`:

```
1use Illuminate\Support\Arr;

2 

3$array = Arr::add(['name' => 'Desk'], 'price', 100);

4 

5// ['name' => 'Desk', 'price' => 100]

6 

7$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

8 

9// ['name' => 'Desk', 'price' => 100]
```

#### [`Arr::array()`](#method-array-array)

The `Arr::array` method retrieves a value from a deeply nested array using "dot" notation (just as [Arr::get()](#method-array-get) does), but throws an `InvalidArgumentException` if the requested value is not an `array`:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

 4 

 5$value = Arr::array($array, 'languages');

 6 

 7// ['PHP', 'Ruby']

 8 

 9$value = Arr::array($array, 'name');

10 

11// throws InvalidArgumentException
```

#### [`Arr::boolean()`](#method-array-boolean)

The `Arr::boolean` method retrieves a value from a deeply nested array using "dot" notation (just as [Arr::get()](#method-array-get) does), but throws an `InvalidArgumentException` if the requested value is not a `boolean`:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['name' => 'Joe', 'available' => true];

 4 

 5$value = Arr::boolean($array, 'available');

 6 

 7// true

 8 

 9$value = Arr::boolean($array, 'name');

10 

11// throws InvalidArgumentException
```

#### [`Arr::collapse()`](#method-array-collapse)

The `Arr::collapse` method collapses an array of arrays or collections into a single array:

```
1use Illuminate\Support\Arr;

2 

3$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

4 

5// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### [`Arr::crossJoin()`](#method-array-crossjoin)

The `Arr::crossJoin` method cross joins the given arrays, returning a Cartesian product with all possible permutations:

```
 1use Illuminate\Support\Arr;

 2 

 3$matrix = Arr::crossJoin([1, 2], ['a', 'b']);

 4 

 5/*

 6    [

 7        [1, 'a'],

 8        [1, 'b'],

 9        [2, 'a'],

10        [2, 'b'],

11    ]

12*/

13 

14$matrix = Arr::crossJoin([1, 2], ['a', 'b'], ['I', 'II']);

15 

16/*

17    [

18        [1, 'a', 'I'],

19        [1, 'a', 'II'],

20        [1, 'b', 'I'],

21        [1, 'b', 'II'],

22        [2, 'a', 'I'],

23        [2, 'a', 'II'],

24        [2, 'b', 'I'],

25        [2, 'b', 'II'],

26    ]

27*/
```

#### [`Arr::divide()`](#method-array-divide)

The `Arr::divide` method returns two arrays: one containing the keys and the other containing the values of the given array:

```
1use Illuminate\Support\Arr;

2 

3[$keys, $values] = Arr::divide(['name' => 'Desk']);

4 

5// $keys: ['name']

6 

7// $values: ['Desk']
```

#### [`Arr::dot()`](#method-array-dot)

The `Arr::dot` method flattens a multi-dimensional array into a single level array that uses "dot" notation to indicate depth:

```
1use Illuminate\Support\Arr;

2 

3$array = ['products' => ['desk' => ['price' => 100]]];

4 

5$flattened = Arr::dot($array);

6 

7// ['products.desk.price' => 100]
```

#### [`Arr::every()`](#method-array-every)

The `Arr::every` method ensures that all values in the array pass a given truth test:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [1, 2, 3];

 4 

 5Arr::every($array, fn ($i) => $i > 0);

 6 

 7// true

 8 

 9Arr::every($array, fn ($i) => $i > 2);

10 

11// false
```

#### [`Arr::except()`](#method-array-except)

The `Arr::except` method removes the given key / value pairs from an array:

```
1use Illuminate\Support\Arr;

2 

3$array = ['name' => 'Desk', 'price' => 100];

4 

5$filtered = Arr::except($array, ['price']);

6 

7// ['name' => 'Desk']
```

#### [`Arr::exceptValues()`](#method-array-except-values)

The `Arr::exceptValues` method removes the specified values from an array:

```
1use Illuminate\Support\Arr;

2 

3$array = ['foo', 'bar', 'baz', 'qux'];

4 

5$filtered = Arr::exceptValues($array, ['foo', 'baz']);

6 

7// ['bar', 'qux']
```

You may also pass `true` to the `strict` argument to use strict type comparisons when filtering:

```
1use Illuminate\Support\Arr;

2 

3$array = [1, '1', 2, '2'];

4 

5$filtered = Arr::exceptValues($array, [1, 2], strict: true);

6 

7// ['1', '2']
```

#### [`Arr::exists()`](#method-array-exists)

The `Arr::exists` method checks that the given key exists in the provided array:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['name' => 'John Doe', 'age' => 17];

 4 

 5$exists = Arr::exists($array, 'name');

 6 

 7// true

 8 

 9$exists = Arr::exists($array, 'salary');

10 

11// false
```

#### [`Arr::first()`](#method-array-first)

The `Arr::first` method returns the first element of an array passing a given truth test:

```
1use Illuminate\Support\Arr;

2 

3$array = [100, 200, 300];

4 

5$first = Arr::first($array, function (int $value, int $key) {

6    return $value >= 150;

7});

8 

9// 200
```

A default value may also be passed as the third parameter to the method. This value will be returned if no value passes the truth test:

```
1use Illuminate\Support\Arr;

2 

3$first = Arr::first($array, $callback, $default);
```

#### [`Arr::flatten()`](#method-array-flatten)

The `Arr::flatten` method flattens a multi-dimensional array into a single level array:

```
1use Illuminate\Support\Arr;

2 

3$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

4 

5$flattened = Arr::flatten($array);

6 

7// ['Joe', 'PHP', 'Ruby']
```

#### [`Arr::float()`](#method-array-float)

The `Arr::float` method retrieves a value from a deeply nested array using "dot" notation (just as [Arr::get()](#method-array-get) does), but throws an `InvalidArgumentException` if the requested value is not a `float`:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['name' => 'Joe', 'balance' => 123.45];

 4 

 5$value = Arr::float($array, 'balance');

 6 

 7// 123.45

 8 

 9$value = Arr::float($array, 'name');

10 

11// throws InvalidArgumentException
```

#### [`Arr::forget()`](#method-array-forget)

The `Arr::forget` method removes a given key / value pairs from a deeply nested array using "dot" notation:

```
1use Illuminate\Support\Arr;

2 

3$array = ['products' => ['desk' => ['price' => 100]]];

4 

5Arr::forget($array, 'products.desk');

6 

7// ['products' => []]
```

#### [`Arr::from()`](#method-array-from)

The `Arr::from` method converts various input types into a plain PHP array. It supports a range of input types, including arrays, objects, and several common Laravel interfaces, such as `Arrayable`, `Enumerable`, `Jsonable`, and `JsonSerializable`. Additionally, it handles `Traversable` and `WeakMap` instances:

```
 1use Illuminate\Support\Arr;

 2 

 3Arr::from((object) ['foo' => 'bar']); // ['foo' => 'bar']

 4 

 5class TestJsonableObject implements Jsonable

 6{

 7    public function toJson($options = 0)

 8    {

 9        return json_encode(['foo' => 'bar']);

10    }

11}

12 

13Arr::from(new TestJsonableObject); // ['foo' => 'bar']
```

#### [`Arr::get()`](#method-array-get)

The `Arr::get` method retrieves a value from a deeply nested array using "dot" notation:

```
1use Illuminate\Support\Arr;

2 

3$array = ['products' => ['desk' => ['price' => 100]]];

4 

5$price = Arr::get($array, 'products.desk.price');

6 

7// 100
```

The `Arr::get` method also accepts a default value, which will be returned if the specified key is not present in the array:

```
1use Illuminate\Support\Arr;

2 

3$discount = Arr::get($array, 'products.desk.discount', 0);

4 

5// 0
```

#### [`Arr::has()`](#method-array-has)

The `Arr::has` method checks whether a given item or items exists in an array using "dot" notation:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['product' => ['name' => 'Desk', 'price' => 100]];

 4 

 5$contains = Arr::has($array, 'product.name');

 6 

 7// true

 8 

 9$contains = Arr::has($array, ['product.price', 'product.discount']);

10 

11// false
```

#### [`Arr::hasAll()`](#method-array-hasall)

The `Arr::hasAll` method determines if all of the specified keys exist in the given array using "dot" notation:

```
1use Illuminate\Support\Arr;

2 

3$array = ['name' => 'Taylor', 'language' => 'PHP'];

4 

5Arr::hasAll($array, ['name']); // true

6Arr::hasAll($array, ['name', 'language']); // true

7Arr::hasAll($array, ['name', 'IDE']); // false
```

#### [`Arr::hasAny()`](#method-array-hasany)

The `Arr::hasAny` method checks whether any item in a given set exists in an array using "dot" notation:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['product' => ['name' => 'Desk', 'price' => 100]];

 4 

 5$contains = Arr::hasAny($array, 'product.name');

 6 

 7// true

 8 

 9$contains = Arr::hasAny($array, ['product.name', 'product.discount']);

10 

11// true

12 

13$contains = Arr::hasAny($array, ['category', 'product.discount']);

14 

15// false
```

#### [`Arr::integer()`](#method-array-integer)

The `Arr::integer` method retrieves a value from a deeply nested array using "dot" notation (just as [Arr::get()](#method-array-get) does), but throws an `InvalidArgumentException` if the requested value is not an `int`:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['name' => 'Joe', 'age' => 42];

 4 

 5$value = Arr::integer($array, 'age');

 6 

 7// 42

 8 

 9$value = Arr::integer($array, 'name');

10 

11// throws InvalidArgumentException
```

#### [`Arr::isAssoc()`](#method-array-isassoc)

The `Arr::isAssoc` method returns `true` if the given array is an associative array. An array is considered "associative" if it doesn't have sequential numerical keys beginning with zero:

```
1use Illuminate\Support\Arr;

2 

3$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

4 

5// true

6 

7$isAssoc = Arr::isAssoc([1, 2, 3]);

8 

9// false
```

#### [`Arr::isList()`](#method-array-islist)

The `Arr::isList` method returns `true` if the given array's keys are sequential integers beginning from zero:

```
1use Illuminate\Support\Arr;

2 

3$isList = Arr::isList(['foo', 'bar', 'baz']);

4 

5// true

6 

7$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

8 

9// false
```

#### [`Arr::join()`](#method-array-join)

The `Arr::join` method joins array elements with a string. Using this method's third argument, you may also specify the joining string for the final element of the array:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

 4 

 5$joined = Arr::join($array, ', ');

 6 

 7// Tailwind, Alpine, Laravel, Livewire

 8 

 9$joined = Arr::join($array, ', ', ', and ');

10 

11// Tailwind, Alpine, Laravel, and Livewire
```

#### [`Arr::keyBy()`](#method-array-keyby)

The `Arr::keyBy` method keys the array by the given key. If multiple items have the same key, only the last one will appear in the new array:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    ['product_id' => 'prod-100', 'name' => 'Desk'],

 5    ['product_id' => 'prod-200', 'name' => 'Chair'],

 6];

 7 

 8$keyed = Arr::keyBy($array, 'product_id');

 9 

10/*

11    [

12        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],

13        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],

14    ]

15*/
```

#### [`Arr::last()`](#method-array-last)

The `Arr::last` method returns the last element of an array passing a given truth test:

```
1use Illuminate\Support\Arr;

2 

3$array = [100, 200, 300, 110];

4 

5$last = Arr::last($array, function (int $value, int $key) {

6    return $value >= 150;

7});

8 

9// 300
```

A default value may be passed as the third argument to the method. This value will be returned if no value passes the truth test:

```
1use Illuminate\Support\Arr;

2 

3$last = Arr::last($array, $callback, $default);
```

#### [`Arr::map()`](#method-array-map)

The `Arr::map` method iterates through the array and passes each value and key to the given callback. The array value is replaced by the value returned by the callback:

```
1use Illuminate\Support\Arr;

2 

3$array = ['first' => 'james', 'last' => 'kirk'];

4 

5$mapped = Arr::map($array, function (string $value, string $key) {

6    return ucfirst($value);

7});

8 

9// ['first' => 'James', 'last' => 'Kirk']
```

#### [`Arr::mapSpread()`](#method-array-map-spread)

The `Arr::mapSpread` method iterates over the array, passing each nested item value into the given closure. The closure is free to modify the item and return it, thus forming a new array of modified items:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    [0, 1],

 5    [2, 3],

 6    [4, 5],

 7    [6, 7],

 8    [8, 9],

 9];

10 

11$mapped = Arr::mapSpread($array, function (int $even, int $odd) {

12    return $even + $odd;

13});

14 

15/*

16    [1, 5, 9, 13, 17]

17*/
```

#### [`Arr::mapWithKeys()`](#method-array-map-with-keys)

The `Arr::mapWithKeys` method iterates through the array and passes each value to the given callback. The callback should return an associative array containing a single key / value pair:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    [

 5        'name' => 'John',

 6        'department' => 'Sales',

 7        'email' => '[[email protected]](/cdn-cgi/l/email-protection)',

 8    ],

 9    [

10        'name' => 'Jane',

11        'department' => 'Marketing',

12        'email' => '[[email protected]](/cdn-cgi/l/email-protection)',

13    ]

14];

15 

16$mapped = Arr::mapWithKeys($array, function (array $item, int $key) {

17    return [$item['email'] => $item['name']];

18});

19 

20/*

21    [

22        '[[email protected]](/cdn-cgi/l/email-protection)' => 'John',

23        '[[email protected]](/cdn-cgi/l/email-protection)' => 'Jane',

24    ]

25*/
```

#### [`Arr::only()`](#method-array-only)

The `Arr::only` method returns only the specified key / value pairs from the given array:

```
1use Illuminate\Support\Arr;

2 

3$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

4 

5$slice = Arr::only($array, ['name', 'price']);

6 

7// ['name' => 'Desk', 'price' => 100]
```

#### [`Arr::onlyValues()`](#method-array-only-values)

The `Arr::onlyValues` method returns only the specified values from an array:

```
1use Illuminate\Support\Arr;

2 

3$array = ['foo', 'bar', 'baz', 'qux'];

4 

5$filtered = Arr::onlyValues($array, ['foo', 'baz']);

6 

7// ['foo', 'baz']
```

You may also pass `true` to the `strict` argument to use strict type comparisons when filtering:

```
1use Illuminate\Support\Arr;

2 

3$array = [1, '1', 2, '2'];

4 

5$filtered = Arr::onlyValues($array, [1, 2], strict: true);

6 

7// [1, 2]
```

#### [`Arr::partition()`](#method-array-partition)

The `Arr::partition` method may be combined with PHP array destructuring to separate elements that pass a given truth test from those that do not:

```
 1<?php

 2 

 3use Illuminate\Support\Arr;

 4 

 5$numbers = [1, 2, 3, 4, 5, 6];

 6 

 7[$underThree, $equalOrAboveThree] = Arr::partition($numbers, function (int $i) {

 8    return $i < 3;

 9});

10 

11dump($underThree);

12 

13// [1, 2]

14 

15dump($equalOrAboveThree);

16 

17// [3, 4, 5, 6]
```

#### [`Arr::pluck()`](#method-array-pluck)

The `Arr::pluck` method retrieves all of the values for a given key from an array:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    ['developer' => ['id' => 1, 'name' => 'Taylor']],

 5    ['developer' => ['id' => 2, 'name' => 'Abigail']],

 6];

 7 

 8$names = Arr::pluck($array, 'developer.name');

 9 

10// ['Taylor', 'Abigail']
```

You may also specify how you wish the resulting list to be keyed:

```
1use Illuminate\Support\Arr;

2 

3$names = Arr::pluck($array, 'developer.name', 'developer.id');

4 

5// [1 => 'Taylor', 2 => 'Abigail']
```

#### [`Arr::prepend()`](#method-array-prepend)

The `Arr::prepend` method will push an item onto the beginning of an array:

```
1use Illuminate\Support\Arr;

2 

3$array = ['one', 'two', 'three', 'four'];

4 

5$array = Arr::prepend($array, 'zero');

6 

7// ['zero', 'one', 'two', 'three', 'four']
```

If needed, you may specify the key that should be used for the value:

```
1use Illuminate\Support\Arr;

2 

3$array = ['price' => 100];

4 

5$array = Arr::prepend($array, 'Desk', 'name');

6 

7// ['name' => 'Desk', 'price' => 100]
```

#### [`Arr::prependKeysWith()`](#method-array-prependkeyswith)

The `Arr::prependKeysWith` prepends all key names of an associative array with the given prefix:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    'name' => 'Desk',

 5    'price' => 100,

 6];

 7 

 8$keyed = Arr::prependKeysWith($array, 'product.');

 9 

10/*

11    [

12        'product.name' => 'Desk',

13        'product.price' => 100,

14    ]

15*/
```

#### [`Arr::pull()`](#method-array-pull)

The `Arr::pull` method returns and removes a key / value pair from an array:

```
1use Illuminate\Support\Arr;

2 

3$array = ['name' => 'Desk', 'price' => 100];

4 

5$name = Arr::pull($array, 'name');

6 

7// $name: Desk

8 

9// $array: ['price' => 100]
```

A default value may be passed as the third argument to the method. This value will be returned if the key doesn't exist:

```
1use Illuminate\Support\Arr;

2 

3$value = Arr::pull($array, $key, $default);
```

#### [`Arr::push()`](#method-array-push)

The `Arr::push` method pushes an item into an array using "dot" notation. If an array does not exist at the given key, it will be created:

```
1use Illuminate\Support\Arr;

2 

3$array = [];

4 

5Arr::push($array, 'office.furniture', 'Desk');

6 

7// $array: ['office' => ['furniture' => ['Desk']]]
```

#### [`Arr::query()`](#method-array-query)

The `Arr::query` method converts the array into a query string:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    'name' => 'Taylor',

 5    'order' => [

 6        'column' => 'created_at',

 7        'direction' => 'desc'

 8    ]

 9];

10 

11Arr::query($array);

12 

13// name=Taylor&order[column]=created_at&order[direction]=desc
```

#### [`Arr::random()`](#method-array-random)

The `Arr::random` method returns a random value from an array:

```
1use Illuminate\Support\Arr;

2 

3$array = [1, 2, 3, 4, 5];

4 

5$random = Arr::random($array);

6 

7// 4 - (retrieved randomly)
```

You may also specify the number of items to return as an optional second argument. Note that providing this argument will return an array even if only one item is desired:

```
1use Illuminate\Support\Arr;

2 

3$items = Arr::random($array, 2);

4 

5// [2, 5] - (retrieved randomly)
```

#### [`Arr::reject()`](#method-array-reject)

The `Arr::reject` method removes items from an array using the given closure:

```
1use Illuminate\Support\Arr;

2 

3$array = [100, '200', 300, '400', 500];

4 

5$filtered = Arr::reject($array, function (string|int $value, int $key) {

6    return is_string($value);

7});

8 

9// [0 => 100, 2 => 300, 4 => 500]
```

#### [`Arr::select()`](#method-array-select)

The `Arr::select` method selects an array of values from an array:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    ['id' => 1, 'name' => 'Desk', 'price' => 200],

 5    ['id' => 2, 'name' => 'Table', 'price' => 150],

 6    ['id' => 3, 'name' => 'Chair', 'price' => 300],

 7];

 8 

 9Arr::select($array, ['name', 'price']);

10 

11// [['name' => 'Desk', 'price' => 200], ['name' => 'Table', 'price' => 150], ['name' => 'Chair', 'price' => 300]]
```

#### [`Arr::set()`](#method-array-set)

The `Arr::set` method sets a value within a deeply nested array using "dot" notation:

```
1use Illuminate\Support\Arr;

2 

3$array = ['products' => ['desk' => ['price' => 100]]];

4 

5Arr::set($array, 'products.desk.price', 200);

6 

7// ['products' => ['desk' => ['price' => 200]]]
```

#### [`Arr::shuffle()`](#method-array-shuffle)

The `Arr::shuffle` method randomly shuffles the items in the array:

```
1use Illuminate\Support\Arr;

2 

3$array = Arr::shuffle([1, 2, 3, 4, 5]);

4 

5// [3, 2, 5, 1, 4] - (generated randomly)
```

#### [`Arr::sole()`](#method-array-sole)

The `Arr::sole` method retrieves a single value from an array using the given closure. If more than one value within the array matches the given truth test, an `Illuminate\Support\MultipleItemsFoundException` exception will be thrown. If no values match the truth test, an `Illuminate\Support\ItemNotFoundException` exception will be thrown:

```
1use Illuminate\Support\Arr;

2 

3$array = ['Desk', 'Table', 'Chair'];

4 

5$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

6 

7// 'Desk'
```

#### [`Arr::some()`](#method-array-some)

The `Arr::some` method ensures that at least one of the values in the array passes a given truth test:

```
1use Illuminate\Support\Arr;

2 

3$array = [1, 2, 3];

4 

5Arr::some($array, fn ($i) => $i > 2);

6 

7// true
```

#### [`Arr::sort()`](#method-array-sort)

The `Arr::sort` method sorts an array by its values:

```
1use Illuminate\Support\Arr;

2 

3$array = ['Desk', 'Table', 'Chair'];

4 

5$sorted = Arr::sort($array);

6 

7// ['Chair', 'Desk', 'Table']
```

You may also sort the array by the results of a given closure:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    ['name' => 'Desk'],

 5    ['name' => 'Table'],

 6    ['name' => 'Chair'],

 7];

 8 

 9$sorted = array_values(Arr::sort($array, function (array $value) {

10    return $value['name'];

11}));

12 

13/*

14    [

15        ['name' => 'Chair'],

16        ['name' => 'Desk'],

17        ['name' => 'Table'],

18    ]

19*/
```

#### [`Arr::sortDesc()`](#method-array-sort-desc)

The `Arr::sortDesc` method sorts an array in descending order by its values:

```
1use Illuminate\Support\Arr;

2 

3$array = ['Desk', 'Table', 'Chair'];

4 

5$sorted = Arr::sortDesc($array);

6 

7// ['Table', 'Desk', 'Chair']
```

You may also sort the array by the results of a given closure:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    ['name' => 'Desk'],

 5    ['name' => 'Table'],

 6    ['name' => 'Chair'],

 7];

 8 

 9$sorted = array_values(Arr::sortDesc($array, function (array $value) {

10    return $value['name'];

11}));

12 

13/*

14    [

15        ['name' => 'Table'],

16        ['name' => 'Desk'],

17        ['name' => 'Chair'],

18    ]

19*/
```

#### [`Arr::sortRecursive()`](#method-array-sort-recursive)

The `Arr::sortRecursive` method recursively sorts an array using the `sort` function for numerically indexed sub-arrays and the `ksort` function for associative sub-arrays:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    ['Roman', 'Taylor', 'Li'],

 5    ['PHP', 'Ruby', 'JavaScript'],

 6    ['one' => 1, 'two' => 2, 'three' => 3],

 7];

 8 

 9$sorted = Arr::sortRecursive($array);

10 

11/*

12    [

13        ['JavaScript', 'PHP', 'Ruby'],

14        ['one' => 1, 'three' => 3, 'two' => 2],

15        ['Li', 'Roman', 'Taylor'],

16    ]

17*/
```

If you would like the results sorted in descending order, you may use the `Arr::sortRecursiveDesc` method.

```
1$sorted = Arr::sortRecursiveDesc($array);
```

#### [`Arr::string()`](#method-array-string)

The `Arr::string` method retrieves a value from a deeply nested array using "dot" notation (just as [Arr::get()](#method-array-get) does), but throws an `InvalidArgumentException` if the requested value is not a `string`:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

 4 

 5$value = Arr::string($array, 'name');

 6 

 7// Joe

 8 

 9$value = Arr::string($array, 'languages');

10 

11// throws InvalidArgumentException
```

#### [`Arr::take()`](#method-array-take)

The `Arr::take` method returns a new array with the specified number of items:

```
1use Illuminate\Support\Arr;

2 

3$array = [0, 1, 2, 3, 4, 5];

4 

5$chunk = Arr::take($array, 3);

6 

7// [0, 1, 2]
```

You may also pass a negative integer to take the specified number of items from the end of the array:

```
1$array = [0, 1, 2, 3, 4, 5];

2 

3$chunk = Arr::take($array, -2);

4 

5// [4, 5]
```

#### [`Arr::toCssClasses()`](#method-array-to-css-classes)

The `Arr::toCssClasses` method conditionally compiles a CSS class string. The method accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list:

```
 1use Illuminate\Support\Arr;

 2 

 3$isActive = false;

 4$hasError = true;

 5 

 6$array = ['p-4', 'font-bold' => $isActive, 'bg-red' => $hasError];

 7 

 8$classes = Arr::toCssClasses($array);

 9 

10/*

11    'p-4 bg-red'

12*/
```

#### [`Arr::toCssStyles()`](#method-array-to-css-styles)

The `Arr::toCssStyles` method conditionally compiles a CSS style string. The method accepts an array of CSS declarations where the array key contains the CSS declaration you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the compiled CSS style string:

```
 1use Illuminate\Support\Arr;

 2 

 3$hasColor = true;

 4 

 5$array = ['background-color: blue', 'color: blue' => $hasColor];

 6 

 7$classes = Arr::toCssStyles($array);

 8 

 9/*

10    'background-color: blue; color: blue;'

11*/
```

This method powers Laravel's functionality allowing [merging classes with a Blade component's attribute bag](/docs/13.x/blade#conditionally-merge-classes) as well as the `@class` [Blade directive](/docs/13.x/blade#conditional-classes).

#### [`Arr::undot()`](#method-array-undot)

The `Arr::undot` method expands a single-dimensional array that uses "dot" notation into a multi-dimensional array:

```
 1use Illuminate\Support\Arr;

 2 

 3$array = [

 4    'user.name' => 'Kevin Malone',

 5    'user.occupation' => 'Accountant',

 6];

 7 

 8$array = Arr::undot($array);

 9 

10// ['user' => ['name' => 'Kevin Malone', 'occupation' => 'Accountant']]
```

#### [`Arr::where()`](#method-array-where)

The `Arr::where` method filters an array using the given closure:

```
1use Illuminate\Support\Arr;

2 

3$array = [100, '200', 300, '400', 500];

4 

5$filtered = Arr::where($array, function (string|int $value, int $key) {

6    return is_string($value);

7});

8 

9// [1 => '200', 3 => '400']
```

#### [`Arr::whereNotNull()`](#method-array-where-not-null)

The `Arr::whereNotNull` method removes all `null` values from the given array:

```
1use Illuminate\Support\Arr;

2 

3$array = [0, null];

4 

5$filtered = Arr::whereNotNull($array);

6 

7// [0 => 0]
```

#### [`Arr::wrap()`](#method-array-wrap)

The `Arr::wrap` method wraps the given value in an array. If the given value is already an array it will be returned without modification:

```
1use Illuminate\Support\Arr;

2 

3$string = 'Laravel';

4 

5$array = Arr::wrap($string);

6 

7// ['Laravel']
```

If the given value is `null`, an empty array will be returned:

```
1use Illuminate\Support\Arr;

2 

3$array = Arr::wrap(null);

4 

5// []
```

#### [`data_fill()`](#method-data-fill)

The `data_fill` function sets a missing value within a nested array or object using "dot" notation:

```
1$data = ['products' => ['desk' => ['price' => 100]]];

2 

3data_fill($data, 'products.desk.price', 200);

4 

5// ['products' => ['desk' => ['price' => 100]]]

6 

7data_fill($data, 'products.desk.discount', 10);

8 

9// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

This function also accepts asterisks as wildcards and will fill the target accordingly:

```
 1$data = [

 2    'products' => [

 3        ['name' => 'Desk 1', 'price' => 100],

 4        ['name' => 'Desk 2'],

 5    ],

 6];

 7 

 8data_fill($data, 'products.*.price', 200);

 9 

10/*

11    [

12        'products' => [

13            ['name' => 'Desk 1', 'price' => 100],

14            ['name' => 'Desk 2', 'price' => 200],

15        ],

16    ]

17*/
```

#### [`data_get()`](#method-data-get)

The `data_get` function retrieves a value from a nested array or object using "dot" notation:

```
1$data = ['products' => ['desk' => ['price' => 100]]];

2 

3$price = data_get($data, 'products.desk.price');

4 

5// 100
```

The `data_get` function also accepts a default value, which will be returned if the specified key is not found:

```
1$discount = data_get($data, 'products.desk.discount', 0);

2 

3// 0
```

The function also accepts wildcards using asterisks, which may target any key of the array or object:

```
1$data = [

2    'product-one' => ['name' => 'Desk 1', 'price' => 100],

3    'product-two' => ['name' => 'Desk 2', 'price' => 150],

4];

5 

6data_get($data, '*.name');

7 

8// ['Desk 1', 'Desk 2'];
```

The `{first}` and `{last}` placeholders may be used to retrieve the first or last items in an array:

```
 1$flight = [

 2    'segments' => [

 3        ['from' => 'LHR', 'departure' => '9:00', 'to' => 'IST', 'arrival' => '15:00'],

 4        ['from' => 'IST', 'departure' => '16:00', 'to' => 'PKX', 'arrival' => '20:00'],

 5    ],

 6];

 7 

 8data_get($flight, 'segments.{first}.arrival');

 9 

10// 15:00
```

#### [`data_set()`](#method-data-set)

The `data_set` function sets a value within a nested array or object using "dot" notation:

```
1$data = ['products' => ['desk' => ['price' => 100]]];

2 

3data_set($data, 'products.desk.price', 200);

4 

5// ['products' => ['desk' => ['price' => 200]]]
```

This function also accepts wildcards using asterisks and will set values on the target accordingly:

```
 1$data = [

 2    'products' => [

 3        ['name' => 'Desk 1', 'price' => 100],

 4        ['name' => 'Desk 2', 'price' => 150],

 5    ],

 6];

 7 

 8data_set($data, 'products.*.price', 200);

 9 

10/*

11    [

12        'products' => [

13            ['name' => 'Desk 1', 'price' => 200],

14            ['name' => 'Desk 2', 'price' => 200],

15        ],

16    ]

17*/
```

By default, any existing values are overwritten. If you wish to only set a value if it doesn't exist, you may pass `false` as the fourth argument to the function:

```
1$data = ['products' => ['desk' => ['price' => 100]]];

2 

3data_set($data, 'products.desk.price', 200, overwrite: false);

4 

5// ['products' => ['desk' => ['price' => 100]]]
```

#### [`data_forget()`](#method-data-forget)

The `data_forget` function removes a value within a nested array or object using "dot" notation:

```
1$data = ['products' => ['desk' => ['price' => 100]]];

2 

3data_forget($data, 'products.desk.price');

4 

5// ['products' => ['desk' => []]]
```

This function also accepts wildcards using asterisks and will remove values on the target accordingly:

```
 1$data = [

 2    'products' => [

 3        ['name' => 'Desk 1', 'price' => 100],

 4        ['name' => 'Desk 2', 'price' => 150],

 5    ],

 6];

 7 

 8data_forget($data, 'products.*.price');

 9 

10/*

11    [

12        'products' => [

13            ['name' => 'Desk 1'],

14            ['name' => 'Desk 2'],

15        ],

16    ]

17*/
```

#### [`head()`](#method-head)

The `head` function returns the first element in the given array. If the array is empty, `false` will be returned:

```
1$array = [100, 200, 300];

2 

3$first = head($array);

4 

5// 100
```

#### [`last()`](#method-last)

The `last` function returns the last element in the given array. If the array is empty, `false` will be returned:

```
1$array = [100, 200, 300];

2 

3$last = last($array);

4 

5// 300
```

## [Numbers](#numbers)

#### [`Number::abbreviate()`](#method-number-abbreviate)

The `Number::abbreviate` method returns the human-readable format of the provided numerical value, with an abbreviation for the units:

```
 1use Illuminate\Support\Number;

 2 

 3$number = Number::abbreviate(1000);

 4 

 5// 1K

 6 

 7$number = Number::abbreviate(489939);

 8 

 9// 490K

10 

11$number = Number::abbreviate(1230000, precision: 2);

12 

13// 1.23M
```

#### [`Number::clamp()`](#method-number-clamp)

The `Number::clamp` method ensures a given number stays within a specified range. If the number is lower than the minimum, the minimum value is returned. If the number is higher than the maximum, the maximum value is returned:

```
 1use Illuminate\Support\Number;

 2 

 3$number = Number::clamp(105, min: 10, max: 100);

 4 

 5// 100

 6 

 7$number = Number::clamp(5, min: 10, max: 100);

 8 

 9// 10

10 

11$number = Number::clamp(10, min: 10, max: 100);

12 

13// 10

14 

15$number = Number::clamp(20, min: 10, max: 100);

16 

17// 20
```

#### [`Number::currency()`](#method-number-currency)

The `Number::currency` method returns the currency representation of the given value as a string:

```
 1use Illuminate\Support\Number;

 2 

 3$currency = Number::currency(1000);

 4 

 5// $1,000.00

 6 

 7$currency = Number::currency(1000, in: 'EUR');

 8 

 9// €1,000.00

10 

11$currency = Number::currency(1000, in: 'EUR', locale: 'de');

12 

13// 1.000,00 €

14 

15$currency = Number::currency(1000, in: 'EUR', locale: 'de', precision: 0);

16 

17// 1.000 €
```

#### [`Number::defaultCurrency()`](#method-default-currency)

The `Number::defaultCurrency` method returns the default currency being used by the `Number` class:

```
1use Illuminate\Support\Number;

2 

3$currency = Number::defaultCurrency();

4 

5// USD
```

#### [`Number::defaultLocale()`](#method-default-locale)

The `Number::defaultLocale` method returns the default locale being used by the `Number` class:

```
1use Illuminate\Support\Number;

2 

3$locale = Number::defaultLocale();

4 

5// en
```

#### [`Number::fileSize()`](#method-number-file-size)

The `Number::fileSize` method returns the file size representation of the given byte value as a string:

```
 1use Illuminate\Support\Number;

 2 

 3$size = Number::fileSize(1024);

 4 

 5// 1 KB

 6 

 7$size = Number::fileSize(1024 * 1024);

 8 

 9// 1 MB

10 

11$size = Number::fileSize(1024, precision: 2);

12 

13// 1.00 KB
```

#### [`Number::forHumans()`](#method-number-for-humans)

The `Number::forHumans` method returns the human-readable format of the provided numerical value:

```
 1use Illuminate\Support\Number;

 2 

 3$number = Number::forHumans(1000);

 4 

 5// 1 thousand

 6 

 7$number = Number::forHumans(489939);

 8 

 9// 490 thousand

10 

11$number = Number::forHumans(1230000, precision: 2);

12 

13// 1.23 million
```

#### [`Number::format()`](#method-number-format)

The `Number::format` method formats the given number into a locale specific string:

```
 1use Illuminate\Support\Number;

 2 

 3$number = Number::format(100000);

 4 

 5// 100,000

 6 

 7$number = Number::format(100000, precision: 2);

 8 

 9// 100,000.00

10 

11$number = Number::format(100000.123, maxPrecision: 2);

12 

13// 100,000.12

14 

15$number = Number::format(100000, locale: 'de');

16 

17// 100.000
```

#### [`Number::ordinal()`](#method-number-ordinal)

The `Number::ordinal` method returns a number's ordinal representation:

```
 1use Illuminate\Support\Number;

 2 

 3$number = Number::ordinal(1);

 4 

 5// 1st

 6 

 7$number = Number::ordinal(2);

 8 

 9// 2nd

10 

11$number = Number::ordinal(21);

12 

13// 21st
```

#### [`Number::pairs()`](#method-number-pairs)

The `Number::pairs` method generates an array of number pairs (sub-ranges) based on a specified range and step value. This method can be useful for dividing a larger range of numbers into smaller, manageable sub-ranges for things like pagination or batching tasks. The `pairs` method returns an array of arrays, where each inner array represents a pair (sub-range) of numbers:

```
1use Illuminate\Support\Number;

2 

3$result = Number::pairs(25, 10);

4 

5// [[0, 9], [10, 19], [20, 25]]

6 

7$result = Number::pairs(25, 10, offset: 0);

8 

9// [[0, 10], [10, 20], [20, 25]]
```

#### [`Number::parse()`](#method-number-parse)

The `Number::parse` method parses a localized numeric string using PHP's `NumberFormatter`:

```
1use Illuminate\Support\Number;

2 

3$result = Number::parse('10,123', locale: 'en');

4 

5// 10123.0

6 

7$result = Number::parse('10,123', locale: 'fr');

8 

9// 10.123
```

#### [`Number::parseInt()`](#method-number-parse-int)

The `Number::parseInt` method parse a string into an integer according to the specified locale:

```
1use Illuminate\Support\Number;

2 

3$result = Number::parseInt('10.123');

4 

5// (int) 10

6 

7$result = Number::parseInt('10,123', locale: 'fr');

8 

9// (int) 10
```

#### [`Number::parseFloat()`](#method-number-parse-float)

The `Number::parseFloat` method parse a string into a float according to the specified locale:

```
1use Illuminate\Support\Number;

2 

3$result = Number::parseFloat('10');

4 

5// (float) 10.0

6 

7$result = Number::parseFloat('10', locale: 'fr');

8 

9// (float) 10.0
```

#### [`Number::percentage()`](#method-number-percentage)

The `Number::percentage` method returns the percentage representation of the given value as a string:

```
 1use Illuminate\Support\Number;

 2 

 3$percentage = Number::percentage(10);

 4 

 5// 10%

 6 

 7$percentage = Number::percentage(10, precision: 2);

 8 

 9// 10.00%

10 

11$percentage = Number::percentage(10.123, maxPrecision: 2);

12 

13// 10.12%

14 

15$percentage = Number::percentage(10, precision: 2, locale: 'de');

16 

17// 10,00%
```

#### [`Number::spell()`](#method-number-spell)

The `Number::spell` method transforms the given number into a string of words:

```
1use Illuminate\Support\Number;

2 

3$number = Number::spell(102);

4 

5// one hundred and two

6 

7$number = Number::spell(88, locale: 'fr');

8 

9// quatre-vingt-huit
```

The `after` argument allows you to specify a value after which all numbers should be spelled out:

```
1$number = Number::spell(10, after: 10);

2 

3// 10

4 

5$number = Number::spell(11, after: 10);

6 

7// eleven
```

The `until` argument allows you to specify a value before which all numbers should be spelled out:

```
1$number = Number::spell(5, until: 10);

2 

3// five

4 

5$number = Number::spell(10, until: 10);

6 

7// 10
```

#### [`Number::spellOrdinal()`](#method-number-spell-ordinal)

The `Number::spellOrdinal` method returns the number's ordinal representation as a string of words:

```
 1use Illuminate\Support\Number;

 2 

 3$number = Number::spellOrdinal(1);

 4 

 5// first

 6 

 7$number = Number::spellOrdinal(2);

 8 

 9// second

10 

11$number = Number::spellOrdinal(21);

12 

13// twenty-first
```

#### [`Number::trim()`](#method-number-trim)

The `Number::trim` method removes any trailing zero digits after the decimal point of the given number:

```
1use Illuminate\Support\Number;

2 

3$number = Number::trim(12.0);

4 

5// 12

6 

7$number = Number::trim(12.30);

8 

9// 12.3
```

#### [`Number::useLocale()`](#method-number-use-locale)

The `Number::useLocale` method sets the default number locale globally, which affects how numbers and currency are formatted by subsequent invocations to the `Number` class's methods:

```
1use Illuminate\Support\Number;

2 

3/**

4 * Bootstrap any application services.

5 */

6public function boot(): void

7{

8    Number::useLocale('de');

9}
```

#### [`Number::withLocale()`](#method-number-with-locale)

The `Number::withLocale` method executes the given closure using the specified locale and then restores the original locale after the callback has executed:

```
1use Illuminate\Support\Number;

2 

3$number = Number::withLocale('de', function () {

4    return Number::format(1500);

5});
```

#### [`Number::useCurrency()`](#method-number-use-currency)

The `Number::useCurrency` method sets the default number currency globally, which affects how the currency is formatted by subsequent invocations to the `Number` class's methods:

```
1use Illuminate\Support\Number;

2 

3/**

4 * Bootstrap any application services.

5 */

6public function boot(): void

7{

8    Number::useCurrency('GBP');

9}
```

#### [`Number::withCurrency()`](#method-number-with-currency)

The `Number::withCurrency` method executes the given closure using the specified currency and then restores the original currency after the callback has executed:

```
1use Illuminate\Support\Number;

2 

3$number = Number::withCurrency('GBP', function () {

4    // ...

5});
```

## [Paths](#paths)

#### [`app_path()`](#method-app-path)

The `app_path` function returns the fully qualified path to your application's `app` directory. You may also use the `app_path` function to generate a fully qualified path to a file relative to the application directory:

```
1$path = app_path();

2 

3$path = app_path('Http/Controllers/Controller.php');
```

#### [`base_path()`](#method-base-path)

The `base_path` function returns the fully qualified path to your application's root directory. You may also use the `base_path` function to generate a fully qualified path to a given file relative to the project root directory:

```
1$path = base_path();

2 

3$path = base_path('vendor/bin');
```

#### [`config_path()`](#method-config-path)

The `config_path` function returns the fully qualified path to your application's `config` directory. You may also use the `config_path` function to generate a fully qualified path to a given file within the application's configuration directory:

```
1$path = config_path();

2 

3$path = config_path('app.php');
```

#### [`database_path()`](#method-database-path)

The `database_path` function returns the fully qualified path to your application's `database` directory. You may also use the `database_path` function to generate a fully qualified path to a given file within the database directory:

```
1$path = database_path();

2 

3$path = database_path('factories/UserFactory.php');
```

#### [`lang_path()`](#method-lang-path)

The `lang_path` function returns the fully qualified path to your application's `lang` directory. You may also use the `lang_path` function to generate a fully qualified path to a given file within the directory:

```
1$path = lang_path();

2 

3$path = lang_path('en/messages.php');
```

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

#### [`public_path()`](#method-public-path)

The `public_path` function returns the fully qualified path to your application's `public` directory. You may also use the `public_path` function to generate a fully qualified path to a given file within the public directory:

```
1$path = public_path();

2 

3$path = public_path('css/app.css');
```

#### [`resource_path()`](#method-resource-path)

The `resource_path` function returns the fully qualified path to your application's `resources` directory. You may also use the `resource_path` function to generate a fully qualified path to a given file within the resources directory:

```
1$path = resource_path();

2 

3$path = resource_path('sass/app.scss');
```

#### [`storage_path()`](#method-storage-path)

The `storage_path` function returns the fully qualified path to your application's `storage` directory. You may also use the `storage_path` function to generate a fully qualified path to a given file within the storage directory:

```
1$path = storage_path();

2 

3$path = storage_path('app/file.txt');
```

## [URLs](#urls)

#### [`action()`](#method-action)

The `action` function generates a URL for the given controller action:

```
1use App\Http\Controllers\HomeController;

2 

3$url = action([HomeController::class, 'index']);
```

If the method accepts route parameters, you may pass them as the second argument to the method:

```
1$url = action([UserController::class, 'profile'], ['id' => 1]);
```

#### [`asset()`](#method-asset)

The `asset` function generates a URL for an asset using the current scheme of the request (HTTP or HTTPS):

```
1$url = asset('img/photo.jpg');
```

You can configure the asset URL host by setting the `ASSET_URL` variable in your `.env` file. This can be useful if you host your assets on an external service like Amazon S3 or another CDN:

```
1// ASSET_URL=http://example.com/assets

2 

3$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

#### [`route()`](#method-route)

The `route` function generates a URL for a given [named route](/docs/13.x/routing#named-routes):

```
1$url = route('route.name');
```

If the route accepts parameters, you may pass them as the second argument to the function:

```
1$url = route('route.name', ['id' => 1]);
```

By default, the `route` function generates an absolute URL. If you wish to generate a relative URL, you may pass `false` as the third argument to the function:

```
1$url = route('route.name', ['id' => 1], false);
```

#### [`secure_asset()`](#method-secure-asset)

The `secure_asset` function generates a URL for an asset using HTTPS:

```
1$url = secure_asset('img/photo.jpg');
```

#### [`secure_url()`](#method-secure-url)

The `secure_url` function generates a fully qualified HTTPS URL to the given path. Additional URL segments may be passed in the function's second argument:

```
1$url = secure_url('user/profile');

2 

3$url = secure_url('user/profile', [1]);
```

#### [`to_action()`](#method-to-action)

The `to_action` function generates a [redirect HTTP response](/docs/13.x/responses#redirects) for a given controller action:

```
1use App\Http\Controllers\UserController;

2 

3return to_action([UserController::class, 'show'], ['user' => 1]);
```

If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the `to_action` method:

```
1return to_action(

2    [UserController::class, 'show'],

3    ['user' => 1],

4    302,

5    ['X-Framework' => 'Laravel']

6);
```

#### [`to_route()`](#method-to-route)

The `to_route` function generates a [redirect HTTP response](/docs/13.x/responses#redirects) for a given [named route](/docs/13.x/routing#named-routes):

```
1return to_route('users.show', ['user' => 1]);
```

If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the `to_route` method:

```
1return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

#### [`uri()`](#method-uri)

The `uri` function generates a [fluent URI instance](#uri) for the given URI:

```
1$uri = uri('https://example.com')

2    ->withPath('/users')

3    ->withQuery(['page' => 1]);
```

If the `uri` function is given an array containing a callable controller and method pair, the function will create a `Uri` instance for the controller method's route path:

```
1use App\Http\Controllers\UserController;

2 

3$uri = uri([UserController::class, 'show'], ['user' => $user]);
```

If the controller is invokable, you may simply provide the controller class name:

```
1use App\Http\Controllers\UserIndexController;

2 

3$uri = uri(UserIndexController::class);
```

If the value given to the `uri` function matches the name of a [named route](/docs/13.x/routing#named-routes), a `Uri` instance will be generated for that route's path:

```
1$uri = uri('users.show', ['user' => $user]);
```

#### [`url()`](#method-url)

The `url` function generates a fully qualified URL to the given path:

```
1$url = url('user/profile');

2 

3$url = url('user/profile', [1]);
```

If no path is provided, an `Illuminate\Routing\UrlGenerator` instance is returned:

```
1$current = url()->current();

2 

3$full = url()->full();

4 

5$previous = url()->previous();
```

For more information on working with the `url` function, consult the [URL generation documentation](/docs/13.x/urls#generating-urls).

## [Miscellaneous](#miscellaneous)

#### [`abort()`](#method-abort)

The `abort` function throws [an HTTP exception](/docs/13.x/errors#http-exceptions) which will be rendered by the [exception handler](/docs/13.x/errors#handling-exceptions):

```
1abort(403);
```

You may also provide the exception's message and custom HTTP response headers that should be sent to the browser:

```
1abort(403, 'Unauthorized.', $headers);
```

#### [`abort_if()`](#method-abort-if)

The `abort_if` function throws an HTTP exception if a given boolean expression evaluates to `true`:

```
1abort_if(! Auth::user()->isAdmin(), 403);
```

Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function.

#### [`abort_unless()`](#method-abort-unless)

The `abort_unless` function throws an HTTP exception if a given boolean expression evaluates to `false`:

```
1abort_unless(Auth::user()->isAdmin(), 403);
```

Like the `abort` method, you may also provide the exception's response text as the third argument and an array of custom response headers as the fourth argument to the function.

#### [`app()`](#method-app)

The `app` function returns the [service container](/docs/13.x/container) instance:

```
1$container = app();
```

You may pass a class or interface name to resolve it from the container:

```
1$api = app('HelpSpot\API');
```

#### [`auth()`](#method-auth)

The `auth` function returns an [authenticator](/docs/13.x/authentication) instance. You may use it as an alternative to the `Auth` facade:

```
1$user = auth()->user();
```

If needed, you may specify which guard instance you would like to access:

```
1$user = auth('admin')->user();
```

#### [`back()`](#method-back)

The `back` function generates a [redirect HTTP response](/docs/13.x/responses#redirects) to the user's previous location:

```
1return back($status = 302, $headers = [], $fallback = '/');

2 

3return back();
```

#### [`bcrypt()`](#method-bcrypt)

The `bcrypt` function [hashes](/docs/13.x/hashing) the given value using Bcrypt. You may use this function as an alternative to the `Hash` facade:

```
1$password = bcrypt('my-secret-password');
```

#### [`blank()`](#method-blank)

The `blank` function determines whether the given value is "blank":

```
 1blank('');

 2blank('   ');

 3blank(null);

 4blank(collect());

 5 

 6// true

 7 

 8blank(0);

 9blank(true);

10blank(false);

11 

12// false
```

For the inverse of `blank`, see the [filled](#method-filled) function.

#### [`broadcast()`](#method-broadcast)

The `broadcast` function [broadcasts](/docs/13.x/broadcasting) the given [event](/docs/13.x/events) to its listeners:

```
1broadcast(new UserRegistered($user));

2 

3broadcast(new UserRegistered($user))->toOthers();
```

#### [`broadcast_if()`](#method-broadcast-if)

The `broadcast_if` function [broadcasts](/docs/13.x/broadcasting) the given [event](/docs/13.x/events) to its listeners if a given boolean expression evaluates to `true`:

```
1broadcast_if($user->isActive(), new UserRegistered($user));

2 

3broadcast_if($user->isActive(), new UserRegistered($user))->toOthers();
```

#### [`broadcast_unless()`](#method-broadcast-unless)

The `broadcast_unless` function [broadcasts](/docs/13.x/broadcasting) the given [event](/docs/13.x/events) to its listeners if a given boolean expression evaluates to `false`:

```
1broadcast_unless($user->isBanned(), new UserRegistered($user));

2 

3broadcast_unless($user->isBanned(), new UserRegistered($user))->toOthers();
```

#### [`cache()`](#method-cache)

The `cache` function may be used to get values from the [cache](/docs/13.x/cache). If the given key does not exist in the cache, an optional default value will be returned:

```
1$value = cache('key');

2 

3$value = cache('key', 'default');
```

You may add items to the cache by passing an array of key / value pairs to the function. You should also pass the number of seconds or duration the cached value should be considered valid:

```
1cache(['key' => 'value'], 300);

2 

3cache(['key' => 'value'], now()->plus(seconds: 10));
```

#### [`class_uses_recursive()`](#method-class-uses-recursive)

The `class_uses_recursive` function returns all traits used by a class, including traits used by all of its parent classes:

```
1$traits = class_uses_recursive(App\Models\User::class);
```

#### [`collect()`](#method-collect)

The `collect` function creates a [collection](/docs/13.x/collections) instance from the given value:

```
1$collection = collect(['Taylor', 'Abigail']);
```

#### [`config()`](#method-config)

The `config` function gets the value of a [configuration](/docs/13.x/configuration) variable. The configuration values may be accessed using "dot" syntax, which includes the name of the file and the option you wish to access. You may also provide a default value that will be returned if the configuration option does not exist:

```
1$value = config('app.timezone');

2 

3$value = config('app.timezone', $default);
```

You may set configuration variables at runtime by passing an array of key / value pairs. However, note that this function only affects the configuration value for the current request and does not update your actual configuration values:

```
1config(['app.debug' => true]);
```

#### [`context()`](#method-context)

The `context` function gets the value from the current [context](/docs/13.x/context). You may also provide a default value that will be returned if the context key does not exist:

```
1$value = context('trace_id');

2 

3$value = context('trace_id', $default);
```

You may set context values by passing an array of key / value pairs:

```
1use Illuminate\Support\Str;

2 

3context(['trace_id' => Str::uuid()->toString()]);
```

#### [`cookie()`](#method-cookie)

The `cookie` function creates a new [cookie](/docs/13.x/requests#cookies) instance:

```
1$cookie = cookie('name', 'value', $minutes);
```

#### [`csrf_field()`](#method-csrf-field)

The `csrf_field` function generates an HTML `hidden` input field containing the value of the CSRF token. For example, using [Blade syntax](/docs/13.x/blade):

```
1{{ csrf_field() }}
```

#### [`csrf_token()`](#method-csrf-token)

The `csrf_token` function retrieves the value of the current CSRF token:

```
1$token = csrf_token();
```

#### [`decrypt()`](#method-decrypt)

The `decrypt` function [decrypts](/docs/13.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade:

```
1$password = decrypt($value);
```

For the inverse of `decrypt`, see the [encrypt](#method-encrypt) function.

#### [`dd()`](#method-dd)

The `dd` function dumps the given variables and ends the execution of the script:

```
1dd($value);

2 

3dd($value1, $value2, $value3, ...);
```

If you do not want to halt the execution of your script, use the [dump](#method-dump) function instead.

#### [`dispatch()`](#method-dispatch)

The `dispatch` function pushes the given [job](/docs/13.x/queues#creating-jobs) onto the Laravel [job queue](/docs/13.x/queues):

```
1dispatch(new App\Jobs\SendEmails);
```

#### [`dispatch_sync()`](#method-dispatch-sync)

The `dispatch_sync` function pushes the given job to the [sync](/docs/13.x/queues#synchronous-dispatching) queue so that it is processed immediately:

```
1dispatch_sync(new App\Jobs\SendEmails);
```

#### [`dump()`](#method-dump)

The `dump` function dumps the given variables:

```
1dump($value);

2 

3dump($value1, $value2, $value3, ...);
```

If you want to stop executing the script after dumping the variables, use the [dd](#method-dd) function instead.

#### [`encrypt()`](#method-encrypt)

The `encrypt` function [encrypts](/docs/13.x/encryption) the given value. You may use this function as an alternative to the `Crypt` facade:

```
1$secret = encrypt('my-secret-value');
```

For the inverse of `encrypt`, see the [decrypt](#method-decrypt) function.

#### [`env()`](#method-env)

The `env` function retrieves the value of an [environment variable](/docs/13.x/configuration#environment-configuration) or returns a default value:

```
1$env = env('APP_ENV');

2 

3$env = env('APP_ENV', 'production');
```

If you execute the `config:cache` command during your deployment process, you should be sure that you are only calling the `env` function from within your configuration files. Once the configuration has been cached, the `.env` file will not be loaded and all calls to the `env` function will return external environment variables such as server-level or system-level environment variables or `null`.

#### [`event()`](#method-event)

The `event` function dispatches the given [event](/docs/13.x/events) to its listeners:

```
1event(new UserRegistered($user));
```

#### [`fake()`](#method-fake)

The `fake` function resolves a [Faker](https://github.com/FakerPHP/Faker) singleton from the container, which can be useful when creating fake data in model factories, database seeding, tests, and prototyping views:

```
1@for ($i = 0; $i < 10; $i++)

2    <dl>

3        <dt>Name</dt>

4        <dd>{{ fake()->name() }}</dd>

5 

6        <dt>Email</dt>

7        <dd>{{ fake()->unique()->safeEmail() }}</dd>

8    </dl>

9@endfor
```

By default, the `fake` function will utilize the `app.faker_locale` configuration option in your `config/app.php` configuration. Typically, this configuration option is set via the `APP_FAKER_LOCALE` environment variable. You may also specify the locale by passing it to the `fake` function. Each locale will resolve an individual singleton:

```
1fake('nl_NL')->name()
```

#### [`filled()`](#method-filled)

The `filled` function determines whether the given value is not "blank":

```
 1filled(0);

 2filled(true);

 3filled(false);

 4 

 5// true

 6 

 7filled('');

 8filled('   ');

 9filled(null);

10filled(collect());

11 

12// false
```

For the inverse of `filled`, see the [blank](#method-blank) function.

#### [`info()`](#method-info)

The `info` function will write information to your application's [log](/docs/13.x/logging):

```
1info('Some helpful information!');
```

An array of contextual data may also be passed to the function:

```
1info('User login attempt failed.', ['id' => $user->id]);
```

#### [`literal()`](#method-literal)

The `literal` function creates a new [stdClass](https://www.php.net/manual/en/class.stdclass.php) instance with the given named arguments as properties:

```
1$obj = literal(

2    name: 'Joe',

3    languages: ['PHP', 'Ruby'],

4);

5 

6$obj->name; // 'Joe'

7$obj->languages; // ['PHP', 'Ruby']
```

#### [`logger()`](#method-logger)

The `logger` function can be used to write a `debug` level message to the [log](/docs/13.x/logging):

```
1logger('Debug message');
```

An array of contextual data may also be passed to the function:

```
1logger('User has logged in.', ['id' => $user->id]);
```

A [logger](/docs/13.x/logging) instance will be returned if no value is passed to the function:

```
1logger()->error('You are not allowed here.');
```

#### [`method_field()`](#method-method-field)

The `method_field` function generates an HTML `hidden` input field containing the spoofed value of the form's HTTP verb. For example, using [Blade syntax](/docs/13.x/blade):

```
1<form method="POST">

2    {{ method_field('DELETE') }}

3</form>
```

#### [`now()`](#method-now)

The `now` function creates a new `Illuminate\Support\Carbon` instance for the current time:

```
1$now = now();
```

#### [`old()`](#method-old)

The `old` function [retrieves](/docs/13.x/requests#retrieving-input) an [old input](/docs/13.x/requests#old-input) value flashed into the session:

```
1$value = old('value');

2 

3$value = old('value', 'default');
```

Since the "default value" provided as the second argument to the `old` function is often an attribute of an Eloquent model, Laravel allows you to simply pass the entire Eloquent model as the second argument to the `old` function. When doing so, Laravel will assume the first argument provided to the `old` function is the name of the Eloquent attribute that should be considered the "default value":

```
1{{ old('name', $user->name) }}

2 

3// Is equivalent to...

4 

5{{ old('name', $user) }}
```

#### [`once()`](#method-once)

The `once` function executes the given callback and caches the result in memory for the duration of the request. Any subsequent calls to the `once` function with the same callback will return the previously cached result:

```
 1function random(): int

 2{

 3    return once(function () {

 4        return random_int(1, 1000);

 5    });

 6}

 7 

 8random(); // 123

 9random(); // 123 (cached result)

10random(); // 123 (cached result)
```

When the `once` function is executed from within an object instance, the cached result will be unique to that object instance:

```
 1<?php

 2 

 3class NumberService

 4{

 5    public function all(): array

 6    {

 7        return once(fn () => [1, 2, 3]);

 8    }

 9}

10 

11$service = new NumberService;

12 

13$service->all();

14$service->all(); // (cached result)

15 

16$secondService = new NumberService;

17 

18$secondService->all();

19$secondService->all(); // (cached result)
```

#### [`optional()`](#method-optional)

The `optional` function accepts any argument and allows you to access properties or call methods on that object. If the given object is `null`, properties and methods will return `null` instead of causing an error:

```
1return optional($user->address)->street;

2 

3{!! old('name', optional($user)->name) !!}
```

The `optional` function also accepts a closure as its second argument. The closure will be invoked if the value provided as the first argument is not null:

```
1return optional(User::find($id), function (User $user) {

2    return $user->name;

3});
```

#### [`policy()`](#method-policy)

The `policy` method retrieves a [policy](/docs/13.x/authorization#creating-policies) instance for a given class:

```
1$policy = policy(App\Models\User::class);
```

#### [`redirect()`](#method-redirect)

The `redirect` function returns a [redirect HTTP response](/docs/13.x/responses#redirects), or returns the redirector instance if called with no arguments:

```
1return redirect($to = null, $status = 302, $headers = [], $secure = null);

2 

3return redirect('/home');

4 

5return redirect()->route('route.name');
```

#### [`report()`](#method-report)

The `report` function will report an exception using your [exception handler](/docs/13.x/errors#handling-exceptions):

```
1report($e);
```

The `report` function also accepts a string as an argument. When a string is given to the function, the function will create an exception with the given string as its message:

```
1report('Something went wrong.');
```

#### [`report_if()`](#method-report-if)

The `report_if` function will report an exception using your [exception handler](/docs/13.x/errors#handling-exceptions) if a given boolean expression evaluates to `true`:

```
1report_if($shouldReport, $e);

2 

3report_if($shouldReport, 'Something went wrong.');
```

#### [`report_unless()`](#method-report-unless)

The `report_unless` function will report an exception using your [exception handler](/docs/13.x/errors#handling-exceptions) if a given boolean expression evaluates to `false`:

```
1report_unless($reportingDisabled, $e);

2 

3report_unless($reportingDisabled, 'Something went wrong.');
```

#### [`request()`](#method-request)

The `request` function returns the current [request](/docs/13.x/requests) instance or obtains an input field's value from the current request:

```
1$request = request();

2 

3$value = request('key', $default);
```

#### [`rescue()`](#method-rescue)

The `rescue` function executes the given closure and catches any exceptions that occur during its execution. All exceptions that are caught will be sent to your [exception handler](/docs/13.x/errors#handling-exceptions); however, the request will continue processing:

```
1return rescue(function () {

2    return $this->method();

3});
```

You may also pass a second argument to the `rescue` function. This argument will be the "default" value that should be returned if an exception occurs while executing the closure:

```
1return rescue(function () {

2    return $this->method();

3}, false);

4 

5return rescue(function () {

6    return $this->method();

7}, function () {

8    return $this->failure();

9});
```

A `report` argument may be provided to the `rescue` function to determine if the exception should be reported via the `report` function:

```
1return rescue(function () {

2    return $this->method();

3}, report: function (Throwable $throwable) {

4    return $throwable instanceof InvalidArgumentException;

5});
```

#### [`resolve()`](#method-resolve)

The `resolve` function resolves a given class or interface name to an instance using the [service container](/docs/13.x/container):

```
1$api = resolve('HelpSpot\API');
```

#### [`response()`](#method-response)

The `response` function creates a [response](/docs/13.x/responses) instance or obtains an instance of the response factory:

```
1return response('Hello World', 200, $headers);

2 

3return response()->json(['foo' => 'bar'], 200, $headers);
```

#### [`retry()`](#method-retry)

The `retry` function attempts to execute the given callback until the given maximum attempt threshold is met. If the callback does not throw an exception, its return value will be returned. If the callback throws an exception, it will automatically be retried. If the maximum attempt count is exceeded, the exception will be thrown:

```
1return retry(5, function () {

2    // Attempt 5 times while resting 100ms between attempts...

3}, 100);
```

The sleep duration also accepts a `CarbonInterval` instance:

```
1use function Illuminate\Support\seconds;

2 

3return retry(5, function () {

4    // Attempt 5 times while resting 5 seconds between attempts...

5}, seconds(5));
```

If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the third argument to the `retry` function:

```
1use Exception;

2 

3return retry(5, function () {

4    // ...

5}, function (int $attempt, Exception $exception) {

6    return $attempt * 100;

7});
```

For convenience, you may provide an array as the first argument to the `retry` function. This array will be used to determine how many milliseconds to sleep between subsequent attempts:

```
1return retry([100, 200], function () {

2    // Sleep for 100ms on first retry, 200ms on second retry...

3});
```

To only retry under specific conditions, you may pass a closure as the fourth argument to the `retry` function:

```
1use App\Exceptions\TemporaryException;

2use Exception;

3 

4return retry(5, function () {

5    // ...

6}, 100, function (Exception $exception) {

7    return $exception instanceof TemporaryException;

8});
```

#### [`session()`](#method-session)

The `session` function may be used to get or set [session](/docs/13.x/session) values:

```
1$value = session('key');
```

You may set values by passing an array of key / value pairs to the function:

```
1session(['chairs' => 7, 'instruments' => 3]);
```

The session store will be returned if no value is passed to the function:

```
1$value = session()->get('key');

2 

3session()->put('key', $value);
```

#### [`tap()`](#method-tap)

The `tap` function accepts two arguments: an arbitrary `$value` and a closure. The `$value` will be passed to the closure and then be returned by the `tap` function. The return value of the closure is irrelevant:

```
1$user = tap(User::first(), function (User $user) {

2    $user->name = 'Taylor';

3 

4    $user->save();

5});
```

If no closure is passed to the `tap` function, you may call any method on the given `$value`. The return value of the method you call will always be `$value`, regardless of what the method actually returns in its definition. For example, the Eloquent `update` method typically returns an integer. However, we can force the method to return the model itself by chaining the `update` method call through the `tap` function:

```
1$user = tap($user)->update([

2    'name' => $name,

3    'email' => $email,

4]);
```

To add a `tap` method to a class, you may add the `Illuminate\Support\Traits\Tappable` trait to the class. The `tap` method of this trait accepts a Closure as its only argument. The object instance itself will be passed to the Closure and then be returned by the `tap` method:

```
1return $user->tap(function (User $user) {

2    // ...

3});
```

#### [`throw_if()`](#method-throw-if)

The `throw_if` function throws the given exception if a given boolean expression evaluates to `true`:

```
1throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

2 

3throw_if(

4    ! Auth::user()->isAdmin(),

5    AuthorizationException::class,

6    'You are not allowed to access this page.'

7);
```

#### [`throw_unless()`](#method-throw-unless)

The `throw_unless` function throws the given exception if a given boolean expression evaluates to `false`:

```
1throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

2 

3throw_unless(

4    Auth::user()->isAdmin(),

5    AuthorizationException::class,

6    'You are not allowed to access this page.'

7);
```

#### [`today()`](#method-today)

The `today` function creates a new `Illuminate\Support\Carbon` instance for the current date:

```
1$today = today();
```

#### [`trait_uses_recursive()`](#method-trait-uses-recursive)

The `trait_uses_recursive` function returns all traits used by a trait:

```
1$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

#### [`transform()`](#method-transform)

The `transform` function executes a closure on a given value if the value is not [blank](#method-blank) and then returns the return value of the closure:

```
1$callback = function (int $value) {

2    return $value * 2;

3};

4 

5$result = transform(5, $callback);

6 

7// 10
```

A default value or closure may be passed as the third argument to the function. This value will be returned if the given value is blank:

```
1$result = transform(null, $callback, 'The value is blank');

2 

3// The value is blank
```

#### [`validator()`](#method-validator)

The `validator` function creates a new [validator](/docs/13.x/validation) instance with the given arguments. You may use it as an alternative to the `Validator` facade:

```
1$validator = validator($data, $rules, $messages);
```

#### [`value()`](#method-value)

The `value` function returns the value it is given. However, if you pass a closure to the function, the closure will be executed and its returned value will be returned:

```
1$result = value(true);

2 

3// true

4 

5$result = value(function () {

6    return false;

7});

8 

9// false
```

Additional arguments may be passed to the `value` function. If the first argument is a closure then the additional parameters will be passed to the closure as arguments, otherwise they will be ignored:

```
1$result = value(function (string $name) {

2    return $name;

3}, 'Taylor');

4 

5// 'Taylor'
```

#### [`view()`](#method-view)

The `view` function retrieves a [view](/docs/13.x/views) instance:

```
1return view('auth.login');
```

#### [`with()`](#method-with)

The `with` function returns the value it is given. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned:

```
 1$callback = function (mixed $value) {

 2    return is_numeric($value) ? $value * 2 : 0;

 3};

 4 

 5$result = with(5, $callback);

 6 

 7// 10

 8 

 9$result = with(null, $callback);

10 

11// 0

12 

13$result = with(5, null);

14 

15// 5
```

#### [`when()`](#method-when)

The `when` function returns the value it is given if a given condition evaluates to `true`. Otherwise, `null` is returned. If a closure is passed as the second argument to the function, the closure will be executed and its returned value will be returned:

```
1$value = when(true, 'Hello World');

2 

3$value = when(true, fn () => 'Hello World');
```

The `when` function is primarily useful for conditionally rendering HTML attributes:

```
1<div {!! when($condition, 'wire:poll="calculate"') !!}>

2    ...

3</div>
```

## [Other Utilities](#other-utilities)

### [Benchmarking](#benchmarking)

Sometimes you may wish to quickly test the performance of certain parts of your application. On those occasions, you may utilize the `Benchmark` support class to measure the number of milliseconds it takes for the given callbacks to complete:

```
 1<?php

 2 

 3use App\Models\User;

 4use Illuminate\Support\Benchmark;

 5 

 6Benchmark::dd(fn () => User::find(1)); // 0.1 ms

 7 

 8Benchmark::dd([

 9    'Scenario 1' => fn () => User::count(), // 0.5 ms

10    'Scenario 2' => fn () => User::all()->count(), // 20.0 ms

11]);
```

By default, the given callbacks will be executed once (one iteration), and their duration will be displayed in the browser / console.

To invoke a callback more than once, you may specify the number of iterations that the callback should be invoked as the second argument to the method. When executing a callback more than once, the `Benchmark` class will return the average number of milliseconds it took to execute the callback across all iterations:

```
1Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

Sometimes, you may want to benchmark the execution of a callback while still obtaining the value returned by the callback. The `value` method will return a tuple containing the value returned by the callback and the number of milliseconds it took to execute the callback:

```
1[$count, $duration] = Benchmark::value(fn () => User::count());
```

### [Dates and Time](#dates)

Laravel includes [Carbon](https://carbon.nesbot.com/guide/getting-started/introduction.html), a powerful date and time manipulation library. To create a new `Carbon` instance, you may invoke the `now` function. This function is globally available within your Laravel application:

```
1$now = now();
```

Or, you may create a new `Carbon` instance using the `Illuminate\Support\Carbon` class:

```
1use Illuminate\Support\Carbon;

2 

3$now = Carbon::now();
```

Laravel also augments `Carbon` instances with `plus` and `minus` methods, allowing easy manipulation of the instance's date and time:

```
1return now()->plus(minutes: 5);

2return now()->plus(hours: 8);

3return now()->plus(weeks: 4);

4 

5return now()->minus(minutes: 5);

6return now()->minus(hours: 8);

7return now()->minus(weeks: 4);
```

For a thorough discussion of Carbon and its features, please consult the [official Carbon documentation](https://carbon.nesbot.com/guide/getting-started/introduction.html).

#### [Interval Functions](#interval-functions)

Laravel also offers `milliseconds`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, and `years` functions that return `CarbonInterval` instances, which extend PHP's [DateInterval](https://www.php.net/manual/en/class.dateinterval.php) class. These functions may be used anywhere that Laravel accepts a `DateInterval` instance:

```
1use Illuminate\Support\Facades\Cache;

2 

3use function Illuminate\Support\{minutes};

4 

5Cache::put('metrics', $metrics, minutes(10));
```

### [Deferred Functions](#deferred-functions)

While Laravel's [queued jobs](/docs/13.x/queues) allow you to queue tasks for background processing, sometimes you may have simple tasks you would like to defer without configuring or maintaining a long-running queue worker.

Deferred functions allow you to defer the execution of a closure until after the HTTP response has been sent to the user, keeping your application feeling fast and responsive. To defer the execution of a closure, simply pass the closure to the `Illuminate\Support\defer` function:

```
 1use App\Services\Metrics;

 2use Illuminate\Http\Request;

 3use Illuminate\Support\Facades\Route;

 4use function Illuminate\Support\defer;

 5 

 6Route::post('/orders', function (Request $request) {

 7    // Create order...

 8 

 9    defer(fn () => Metrics::reportOrder($order));

10 

11    return $order;

12});
```

By default, deferred functions will only be executed if the HTTP response, Artisan command, or queued job from which `Illuminate\Support\defer` is invoked completes successfully. This means that deferred functions will not be executed if a request results in a `4xx` or `5xx` HTTP response. If you would like a deferred function to always execute, you may chain the `always` method onto your deferred function:

```
1defer(fn () => Metrics::reportOrder($order))->always();
```

If you have the [Swoole PHP extension](https://www.php.net/manual/en/book.swoole.php) installed, Laravel's `defer` function may conflict with Swoole's own global `defer` function, leading to web server errors. Make sure you call Laravel's `defer` helper by explicitly namespacing it: `use function Illuminate\Support\defer;`

#### [Cancelling Deferred Functions](#cancelling-deferred-functions)

If you need to cancel a deferred function before it is executed, you can use the `forget` method to cancel the function by its name. To name a deferred function, provide a second argument to the `Illuminate\Support\defer` function:

```
1defer(fn () => Metrics::report(), 'reportMetrics');

2 

3defer()->forget('reportMetrics');
```

#### [Disabling Deferred Functions in Tests](#disabling-deferred-functions-in-tests)

When writing tests, it may be useful to disable deferred functions. You may call `withoutDefer` in your test to instruct Laravel to invoke all deferred functions immediately:

Pest

PHPUnit

```
1test('without defer', function () {

2    $this->withoutDefer();

3 

4    // ...

5});
```

```
 1use Tests\TestCase;

 2 

 3class ExampleTest extends TestCase

 4{

 5    public function test_without_defer(): void

 6    {

 7        $this->withoutDefer();

 8 

 9        // ...

10    }

11}
```

If you would like to disable deferred functions for all tests within a test case, you may call the `withoutDefer` method from the `setUp` method on your base `TestCase` class:

```
 1<?php

 2 

 3namespace Tests;

 4 

 5use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

 6 

 7abstract class TestCase extends BaseTestCase

 8{

 9    protected function setUp(): void

10    {

11        parent::setUp();

12 

13        $this->withoutDefer();

14    }

15}
```

### [Lottery](#lottery)

Laravel's lottery class may be used to execute callbacks based on a set of given odds. This can be particularly useful when you only want to execute code for a percentage of your incoming requests:

```
1use Illuminate\Support\Lottery;

2 

3Lottery::odds(1, 20)

4    ->winner(fn () => $user->won())

5    ->loser(fn () => $user->lost())

6    ->choose();
```

You may combine Laravel's lottery class with other Laravel features. For example, you may wish to only report a small percentage of slow queries to your exception handler. And, since the lottery class is callable, we may pass an instance of the class into any method that accepts callables:

```
1use Carbon\CarbonInterval;

2use Illuminate\Support\Facades\DB;

3use Illuminate\Support\Lottery;

4 

5DB::whenQueryingForLongerThan(

6    CarbonInterval::seconds(2),

7    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),

8);
```

#### [Testing Lotteries](#testing-lotteries)

Laravel provides some simple methods to allow you to easily test your application's lottery invocations:

```
 1// Lottery will always win...

 2Lottery::alwaysWin();

 3 

 4// Lottery will always lose...

 5Lottery::alwaysLose();

 6 

 7// Lottery will win then lose, and finally return to normal behavior...

 8Lottery::fix([true, false]);

 9 

10// Lottery will return to normal behavior...

11Lottery::determineResultsNormally();
```

### [Pipeline](#pipeline)

Laravel's `Pipeline` facade provides a convenient way to "pipe" a given input through a series of invokable classes, closures, or callables, giving each class the opportunity to inspect or modify the input and invoke the next callable in the pipeline:

```
 1use Closure;

 2use App\Models\User;

 3use Illuminate\Support\Facades\Pipeline;

 4 

 5$user = Pipeline::send($user)

 6    ->through([

 7        function (User $user, Closure $next) {

 8            // ...

 9 

10            return $next($user);

11        },

12        function (User $user, Closure $next) {

13            // ...

14 

15            return $next($user);

16        },

17    ])

18    ->then(fn (User $user) => $user);
```

As you can see, each invokable class or closure in the pipeline is provided the input and a `$next` closure. Invoking the `$next` closure will invoke the next callable in the pipeline. As you may have noticed, this is very similar to [middleware](/docs/13.x/middleware).

When the last callable in the pipeline invokes the `$next` closure, the callable provided to the `then` method will be invoked. Typically, this callable will simply return the given input. For convenience, if you simply want to return the input after it has been processed, you may use the `thenReturn` method.

Of course, as discussed previously, you are not limited to providing closures to your pipeline. You may also provide invokable classes. If a class name is provided, the class will be instantiated via Laravel's [service container](/docs/13.x/container), allowing dependencies to be injected into the invokable class:

```
1$user = Pipeline::send($user)

2    ->through([

3        GenerateProfilePhoto::class,

4        ActivateSubscription::class,

5        SendWelcomeEmail::class,

6    ])

7    ->thenReturn();
```

The `withinTransaction` method may be invoked on the pipeline to automatically wrap all steps of the pipeline within a single database transaction:

```
1$user = Pipeline::send($user)

2    ->withinTransaction()

3    ->through([

4        ProcessOrder::class,

5        TransferFunds::class,

6        UpdateInventory::class,

7    ])

8    ->thenReturn();
```

### [Sleep](#sleep)

Laravel's `Sleep` class is a light-weight wrapper around PHP's native `sleep` and `usleep` functions, offering greater testability while also exposing a developer friendly API for working with time:

```
1use Illuminate\Support\Sleep;

2 

3$waiting = true;

4 

5while ($waiting) {

6    Sleep::for(1)->second();

7 

8    $waiting = /* ... */;

9}
```

The `Sleep` class offers a variety of methods that allow you to work with different units of time:

```
 1// Return a value after sleeping...

 2$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

 3 

 4// Sleep while a given value is true...

 5Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

 6 

 7// Pause execution for 90 seconds...

 8Sleep::for(1.5)->minutes();

 9 

10// Pause execution for 2 seconds...

11Sleep::for(2)->seconds();

12 

13// Pause execution for 500 milliseconds...

14Sleep::for(500)->milliseconds();

15 

16// Pause execution for 5,000 microseconds...

17Sleep::for(5000)->microseconds();

18 

19// Pause execution until a given time...

20Sleep::until(now()->plus(minutes: 1));

21 

22// Alias of PHP's native "sleep" function...

23Sleep::sleep(2);

24 

25// Alias of PHP's native "usleep" function...

26Sleep::usleep(5000);
```

To easily combine units of time, you may use the `and` method:

```
1Sleep::for(1)->second()->and(10)->milliseconds();
```

#### [Testing Sleep](#testing-sleep)

When testing code that utilizes the `Sleep` class or PHP's native sleep functions, your test will pause execution. As you might expect, this makes your test suite significantly slower. For example, imagine you are testing the following code:

```
1$waiting = /* ... */;

2 

3$seconds = 1;

4 

5while ($waiting) {

6    Sleep::for($seconds++)->seconds();

7 

8    $waiting = /* ... */;

9}
```

Typically, testing this code would take *at least* one second. Luckily, the `Sleep` class allows us to "fake" sleeping so that our test suite stays fast:

Pest

PHPUnit

```
1it('waits until ready', function () {

2    Sleep::fake();

3 

4    // ...

5});
```

```
1public function test_it_waits_until_ready()

2{

3    Sleep::fake();

4 

5    // ...

6}
```

When faking the `Sleep` class, the actual execution pause is bypassed, leading to a substantially faster test.

Once the `Sleep` class has been faked, it is possible to make assertions against the expected "sleeps" that should have occurred. To illustrate this, let's imagine we are testing code that pauses execution three times, with each pause increasing by a single second. Using the `assertSequence` method, we can assert that our code "slept" for the proper amount of time while keeping our test fast:

Pest

PHPUnit

```
 1it('checks if ready three times', function () {

 2    Sleep::fake();

 3 

 4    // ...

 5 

 6    Sleep::assertSequence([

 7        Sleep::for(1)->second(),

 8        Sleep::for(2)->seconds(),

 9        Sleep::for(3)->seconds(),

10    ]);

11}
```

```
 1public function test_it_checks_if_ready_three_times()

 2{

 3    Sleep::fake();

 4 

 5    // ...

 6 

 7    Sleep::assertSequence([

 8        Sleep::for(1)->second(),

 9        Sleep::for(2)->seconds(),

10        Sleep::for(3)->seconds(),

11    ]);

12}
```

Of course, the `Sleep` class offers a variety of other assertions you may use when testing:

```
 1use Carbon\CarbonInterval as Duration;

 2use Illuminate\Support\Sleep;

 3 

 4// Assert that sleep was called 3 times...

 5Sleep::assertSleptTimes(3);

 6 

 7// Assert against the duration of sleep...

 8Sleep::assertSlept(function (Duration $duration): bool {

 9    return /* ... */;

10}, times: 1);

11 

12// Assert that the Sleep class was never invoked...

13Sleep::assertNeverSlept();

14 

15// Assert that, even if Sleep was called, no execution paused occurred...

16Sleep::assertInsomniac();
```

Sometimes it may be useful to perform an action whenever a fake sleep occurs. To achieve this, you may provide a callback to the `whenFakingSleep` method. In the following example, we use Laravel's [time manipulation helpers](/docs/13.x/mocking#interacting-with-time) to instantly progress time by the duration of each sleep:

```
 1use Carbon\CarbonInterval as Duration;

 2 

 3$this->freezeTime();

 4 

 5Sleep::fake();

 6 

 7Sleep::whenFakingSleep(function (Duration $duration) {

 8    // Progress time when faking sleep...

 9    $this->travel($duration->totalMilliseconds)->milliseconds();

10});
```

As progressing time is a common requirement, the `fake` method accepts a `syncWithCarbon` argument to keep Carbon in sync when sleeping within a test:

```
1Sleep::fake(syncWithCarbon: true);

2 

3$start = now();

4 

5Sleep::for(1)->second();

6 

7$start->diffForHumans(); // 1 second ago
```

Laravel uses the `Sleep` class internally whenever it is pausing execution. For example, the [retry](#method-retry) helper uses the `Sleep` class when sleeping, allowing for improved testability when using that helper.

### [Timebox](#timebox)

Laravel's `Timebox` class ensures that the given callback always takes a fixed amount of time to execute, even if its actual execution completes sooner. This is particularly useful for cryptographic operations and user authentication checks, where attackers might exploit variations in execution time to infer sensitive information.

If the execution exceeds the fixed duration, `Timebox` has no effect. It is up to the developer to choose a sufficiently long time as the fixed duration to account for worst-case scenarios.

The call method accepts a closure and a time limit in microseconds, and then executes the closure and waits until the time limit is reached:

```
1use Illuminate\Support\Timebox;

2 

3(new Timebox)->call(function ($timebox) {

4    // ...

5}, microseconds: 10000);
```

If an exception is thrown within the closure, this class will respect the defined delay and re-throw the exception after the delay.

### [URI](#uri)

Laravel's `Uri` class provides a convenient and fluent interface for creating and manipulating URIs. This class wraps the functionality provided by the underlying League URI package and integrates seamlessly with Laravel's routing system.

You can create a `Uri` instance easily using static methods:

```
 1use App\Http\Controllers\UserController;

 2use App\Http\Controllers\InvokableController;

 3use Illuminate\Support\Uri;

 4 

 5// Generate a URI instance from the given string...

 6$uri = Uri::of('https://example.com/path');

 7 

 8// Generate URI instances to paths, named routes, or controller actions...

 9$uri = Uri::to('/dashboard');

10$uri = Uri::route('users.show', ['user' => 1]);

11$uri = Uri::signedRoute('users.show', ['user' => 1]);

12$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));

13$uri = Uri::action([UserController::class, 'index']);

14$uri = Uri::action(InvokableController::class);

15 

16// Generate a URI instance from the current request URL...

17$uri = $request->uri();
```

Once you have a URI instance, you can fluently modify it:

```
1$uri = Uri::of('https://example.com')

2    ->withScheme('http')

3    ->withHost('test.com')

4    ->withPort(8000)

5    ->withPath('/users')

6    ->withQuery(['page' => 2])

7    ->withFragment('section-1');
```

#### [Inspecting URIs](#inspecting-uris)

The `Uri` class also allows you to easily inspect the various components of the underlying URI:

```
1$scheme = $uri->scheme();

2$authority = $uri->authority();

3$host = $uri->host();

4$port = $uri->port();

5$path = $uri->path();

6$segments = $uri->pathSegments();

7$query = $uri->query();

8$fragment = $uri->fragment();
```

#### [Manipulating Query Strings](#manipulating-query-strings)

The `Uri` class offers several methods that may be used to manipulate a URI's query string. The `withQuery` method may be used to merge additional query string parameters into the existing query string:

```
1$uri = $uri->withQuery(['sort' => 'name']);
```

The `withQueryIfMissing` method may be used to merge additional query string parameters into the existing query string if the given keys do not already exist in the query string:

```
1$uri = $uri->withQueryIfMissing(['page' => 1]);
```

The `replaceQuery` method may be used to complete replace the existing query string with a new one:

```
1$uri = $uri->replaceQuery(['page' => 1]);
```

The `pushOntoQuery` method may be used to push additional parameters onto a query string parameter that has an array value:

```
1$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

The `withoutQuery` method may be used to remove parameters from the query string:

```
1$uri = $uri->withoutQuery(['page']);
```

#### [Generating Responses From URIs](#generating-responses-from-uris)

The `redirect` method may be used to generate a `RedirectResponse` instance to the given URI:

```
1$uri = Uri::of('https://example.com');

2 

3return $uri->redirect();
```

Or, you may simply return the `Uri` instance from a route or controller action, which will automatically generate a redirect response to the returned URI:

```
1use Illuminate\Support\Facades\Route;

2use Illuminate\Support\Uri;

3 

4Route::get('/redirect', function () {

5    return Uri::to('/index')

6        ->withQuery(['sort' => 'name']);

7});
```
