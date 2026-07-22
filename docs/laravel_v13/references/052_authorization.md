# Authorization

- [Introduction](#introduction)
- [Gates](#gates)
  * [Writing Gates](#writing-gates)
  * [Authorizing Actions](#authorizing-actions-via-gates)
  * [Gate Responses](#gate-responses)
  * [Intercepting Gate Checks](#intercepting-gate-checks)
  * [Inline Authorization](#inline-authorization)
- [Creating Policies](#creating-policies)
  * [Generating Policies](#generating-policies)
  * [Registering Policies](#registering-policies)
- [Writing Policies](#writing-policies)
  * [Policy Methods](#policy-methods)
  * [Policy Responses](#policy-responses)
  * [Methods Without Models](#methods-without-models)
  * [Guest Users](#guest-users)
  * [Policy Filters](#policy-filters)
- [Authorizing Actions Using Policies](#authorizing-actions-using-policies)
  * [Via the User Model](#via-the-user-model)
  * [Via the Gate Facade](#via-the-gate-facade)
  * [Via Middleware](#via-middleware)
  * [Via Blade Templates](#via-blade-templates)
  * [Supplying Additional Context](#supplying-additional-context)
- [Authorization & Inertia](#authorization-and-inertia)

## [Introduction](#introduction)

In addition to providing built-in [authentication](/docs/13.x/authentication) services, Laravel also provides a simple way to authorize user actions against a given resource. For example, even though a user is authenticated, they may not be authorized to update or delete certain Eloquent models or database records managed by your application. Laravel's authorization features provide an easy, organized way of managing these types of authorization checks.

Laravel provides two primary ways of authorizing actions: [gates](#gates) and [policies](#creating-policies). Think of gates and policies like routes and controllers. Gates provide a simple, closure-based approach to authorization while policies, like controllers, group logic around a particular model or resource. In this documentation, we'll explore gates first and then examine policies.

You do not need to choose between exclusively using gates or exclusively using policies when building an application. Most applications will most likely contain some mixture of gates and policies, and that is perfectly fine! Gates are most applicable to actions that are not related to any model or resource, such as viewing an administrator dashboard. In contrast, policies should be used when you wish to authorize an action for a particular model or resource.

## [Gates](#gates)

### [Writing Gates](#writing-gates)

Gates are a great way to learn the basics of Laravel's authorization features; however, when building robust Laravel applications you should consider using [policies](#creating-policies) to organize your authorization rules.

Gates are simply closures that determine if a user is authorized to perform a given action. Typically, gates are defined within the `boot` method of the `App\Providers\AppServiceProvider` class using the `Gate` facade. Gates always receive a user instance as their first argument and may optionally receive additional arguments such as a relevant Eloquent model.

In this example, we'll define a gate to determine if a user can update a given `App\Models\Post` model. The gate will accomplish this by comparing the user's `id` against the `user_id` of the user that created the post:

```
 1use App\Models\Post;

 2use App\Models\User;

 3use Illuminate\Support\Facades\Gate;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Gate::define('update-post', function (User $user, Post $post) {

11        return $user->id === $post->user_id;

12    });

13}
```

Like controllers, gates may also be defined using a class callback array:

```
 1use App\Policies\PostPolicy;

 2use Illuminate\Support\Facades\Gate;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Gate::define('update-post', [PostPolicy::class, 'update']);

10}
```

### [Authorizing Actions](#authorizing-actions-via-gates)

To authorize an action using gates, you should use the `allows` or `denies` methods provided by the `Gate` facade. Note that you are not required to pass the currently authenticated user to these methods. Laravel will automatically take care of passing the user into the gate closure. It is typical to call the gate authorization methods within your application's controllers before performing an action that requires authorization:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Models\Post;

 6use Illuminate\Http\RedirectResponse;

 7use Illuminate\Http\Request;

 8use Illuminate\Support\Facades\Gate;

 9 

10class PostController extends Controller

11{

12    /**

13     * Update the given post.

14     */

15    public function update(Request $request, Post $post): RedirectResponse

16    {

17        if (! Gate::allows('update-post', $post)) {

18            abort(403);

19        }

20 

21        // Update the post...

22 

23        return redirect('/posts');

24    }

25}
```

If you would like to determine if a user other than the currently authenticated user is authorized to perform an action, you may use the `forUser` method on the `Gate` facade:

```
1if (Gate::forUser($user)->allows('update-post', $post)) {

2    // The user can update the post...

3}

4 

5if (Gate::forUser($user)->denies('update-post', $post)) {

6    // The user can't update the post...

7}
```

You may authorize multiple actions at a time using the `any` or `none` methods:

```
1if (Gate::any(['update-post', 'delete-post'], $post)) {

2    // The user can update or delete the post...

3}

4 

5if (Gate::none(['update-post', 'delete-post'], $post)) {

6    // The user can't update or delete the post...

7}
```

#### [Authorizing or Throwing Exceptions](#authorizing-or-throwing-exceptions)

If you would like to attempt to authorize an action and automatically throw an `Illuminate\Auth\Access\AuthorizationException` if the user is not allowed to perform the given action, you may use the `Gate` facade's `authorize` method. Instances of `AuthorizationException` are automatically converted to a 403 HTTP response by Laravel:

```
1Gate::authorize('update-post', $post);

2 

3// The action is authorized...
```

#### [Supplying Additional Context](#gates-supplying-additional-context)

The gate methods for authorizing abilities (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) and the authorization [Blade directives](#via-blade-templates) (`@can`, `@cannot`, `@canany`) can receive an array as their second argument. These array elements are passed as parameters to the gate closure, and can be used for additional context when making authorization decisions:

```
 1use App\Models\Category;

 2use App\Models\User;

 3use Illuminate\Support\Facades\Gate;

 4 

 5Gate::define('create-post', function (User $user, Category $category, bool $pinned) {

 6    if (! $user->canPublishToGroup($category->group)) {

 7        return false;

 8    } elseif ($pinned && ! $user->canPinPosts()) {

 9        return false;

10    }

11 

12    return true;

13});

14 

15if (Gate::check('create-post', [$category, $pinned])) {

16    // The user can create the post...

17}
```

### [Gate Responses](#gate-responses)

So far, we have only examined gates that return simple boolean values. However, sometimes you may wish to return a more detailed response, including an error message. To do so, you may return an `Illuminate\Auth\Access\Response` from your gate:

```
1use App\Models\User;

2use Illuminate\Auth\Access\Response;

3use Illuminate\Support\Facades\Gate;

4 

5Gate::define('edit-settings', function (User $user) {

6    return $user->isAdmin

7        ? Response::allow()

8        : Response::deny('You must be an administrator.');

9});
```

Even when you return an authorization response from your gate, the `Gate::allows` method will still return a simple boolean value; however, you may use the `Gate::inspect` method to get the full authorization response returned by the gate:

```
1$response = Gate::inspect('edit-settings');

2 

3if ($response->allowed()) {

4    // The action is authorized...

5} else {

6    echo $response->message();

7}
```

When using the `Gate::authorize` method, which throws an `AuthorizationException` if the action is not authorized, the error message provided by the authorization response will be propagated to the HTTP response:

```
1Gate::authorize('edit-settings');

2 

3// The action is authorized...
```

#### [Customizing The HTTP Response Status](#customizing-gate-response-status)

When an action is denied via a Gate, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class:

```
1use App\Models\User;

2use Illuminate\Auth\Access\Response;

3use Illuminate\Support\Facades\Gate;

4 

5Gate::define('edit-settings', function (User $user) {

6    return $user->isAdmin

7        ? Response::allow()

8        : Response::denyWithStatus(404);

9});
```

Because hiding resources via a `404` response is such a common pattern for web applications, the `denyAsNotFound` method is offered for convenience:

```
1use App\Models\User;

2use Illuminate\Auth\Access\Response;

3use Illuminate\Support\Facades\Gate;

4 

5Gate::define('edit-settings', function (User $user) {

6    return $user->isAdmin

7        ? Response::allow()

8        : Response::denyAsNotFound();

9});
```

### [Intercepting Gate Checks](#intercepting-gate-checks)

Sometimes, you may wish to grant all abilities to a specific user. You may use the `before` method to define a closure that is run before all other authorization checks:

```
1use App\Models\User;

2use Illuminate\Support\Facades\Gate;

3 

4Gate::before(function (User $user, string $ability) {

5    if ($user->isAdministrator()) {

6        return true;

7    }

8});
```

If the `before` closure returns a non-null result that result will be considered the result of the authorization check.

You may use the `after` method to define a closure to be executed after all other authorization checks:

```
1use App\Models\User;

2 

3Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {

4    if ($user->isAdministrator()) {

5        return true;

6    }

7});
```

Values returned by `after` closures will not override the result of the authorization check unless the gate or policy returned `null`.

### [Inline Authorization](#inline-authorization)

Occasionally, you may wish to determine if the currently authenticated user is authorized to perform a given action without writing a dedicated gate that corresponds to the action. Laravel allows you to perform these types of "inline" authorization checks via the `Gate::allowIf` and `Gate::denyIf` methods. Inline authorization does not execute any defined ["before" or "after" authorization hooks](#intercepting-gate-checks):

```
1use App\Models\User;

2use Illuminate\Support\Facades\Gate;

3 

4Gate::allowIf(fn (User $user) => $user->isAdministrator());

5 

6Gate::denyIf(fn (User $user) => $user->banned());
```

If the action is not authorized or if no user is currently authenticated, Laravel will automatically throw an `Illuminate\Auth\Access\AuthorizationException` exception. Instances of `AuthorizationException` are automatically converted to a 403 HTTP response by Laravel's exception handler.

## [Creating Policies](#creating-policies)

### [Generating Policies](#generating-policies)

Policies are classes that organize authorization logic around a particular model or resource. For example, if your application is a blog, you may have an `App\Models\Post` model and a corresponding `App\Policies\PostPolicy` to authorize user actions such as creating or updating posts.

You may generate a policy using the `make:policy` Artisan command. The generated policy will be placed in the `app/Policies` directory. If this directory does not exist in your application, Laravel will create it for you:

```
1php artisan make:policy PostPolicy
```

The `make:policy` command will generate an empty policy class. If you would like to generate a class with example policy methods related to viewing, creating, updating, and deleting the resource, you may provide a `--model` option when executing the command:

```
1php artisan make:policy PostPolicy --model=Post
```

### [Registering Policies](#registering-policies)

#### [Policy Discovery](#policy-discovery)

By default, Laravel automatically discover policies as long as the model and policy follow standard Laravel naming conventions. Specifically, the policies must be in a `Policies` directory at or above the directory that contains your models. So, for example, the models may be placed in the `app/Models` directory while the policies may be placed in the `app/Policies` directory. In this situation, Laravel will check for policies in `app/Models/Policies` then `app/Policies`. In addition, the policy name must match the model name and have a `Policy` suffix. So, a `User` model would correspond to a `UserPolicy` policy class.

If you would like to define your own policy discovery logic, you may register a custom policy discovery callback using the `Gate::guessPolicyNamesUsing` method. Typically, this method should be called from the `boot` method of your application's `AppServiceProvider`:

```
1use Illuminate\Support\Facades\Gate;

2 

3Gate::guessPolicyNamesUsing(function (string $modelClass) {

4    // Return the name of the policy class for the given model...

5});
```

#### [Manually Registering Policies](#manually-registering-policies)

Using the `Gate` facade, you may manually register policies and their corresponding models within the `boot` method of your application's `AppServiceProvider`:

```
 1use App\Models\Order;

 2use App\Policies\OrderPolicy;

 3use Illuminate\Support\Facades\Gate;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Gate::policy(Order::class, OrderPolicy::class);

11}
```

Alternatively, you may place the `UsePolicy` attribute on a model class to inform Laravel of the model's corresponding policy:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use App\Policies\OrderPolicy;

 6use Illuminate\Database\Eloquent\Attributes\UsePolicy;

 7use Illuminate\Database\Eloquent\Model;

 8 

 9#[UsePolicy(OrderPolicy::class)]

10class Order extends Model

11{

12    //

13}
```

## [Writing Policies](#writing-policies)

### [Policy Methods](#policy-methods)

Once the policy class has been registered, you may add methods for each action it authorizes. For example, let's define an `update` method on our `PostPolicy` which determines if a given `App\Models\User` can update a given `App\Models\Post` instance.

The `update` method will receive a `User` and a `Post` instance as its arguments, and should return `true` or `false` indicating whether the user is authorized to update the given `Post`. So, in this example, we will verify that the user's `id` matches the `user_id` on the post:

```
 1<?php

 2 

 3namespace App\Policies;

 4 

 5use App\Models\Post;

 6use App\Models\User;

 7 

 8class PostPolicy

 9{

10    /**

11     * Determine if the given post can be updated by the user.

12     */

13    public function update(User $user, Post $post): bool

14    {

15        return $user->id === $post->user_id;

16    }

17}
```

You may continue to define additional methods on the policy as needed for the various actions it authorizes. For example, you might define `view` or `delete` methods to authorize various `Post` related actions, but remember you are free to give your policy methods any name you like.

If you used the `--model` option when generating your policy via the Artisan console, it will already contain methods for the `viewAny`, `view`, `create`, `update`, `delete`, `restore`, and `forceDelete` actions.

All policies are resolved via the Laravel [service container](/docs/13.x/container), allowing you to type-hint any needed dependencies in the policy's constructor to have them automatically injected.

### [Policy Responses](#policy-responses)

So far, we have only examined policy methods that return simple boolean values. However, sometimes you may wish to return a more detailed response, including an error message. To do so, you may return an `Illuminate\Auth\Access\Response` instance from your policy method:

```
 1use App\Models\Post;

 2use App\Models\User;

 3use Illuminate\Auth\Access\Response;

 4 

 5/**

 6 * Determine if the given post can be updated by the user.

 7 */

 8public function update(User $user, Post $post): Response

 9{

10    return $user->id === $post->user_id

11        ? Response::allow()

12        : Response::deny('You do not own this post.');

13}
```

When returning an authorization response from your policy, the `Gate::allows` method will still return a simple boolean value; however, you may use the `Gate::inspect` method to get the full authorization response returned by the gate:

```
1use Illuminate\Support\Facades\Gate;

2 

3$response = Gate::inspect('update', $post);

4 

5if ($response->allowed()) {

6    // The action is authorized...

7} else {

8    echo $response->message();

9}
```

When using the `Gate::authorize` method, which throws an `AuthorizationException` if the action is not authorized, the error message provided by the authorization response will be propagated to the HTTP response:

```
1Gate::authorize('update', $post);

2 

3// The action is authorized...
```

#### [Customizing the HTTP Response Status](#customizing-policy-response-status)

When an action is denied via a policy method, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class:

```
 1use App\Models\Post;

 2use App\Models\User;

 3use Illuminate\Auth\Access\Response;

 4 

 5/**

 6 * Determine if the given post can be updated by the user.

 7 */

 8public function update(User $user, Post $post): Response

 9{

10    return $user->id === $post->user_id

11        ? Response::allow()

12        : Response::denyWithStatus(404);

13}
```

Because hiding resources via a `404` response is such a common pattern for web applications, the `denyAsNotFound` method is offered for convenience:

```
 1use App\Models\Post;

 2use App\Models\User;

 3use Illuminate\Auth\Access\Response;

 4 

 5/**

 6 * Determine if the given post can be updated by the user.

 7 */

 8public function update(User $user, Post $post): Response

 9{

10    return $user->id === $post->user_id

11        ? Response::allow()

12        : Response::denyAsNotFound();

13}
```

### [Methods Without Models](#methods-without-models)

Some policy methods only receive an instance of the currently authenticated user. This situation is most common when authorizing `create` actions. For example, if you are creating a blog, you may wish to determine if a user is authorized to create any posts at all. In these situations, your policy method should only expect to receive a user instance:

```
1/**

2 * Determine if the given user can create posts.

3 */

4public function create(User $user): bool

5{

6    return $user->role == 'writer';

7}
```

### [Guest Users](#guest-users)

By default, all gates and policies automatically return `false` if the incoming HTTP request was not initiated by an authenticated user. However, you may allow these authorization checks to pass through to your gates and policies by declaring an "optional" type-hint or supplying a `null` default value for the user argument definition:

```
 1<?php

 2 

 3namespace App\Policies;

 4 

 5use App\Models\Post;

 6use App\Models\User;

 7 

 8class PostPolicy

 9{

10    /**

11     * Determine if the given post can be updated by the user.

12     */

13    public function update(?User $user, Post $post): bool

14    {

15        return $user?->id === $post->user_id;

16    }

17}
```

### [Policy Filters](#policy-filters)

For certain users, you may wish to authorize all actions within a given policy. To accomplish this, define a `before` method on the policy. The `before` method will be executed before any other methods on the policy, giving you an opportunity to authorize the action before the intended policy method is actually called. This feature is most commonly used for authorizing application administrators to perform any action:

```
 1use App\Models\User;

 2 

 3/**

 4 * Perform pre-authorization checks.

 5 */

 6public function before(User $user, string $ability): bool|null

 7{

 8    if ($user->isAdministrator()) {

 9        return true;

10    }

11 

12    return null;

13}
```

If you would like to deny all authorization checks for a particular type of user then you may return `false` from the `before` method. If `null` is returned, the authorization check will fall through to the policy method.

The `before` method of a policy class will not be called if the class doesn't contain a method with a name matching the name of the ability being checked.

## [Authorizing Actions Using Policies](#authorizing-actions-using-policies)

### [Via the User Model](#via-the-user-model)

The `App\Models\User` model that is included with your Laravel application includes two helpful methods for authorizing actions: `can` and `cannot`. The `can` and `cannot` methods receive the name of the action you wish to authorize and the relevant model. For example, let's determine if a user is authorized to update a given `App\Models\Post` model. Typically, this will be done within a controller method:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Models\Post;

 6use Illuminate\Http\RedirectResponse;

 7use Illuminate\Http\Request;

 8 

 9class PostController extends Controller

10{

11    /**

12     * Update the given post.

13     */

14    public function update(Request $request, Post $post): RedirectResponse

15    {

16        if ($request->user()->cannot('update', $post)) {

17            abort(403);

18        }

19 

20        // Update the post...

21 

22        return redirect('/posts');

23    }

24}
```

If a [policy is registered](#registering-policies) for the given model, the `can` method will automatically call the appropriate policy and return the boolean result. If no policy is registered for the model, the `can` method will attempt to call the closure-based Gate matching the given action name.

#### [Actions That Don't Require Models](#user-model-actions-that-dont-require-models)

Remember, some actions may correspond to policy methods like `create` that do not require a model instance. In these situations, you may pass a class name to the `can` method. The class name will be used to determine which policy to use when authorizing the action:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Models\Post;

 6use Illuminate\Http\RedirectResponse;

 7use Illuminate\Http\Request;

 8 

 9class PostController extends Controller

10{

11    /**

12     * Create a post.

13     */

14    public function store(Request $request): RedirectResponse

15    {

16        if ($request->user()->cannot('create', Post::class)) {

17            abort(403);

18        }

19 

20        // Create the post...

21 

22        return redirect('/posts');

23    }

24}
```

### [Via the `Gate` Facade](#via-the-gate-facade)

In addition to helpful methods provided to the `App\Models\User` model, you can always authorize actions via the `Gate` facade's `authorize` method.

Like the `can` method, this method accepts the name of the action you wish to authorize and the relevant model. If the action is not authorized, the `authorize` method will throw an `Illuminate\Auth\Access\AuthorizationException` exception which the Laravel exception handler will automatically convert to an HTTP response with a 403 status code:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Models\Post;

 6use Illuminate\Http\RedirectResponse;

 7use Illuminate\Http\Request;

 8use Illuminate\Support\Facades\Gate;

 9 

10class PostController extends Controller

11{

12    /**

13     * Update the given blog post.

14     *

15     * @throws \Illuminate\Auth\Access\AuthorizationException

16     */

17    public function update(Request $request, Post $post): RedirectResponse

18    {

19        Gate::authorize('update', $post);

20 

21        // The current user can update the blog post...

22 

23        return redirect('/posts');

24    }

25}
```

#### [Actions That Don't Require Models](#controller-actions-that-dont-require-models)

As previously discussed, some policy methods like `create` do not require a model instance. In these situations, you should pass a class name to the `authorize` method. The class name will be used to determine which policy to use when authorizing the action:

```
 1use App\Models\Post;

 2use Illuminate\Http\RedirectResponse;

 3use Illuminate\Http\Request;

 4use Illuminate\Support\Facades\Gate;

 5 

 6/**

 7 * Create a new blog post.

 8 *

 9 * @throws \Illuminate\Auth\Access\AuthorizationException

10 */

11public function create(Request $request): RedirectResponse

12{

13    Gate::authorize('create', Post::class);

14 

15    // The current user can create blog posts...

16 

17    return redirect('/posts');

18}
```

### [Via Middleware](#via-middleware)

Laravel includes a middleware that can authorize actions before the incoming request even reaches your routes or controllers. By default, the `Illuminate\Auth\Middleware\Authorize` middleware may be attached to a route using the `can` [middleware alias](/docs/13.x/middleware#middleware-aliases), which is automatically registered by Laravel. Let's explore an example of using the `can` middleware to authorize that a user can update a post:

```
1use App\Models\Post;

2 

3Route::put('/post/{post}', function (Post $post) {

4    // The current user may update the post...

5})->middleware('can:update,post');
```

In this example, we're passing the `can` middleware two arguments. The first is the name of the action we wish to authorize and the second is the route parameter we wish to pass to the policy method. In this case, since we are using [implicit model binding](/docs/13.x/routing#implicit-binding), an `App\Models\Post` model will be passed to the policy method. If the user is not authorized to perform the given action, an HTTP response with a 403 status code will be returned by the middleware.

For convenience, you may also attach the `can` middleware to your route using the `can` method:

```
1use App\Models\Post;

2 

3Route::put('/post/{post}', function (Post $post) {

4    // The current user may update the post...

5})->can('update', 'post');
```

If you are using [controller middleware attributes](/docs/13.x/controllers#middleware-attributes), you may apply the `can` middleware via the `Authorize` attribute:

```
1use Illuminate\Routing\Attributes\Controllers\Authorize;

2 

3#[Authorize('update', 'post')]

4public function update(Post $post)

5{

6    // The current user may update the post...

7}
```

#### [Actions That Don't Require Models](#middleware-actions-that-dont-require-models)

Again, some policy methods like `create` do not require a model instance. In these situations, you may pass a class name to the middleware. The class name will be used to determine which policy to use when authorizing the action:

```
1Route::post('/post', function () {

2    // The current user may create posts...

3})->middleware('can:create,App\Models\Post');
```

Specifying the entire class name within a string middleware definition can become cumbersome. For that reason, you may choose to attach the `can` middleware to your route using the `can` method:

```
1use App\Models\Post;

2 

3Route::post('/post', function () {

4    // The current user may create posts...

5})->can('create', Post::class);
```

### [Via Blade Templates](#via-blade-templates)

When writing Blade templates, you may wish to display a portion of the page only if the user is authorized to perform a given action. For example, you may wish to show an update form for a blog post only if the user can actually update the post. In this situation, you may use the `@can` and `@cannot` directives:

```
 1@can('update', $post)

 2    <!-- The current user can update the post... -->

 3@elsecan('create', App\Models\Post::class)

 4    <!-- The current user can create new posts... -->

 5@else

 6    <!-- ... -->

 7@endcan

 8 

 9@cannot('update', $post)

10    <!-- The current user cannot update the post... -->

11@elsecannot('create', App\Models\Post::class)

12    <!-- The current user cannot create new posts... -->

13@endcannot
```

These directives are convenient shortcuts for writing `@if` and `@unless` statements. The `@can` and `@cannot` statements above are equivalent to the following statements:

```
1@if (Auth::user()->can('update', $post))

2    <!-- The current user can update the post... -->

3@endif

4 

5@unless (Auth::user()->can('update', $post))

6    <!-- The current user cannot update the post... -->

7@endunless
```

You may also determine if a user is authorized to perform any action from a given array of actions. To accomplish this, use the `@canany` directive:

```
1@canany(['update', 'view', 'delete'], $post)

2    <!-- The current user can update, view, or delete the post... -->

3@elsecanany(['create'], \App\Models\Post::class)

4    <!-- The current user can create a post... -->

5@endcanany
```

#### [Actions That Don't Require Models](#blade-actions-that-dont-require-models)

Like most of the other authorization methods, you may pass a class name to the `@can` and `@cannot` directives if the action does not require a model instance:

```
1@can('create', App\Models\Post::class)

2    <!-- The current user can create posts... -->

3@endcan

4 

5@cannot('create', App\Models\Post::class)

6    <!-- The current user can't create posts... -->

7@endcannot
```

### [Supplying Additional Context](#supplying-additional-context)

When authorizing actions using policies, you may pass an array as the second argument to the various authorization functions and helpers. The first element in the array will be used to determine which policy should be invoked, while the rest of the array elements are passed as parameters to the policy method and can be used for additional context when making authorization decisions. For example, consider the following `PostPolicy` method definition which contains an additional `$category` parameter:

```
1/**

2 * Determine if the given post can be updated by the user.

3 */

4public function update(User $user, Post $post, int $category): bool

5{

6    return $user->id === $post->user_id &&

7           $user->canUpdateCategory($category);

8}
```

When attempting to determine if the authenticated user can update a given post, we can invoke this policy method like so:

```
 1/**

 2 * Update the given blog post.

 3 *

 4 * @throws \Illuminate\Auth\Access\AuthorizationException

 5 */

 6public function update(Request $request, Post $post): RedirectResponse

 7{

 8    Gate::authorize('update', [$post, $request->category]);

 9 

10    // The current user can update the blog post...

11 

12    return redirect('/posts');

13}
```

## [Authorization & Inertia](#authorization-and-inertia)

Although authorization must always be handled on the server, it can often be convenient to provide your frontend application with authorization data in order to properly render your application's UI. Laravel does not define a required convention for exposing authorization information to an Inertia powered frontend.

However, if you are using one of Laravel's Inertia-based [starter kits](/docs/13.x/starter-kits), your application already contains a `HandleInertiaRequests` middleware. Within this middleware's `share` method, you may return shared data that will be provided to all Inertia pages in your application. This shared data can serve as a convenient location to define authorization information for the user:

```
 1<?php

 2 

 3namespace App\Http\Middleware;

 4 

 5use App\Models\Post;

 6use Illuminate\Http\Request;

 7use Inertia\Middleware;

 8 

 9class HandleInertiaRequests extends Middleware

10{

11    // ...

12 

13    /**

14     * Define the props that are shared by default.

15     *

16     * @return array<string, mixed>

17     */

18    public function share(Request $request)

19    {

20        return [

21            ...parent::share($request),

22            'auth' => [

23                'user' => $request->user(),

24                'permissions' => [

25                    'post' => [

26                        'create' => $request->user()->can('create', Post::class),

27                    ],

28                ],

29            ],

30        ];

31    }

32}
```
