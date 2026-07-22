# Testing: Getting Started

- [Introduction](#introduction)
- [Environment](#environment)
- [Creating Tests](#creating-tests)
- [Running Tests](#running-tests)
  * [Running Tests in Parallel](#running-tests-in-parallel)
  * [Reporting Test Coverage](#reporting-test-coverage)
  * [Profiling Tests](#profiling-tests)
- [Configuration Caching](#configuration-caching)

## [Introduction](#introduction)

Laravel is built with testing in mind. In fact, support for testing with [Pest](https://pestphp.com) and [PHPUnit](https://phpunit.de) is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications.

By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services.

Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.**

An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` commands to run your tests.

## [Environment](#environment)

When running tests, Laravel will automatically set the [configuration environment](/docs/13.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver so that no session or cache data will be persisted while testing.

You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests!

#### [The `.env.testing` Environment File](#the-env-testing-environment-file)

In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running Pest and PHPUnit tests or executing Artisan commands with the `--env=testing` option.

## [Creating Tests](#creating-tests)

To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory:

```
1php artisan make:test UserTest
```

If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command:

```
1php artisan make:test UserTest --unit
```

If you have a test class that mostly relies on Laravel's testing features, but a specific test method does not need the framework booted, you may apply the `#[UnitTest]` attribute to that method to skip booting the application for just that test.

PHPUnit

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use Illuminate\Foundation\Testing\Attributes\UnitTest;

 6use Tests\TestCase;

 7 

 8class LocationServiceTest extends TestCase

 9{

10    public function test_get_coordinates_resolves_address(): void

11    {

12        // This test uses Laravel's testing features...

13    }

14 

15    #[UnitTest]

16    public function test_get_state_returns_state_from_abbreviation(): void

17    {

18        // This test runs without booting the application...

19    }

20}
```

Test stubs may be customized using [stub publishing](/docs/13.x/artisan#stub-customization).

Once the test has been generated, you may define test as you normally would using Pest or PHPUnit. To run your tests, execute the `vendor/bin/pest`, `vendor/bin/phpunit`, or `php artisan test` command from your terminal:

Pest

PHPUnit

```
1<?php

2 

3test('basic', function () {

4    expect(true)->toBeTrue();

5});
```

```
 1<?php

 2 

 3namespace Tests\Unit;

 4 

 5use PHPUnit\Framework\TestCase;

 6 

 7class ExampleTest extends TestCase

 8{

 9    /**

10     * A basic test example.

11     */

12    public function test_basic_test(): void

13    {

14        $this->assertTrue(true);

15    }

16}
```

If you define your own `setUp` / `tearDown` methods within a test class, be sure to call the respective `parent::setUp()` / `parent::tearDown()` methods on the parent class. Typically, you should invoke `parent::setUp()` at the start of your own `setUp` method, and `parent::tearDown()` at the end of your `tearDown` method.

## [Running Tests](#running-tests)

As mentioned previously, once you've written tests, you may run them using `pest` or `phpunit`:

Pest

PHPUnit

```
1./vendor/bin/pest
```

```
1./vendor/bin/phpunit
```

In addition to the `pest` or `phpunit` commands, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging:

```
1php artisan test
```

Any arguments that can be passed to the `pest` or `phpunit` commands may also be passed to the Artisan `test` command:

```
1php artisan test --testsuite=Feature --stop-on-failure
```

### [Running Tests in Parallel](#running-tests-in-parallel)

By default, Laravel and Pest / PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, you should install the `brianium/paratest` Composer package as a "dev" dependency. Then, include the `--parallel` option when executing the `test` Artisan command:

```
1composer require brianium/paratest --dev

2 

3php artisan test --parallel
```

By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option:

```
1php artisan test --parallel --processes=4
```

When running tests in parallel, some Pest / PHPUnit options (such as `--do-not-cache-result`) may not be available.

#### [Parallel Testing and Databases](#parallel-testing-and-databases)

As long as you have configured a primary database connection, Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases.

By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option:

```
1php artisan test --parallel --recreate-databases
```

#### [Parallel Testing Hooks](#parallel-testing-hooks)

Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes.

Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Support\Facades\Artisan;

 6use Illuminate\Support\Facades\ParallelTesting;

 7use Illuminate\Support\ServiceProvider;

 8use PHPUnit\Framework\TestCase;

 9 

10class AppServiceProvider extends ServiceProvider

11{

12    /**

13     * Bootstrap any application services.

14     */

15    public function boot(): void

16    {

17        ParallelTesting::setUpProcess(function (int $token) {

18            // ...

19        });

20 

21        ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {

22            // ...

23        });

24 

25        // Executed when a test database is created...

26        ParallelTesting::setUpTestDatabase(function (string $database, int $token) {

27            Artisan::call('db:seed');

28        });

29 

30        ParallelTesting::tearDownTestCase(function (int $token, TestCase $testCase) {

31            // ...

32        });

33 

34        ParallelTesting::tearDownProcess(function (int $token) {

35            // ...

36        });

37    }

38}
```

#### [Accessing the Parallel Testing Token](#accessing-the-parallel-testing-token)

If you would like to access the current parallel process "token" from any other location in your application's test code, you may use the `token` method. This token is a unique, string identifier for an individual test process and may be used to segment resources across parallel test processes. For example, Laravel automatically appends this token to the end of the test databases created by each parallel testing process:

```
1$token = ParallelTesting::token();
```

### [Reporting Test Coverage](#reporting-test-coverage)

This feature requires [Xdebug](https://xdebug.org) or [PCOV](https://pecl.php.net/package/pcov).

When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command:

```
1php artisan test --coverage
```

#### [Enforcing a Minimum Coverage Threshold](#enforcing-a-minimum-coverage-threshold)

You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met:

```
1php artisan test --coverage --min=80.3
```

### [Profiling Tests](#profiling-tests)

The Artisan test runner also includes a convenient mechanism for listing your application's slowest tests. Invoke the `test` command with the `--profile` option to be presented with a list of your ten slowest tests, allowing you to easily investigate which tests can be improved to speed up your test suite:

```
1php artisan test --profile
```

## [Configuration Caching](#configuration-caching)

When running tests, Laravel boots the application for each individual test method. Without a cached configuration file, each configuration file in your application must be loaded at the start of a test. To build the configuration once and re-use it for all tests in a single run, you may use the `Illuminate\Foundation\Testing\WithCachedConfig` trait:

Pest

PHPUnit

```
1<?php

2 

3use Illuminate\Foundation\Testing\WithCachedConfig;

4 

5pest()->use(WithCachedConfig::class);

6 

7// ...
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use Illuminate\Foundation\Testing\WithCachedConfig;

 6use Tests\TestCase;

 7 

 8class ConfigTest extends TestCase

 9{

10    use WithCachedConfig;

11 

12    // ...

13}
```
