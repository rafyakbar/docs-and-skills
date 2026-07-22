# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Defining Features](#defining-features)
  * [Class Based Features](#class-based-features)
- [Checking Features](#checking-features)
  * [Conditional Execution](#conditional-execution)
  * [The `HasFeatures` Trait](#the-has-features-trait)
  * [Blade Directive](#blade-directive)
  * [Middleware](#middleware)
  * [Intercepting Feature Checks](#intercepting-feature-checks)
  * [In-Memory Cache](#in-memory-cache)
- [Scope](#scope)
  * [Specifying the Scope](#specifying-the-scope)
  * [Default Scope](#default-scope)
  * [Nullable Scope](#nullable-scope)
  * [Identifying Scope](#identifying-scope)
  * [Serializing Scope](#serializing-scope)
- [Rich Feature Values](#rich-feature-values)
- [Retrieving Multiple Features](#retrieving-multiple-features)
- [Eager Loading](#eager-loading)
- [Updating Values](#updating-values)
  * [Bulk Updates](#bulk-updates)
  * [Purging Features](#purging-features)
- [Testing](#testing)
- [Adding Custom Pennant Drivers](#adding-custom-pennant-drivers)
  * [Implementing the Driver](#implementing-the-driver)
  * [Registering the Driver](#registering-the-driver)
  * [Defining Features Externally](#defining-features-externally)
- [Events](#events)

## [Introduction](#introduction)

[Laravel Pennant](https://github.com/laravel/pennant) is a simple and light-weight feature flag package - without the cruft. Feature flags enable you to incrementally roll out new application features with confidence, A/B test new interface designs, complement a trunk-based development strategy, and much more.

## [Installation](#installation)

First, install Pennant into your project using the Composer package manager:

```
1composer require laravel/pennant
```

Next, you should publish the Pennant configuration and migration files using the `vendor:publish` Artisan command:

```
1php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

Finally, you should run your application's database migrations. This will create a `features` table that Pennant uses to power its `database` driver:

```
1php artisan migrate
```

## [Configuration](#configuration)

After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to specify the default storage mechanism that will be used by Pennant to store resolved feature flag values.

Pennant includes support for storing resolved feature flag values in an in-memory array via the `array` driver. Or, Pennant can store resolved feature flag values persistently in a relational database via the `database` driver, which is the default storage mechanism used by Pennant.

## [Defining Features](#defining-features)

To define a feature, you may use the `define` method offered by the `Feature` facade. You will need to provide a name for the feature, as well as a closure that will be invoked to resolve the feature's initial value.

Typically, features are defined in a service provider using the `Feature` facade. The closure will receive the "scope" for the feature check. Most commonly, the scope is the currently authenticated user. In this example, we will define a feature for incrementally rolling out a new API to our application's users:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use App\Models\User;

 6use Illuminate\Support\Lottery;

 7use Illuminate\Support\ServiceProvider;

 8use Laravel\Pennant\Feature;

 9 

10class AppServiceProvider extends ServiceProvider

11{

12    /**

13     * Bootstrap any application services.

14     */

15    public function boot(): void

16    {

17        Feature::define('new-api', fn (User $user) => match (true) {

18            $user->isInternalTeamMember() => true,

19            $user->isHighTrafficCustomer() => false,

20            default => Lottery::odds(1 / 100),

21        });

22    }

23}
```

As you can see, we have the following rules for our feature:

- All internal team members should be using the new API.
- Any high traffic customers should not be using the new API.
- Otherwise, the feature should be randomly assigned to users with a 1 in 100 chance of being active.

The first time the `new-api` feature is checked for a given user, the result of the closure will be stored by the storage driver. The next time the feature is checked against the same user, the value will be retrieved from storage and the closure will not be invoked.

For convenience, if a feature definition only returns a lottery, you may omit the closure completely:

```
1Feature::define('site-redesign', Lottery::odds(1, 1000));
```

### [Class Based Features](#class-based-features)

Pennant also allows you to define class-based features. Unlike closure-based feature definitions, there is no need to register a class-based feature in a service provider. To create a class-based feature, you may invoke the `pennant:feature` Artisan command. By default, the feature class will be placed in your application's `app/Features` directory:

```
1php artisan pennant:feature NewApi
```

When writing a feature class, you only need to define a `resolve` method, which will be invoked to resolve the feature's initial value for a given scope. Again, the scope will typically be the currently authenticated user:

```
 1<?php

 2 

 3namespace App\Features;

 4 

 5use App\Models\User;

 6use Illuminate\Support\Lottery;

 7 

 8class NewApi

 9{

10    /**

11     * Resolve the feature's initial value.

12     */

13    public function resolve(User $user): mixed

14    {

15        return match (true) {

16            $user->isInternalTeamMember() => true,

17            $user->isHighTrafficCustomer() => false,

18            default => Lottery::odds(1 / 100),

19        };

20    }

21}
```

If you would like to manually resolve an instance of a class-based feature, you may invoke the `instance` method on the `Feature` facade:

```
1use Illuminate\Support\Facades\Feature;

2 

3$instance = Feature::instance(NewApi::class);
```

Feature classes are resolved via the [container](/docs/13.x/container), so you may inject dependencies into the feature class's constructor when needed.

#### Customizing the Stored Feature Name

By default, Pennant will store the feature class's fully qualified class name. If you would like to decouple the stored feature name from the application's internal structure, you may add the `Name` attribute on the feature class. The value of this attribute will be stored in place of the class name:

```
 1<?php

 2 

 3namespace App\Features;

 4 

 5use Laravel\Pennant\Attributes\Name;

 6 

 7#[Name('new-api')]

 8class NewApi

 9{

10    // ...

11}
```

## [Checking Features](#checking-features)

To determine if a feature is active, you may use the `active` method on the `Feature` facade. By default, features are checked against the currently authenticated user:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Http\Request;

 6use Illuminate\Http\Response;

 7use Laravel\Pennant\Feature;

 8 

 9class PodcastController

10{

11    /**

12     * Display a listing of the resource.

13     */

14    public function index(Request $request): Response

15    {

16        return Feature::active('new-api')

17            ? $this->resolveNewApiResponse($request)

18            : $this->resolveLegacyApiResponse($request);

19    }

20 

21    // ...

22}
```

Although features are checked against the currently authenticated user by default, you may easily check the feature against another user or [scope](#scope). To accomplish this, use the `for` method offered by the `Feature` facade:

```
1return Feature::for($user)->active('new-api')

2    ? $this->resolveNewApiResponse($request)

3    : $this->resolveLegacyApiResponse($request);
```

Pennant also offers some additional convenience methods that may prove useful when determining if a feature is active or not:

```
 1// Determine if all of the given features are active...

 2Feature::allAreActive(['new-api', 'site-redesign']);

 3 

 4// Determine if any of the given features are active...

 5Feature::someAreActive(['new-api', 'site-redesign']);

 6 

 7// Determine if a feature is inactive...

 8Feature::inactive('new-api');

 9 

10// Determine if all of the given features are inactive...

11Feature::allAreInactive(['new-api', 'site-redesign']);

12 

13// Determine if any of the given features are inactive...

14Feature::someAreInactive(['new-api', 'site-redesign']);
```

When using Pennant outside of an HTTP context, such as in an Artisan command or a queued job, you should typically [explicitly specify the feature's scope](#specifying-the-scope). Alternatively, you may define a [default scope](#default-scope) that accounts for both authenticated HTTP contexts and unauthenticated contexts.

#### [Checking Class Based Features](#checking-class-based-features)

For class-based features, you should provide the class name when checking the feature:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Features\NewApi;

 6use Illuminate\Http\Request;

 7use Illuminate\Http\Response;

 8use Laravel\Pennant\Feature;

 9 

10class PodcastController

11{

12    /**

13     * Display a listing of the resource.

14     */

15    public function index(Request $request): Response

16    {

17        return Feature::active(NewApi::class)

18            ? $this->resolveNewApiResponse($request)

19            : $this->resolveLegacyApiResponse($request);

20    }

21 

22    // ...

23}
```

### [Conditional Execution](#conditional-execution)

The `when` method may be used to fluently execute a given closure if a feature is active. Additionally, a second closure may be provided and will be executed if the feature is inactive:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Features\NewApi;

 6use Illuminate\Http\Request;

 7use Illuminate\Http\Response;

 8use Laravel\Pennant\Feature;

 9 

10class PodcastController

11{

12    /**

13     * Display a listing of the resource.

14     */

15    public function index(Request $request): Response

16    {

17        return Feature::when(NewApi::class,

18            fn () => $this->resolveNewApiResponse($request),

19            fn () => $this->resolveLegacyApiResponse($request),

20        );

21    }

22 

23    // ...

24}
```

The `unless` method serves as the inverse of the `when` method, executing the first closure if the feature is inactive:

```
1return Feature::unless(NewApi::class,

2    fn () => $this->resolveLegacyApiResponse($request),

3    fn () => $this->resolveNewApiResponse($request),

4);
```

### [The `HasFeatures` Trait](#the-has-features-trait)

Pennant's `HasFeatures` trait may be added to your application's `User` model (or any other model that has features) to provide a fluent, convenient way to check features directly from the model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Foundation\Auth\User as Authenticatable;

 6use Laravel\Pennant\Concerns\HasFeatures;

 7 

 8class User extends Authenticatable

 9{

10    use HasFeatures;

11 

12    // ...

13}
```

Once the trait has been added to your model, you may easily check features by invoking the `features` method:

```
1if ($user->features()->active('new-api')) {

2    // ...

3}
```

Of course, the `features` method provides access to many other convenient methods for interacting with features:

```
 1// Values...

 2$value = $user->features()->value('purchase-button')

 3$values = $user->features()->values(['new-api', 'purchase-button']);

 4 

 5// State...

 6$user->features()->active('new-api');

 7$user->features()->allAreActive(['new-api', 'server-api']);

 8$user->features()->someAreActive(['new-api', 'server-api']);

 9 

10$user->features()->inactive('new-api');

11$user->features()->allAreInactive(['new-api', 'server-api']);

12$user->features()->someAreInactive(['new-api', 'server-api']);

13 

14// Conditional execution...

15$user->features()->when('new-api',

16    fn () => /* ... */,

17    fn () => /* ... */,

18);

19 

20$user->features()->unless('new-api',

21    fn () => /* ... */,

22    fn () => /* ... */,

23);
```

### [Blade Directive](#blade-directive)

To make checking features in Blade a seamless experience, Pennant offers the `@feature` and `@featureany` directive:

```
1@feature('site-redesign')

2    <!-- 'site-redesign' is active -->

3@else

4    <!-- 'site-redesign' is inactive -->

5@endfeature

6 

7@featureany(['site-redesign', 'beta'])

8    <!-- 'site-redesign' or `beta` is active -->

9@endfeatureany
```

### [Middleware](#middleware)

Pennant also includes a [middleware](/docs/13.x/middleware) that may be used to verify the currently authenticated user has access to a feature before a route is even invoked. You may assign the middleware to a route and specify the features that are required to access the route. If any of the specified features are inactive for the currently authenticated user, a `400 Bad Request` HTTP response will be returned by the route. Multiple features may be passed to the static `using` method.

```
1use Illuminate\Support\Facades\Route;

2use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

3 

4Route::get('/api/servers', function () {

5    // ...

6})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

#### [Customizing the Response](#customizing-the-response)

If you would like to customize the response that is returned by the middleware when one of the listed features is inactive, you may use the `whenInactive` method provided by the `EnsureFeaturesAreActive` middleware. Typically, this method should be invoked within the `boot` method of one of your application's service providers:

```
 1use Illuminate\Http\Request;

 2use Illuminate\Http\Response;

 3use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    EnsureFeaturesAreActive::whenInactive(

11        function (Request $request, array $features) {

12            return new Response(status: 403);

13        }

14    );

15 

16    // ...

17}
```

### [Intercepting Feature Checks](#intercepting-feature-checks)

Sometimes it can be useful to perform some in-memory checks before retrieving the stored value of a given feature. Imagine you are developing a new API behind a feature flag and want the ability to disable the new API without losing any of the resolved feature values in storage. If you notice a bug in the new API, you could easily disable it for everyone except internal team members, fix the bug, and then re-enable the new API for the users that previously had access to the feature.

You can achieve this with a [class-based feature's](#class-based-features) `before` method. When present, the `before` method is always run in-memory before retrieving the value from storage. If a non-`null` value is returned from the method, it will be used in place of the feature's stored value for the duration of the request:

```
 1<?php

 2 

 3namespace App\Features;

 4 

 5use App\Models\User;

 6use Illuminate\Support\Facades\Config;

 7use Illuminate\Support\Lottery;

 8 

 9class NewApi

10{

11    /**

12     * Run an always-in-memory check before the stored value is retrieved.

13     */

14    public function before(User $user): mixed

15    {

16        if (Config::get('features.new-api.disabled')) {

17            return $user->isInternalTeamMember();

18        }

19    }

20 

21    /**

22     * Resolve the feature's initial value.

23     */

24    public function resolve(User $user): mixed

25    {

26        return match (true) {

27            $user->isInternalTeamMember() => true,

28            $user->isHighTrafficCustomer() => false,

29            default => Lottery::odds(1 / 100),

30        };

31    }

32}
```

You could also use this feature to schedule the global rollout of a feature that was previously behind a feature flag:

```
 1<?php

 2 

 3namespace App\Features;

 4 

 5use Illuminate\Support\Carbon;

 6use Illuminate\Support\Facades\Config;

 7 

 8class NewApi

 9{

10    /**

11     * Run an always-in-memory check before the stored value is retrieved.

12     */

13    public function before(User $user): mixed

14    {

15        if (Config::get('features.new-api.disabled')) {

16            return $user->isInternalTeamMember();

17        }

18 

19        if (Carbon::parse(Config::get('features.new-api.rollout-date'))->isPast()) {

20            return true;

21        }

22    }

23 

24    // ...

25}
```

### [In-Memory Cache](#in-memory-cache)

When checking a feature, Pennant will create an in-memory cache of the result. If you are using the `database` driver, this means that re-checking the same feature flag within a single request will not trigger additional database queries. This also ensures that the feature has a consistent result for the duration of the request.

If you need to manually flush the in-memory cache, you may use the `flushCache` method offered by the `Feature` facade:

```
1Feature::flushCache();
```

## [Scope](#scope)

### [Specifying the Scope](#specifying-the-scope)

As discussed, features are typically checked against the currently authenticated user. However, this may not always suit your needs. Therefore, it is possible to specify the scope you would like to check a given feature against via the `Feature` facade's `for` method:

```
1return Feature::for($user)->active('new-api')

2    ? $this->resolveNewApiResponse($request)

3    : $this->resolveLegacyApiResponse($request);
```

Of course, feature scopes are not limited to "users". Imagine you have built a new billing experience that you are rolling out to entire teams rather than individual users. Perhaps you would like the oldest teams to have a slower rollout than the newer teams. Your feature resolution closure might look something like the following:

```
 1use App\Models\Team;

 2use Illuminate\Support\Carbon;

 3use Illuminate\Support\Lottery;

 4use Laravel\Pennant\Feature;

 5 

 6Feature::define('billing-v2', function (Team $team) {

 7    if ($team->created_at->isAfter(new Carbon('1st Jan, 2023'))) {

 8        return true;

 9    }

10 

11    if ($team->created_at->isAfter(new Carbon('1st Jan, 2019'))) {

12        return Lottery::odds(1 / 100);

13    }

14 

15    return Lottery::odds(1 / 1000);

16});
```

You will notice that the closure we have defined is not expecting a `User`, but is instead expecting a `Team` model. To determine if this feature is active for a user's team, you should pass the team to the `for` method offered by the `Feature` facade:

```
1if (Feature::for($user->team)->active('billing-v2')) {

2    return redirect('/billing/v2');

3}

4 

5// ...
```

### [Default Scope](#default-scope)

It is also possible to customize the default scope Pennant uses to check features. For example, maybe all of your features are checked against the currently authenticated user's team instead of the user. Instead of having to call `Feature::for($user->team)` every time you check a feature, you may instead specify the team as the default scope. Typically, this should be done in one of your application's service providers:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Support\Facades\Auth;

 6use Illuminate\Support\ServiceProvider;

 7use Laravel\Pennant\Feature;

 8 

 9class AppServiceProvider extends ServiceProvider

10{

11    /**

12     * Bootstrap any application services.

13     */

14    public function boot(): void

15    {

16        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

17 

18        // ...

19    }

20}
```

If no scope is explicitly provided via the `for` method, the feature check will now use the currently authenticated user's team as the default scope:

```
1Feature::active('billing-v2');

2 

3// Is now equivalent to...

4 

5Feature::for($user->team)->active('billing-v2');
```

### [Nullable Scope](#nullable-scope)

If the scope you provide when checking a feature is `null` and the feature's definition does not support `null` via a nullable type or by including `null` in a union type, Pennant will automatically return `false` as the feature's result value.

So, if the scope you are passing to a feature is potentially `null` and you want the feature's value resolver to be invoked, you should account for that in your feature's definition. A `null` scope may occur if you check a feature within an Artisan command, queued job, or unauthenticated route. Since there is usually not an authenticated user in these contexts, the default scope will be `null`.

If you do not always [explicitly specify your feature scope](#specifying-the-scope) then you should ensure the scope's type is "nullable" and handle the `null` scope value within your feature definition logic:

```
 1use App\Models\User;

 2use Illuminate\Support\Lottery;

 3use Laravel\Pennant\Feature;

 4 

 5Feature::define('new-api', fn (User $user) => match (true) {

 6Feature::define('new-api', fn (User|null $user) => match (true) {

 7    $user === null => true,

 8    $user->isInternalTeamMember() => true,

 9    $user->isHighTrafficCustomer() => false,

10    default => Lottery::odds(1 / 100),

11});
```

### [Identifying Scope](#identifying-scope)

Pennant's built-in `array` and `database` storage drivers know how to properly store scope identifiers for all PHP data types as well as Eloquent models. However, if your application utilizes a third-party Pennant driver, that driver may not know how to properly store an identifier for an Eloquent model or other custom types in your application.

In light of this, Pennant allows you to format scope values for storage by implementing the `FeatureScopeable` contract on the objects in your application that are used as Pennant scopes.

For example, imagine you are using two different feature drivers in a single application: the built-in `database` driver and a third-party "Flag Rocket" driver. The "Flag Rocket" driver does not know how to properly store an Eloquent model. Instead, it requires a `FlagRocketUser` instance. By implementing the `toFeatureIdentifier` defined by the `FeatureScopeable` contract, we can customize the storable scope value provided to each driver used by our application:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use FlagRocket\FlagRocketUser;

 6use Illuminate\Database\Eloquent\Model;

 7use Laravel\Pennant\Contracts\FeatureScopeable;

 8 

 9class User extends Model implements FeatureScopeable

10{

11    /**

12     * Cast the object to a feature scope identifier for the given driver.

13     */

14    public function toFeatureIdentifier(string $driver): mixed

15    {

16        return match($driver) {

17            'database' => $this,

18            'flag-rocket' => FlagRocketUser::fromId($this->flag_rocket_id),

19        };

20    }

21}
```

### [Serializing Scope](#serializing-scope)

By default, Pennant will use a fully qualified class name when storing a feature associated with an Eloquent model. If you are already using an [Eloquent morph map](/docs/13.x/eloquent-relationships#custom-polymorphic-types), you may choose to have Pennant also use the morph map to decouple the stored feature from your application structure.

To achieve this, after defining your Eloquent morph map in a service provider, you may invoke the `Feature` facade's `useMorphMap` method:

```
1use Illuminate\Database\Eloquent\Relations\Relation;

2use Laravel\Pennant\Feature;

3 

4Relation::enforceMorphMap([

5    'post' => 'App\Models\Post',

6    'video' => 'App\Models\Video',

7]);

8 

9Feature::useMorphMap();
```

## [Rich Feature Values](#rich-feature-values)

Until now, we have primarily shown features as being in a binary state, meaning they are either "active" or "inactive", but Pennant also allows you to store rich values as well.

For example, imagine you are testing three new colors for the "Buy now" button of your application. Instead of returning `true` or `false` from the feature definition, you may instead return a string:

```
1use Illuminate\Support\Arr;

2use Laravel\Pennant\Feature;

3 

4Feature::define('purchase-button', fn (User $user) => Arr::random([

5    'blue-sapphire',

6    'seafoam-green',

7    'tart-orange',

8]));
```

You may retrieve the value of the `purchase-button` feature using the `value` method:

```
1$color = Feature::value('purchase-button');
```

Pennant's included Blade directive also makes it easy to conditionally render content based on the current value of the feature:

```
1@feature('purchase-button', 'blue-sapphire')

2    <!-- 'blue-sapphire' is active -->

3@elsefeature('purchase-button', 'seafoam-green')

4    <!-- 'seafoam-green' is active -->

5@elsefeature('purchase-button', 'tart-orange')

6    <!-- 'tart-orange' is active -->

7@endfeature
```

When using rich values, it is important to know that a feature is considered "active" when it has any value other than `false`.

When calling the [conditional `when`](#conditional-execution) method, the feature's rich value will be provided to the first closure:

```
1Feature::when('purchase-button',

2    fn ($color) => /* ... */,

3    fn () => /* ... */,

4);
```

Likewise, when calling the conditional `unless` method, the feature's rich value will be provided to the optional second closure:

```
1Feature::unless('purchase-button',

2    fn () => /* ... */,

3    fn ($color) => /* ... */,

4);
```

## [Retrieving Multiple Features](#retrieving-multiple-features)

The `values` method allows the retrieval of multiple features for a given scope:

```
1Feature::values(['billing-v2', 'purchase-button']);

2 

3// [

4//     'billing-v2' => false,

5//     'purchase-button' => 'blue-sapphire',

6// ]
```

Or, you may use the `all` method to retrieve the values of all defined features for a given scope:

```
1Feature::all();

2 

3// [

4//     'billing-v2' => false,

5//     'purchase-button' => 'blue-sapphire',

6//     'site-redesign' => true,

7// ]
```

However, class-based features are dynamically registered and are not known by Pennant until they are explicitly checked. This means your application's class-based features may not appear in the results returned by the `all` method if they have not already been checked during the current request.

If you would like to ensure that feature classes are always included when using the `all` method, you may use Pennant's feature discovery capabilities. To get started, invoke the `discover` method in one of your application's service providers:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Support\ServiceProvider;

 6use Laravel\Pennant\Feature;

 7 

 8class AppServiceProvider extends ServiceProvider

 9{

10    /**

11     * Bootstrap any application services.

12     */

13    public function boot(): void

14    {

15        Feature::discover();

16 

17        // ...

18    }

19}
```

The `discover` method will register all of the feature classes in your application's `app/Features` directory. The `all` method will now include these classes in its results, regardless of whether they have been checked during the current request:

```
1Feature::all();

2 

3// [

4//     'App\Features\NewApi' => true,

5//     'billing-v2' => false,

6//     'purchase-button' => 'blue-sapphire',

7//     'site-redesign' => true,

8// ]
```

## [Eager Loading](#eager-loading)

Although Pennant keeps an in-memory cache of all resolved features for a single request, it is still possible to encounter performance issues. To alleviate this, Pennant offers the ability to eager load feature values.

To illustrate this, imagine that we are checking if a feature is active within a loop:

```
1use Laravel\Pennant\Feature;

2 

3foreach ($users as $user) {

4    if (Feature::for($user)->active('notifications-beta')) {

5        $user->notify(new RegistrationSuccess);

6    }

7}
```

Assuming we are using the database driver, this code will execute a database query for every user in the loop - executing potentially hundreds of queries. However, using Pennant's `load` method, we can remove this potential performance bottleneck by eager loading the feature values for a collection of users or scopes:

```
1Feature::for($users)->load(['notifications-beta']);

2 

3foreach ($users as $user) {

4    if (Feature::for($user)->active('notifications-beta')) {

5        $user->notify(new RegistrationSuccess);

6    }

7}
```

To load feature values only when they have not already been loaded, you may use the `loadMissing` method:

```
1Feature::for($users)->loadMissing([

2    'new-api',

3    'purchase-button',

4    'notifications-beta',

5]);
```

You may load all defined features using the `loadAll` method:

```
1Feature::for($users)->loadAll();
```

## [Updating Values](#updating-values)

When a feature's value is resolved for the first time, the underlying driver will store the result in storage. This is often necessary to ensure a consistent experience for your users across requests. However, at times, you may want to manually update the feature's stored value.

To accomplish this, you may use the `activate` and `deactivate` methods to toggle a feature "on" or "off":

```
1use Laravel\Pennant\Feature;

2 

3// Activate the feature for the default scope...

4Feature::activate('new-api');

5 

6// Deactivate the feature for the given scope...

7Feature::for($user->team)->deactivate('billing-v2');
```

It is also possible to manually set a rich value for a feature by providing a second argument to the `activate` method:

```
1Feature::activate('purchase-button', 'seafoam-green');
```

To instruct Pennant to forget the stored value for a feature, you may use the `forget` method. When the feature is checked again, Pennant will resolve the feature's value from its feature definition:

```
1Feature::forget('purchase-button');
```

### [Bulk Updates](#bulk-updates)

To update stored feature values in bulk, you may use the `activateForEveryone` and `deactivateForEveryone` methods.

For example, imagine you are now confident in the `new-api` feature's stability and have landed on the best `'purchase-button'` color for your checkout flow - you can update the stored value for all users accordingly:

```
1use Laravel\Pennant\Feature;

2 

3Feature::activateForEveryone('new-api');

4 

5Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

Alternatively, you may deactivate the feature for all users:

```
1Feature::deactivateForEveryone('new-api');
```

This will only update the resolved feature values that have been stored by Pennant's storage driver. You will also need to update the feature definition in your application.

### [Purging Features](#purging-features)

Sometimes, it can be useful to purge an entire feature from storage. This is typically necessary if you have removed the feature from your application or you have made adjustments to the feature's definition that you would like to rollout to all users.

You may remove all stored values for a feature using the `purge` method:

```
1// Purging a single feature...

2Feature::purge('new-api');

3 

4// Purging multiple features...

5Feature::purge(['new-api', 'purchase-button']);
```

If you would like to purge *all* features from storage, you may invoke the `purge` method without any arguments:

```
1Feature::purge();
```

As it can be useful to purge features as part of your application's deployment pipeline, Pennant includes a `pennant:purge` Artisan command which will purge the provided features from storage:

```
1php artisan pennant:purge new-api

2 

3php artisan pennant:purge new-api purchase-button
```

It is also possible to purge all features *except* those in a given feature list. For example, imagine you wanted to purge all features but keep the values for the "new-api" and "purchase-button" features in storage. To accomplish this, you can pass those feature names to the `--except` option:

```
1php artisan pennant:purge --except=new-api --except=purchase-button
```

For convenience, the `pennant:purge` command also supports an `--except-registered` flag. This flag indicates that all features except those explicitly registered in a service provider should be purged:

```
1php artisan pennant:purge --except-registered
```

## [Testing](#testing)

When testing code that interacts with feature flags, the easiest way to control the feature flag's returned value in your tests is to simply re-define the feature. For example, imagine you have the following feature defined in one of your application's service provider:

```
1use Illuminate\Support\Arr;

2use Laravel\Pennant\Feature;

3 

4Feature::define('purchase-button', fn () => Arr::random([

5    'blue-sapphire',

6    'seafoam-green',

7    'tart-orange',

8]));
```

To modify the feature's returned value in your tests, you may re-define the feature at the beginning of the test. The following test will always pass, even though the `Arr::random()` implementation is still present in the service provider:

Pest

PHPUnit

```
1use Laravel\Pennant\Feature;

2 

3test('it can control feature values', function () {

4    Feature::define('purchase-button', 'seafoam-green');

5 

6    expect(Feature::value('purchase-button'))->toBe('seafoam-green');

7});
```

```
1use Laravel\Pennant\Feature;

2 

3public function test_it_can_control_feature_values()

4{

5    Feature::define('purchase-button', 'seafoam-green');

6 

7    $this->assertSame('seafoam-green', Feature::value('purchase-button'));

8}
```

The same approach may be used for class-based features:

Pest

PHPUnit

```
1use Laravel\Pennant\Feature;

2 

3test('it can control feature values', function () {

4    Feature::define(NewApi::class, true);

5 

6    expect(Feature::value(NewApi::class))->toBeTrue();

7});
```

```
1use App\Features\NewApi;

2use Laravel\Pennant\Feature;

3 

4public function test_it_can_control_feature_values()

5{

6    Feature::define(NewApi::class, true);

7 

8    $this->assertTrue(Feature::value(NewApi::class));

9}
```

If your feature is returning a `Lottery` instance, there are a handful of useful [testing helpers available](/docs/13.x/helpers#testing-lotteries).

#### [Store Configuration](#store-configuration)

You may configure the store that Pennant will use during testing by defining the `PENNANT_STORE` environment variable in your application's `phpunit.xml` file:

```
1<?xml version="1.0" encoding="UTF-8"?>

2<phpunit colors="true">

3    <!-- ... -->

4    <php>

5        <env name="PENNANT_STORE" value="array"/>

6        <!-- ... -->

7    </php>

8</phpunit>
```

## [Adding Custom Pennant Drivers](#adding-custom-pennant-drivers)

#### [Implementing the Driver](#implementing-the-driver)

If none of Pennant's existing storage drivers fit your application's needs, you may write your own storage driver. Your custom driver should implement the `Laravel\Pennant\Contracts\Driver` interface:

```
 1<?php

 2 

 3namespace App\Extensions;

 4 

 5use Laravel\Pennant\Contracts\Driver;

 6 

 7class RedisFeatureDriver implements Driver

 8{

 9    public function define(string $feature, callable $resolver): void {}

10    public function defined(): array {}

11    public function getAll(array $features): array {}

12    public function get(string $feature, mixed $scope): mixed {}

13    public function set(string $feature, mixed $scope, mixed $value): void {}

14    public function setForAllScopes(string $feature, mixed $value): void {}

15    public function delete(string $feature, mixed $scope): void {}

16    public function purge(array|null $features): void {}

17}
```

Now, we just need to implement each of these methods using a Redis connection. For an example of how to implement each of these methods, take a look at the `Laravel\Pennant\Drivers\DatabaseDriver` in the [Pennant source code](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)

Laravel does not ship with a directory to contain your extensions. You are free to place them anywhere you like. In this example, we have created an `Extensions` directory to house the `RedisFeatureDriver`.

#### [Registering the Driver](#registering-the-driver)

Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Pennant, you may use the `extend` method provided by the `Feature` facade. You should call the `extend` method from the `boot` method of one of your application's [service provider](/docs/13.x/providers):

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use App\Extensions\RedisFeatureDriver;

 6use Illuminate\Contracts\Foundation\Application;

 7use Illuminate\Support\ServiceProvider;

 8use Laravel\Pennant\Feature;

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

25        Feature::extend('redis', function (Application $app) {

26            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);

27        });

28    }

29}
```

Once the driver has been registered, you may use the `redis` driver in your application's `config/pennant.php` configuration file:

```
 1'stores' => [

 2 

 3    'redis' => [

 4        'driver' => 'redis',

 5        'connection' => null,

 6    ],

 7 

 8    // ...

 9 

10],
```

### [Defining Features Externally](#defining-features-externally)

If your driver is a wrapper around a third-party feature flag platform, you will likely define features on the platform rather than using Pennant's `Feature::define` method. If that is the case, your custom driver should also implement the `Laravel\Pennant\Contracts\DefinesFeaturesExternally` interface:

```
 1<?php

 2 

 3namespace App\Extensions;

 4 

 5use Laravel\Pennant\Contracts\Driver;

 6use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

 7 

 8class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally

 9{

10    /**

11     * Get the features defined for the given scope.

12     */

13    public function definedFeaturesForScope(mixed $scope): array {}

14 

15    /* ... */

16}
```

The `definedFeaturesForScope` method should return a list of feature names defined for the provided scope.

## [Events](#events)

Pennant dispatches a variety of events that can be useful when tracking feature flags throughout your application.

### `Laravel\Pennant\Events\FeatureRetrieved`

This event is dispatched whenever a [feature is checked](#checking-features). This event may be useful for creating and tracking metrics against a feature flag's usage throughout your application.

### `Laravel\Pennant\Events\FeatureResolved`

This event is dispatched the first time a feature's value is resolved for a specific scope.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

This event is dispatched the first time an unknown feature is resolved for a specific scope. Listening to this event may be useful if you have intended to remove a feature flag but have accidentally left stray references to it throughout your application:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Support\ServiceProvider;

 6use Illuminate\Support\Facades\Event;

 7use Illuminate\Support\Facades\Log;

 8use Laravel\Pennant\Events\UnknownFeatureResolved;

 9 

10class AppServiceProvider extends ServiceProvider

11{

12    /**

13     * Bootstrap any application services.

14     */

15    public function boot(): void

16    {

17        Event::listen(function (UnknownFeatureResolved $event) {

18            Log::error("Resolving unknown feature [{$event->feature}].");

19        });

20    }

21}
```

### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass`

This event is dispatched when a [class-based feature](#class-based-features) is dynamically checked for the first time during a request.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

This event is dispatched when a `null` scope is passed to a feature definition that [doesn't support null](#nullable-scope).

This situation is handled gracefully and the feature will return `false`. However, if you would like to opt out of this feature's default graceful behavior, you may register a listener for this event in the `boot` method of your application's `AppServiceProvider`:

```
 1use Illuminate\Support\Facades\Log;

 2use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));

10}
```

### `Laravel\Pennant\Events\FeatureUpdated`

This event is dispatched when updating a feature for a scope, usually by calling `activate` or `deactivate`.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

This event is dispatched when updating a feature for all scopes, usually by calling `activateForEveryone` or `deactivateForEveryone`.

### `Laravel\Pennant\Events\FeatureDeleted`

This event is dispatched when deleting a feature for a scope, usually by calling `forget`.

### `Laravel\Pennant\Events\FeaturesPurged`

This event is dispatched when purging specific features.

### `Laravel\Pennant\Events\AllFeaturesPurged`

This event is dispatched when purging all features.
