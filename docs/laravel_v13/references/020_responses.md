# HTTP Responses

- [Creating Responses](#creating-responses)
  * [Attaching Headers to Responses](#attaching-headers-to-responses)
  * [Attaching Cookies to Responses](#attaching-cookies-to-responses)
  * [Cookies and Encryption](#cookies-and-encryption)
- [Redirects](#redirects)
  * [Redirecting to Named Routes](#redirecting-named-routes)
  * [Redirecting to Controller Actions](#redirecting-controller-actions)
  * [Redirecting to External Domains](#redirecting-external-domains)
  * [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)
- [Other Response Types](#other-response-types)
  * [View Responses](#view-responses)
  * [JSON Responses](#json-responses)
  * [File Downloads](#file-downloads)
  * [File Responses](#file-responses)
- [Streamed Responses](#streamed-responses)
  * [Consuming Streamed Responses](#consuming-streamed-responses)
  * [Streamed JSON Responses](#streamed-json-responses)
  * [Event Streams (SSE)](#event-streams)
  * [Streamed Downloads](#streamed-downloads)
- [Response Macros](#response-macros)

## [Creating Responses](#creating-responses)

#### [Strings and Arrays](#strings-arrays)

All routes and controllers should return a response to be sent back to the user's browser. Laravel provides several different ways to return responses. The most basic response is returning a string from a route or controller. The framework will automatically convert the string into a full HTTP response:

```
1Route::get('/', function () {

2    return 'Hello World';

3});
```

In addition to returning strings from your routes and controllers, you may also return arrays. The framework will automatically convert the array into a JSON response:

```
1Route::get('/', function () {

2    return [1, 2, 3];

3});
```

Did you know you can also return [Eloquent collections](/docs/13.x/eloquent-collections) from your routes or controllers? They will automatically be converted to JSON. Give it a shot!

#### [Response Objects](#response-objects)

Typically, you won't just be returning simple strings or arrays from your route actions. Instead, you will be returning full `Illuminate\Http\Response` instances or [views](/docs/13.x/views).

Returning a full `Response` instance allows you to customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, which provides a variety of methods for building HTTP responses:

```
1Route::get('/home', function () {

2    return response('Hello World', 200)

3        ->header('Content-Type', 'text/plain');

4});
```

#### [Eloquent Models and Collections](#eloquent-models-and-collections)

You may also return [Eloquent ORM](/docs/13.x/eloquent) models and collections directly from your routes and controllers. When you do, Laravel will automatically convert the models and collections to JSON responses while respecting the model's [hidden attributes](/docs/13.x/eloquent-serialization#hiding-attributes-from-json):

```
1use App\Models\User;

2 

3Route::get('/user/{user}', function (User $user) {

4    return $user;

5});
```

### [Attaching Headers to Responses](#attaching-headers-to-responses)

Keep in mind that most response methods are chainable, allowing for the fluent construction of response instances. For example, you may use the `header` method to add a series of headers to the response before sending it back to the user:

```
1return response($content)

2    ->header('Content-Type', $type)

3    ->header('X-Header-One', 'Header Value')

4    ->header('X-Header-Two', 'Header Value');
```

Or, you may use the `withHeaders` method to specify an array of headers to be added to the response:

```
1return response($content)

2    ->withHeaders([

3        'Content-Type' => $type,

4        'X-Header-One' => 'Header Value',

5        'X-Header-Two' => 'Header Value',

6    ]);
```

You can remove specific headers from an outgoing response using the `withoutHeader` method:

```
1return response($content)->withoutHeader('X-Debug');

2 

3return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

#### [Cache Control Middleware](#cache-control-middleware)

Laravel includes a `cache.headers` middleware, which may be used to quickly set the `Cache-Control` header for a group of routes. Directives should be provided using the "snake case" equivalent of the corresponding cache-control directive and should be separated by a semicolon. If `etag` is specified in the list of directives, an MD5 hash of the response content will automatically be set as the ETag identifier:

```
1Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () {

2    Route::get('/privacy', function () {

3        // ...

4    });

5 

6    Route::get('/terms', function () {

7        // ...

8    });

9});
```

### [Attaching Cookies to Responses](#attaching-cookies-to-responses)

You may attach a cookie to an outgoing `Illuminate\Http\Response` instance using the `cookie` method. You should pass the name, value, and the number of minutes the cookie should be considered valid to this method:

```
1return response('Hello World')->cookie(

2    'name', 'value', $minutes

3);
```

The `cookie` method also accepts a few more arguments which are used less frequently. Generally, these arguments have the same purpose and meaning as the arguments that would be given to PHP's native [setcookie](https://secure.php.net/manual/en/function.setcookie.php) method:

```
1return response('Hello World')->cookie(

2    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly

3);
```

If you would like to ensure that a cookie is sent with the outgoing response but you do not yet have an instance of that response, you can use the `Cookie` facade to "queue" cookies for attachment to the response when it is sent. The `queue` method accepts the arguments needed to create a cookie instance. These cookies will be attached to the outgoing response before it is sent to the browser:

```
1use Illuminate\Support\Facades\Cookie;

2 

3Cookie::queue('name', 'value', $minutes);
```

#### [Generating Cookie Instances](#generating-cookie-instances)

If you would like to generate a `Symfony\Component\HttpFoundation\Cookie` instance that can be attached to a response instance at a later time, you may use the global `cookie` helper. This cookie will not be sent back to the client unless it is attached to a response instance:

```
1$cookie = cookie('name', 'value', $minutes);

2 

3return response('Hello World')->cookie($cookie);
```

#### [Expiring Cookies Early](#expiring-cookies-early)

You may remove a cookie by expiring it via the `withoutCookie` method of an outgoing response:

```
1return response('Hello World')->withoutCookie('name');
```

If you do not yet have an instance of the outgoing response, you may use the `Cookie` facade's `expire` method to expire a cookie:

```
1Cookie::expire('name');
```

### [Cookies and Encryption](#cookies-and-encryption)

By default, thanks to the `Illuminate\Cookie\Middleware\EncryptCookies` middleware, all cookies generated by Laravel are encrypted and signed so that they can't be modified or read by the client. If you would like to disable encryption for a subset of cookies generated by your application, you may use the `encryptCookies` method in your application's `bootstrap/app.php` file:

```
1->withMiddleware(function (Middleware $middleware): void {

2    $middleware->encryptCookies(except: [

3        'cookie_name',

4    ]);

5})
```

In general, cookie encryption should never be disabled, as this exposes your cookies to potential client-side data exposure and tampering.

## [Redirects](#redirects)

Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper:

```
1Route::get('/dashboard', function () {

2    return redirect('/home/dashboard');

3});
```

Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/13.x/session), make sure the route calling the `back` function is using the `web` middleware group:

```
1Route::post('/user/profile', function () {

2    // Validate the request...

3 

4    return back()->withInput();

5});
```

### [Redirecting to Named Routes](#redirecting-named-routes)

When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method:

```
1return redirect()->route('login');
```

If your route has parameters, you may pass them as the second argument to the `route` method:

```
1// For a route with the following URI: /profile/{id}

2 

3return redirect()->route('profile', ['id' => 1]);
```

#### [Populating Parameters via Eloquent Models](#populating-parameters-via-eloquent-models)

If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically:

```
1// For a route with the following URI: /profile/{id}

2 

3return redirect()->route('profile', [$user]);
```

If you would like to customize the value that is placed in the route parameter, you can specify the column in the route parameter definition (`/profile/{id:slug}`) or you can override the `getRouteKey` method on your Eloquent model:

```
1/**

2 * Get the value of the model's route key.

3 */

4public function getRouteKey(): mixed

5{

6    return $this->slug;

7}
```

### [Redirecting to Controller Actions](#redirecting-controller-actions)

You may also generate redirects to [controller actions](/docs/13.x/controllers). To do so, pass the controller and action name to the `action` method:

```
1use App\Http\Controllers\UserController;

2 

3return redirect()->action([UserController::class, 'index']);
```

If your controller route requires parameters, you may pass them as the second argument to the `action` method:

```
1return redirect()->action(

2    [UserController::class, 'profile'], ['id' => 1]

3);
```

### [Redirecting to External Domains](#redirecting-external-domains)

Sometimes you may need to redirect to a domain outside of your application. You may do so by calling the `away` method, which creates a `RedirectResponse` without any additional URL encoding, validation, or verification:

```
1return redirect()->away('https://www.google.com');
```

### [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)

Redirecting to a new URL and [flashing data to the session](/docs/13.x/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain:

```
1Route::post('/user/profile', function () {

2    // ...

3 

4    return redirect('/dashboard')->with('status', 'Profile updated!');

5});
```

After the user is redirected, you may display the flashed message from the [session](/docs/13.x/session). For example, using [Blade syntax](/docs/13.x/blade):

```
1@if (session('status'))

2    <div class="alert alert-success">

3        {{ session('status') }}

4    </div>

5@endif
```

#### [Redirecting With Input](#redirecting-with-input)

You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/13.x/requests#retrieving-old-input) during the next request to repopulate the form:

```
1return back()->withInput();
```

## [Other Response Types](#other-response-types)

The `response` helper may be used to generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/13.x/contracts) is returned. This contract provides several helpful methods for generating responses.

### [View Responses](#view-responses)

If you need control over the response's status and headers but also need to return a [view](/docs/13.x/views) as the response's content, you should use the `view` method:

```
1return response()

2    ->view('hello', $data, 200)

3    ->header('Content-Type', $type);
```

Of course, if you do not need to pass a custom HTTP status code or custom headers, you may use the global `view` helper function.

### [JSON Responses](#json-responses)

The `json` method will automatically set the `Content-Type` header to `application/json`, as well as convert the given array to JSON using the `json_encode` PHP function:

```
1return response()->json([

2    'name' => 'Abigail',

3    'state' => 'CA',

4]);
```

If you would like to create a JSONP response, you may use the `json` method in combination with the `withCallback` method:

```
1return response()

2    ->json(['name' => 'Abigail', 'state' => 'CA'])

3    ->withCallback($request->input('callback'));
```

### [File Downloads](#file-downloads)

The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method:

```
1return response()->download($pathToFile);

2 

3return response()->download($pathToFile, $name, $headers);
```

Symfony HttpFoundation, which manages file downloads, requires the file being downloaded to have an ASCII filename.

### [File Responses](#file-responses)

The `file` method may be used to display a file, such as an image or PDF, directly in the user's browser instead of initiating a download. This method accepts the absolute path to the file as its first argument and an array of headers as its second argument:

```
1return response()->file($pathToFile);

2 

3return response()->file($pathToFile, $headers);
```

## [Streamed Responses](#streamed-responses)

By streaming data to the client as it is generated, you can significantly reduce memory usage and improve performance, especially for very large responses. Streamed responses allow the client to begin processing data before the server has finished sending it:

```
 1Route::get('/stream', function () {

 2    return response()->stream(function (): void {

 3        foreach (['developer', 'admin'] as $string) {

 4            echo $string;

 5            ob_flush();

 6            flush();

 7            sleep(2); // Simulate delay between chunks...

 8        }

 9    }, 200, ['X-Accel-Buffering' => 'no']);

10});
```

For convenience, if the closure you provide to the `stream` method returns a [Generator](https://www.php.net/manual/en/language.generators.overview.php), Laravel will automatically flush the output buffer between strings returned by the generator, as well as disable Nginx output buffering:

```
1Route::post('/chat', function () {

2    return response()->stream(function (): Generator {

3        $stream = OpenAI::client()->chat()->createStreamed(...);

4 

5        foreach ($stream as $response) {

6            yield $response->choices[0];

7        }

8    });

9});
```

### [Consuming Streamed Responses](#consuming-streamed-responses)

Streamed responses may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel response and event streams. To get started, install the `@laravel/stream-react`, `@laravel/stream-vue`, or `@laravel/stream-svelte` package:

React

Vue

Svelte

```
1npm install @laravel/stream-react
```

```
1npm install @laravel/stream-vue
```

```
1npm install @laravel/stream-svelte
```

Then, `useStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `data` with the concatenated response as content is returned from your Laravel application:

React

Vue

Svelte

```
 1import { useStream } from "@laravel/stream-react";

 2 

 3function App() {

 4    const { data, isFetching, isStreaming, send } = useStream("chat");

 5 

 6    const sendMessage = () => {

 7        send({

 8            message: `Current timestamp: ${Date.now()}`,

 9        });

10    };

11 

12    return (

13        <div>

14            <div>{data}</div>

15            {isFetching && <div>Connecting...</div>}

16            {isStreaming && <div>Generating...</div>}

17            <button onClick={sendMessage}>Send Message</button>

18        </div>

19    );

20}
```

```
 1<script setup lang="ts">

 2import { useStream } from "@laravel/stream-vue";

 3 

 4const { data, isFetching, isStreaming, send } = useStream("chat");

 5 

 6const sendMessage = () => {

 7    send({

 8        message: `Current timestamp: ${Date.now()}`,

 9    });

10};

11</script>

12 

13<template>

14    <div>

15        <div>{{ data }}</div>

16        <div v-if="isFetching">Connecting...</div>

17        <div v-if="isStreaming">Generating...</div>

18        <button @click="sendMessage">Send Message</button>

19    </div>

20</template>
```

```
<script>

import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");

const sendMessage = () => {

    stream.send({

        message: `Current timestamp: ${Date.now()}`,

    });

};

</script>

<div>

    <div>{$stream.data}</div>

    {#if $stream.isFetching}

        <div>Connecting...</div>

    {/if}

    {#if $stream.isStreaming}

        <div>Generating...</div>

    {/if}

    <button onclick={sendMessage}>Send Message</button>

</div>
```

When sending data back to the stream via `send`, the active connection to the stream is canceled before sending the new data. All requests are sent as JSON `POST` requests.

Since the `useStream` hook makes a `POST` request to your application, a valid CSRF token is required. The easiest way to provide the CSRF token is to [include it via a meta tag in your application layout's head](/docs/13.x/csrf#csrf-x-csrf-token).

The second argument given to `useStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below:

React

Vue

Svelte

```
 1import { useStream } from "@laravel/stream-react";

 2 

 3function App() {

 4    const { data } = useStream("chat", {

 5        id: undefined,

 6        initialInput: undefined,

 7        headers: undefined,

 8        csrfToken: undefined,

 9        onResponse: (response: Response) => void,

10        onData: (data: string) => void,

11        onCancel: () => void,

12        onFinish: () => void,

13        onError: (error: Error) => void,

14    });

15 

16    return <div>{data}</div>;

17}
```

```
 1<script setup lang="ts">

 2import { useStream } from "@laravel/stream-vue";

 3 

 4const { data } = useStream("chat", {

 5    id: undefined,

 6    initialInput: undefined,

 7    headers: undefined,

 8    csrfToken: undefined,

 9    onResponse: (response: Response) => void,

10    onData: (data: string) => void,

11    onCancel: () => void,

12    onFinish: () => void,

13    onError: (error: Error) => void,

14});

15</script>

16 

17<template>

18    <div>{{ data }}</div>

19</template>
```

```
 1<script>

 2import { useStream } from "@laravel/stream-svelte";

 3 

 4const stream = useStream("chat", {

 5    id: undefined,

 6    initialInput: undefined,

 7    headers: undefined,

 8    csrfToken: undefined,

 9    onResponse: (response) => {},

10    onData: (data) => {},

11    onCancel: () => {},

12    onFinish: () => {},

13    onError: (error) => {},

14});

15</script>

16 

17<div>{$stream.data}</div>
```

`onResponse` is triggered after a successful initial response from the stream and the raw [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) is passed to the callback. `onData` is called as each chunk is received - the current chunk is passed to the callback. `onFinish` is called when a stream has finished and when an error is thrown during the fetch / read cycle.

By default, a request is not made to the stream on initialization. You may pass an initial payload to the stream by using the `initialInput` option:

React

Vue

Svelte

```
 1import { useStream } from "@laravel/stream-react";

 2 

 3function App() {

 4    const { data } = useStream("chat", {

 5        initialInput: {

 6            message: "Introduce yourself.",

 7        },

 8    });

 9 

10    return <div>{data}</div>;

11}
```

```
 1<script setup lang="ts">

 2import { useStream } from "@laravel/stream-vue";

 3 

 4const { data } = useStream("chat", {

 5    initialInput: {

 6        message: "Introduce yourself.",

 7    },

 8});

 9</script>

10 

11<template>

12    <div>{{ data }}</div>

13</template>
```

```
 1<script>

 2import { useStream } from "@laravel/stream-svelte";

 3 

 4const stream = useStream("chat", {

 5    initialInput: {

 6        message: "Introduce yourself.",

 7    },

 8});

 9</script>

10 

11<div>{$stream.data}</div>
```

To cancel a stream manually, you may use the `cancel` method returned from the hook:

React

Vue

Svelte

```
 1import { useStream } from "@laravel/stream-react";

 2 

 3function App() {

 4    const { data, cancel } = useStream("chat");

 5 

 6    return (

 7        <div>

 8            <div>{data}</div>

 9            <button onClick={cancel}>Cancel</button>

10        </div>

11    );

12}
```

```
 1<script setup lang="ts">

 2import { useStream } from "@laravel/stream-vue";

 3 

 4const { data, cancel } = useStream("chat");

 5</script>

 6 

 7<template>

 8    <div>

 9        <div>{{ data }}</div>

10        <button @click="cancel">Cancel</button>

11    </div>

12</template>
```

```
 1<script>

 2import { useStream } from "@laravel/stream-svelte";

 3 

 4const stream = useStream("chat");

 5</script>

 6 

 7<div>

 8    <div>{$stream.data}</div>

 9    <button onclick={() => stream.cancel()}>Cancel</button>

10</div>
```

Each time the `useStream` hook is used, a random `id` is generated to identify the stream. This is sent back to the server with each request in the `X-STREAM-ID` header. When consuming the same stream from multiple components, you can read and write to the stream by providing your own `id`:

React

Vue

Svelte

```
 1// App.tsx

 2import { useStream } from "@laravel/stream-react";

 3 

 4function App() {

 5    const { data, id } = useStream("chat");

 6 

 7    return (

 8        <div>

 9            <div>{data}</div>

10            <StreamStatus id={id} />

11        </div>

12    );

13}

14 

15// StreamStatus.tsx

16import { useStream } from "@laravel/stream-react";

17 

18function StreamStatus({ id }) {

19    const { isFetching, isStreaming } = useStream("chat", { id });

20 

21    return (

22        <div>

23            {isFetching && <div>Connecting...</div>}

24            {isStreaming && <div>Generating...</div>}

25        </div>

26    );

27}
```

```
 1<!-- App.vue -->

 2<script setup lang="ts">

 3import { useStream } from "@laravel/stream-vue";

 4import StreamStatus from "./StreamStatus.vue";

 5 

 6const { data, id } = useStream("chat");

 7</script>

 8 

 9<template>

10    <div>

11        <div>{{ data }}</div>

12        <StreamStatus :id="id" />

13    </div>

14</template>

15 

16<!-- StreamStatus.vue -->

17<script setup lang="ts">

18import { useStream } from "@laravel/stream-vue";

19 

20const props = defineProps<{

21    id: string;

22}>();

23 

24const { isFetching, isStreaming } = useStream("chat", { id: props.id });

25</script>

26 

27<template>

28    <div>

29        <div v-if="isFetching">Connecting...</div>

30        <div v-if="isStreaming">Generating...</div>

31    </div>

32</template>
```

```
<!-- App.svelte -->

<script>

import { useStream } from "@laravel/stream-svelte";

import StreamStatus from "./StreamStatus.svelte";

const stream = useStream("chat");

</script>

<div>

    <div>{$stream.data}</div>

    <StreamStatus id={stream.id} />

</div>

<!-- StreamStatus.svelte -->

<script>

import { useStream } from "@laravel/stream-svelte";

let { id } = $props();

const stream = useStream("chat", { id });

</script>

<div>

    {#if $stream.isFetching}

        <div>Connecting...</div>

    {/if}

    {#if $stream.isStreaming}

        <div>Generating...</div>

    {/if}

</div>
```

### [Streamed JSON Responses](#streamed-json-responses)

If you need to stream JSON data incrementally, you may utilize the `streamJson` method. This method is especially useful for large datasets that need to be sent progressively to the browser in a format that can be easily parsed by JavaScript:

```
1use App\Models\User;

2 

3Route::get('/users.json', function () {

4    return response()->streamJson([

5        'users' => User::cursor(),

6    ]);

7});
```

The `useJsonStream` hook is identical to the [useStream hook](#consuming-streamed-responses) except that it will attempt to parse the data as JSON once it has finished streaming:

React

Vue

Svelte

```
 1import { useJsonStream } from "@laravel/stream-react";

 2 

 3type User = {

 4    id: number;

 5    name: string;

 6    email: string;

 7};

 8 

 9function App() {

10    const { data, send } = useJsonStream<{ users: User[] }>("users");

11 

12    const loadUsers = () => {

13        send({

14            query: "taylor",

15        });

16    };

17 

18    return (

19        <div>

20            <ul>

21                {data?.users.map((user) => (

22                    <li>

23                        {user.id}: {user.name}

24                    </li>

25                ))}

26            </ul>

27            <button onClick={loadUsers}>Load Users</button>

28        </div>

29    );

30}
```

```
 1<script setup lang="ts">

 2import { useJsonStream } from "@laravel/stream-vue";

 3 

 4type User = {

 5    id: number;

 6    name: string;

 7    email: string;

 8};

 9 

10const { data, send } = useJsonStream<{ users: User[] }>("users");

11 

12const loadUsers = () => {

13    send({

14        query: "taylor",

15    });

16};

17</script>

18 

19<template>

20    <div>

21        <ul>

22            <li v-for="user in data?.users" :key="user.id">

23                {{ user.id }}: {{ user.name }}

24            </li>

25        </ul>

26        <button @click="loadUsers">Load Users</button>

27    </div>

28</template>
```

```
<script>

import { useJsonStream } from "@laravel/stream-svelte";

const stream = useJsonStream("users");

const loadUsers = () => {

    stream.send({

        query: "taylor",

    });

};

</script>

<div>

    <ul>

        {#if $stream.data?.users}

            {#each $stream.data.users as user (user.id)}

                <li>{user.id}: {user.name}</li>

            {/each}

        {/if}

    </ul>

    <button onclick={loadUsers}>Load Users</button>

</div>
```

### [Event Streams (SSE)](#event-streams)

The `eventStream` method may be used to return a server-sent events (SSE) streamed response using the `text/event-stream` content type. The `eventStream` method accepts a closure which should [yield](https://www.php.net/manual/en/language.generators.overview.php) responses to the stream as the responses become available:

```
1Route::get('/chat', function () {

2    return response()->eventStream(function () {

3        $stream = OpenAI::client()->chat()->createStreamed(...);

4 

5        foreach ($stream as $response) {

6            yield $response->choices[0];

7        }

8    });

9});
```

If you would like to customize the name of the event, you may yield an instance of the `StreamedEvent` class:

```
1use Illuminate\Http\StreamedEvent;

2 

3yield new StreamedEvent(

4    event: 'update',

5    data: $response->choices[0],

6);
```

#### [Consuming Event Streams](#consuming-event-streams)

Event streams may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel event streams. To get started, install the `@laravel/stream-react`, `@laravel/stream-vue`, or `@laravel/stream-svelte` package:

React

Vue

Svelte

```
1npm install @laravel/stream-react
```

```
1npm install @laravel/stream-vue
```

```
1npm install @laravel/stream-svelte
```

Then, `useEventStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `message` with the concatenated response as messages are returned from your Laravel application:

React

Vue

Svelte

```
1import { useEventStream } from "@laravel/stream-react";

2 

3function App() {

4  const { message } = useEventStream("/chat");

5 

6  return <div>{message}</div>;

7}
```

```
1<script setup lang="ts">

2import { useEventStream } from "@laravel/stream-vue";

3 

4const { message } = useEventStream("/chat");

5</script>

6 

7<template>

8  <div>{{ message }}</div>

9</template>
```

```
1<script>

2import { useEventStream } from "@laravel/stream-svelte";

3 

4const eventStream = useEventStream("/chat");

5</script>

6 

7<div>{$eventStream.message}</div>
```

The second argument given to `useEventStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below:

React

Vue

Svelte

```
 1import { useEventStream } from "@laravel/stream-react";

 2 

 3function App() {

 4  const { message } = useEventStream("/stream", {

 5    eventName: "update",

 6    onMessage: (message) => {

 7      //

 8    },

 9    onError: (error) => {

10      //

11    },

12    onComplete: () => {

13      //

14    },

15    endSignal: "</stream>",

16    glue: " ",

17  });

18 

19  return <div>{message}</div>;

20}
```

```
 1<script setup lang="ts">

 2import { useEventStream } from "@laravel/stream-vue";

 3 

 4const { message } = useEventStream("/chat", {

 5  eventName: "update",

 6  onMessage: (message) => {

 7    // ...

 8  },

 9  onError: (error) => {

10    // ...

11  },

12  onComplete: () => {

13    // ...

14  },

15  endSignal: "</stream>",

16  glue: " ",

17});

18</script>
```

```
 1<script>

 2import { useEventStream } from "@laravel/stream-svelte";

 3 

 4const eventStream = useEventStream("/chat", {

 5    eventName: "update",

 6    onMessage: (event) => {

 7        //

 8    },

 9    onError: (error) => {

10        //

11    },

12    onComplete: () => {

13        //

14    },

15    endSignal: "</stream>",

16    glue: " ",

17    replace: false,

18});

19</script>
```

Event streams may also be manually consumed via an [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) object by your application's frontend. The `eventStream` method will automatically send a `</stream>` update to the event stream when the stream is complete:

```
 1const source = new EventSource('/chat');

 2 

 3source.addEventListener('update', (event) => {

 4    if (event.data === '</stream>') {

 5        source.close();

 6 

 7        return;

 8    }

 9 

10    console.log(event.data);

11});
```

To customize the final event that is sent to the event stream, you may provide a `StreamedEvent` instance to the `eventStream` method's `endStreamWith` argument:

```
1return response()->eventStream(function () {

2    // ...

3}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

### [Streamed Downloads](#streamed-downloads)

Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments:

```
1use App\Services\GitHub;

2 

3return response()->streamDownload(function () {

4    echo GitHub::api('repo')

5        ->contents()

6        ->readme('laravel', 'laravel')['contents'];

7}, 'laravel-readme.md');
```

## [Response Macros](#response-macros)

If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade. Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/13.x/providers), such as the `App\Providers\AppServiceProvider` service provider:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Support\Facades\Response;

 6use Illuminate\Support\ServiceProvider;

 7 

 8class AppServiceProvider extends ServiceProvider

 9{

10    /**

11     * Bootstrap any application services.

12     */

13    public function boot(): void

14    {

15        Response::macro('caps', function (string $value) {

16            return Response::make(strtoupper($value));

17        });

18    }

19}
```

The `macro` function accepts a name as its first argument and a closure as its second argument. The macro's closure will be executed when calling the macro name from a `ResponseFactory` implementation or the `response` helper:

```
1return response()->caps('foo');
```
