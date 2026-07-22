# Mocking

- [Introduction](#introduction)
- [Mocking Objects](#mocking-objects)
- [Mocking Facades](#mocking-facades)
  * [Facade Spies](#facade-spies)
- [Interacting With Time](#interacting-with-time)

## [Introduction](#introduction)

When testing Laravel applications, you may wish to "mock" certain aspects of your application so they are not actually executed during a given test. For example, when testing a controller that dispatches an event, you may wish to mock the event listeners so they are not actually executed during the test. This allows you to only test the controller's HTTP response without worrying about the execution of the event listeners since the event listeners can be tested in their own test case.

Laravel provides helpful methods for mocking events, jobs, and other facades out of the box. These helpers primarily provide a convenience layer over Mockery so you do not have to manually make complicated Mockery method calls.

## [Mocking Objects](#mocking-objects)

When mocking an object that is going to be injected into your application via Laravel's [service container](/docs/13.x/container), you will need to bind your mocked instance into the container as an `instance` binding. This will instruct the container to use your mocked instance of the object instead of constructing the object itself:

Pest

PHPUnit

```
 1use App\Service;

 2use Mockery;

 3use Mockery\MockInterface;

 4 

 5test('something can be mocked', function () {

 6    $this->instance(

 7        Service::class,

 8        Mockery::mock(Service::class, function (MockInterface $mock) {

 9            $mock->expects('process');

10        })

11    );

12});
```

```
 1use App\Service;

 2use Mockery;

 3use Mockery\MockInterface;

 4 

 5public function test_something_can_be_mocked(): void

 6{

 7    $this->instance(

 8        Service::class,

 9        Mockery::mock(Service::class, function (MockInterface $mock) {

10            $mock->expects('process');

11        })

12    );

13}
```

In order to make this more convenient, you may use the `mock` method that is provided by Laravel's base test case class. For example, the following example is equivalent to the example above:

```
1use App\Service;

2use Mockery\MockInterface;

3 

4$mock = $this->mock(Service::class, function (MockInterface $mock) {

5    $mock->expects('process');

6});
```

You may use the `partialMock` method when you only need to mock a few methods of an object. The methods that are not mocked will be executed normally when called:

```
1use App\Service;

2use Mockery\MockInterface;

3 

4$mock = $this->partialMock(Service::class, function (MockInterface $mock) {

5    $mock->expects('process');

6});
```

Similarly, if you want to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on an object, Laravel's base test case class offers a `spy` method as a convenient wrapper around the `Mockery::spy` method. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed:

```
1use App\Service;

2 

3$spy = $this->spy(Service::class);

4 

5// ...

6 

7$spy->shouldHaveReceived('process');
```

## [Mocking Facades](#mocking-facades)

Unlike traditional static method calls, [facades](/docs/13.x/facades) (including [real-time facades](/docs/13.x/facades#real-time-facades)) may be mocked. This provides a great advantage over traditional static methods and grants you the same testability that you would have if you were using traditional dependency injection. When testing, you may often want to mock a call to a Laravel facade that occurs in one of your controllers. For example, consider the following controller action:

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

10     * Retrieve a list of all users of the application.

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

We can mock the call to the `Cache` facade by using the `expects` method, which will return an instance of a [Mockery](https://github.com/padraic/mockery) mock. Since facades are actually resolved and managed by the Laravel [service container](/docs/13.x/container), they have much more testability than a typical static class. For example, let's mock our call to the `Cache` facade's `get` method:

Pest

PHPUnit

```
 1<?php

 2 

 3use Illuminate\Support\Facades\Cache;

 4 

 5test('get index', function () {

 6    Cache::expects('get')

 7        ->with('key')

 8        ->andReturn('value');

 9 

10    $response = $this->get('/users');

11 

12    // ...

13});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use Illuminate\Support\Facades\Cache;

 6use Tests\TestCase;

 7 

 8class UserControllerTest extends TestCase

 9{

10    public function test_get_index(): void

11    {

12        Cache::expects('get')

13            ->with('key')

14            ->andReturn('value');

15 

16        $response = $this->get('/users');

17 

18        // ...

19    }

20}
```

You should not mock the `Request` facade. Instead, pass the input you desire into the [HTTP testing methods](/docs/13.x/http-tests) such as `get` and `post` when running your test. Likewise, instead of mocking the `Config` facade, call the `Config::set` method in your tests.

### [Facade Spies](#facade-spies)

If you would like to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on a facade, you may call the `spy` method on the corresponding facade. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed:

Pest

PHPUnit

```
 1<?php

 2 

 3use Illuminate\Support\Facades\Cache;

 4 

 5test('values are stored in cache', function () {

 6    Cache::spy();

 7 

 8    $response = $this->get('/');

 9 

10    $response->assertStatus(200);

11 

12    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);

13});
```

```
 1use Illuminate\Support\Facades\Cache;

 2 

 3public function test_values_are_stored_in_cache(): void

 4{

 5    Cache::spy();

 6 

 7    $response = $this->get('/');

 8 

 9    $response->assertStatus(200);

10 

11    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);

12}
```

## [Interacting With Time](#interacting-with-time)

When testing, you may occasionally need to modify the time returned by helpers such as `now` or `Illuminate\Support\Carbon::now()`. Thankfully, Laravel's base feature test class includes helpers that allow you to manipulate the current time:

Pest

PHPUnit

```
 1test('time can be manipulated', function () {

 2    // Travel into the future...

 3    $this->travel(5)->milliseconds();

 4    $this->travel(5)->seconds();

 5    $this->travel(5)->minutes();

 6    $this->travel(5)->hours();

 7    $this->travel(5)->days();

 8    $this->travel(5)->weeks();

 9    $this->travel(5)->years();

10 

11    // Travel into the past...

12    $this->travel(-5)->hours();

13 

14    // Travel to an explicit time...

15    $this->travelTo(now()->minus(hours: 6));

16 

17    // Return back to the present time...

18    $this->travelBack();

19});
```

```
 1public function test_time_can_be_manipulated(): void

 2{

 3    // Travel into the future...

 4    $this->travel(5)->milliseconds();

 5    $this->travel(5)->seconds();

 6    $this->travel(5)->minutes();

 7    $this->travel(5)->hours();

 8    $this->travel(5)->days();

 9    $this->travel(5)->weeks();

10    $this->travel(5)->years();

11 

12    // Travel into the past...

13    $this->travel(-5)->hours();

14 

15    // Travel to an explicit time...

16    $this->travelTo(now()->minus(hours: 6));

17 

18    // Return back to the present time...

19    $this->travelBack();

20}
```

You may also provide a closure to the various time travel methods. The closure will be invoked with time frozen at the specified time. Once the closure has executed, time will resume as normal:

```
1$this->travel(5)->days(function () {

2    // Test something five days into the future...

3});

4 

5$this->travelTo(now()->mins(days: 10), function () {

6    // Test something during a given moment...

7});
```

The `freezeTime` method may be used to freeze the current time. Similarly, the `freezeSecond` method will freeze the current time but at the start of the current second:

```
 1use Illuminate\Support\Carbon;

 2 

 3// Freeze time and resume normal time after executing closure...

 4$this->freezeTime(function (Carbon $time) {

 5    // ...

 6});

 7 

 8// Freeze time at the current second and resume normal time after executing closure...

 9$this->freezeSecond(function (Carbon $time) {

10    // ...

11})
```

As you would expect, all of the methods discussed above are primarily useful for testing time sensitive application behavior, such as locking inactive posts on a discussion forum:

Pest

PHPUnit

```
1use App\Models\Thread;

2 

3test('forum threads lock after one week of inactivity', function () {

4    $thread = Thread::factory()->create();

5 

6    $this->travel(1)->week();

7 

8    expect($thread->isLockedByInactivity())->toBeTrue();

9});
```

```
 1use App\Models\Thread;

 2 

 3public function test_forum_threads_lock_after_one_week_of_inactivity()

 4{

 5    $thread = Thread::factory()->create();

 6 

 7    $this->travel(1)->week();

 8 

 9    $this->assertTrue($thread->isLockedByInactivity());

10}
```
