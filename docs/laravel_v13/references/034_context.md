# Context

- [Introduction](#introduction)
  * [How it Works](#how-it-works)
- [Capturing Context](#capturing-context)
  * [Stacks](#stacks)
- [Retrieving Context](#retrieving-context)
  * [Determining Item Existence](#determining-item-existence)
- [Removing Context](#removing-context)
- [Hidden Context](#hidden-context)
- [Events](#events)
  * [Dehydrating](#dehydrating)
  * [Hydrated](#hydrated)

## [Introduction](#introduction)

Laravel's "context" capabilities enable you to capture, retrieve, and share information throughout requests, jobs, and commands executing within your application. This captured information is also included in logs written by your application, giving you deeper insight into the surrounding code execution history that occurred before a log entry was written and allowing you to trace execution flows throughout a distributed system.

### [How it Works](#how-it-works)

The best way to understand Laravel's context capabilities is to see it in action using the built-in logging features. To get started, you may [add information to the context](#capturing-context) using the `Context` facade. In this example, we will use a [middleware](/docs/13.x/middleware) to add the request URL and a unique trace ID to the context on every incoming request:

```
 1<?php

 2 

 3namespace App\Http\Middleware;

 4 

 5use Closure;

 6use Illuminate\Http\Request;

 7use Illuminate\Support\Facades\Context;

 8use Illuminate\Support\Str;

 9use Symfony\Component\HttpFoundation\Response;

10 

11class AddContext

12{

13    /**

14     * Handle an incoming request.

15     */

16    public function handle(Request $request, Closure $next): Response

17    {

18        Context::add('url', $request->url());

19        Context::add('trace_id', Str::uuid()->toString());

20 

21        return $next($request);

22    }

23}
```

Information added to the context is automatically appended as metadata to any [log entries](/docs/13.x/logging) that are written throughout the request. Appending context as metadata allows information passed to individual log entries to be differentiated from the information shared via `Context`. For example, imagine we write the following log entry:

```
1Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

The written log will contain the `auth_id` passed to the log entry, but it will also contain the context's `url` and `trace_id` as metadata:

```
1User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Information added to the context is also made available to jobs dispatched to the queue. For example, imagine we dispatch a `ProcessPodcast` job to the queue after adding some information to the context:

```
1// In our middleware...

2Context::add('url', $request->url());

3Context::add('trace_id', Str::uuid()->toString());

4 

5// In our controller...

6ProcessPodcast::dispatch($podcast);
```

When the job is dispatched, any information currently stored in the context is captured and shared with the job. The captured information is then hydrated back into the current context while the job is executing. So, if our job's handle method was to write to the log:

```
 1class ProcessPodcast implements ShouldQueue

 2{

 3    use Queueable;

 4 

 5    // ...

 6 

 7    /**

 8     * Execute the job.

 9     */

10    public function handle(): void

11    {

12        Log::info('Processing podcast.', [

13            'podcast_id' => $this->podcast->id,

14        ]);

15 

16        // ...

17    }

18}
```

The resulting log entry would contain the information that was added to the context during the request that originally dispatched the job:

```
1Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Although we have focused on the built-in logging related features of Laravel's context, the following documentation will illustrate how context allows you to share information across the HTTP request / queued job boundary and even how to add [hidden context data](#hidden-context) that is not written with log entries.

## [Capturing Context](#capturing-context)

You may store information in the current context using the `Context` facade's `add` method:

```
1use Illuminate\Support\Facades\Context;

2 

3Context::add('key', 'value');
```

To add multiple items at once, you may pass an associative array to the `add` method:

```
1Context::add([

2    'first_key' => 'value',

3    'second_key' => 'value',

4]);
```

The `add` method will override any existing value that shares the same key. If you only wish to add information to the context if the key does not already exist, you may use the `addIf` method:

```
1Context::add('key', 'first');

2 

3Context::get('key');

4// "first"

5 

6Context::addIf('key', 'second');

7 

8Context::get('key');

9// "first"
```

Context also provides convenient methods for incrementing or decrementing a given key. Both of these methods accept at least one argument: the key to track. A second argument may be provided to specify the amount by which the key should be incremented or decremented:

```
1Context::increment('records_added');

2Context::increment('records_added', 5);

3 

4Context::decrement('records_added');

5Context::decrement('records_added', 5);
```

#### [Conditional Context](#conditional-context)

The `when` method may be used to add data to the context based on a given condition. The first closure provided to the `when` method will be invoked if the given condition evaluates to `true`, while the second closure will be invoked if the condition evaluates to `false`:

```
1use Illuminate\Support\Facades\Auth;

2use Illuminate\Support\Facades\Context;

3 

4Context::when(

5    Auth::user()->isAdmin(),

6    fn ($context) => $context->add('permissions', Auth::user()->permissions),

7    fn ($context) => $context->add('permissions', []),

8);
```

#### [Scoped Context](#scoped-context)

The `scope` method provides a way to temporarily modify the context during the execution of a given callback and restore the context to its original state when the callback finishes executing. Additionally, you can pass extra data that should be merged into the context (as the second and third arguments) while the closure executes.

```
 1use Illuminate\Support\Facades\Context;

 2use Illuminate\Support\Facades\Log;

 3 

 4Context::add('trace_id', 'abc-999');

 5Context::addHidden('user_id', 123);

 6 

 7Context::scope(

 8    function () {

 9        Context::add('action', 'adding_friend');

10 

11        $userId = Context::getHidden('user_id');

12 

13        Log::debug("Adding user [{$userId}] to friends list.");

14        // Adding user [987] to friends list.  {"trace_id":"abc-999","user_name":"taylor_otwell","action":"adding_friend"}

15    },

16    data: ['user_name' => 'taylor_otwell'],

17    hidden: ['user_id' => 987],

18);

19 

20Context::all();

21// [

22//     'trace_id' => 'abc-999',

23// ]

24 

25Context::allHidden();

26// [

27//     'user_id' => 123,

28// ]
```

If an object within the context is modified inside the scoped closure, that mutation will be reflected outside of the scope.

### [Stacks](#stacks)

Context offers the ability to create "stacks", which are lists of data stored in the order that they were added. You can add information to a stack by invoking the `push` method:

```
 1use Illuminate\Support\Facades\Context;

 2 

 3Context::push('breadcrumbs', 'first_value');

 4 

 5Context::push('breadcrumbs', 'second_value', 'third_value');

 6 

 7Context::get('breadcrumbs');

 8// [

 9//     'first_value',

10//     'second_value',

11//     'third_value',

12// ]
```

Stacks can be useful to capture historical information about a request, such as events that are happening throughout your application. For example, you could create an event listener to push to a stack every time a query is executed, capturing the query SQL and duration as a tuple:

```
1use Illuminate\Support\Facades\Context;

2use Illuminate\Support\Facades\DB;

3 

4// In AppServiceProvider.php...

5DB::listen(function ($event) {

6    Context::push('queries', [$event->time, $event->sql]);

7});
```

You may determine if a value is in a stack using the `stackContains` and `hiddenStackContains` methods:

```
1if (Context::stackContains('breadcrumbs', 'first_value')) {

2    //

3}

4 

5if (Context::hiddenStackContains('secrets', 'first_value')) {

6    //

7}
```

The `stackContains` and `hiddenStackContains` methods also accept a closure as their second argument, allowing more control over the value comparison operation:

```
1use Illuminate\Support\Facades\Context;

2use Illuminate\Support\Str;

3 

4return Context::stackContains('breadcrumbs', function ($value) {

5    return Str::startsWith($value, 'query_');

6});
```

## [Retrieving Context](#retrieving-context)

You may retrieve information from the context using the `Context` facade's `get` method:

```
1use Illuminate\Support\Facades\Context;

2 

3$value = Context::get('key');
```

The `only` and `except` methods may be used to retrieve a subset of the information in the context:

```
1$data = Context::only(['first_key', 'second_key']);

2 

3$data = Context::except(['first_key']);
```

The `pull` method may be used to retrieve information from the context and immediately remove it from the context:

```
1$value = Context::pull('key');
```

If context data is stored in a [stack](#stacks), you may pop items from the stack using the `pop` method:

```
1Context::push('breadcrumbs', 'first_value', 'second_value');

2 

3Context::pop('breadcrumbs');

4// second_value

5 

6Context::get('breadcrumbs');

7// ['first_value']
```

The `remember` and `rememberHidden` methods may be used to retrieve information from the context, while setting the context value to the value returned by the given closure if the requested information doesn't exist:

```
1$permissions = Context::remember(

2    'user-permissions',

3    fn () => $user->permissions,

4);
```

If you would like to retrieve all of the information stored in the context, you may invoke the `all` method:

```
1$data = Context::all();
```

### [Determining Item Existence](#determining-item-existence)

You may use the `has` and `missing` methods to determine if the context has any value stored for the given key:

```
1use Illuminate\Support\Facades\Context;

2 

3if (Context::has('key')) {

4    // ...

5}

6 

7if (Context::missing('key')) {

8    // ...

9}
```

The `has` method will return `true` regardless of the value stored. So, for example, a key with a `null` value will be considered present:

```
1Context::add('key', null);

2 

3Context::has('key');

4// true
```

## [Removing Context](#removing-context)

The `forget` method may be used to remove a key and its value from the current context:

```
1use Illuminate\Support\Facades\Context;

2 

3Context::add(['first_key' => 1, 'second_key' => 2]);

4 

5Context::forget('first_key');

6 

7Context::all();

8 

9// ['second_key' => 2]
```

You may forget several keys at once by providing an array to the `forget` method:

```
1Context::forget(['first_key', 'second_key']);
```

## [Hidden Context](#hidden-context)

Context offers the ability to store "hidden" data. This hidden information is not appended to logs, and is not accessible via the data retrieval methods documented above. Context provides a different set of methods to interact with hidden context information:

```
1use Illuminate\Support\Facades\Context;

2 

3Context::addHidden('key', 'value');

4 

5Context::getHidden('key');

6// 'value'

7 

8Context::get('key');

9// null
```

The "hidden" methods mirror the functionality of the non-hidden methods documented above:

```
 1Context::addHidden(/* ... */);

 2Context::addHiddenIf(/* ... */);

 3Context::pushHidden(/* ... */);

 4Context::getHidden(/* ... */);

 5Context::pullHidden(/* ... */);

 6Context::popHidden(/* ... */);

 7Context::onlyHidden(/* ... */);

 8Context::exceptHidden(/* ... */);

 9Context::allHidden(/* ... */);

10Context::hasHidden(/* ... */);

11Context::missingHidden(/* ... */);

12Context::forgetHidden(/* ... */);
```

## [Events](#events)

Context dispatches two events that allow you to hook into the hydration and dehydration process of the context.

To illustrate how these events may be used, imagine that in a middleware of your application you set the `app.locale` configuration value based on the incoming HTTP request's `Accept-Language` header. Context's events allow you to capture this value during the request and restore it on the queue, ensuring notifications sent on the queue have the correct `app.locale` value. We can use context's events and [hidden](#hidden-context) data to achieve this, which the following documentation will illustrate.

### [Dehydrating](#dehydrating)

Whenever a job is dispatched to the queue the data in the context is "dehydrated" and captured alongside the job's payload. The `Context::dehydrating` method allows you to register a closure that will be invoked during the dehydration process. Within this closure, you may make changes to the data that will be shared with the queued job.

Typically, you should register `dehydrating` callbacks within the `boot` method of your application's `AppServiceProvider` class:

```
 1use Illuminate\Log\Context\Repository;

 2use Illuminate\Support\Facades\Config;

 3use Illuminate\Support\Facades\Context;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Context::dehydrating(function (Repository $context) {

11        $context->addHidden('locale', Config::get('app.locale'));

12    });

13}
```

You should not use the `Context` facade within the `dehydrating` callback, as that will change the context of the current process. Ensure you only make changes to the repository passed to the callback.

### [Hydrated](#hydrated)

Whenever a queued job begins executing on the queue, any context that was shared with the job will be "hydrated" back into the current context. The `Context::hydrated` method allows you to register a closure that will be invoked during the hydration process.

Typically, you should register `hydrated` callbacks within the `boot` method of your application's `AppServiceProvider` class:

```
 1use Illuminate\Log\Context\Repository;

 2use Illuminate\Support\Facades\Config;

 3use Illuminate\Support\Facades\Context;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Context::hydrated(function (Repository $context) {

11        if ($context->hasHidden('locale')) {

12            Config::set('app.locale', $context->getHidden('locale'));

13        }

14    });

15}
```

You should not use the `Context` facade within the `hydrated` callback and instead ensure you only make changes to the repository passed to the callback.
