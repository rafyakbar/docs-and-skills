# Database Testing

- [Introduction](#introduction)
  * [Resetting the Database After Each Test](#resetting-the-database-after-each-test)
- [Model Factories](#model-factories)
- [Running Seeders](#running-seeders)
- [Available Assertions](#available-assertions)

## [Introduction](#introduction)

Laravel provides a variety of helpful tools and assertions to make it easier to test your database driven applications. In addition, Laravel model factories and seeders make it painless to create test database records using your application's Eloquent models and relationships. We'll discuss all of these powerful features in the following documentation.

### [Resetting the Database After Each Test](#resetting-the-database-after-each-test)

Before proceeding much further, let's discuss how to reset your database after each of your tests so that data from a previous test does not interfere with subsequent tests. Laravel's included `Illuminate\Foundation\Testing\RefreshDatabase` trait will take care of this for you. Simply use the trait on your test class:

Pest

PHPUnit

```
 1<?php

 2 

 3use Illuminate\Foundation\Testing\RefreshDatabase;

 4 

 5pest()->use(RefreshDatabase::class);

 6 

 7test('basic example', function () {

 8    $response = $this->get('/');

 9 

10    // ...

11});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use Illuminate\Foundation\Testing\RefreshDatabase;

 6use Tests\TestCase;

 7 

 8class ExampleTest extends TestCase

 9{

10    use RefreshDatabase;

11 

12    /**

13     * A basic functional test example.

14     */

15    public function test_basic_example(): void

16    {

17        $response = $this->get('/');

18 

19        // ...

20    }

21}
```

The `Illuminate\Foundation\Testing\RefreshDatabase` trait does not migrate your database if your schema is up to date. Instead, it will only execute the test within a database transaction. Therefore, any records added to the database by test cases that do not use this trait may still exist in the database.

If you would like to totally reset the database, you may use the `Illuminate\Foundation\Testing\DatabaseMigrations` or `Illuminate\Foundation\Testing\DatabaseTruncation` traits instead. However, both of these options are significantly slower than the `RefreshDatabase` trait.

## [Model Factories](#model-factories)

When testing, you may need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/13.x/eloquent) using [model factories](/docs/13.x/eloquent-factories).

To learn more about creating and utilizing model factories to create models, please consult the complete [model factory documentation](/docs/13.x/eloquent-factories). Once you have defined a model factory, you may utilize the factory within your test to create models:

Pest

PHPUnit

```
1use App\Models\User;

2 

3test('models can be instantiated', function () {

4    $user = User::factory()->create();

5 

6    // ...

7});
```

```
1use App\Models\User;

2 

3public function test_models_can_be_instantiated(): void

4{

5    $user = User::factory()->create();

6 

7    // ...

8}
```

## [Running Seeders](#running-seeders)

If you would like to use [database seeders](/docs/13.x/seeding) to populate your database during a feature test, you may invoke the `seed` method. By default, the `seed` method will execute the `DatabaseSeeder`, which should execute all of your other seeders. Alternatively, you pass a specific seeder class name to the `seed` method:

Pest

PHPUnit

```
 1<?php

 2 

 3use Database\Seeders\OrderStatusSeeder;

 4use Database\Seeders\TransactionStatusSeeder;

 5use Illuminate\Foundation\Testing\RefreshDatabase;

 6 

 7pest()->use(RefreshDatabase::class);

 8 

 9test('orders can be created', function () {

10    // Run the DatabaseSeeder...

11    $this->seed();

12 

13    // Run a specific seeder...

14    $this->seed(OrderStatusSeeder::class);

15 

16    // ...

17 

18    // Run an array of specific seeders...

19    $this->seed([

20        OrderStatusSeeder::class,

21        TransactionStatusSeeder::class,

22        // ...

23    ]);

24});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use Database\Seeders\OrderStatusSeeder;

 6use Database\Seeders\TransactionStatusSeeder;

 7use Illuminate\Foundation\Testing\RefreshDatabase;

 8use Tests\TestCase;

 9 

10class ExampleTest extends TestCase

11{

12    use RefreshDatabase;

13 

14    /**

15     * Test creating a new order.

16     */

17    public function test_orders_can_be_created(): void

18    {

19        // Run the DatabaseSeeder...

20        $this->seed();

21 

22        // Run a specific seeder...

23        $this->seed(OrderStatusSeeder::class);

24 

25        // ...

26 

27        // Run an array of specific seeders...

28        $this->seed([

29            OrderStatusSeeder::class,

30            TransactionStatusSeeder::class,

31            // ...

32        ]);

33    }

34}
```

Alternatively, you may instruct Laravel to automatically seed the database before each test that uses the `RefreshDatabase` trait. You may accomplish this by adding the `Seed` attribute to your base test class:

```
 1<?php

 2 

 3namespace Tests;

 4 

 5use Illuminate\Foundation\Testing\Attributes\Seed;

 6use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

 7 

 8#[Seed]

 9abstract class TestCase extends BaseTestCase

10{

11}
```

When the `Seed` attribute is present, the test will run the `Database\Seeders\DatabaseSeeder` class before each test that uses the `RefreshDatabase` trait. However, you may specify a specific seeder that should be executed by using the `Seeder` attribute on your test class:

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use Database\Seeders\OrderStatusSeeder;

 6use Illuminate\Foundation\Testing\Attributes\Seeder;

 7use Illuminate\Foundation\Testing\RefreshDatabase;

 8use Tests\TestCase;

 9 

10#[Seeder(OrderStatusSeeder::class)]

11class OrderTest extends TestCase

12{

13    use RefreshDatabase;

14 

15    // ...

16}
```

## [Available Assertions](#available-assertions)

Laravel provides several database assertions for your [Pest](https://pestphp.com) or [PHPUnit](https://phpunit.de) feature tests. We'll discuss each of these assertions below.

#### [assertDatabaseCount](#assert-database-count)

Assert that a table in the database contains the given number of records:

```
1$this->assertDatabaseCount('users', 5);
```

#### [assertDatabaseEmpty](#assert-database-empty)

Assert that a table in the database contains no records:

```
1$this->assertDatabaseEmpty('users');
```

#### [assertDatabaseHas](#assert-database-has)

Assert that a table in the database contains records matching the given key / value query constraints:

```
1$this->assertDatabaseHas('users', [

2    'email' => '[[email protected]](/cdn-cgi/l/email-protection)',

3]);
```

#### [assertDatabaseMissing](#assert-database-missing)

Assert that a table in the database does not contain records matching the given key / value query constraints:

```
1$this->assertDatabaseMissing('users', [

2    'email' => '[[email protected]](/cdn-cgi/l/email-protection)',

3]);
```

#### [assertSoftDeleted](#assert-deleted)

The `assertSoftDeleted` method may be used to assert a given Eloquent model has been "soft deleted":

```
1$this->assertSoftDeleted($user);
```

#### [assertNotSoftDeleted](#assert-not-deleted)

The `assertNotSoftDeleted` method may be used to assert a given Eloquent model hasn't been "soft deleted":

```
1$this->assertNotSoftDeleted($user);
```

#### [assertModelExists](#assert-model-exists)

Assert that a given model or collection of models exist in the database:

```
1use App\Models\User;

2 

3$user = User::factory()->create();

4 

5$this->assertModelExists($user);
```

#### [assertModelMissing](#assert-model-missing)

Assert that a given model or collection of models do not exist in the database:

```
1use App\Models\User;

2 

3$user = User::factory()->create();

4 

5$user->delete();

6 

7$this->assertModelMissing($user);
```

#### [expectsDatabaseQueryCount](#expects-database-query-count)

The `expectsDatabaseQueryCount` method may be invoked at the beginning of your test to specify the total number of database queries that you expect to be run during the test. If the actual number of executed queries does not exactly match this expectation, the test will fail:

```
1$this->expectsDatabaseQueryCount(5);

2 

3// Test...
```
