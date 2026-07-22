# Laravel Sanctum

- [Introduction](#introduction)
  * [How it Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
  * [Overriding Default Models](#overriding-default-models)
- [API Token Authentication](#api-token-authentication)
  * [Issuing API Tokens](#issuing-api-tokens)
  * [Token Abilities](#token-abilities)
  * [Protecting Routes](#protecting-routes)
  * [Revoking Tokens](#revoking-tokens)
  * [Token Expiration](#token-expiration)
- [SPA Authentication](#spa-authentication)
  * [Configuration](#spa-configuration)
  * [Authenticating](#spa-authenticating)
  * [Protecting Routes](#protecting-spa-routes)
  * [Authorizing Private Broadcast Channels](#authorizing-private-broadcast-channels)
- [Mobile Application Authentication](#mobile-application-authentication)
  * [Issuing API Tokens](#issuing-mobile-api-tokens)
  * [Protecting Routes](#protecting-mobile-api-routes)
  * [Revoking Tokens](#revoking-mobile-api-tokens)
- [Testing](#testing)

## [Introduction](#introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum) provides a featherweight authentication system for SPAs (single page applications), mobile applications, and simple, token based APIs. Sanctum allows each user of your application to generate multiple API tokens for their account. These tokens may be granted abilities / scopes which specify which actions the tokens are allowed to perform.

### [How it Works](#how-it-works)

Laravel Sanctum exists to solve two separate problems. Let's discuss each before digging deeper into the library.

#### [API Tokens](#how-it-works-api-tokens)

First, Sanctum is a simple package you may use to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub and other applications which issue "personal access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Sanctum to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user anytime.

Laravel Sanctum offers this feature by storing user API tokens in a single database table and authenticating incoming HTTP requests via the `Authorization` header which should contain a valid API token.

#### [SPA Authentication](#how-it-works-spa-authentication)

Second, Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as an SPA created using Next.js or Nuxt.

For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. Typically, Sanctum utilizes Laravel's `web` authentication guard to accomplish this. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS.

Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend. When Sanctum examines an incoming HTTP request, it will first check for an authentication cookie and, if none is present, Sanctum will then examine the `Authorization` header for a valid API token.

It is perfectly fine to use Sanctum only for API token authentication or only for SPA authentication. Just because you use Sanctum does not mean you are required to use both features it offers.

## [Installation](#installation)

You may install Laravel Sanctum via the `install:api` Artisan command:

```
1php artisan install:api
```

Next, if you plan to utilize Sanctum to authenticate an SPA, please refer to the [SPA Authentication](#spa-authentication) section of this documentation.

## [Configuration](#configuration)

### [Overriding Default Models](#overriding-default-models)

Although not typically required, you are free to extend the `PersonalAccessToken` model used internally by Sanctum:

```
1use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

2 

3class PersonalAccessToken extends SanctumPersonalAccessToken

4{

5    // ...

6}
```

Then, you may instruct Sanctum to use your custom model via the `usePersonalAccessTokenModel` method provided by Sanctum. Typically, you should call this method in the `boot` method of your application's `AppServiceProvider` file:

```
 1use App\Models\Sanctum\PersonalAccessToken;

 2use Laravel\Sanctum\Sanctum;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);

10}
```

## [API Token Authentication](#api-token-authentication)

You should not use API tokens to authenticate your own first-party SPA. Instead, use Sanctum's built-in [SPA authentication features](#spa-authentication).

### [Issuing API Tokens](#issuing-api-tokens)

Sanctum allows you to issue API tokens / personal access tokens that may be used to authenticate API requests to your application. When making requests using API tokens, the token should be included in the `Authorization` header as a `Bearer` token.

To begin issuing tokens for users, your User model should use the `Laravel\Sanctum\HasApiTokens` trait:

```
1use Laravel\Sanctum\HasApiTokens;

2 

3class User extends Authenticatable

4{

5    use HasApiTokens, HasFactory, Notifiable;

6}
```

To issue a token, you may use the `createToken` method. The `createToken` method returns a `Laravel\Sanctum\NewAccessToken` instance. API tokens are hashed using SHA-256 hashing before being stored in your database, but you may access the plain-text value of the token using the `plainTextToken` property of the `NewAccessToken` instance. You should display this value to the user immediately after the token has been created:

```
1use Illuminate\Http\Request;

2 

3Route::post('/tokens/create', function (Request $request) {

4    $token = $request->user()->createToken($request->token_name);

5 

6    return ['token' => $token->plainTextToken];

7});
```

You may access all of the user's tokens using the `tokens` Eloquent relationship provided by the `HasApiTokens` trait:

```
1foreach ($user->tokens as $token) {

2    // ...

3}
```

### [Token Abilities](#token-abilities)

Sanctum allows you to assign "abilities" to tokens. Abilities serve a similar purpose as OAuth's "scopes". You may pass an array of string abilities as the second argument to the `createToken` method:

```
1return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

When handling an incoming request authenticated by Sanctum, you may determine if the token has a given ability using the `tokenCan` or `tokenCant` methods:

```
1if ($user->tokenCan('server:update')) {

2    // ...

3}

4 

5if ($user->tokenCant('server:update')) {

6    // ...

7}
```

#### [Token Ability Middleware](#token-ability-middleware)

Sanctum also includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given ability. To get started, define the following middleware aliases in your application's `bootstrap/app.php` file:

```
1use Laravel\Sanctum\Http\Middleware\CheckAbilities;

2use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

3 

4->withMiddleware(function (Middleware $middleware): void {

5    $middleware->alias([

6        'abilities' => CheckAbilities::class,

7        'ability' => CheckForAnyAbility::class,

8    ]);

9})
```

The `abilities` middleware may be assigned to a route to verify that the incoming request's token has all of the listed abilities:

```
1Route::get('/orders', function () {

2    // Token has both "check-status" and "place-orders" abilities...

3})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

The `ability` middleware may be assigned to a route to verify that the incoming request's token has *at least one* of the listed abilities:

```
1Route::get('/orders', function () {

2    // Token has the "check-status" or "place-orders" ability...

3})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

#### [First-Party UI Initiated Requests](#first-party-ui-initiated-requests)

For convenience, the `tokenCan` method will always return `true` if the incoming authenticated request was from your first-party SPA and you are using Sanctum's built-in [SPA authentication](#spa-authentication).

However, this does not necessarily mean that your application has to allow the user to perform the action. Typically, your application's [authorization policies](/docs/13.x/authorization#creating-policies) will determine if the token has been granted the permission to perform the abilities as well as check that the user instance itself should be allowed to perform the action.

For example, if we imagine an application that manages servers, this might mean checking that the token is authorized to update servers **and** that the server belongs to the user:

```
1return $request->user()->id === $server->user_id &&

2       $request->user()->tokenCan('server:update')
```

At first, allowing the `tokenCan` method to be called and always return `true` for first-party UI initiated requests may seem strange; however, it is convenient to be able to always assume an API token is available and can be inspected via the `tokenCan` method. By taking this approach, you may always call the `tokenCan` method within your application's authorization policies without worrying about whether the request was triggered from your application's UI or was initiated by one of your API's third-party consumers.

### [Protecting Routes](#protecting-routes)

To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your protected routes within your `routes/web.php` and `routes/api.php` route files. This guard will ensure that incoming requests are authenticated as either stateful, cookie authenticated requests or contain a valid API token header if the request is from a third party.

You may be wondering why we suggest that you authenticate the routes within your application's `routes/web.php` file using the `sanctum` guard. Remember, Sanctum will first attempt to authenticate incoming requests using Laravel's typical session authentication cookie. If that cookie is not present then Sanctum will attempt to authenticate the request using a token in the request's `Authorization` header. In addition, authenticating all requests using Sanctum ensures that we may always call the `tokenCan` method on the currently authenticated user instance:

```
1use Illuminate\Http\Request;

2 

3Route::get('/user', function (Request $request) {

4    return $request->user();

5})->middleware('auth:sanctum');
```

### [Revoking Tokens](#revoking-tokens)

You may "revoke" tokens by deleting them from your database using the `tokens` relationship that is provided by the `Laravel\Sanctum\HasApiTokens` trait:

```
1// Revoke all tokens...

2$user->tokens()->delete();

3 

4// Revoke the token that was used to authenticate the current request...

5$request->user()->currentAccessToken()->delete();

6 

7// Revoke a specific token...

8$user->tokens()->where('id', $tokenId)->delete();
```

### [Token Expiration](#token-expiration)

By default, Sanctum tokens never expire and may only be invalidated by [revoking the token](#revoking-tokens). However, if you would like to configure an expiration time for your application's API tokens, you may do so via the `expiration` configuration option defined in your application's `sanctum` configuration file. This configuration option defines the number of minutes until an issued token will be considered expired:

```
1'expiration' => 525600,
```

If you would like to specify the expiration time of each token independently, you may do so by providing the expiration time as the third argument to the `createToken` method:

```
1return $user->createToken(

2    'token-name', ['*'], now()->plus(weeks: 1)

3)->plainTextToken;
```

If you have configured a token expiration time for your application, you may also wish to [schedule a task](/docs/13.x/scheduling) to prune your application's expired tokens. Thankfully, Sanctum includes a `sanctum:prune-expired` Artisan command that you may use to accomplish this. For example, you may configure a scheduled task to delete all expired token database records that have been expired for at least 24 hours:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

## [SPA Authentication](#spa-authentication)

Sanctum also exists to provide a simple method of authenticating single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository.

For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This approach to authentication provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS.

In order to authenticate, your SPA and API must share the same top-level domain. However, they may be placed on different subdomains. Additionally, you should ensure that you send the `Accept: application/json` header and either the `Referer` or `Origin` header with your request.

### [Configuration](#spa-configuration)

#### [Configuring Your First-Party Domains](#configuring-your-first-party-domains)

First, you should configure which domains your SPA will be making requests from. You may configure these domains using the `stateful` configuration option in your `sanctum` configuration file. This configuration setting determines which domains will maintain "stateful" authentication using Laravel session cookies when making requests to your API.

To assist you in setting up your first-party stateful domains, Sanctum provides two helper functions that you can include in the configuration. First, `Sanctum::currentApplicationUrlWithPort()` will return the current application URL from the `APP_URL` environment variable, and `Sanctum::currentRequestHost()` will inject a placeholder into the stateful domain list which, at runtime, will be replaced by the host from the current request so that all requests with the same domain are considered stateful.

If you are accessing your application via a URL that includes a port (`127.0.0.1:8000`), you should ensure that you include the port number with the domain.

#### [Sanctum Middleware](#sanctum-middleware)

Next, you should instruct Laravel that incoming requests from your SPA can authenticate using Laravel's session cookies, while still allowing requests from third parties or mobile applications to authenticate using API tokens. This can be easily accomplished by invoking the `statefulApi` middleware method in your application's `bootstrap/app.php` file:

```
1->withMiddleware(function (Middleware $middleware): void {

2    $middleware->statefulApi();

3})
```

#### [CORS and Cookies](#cors-and-cookies)

If you are having trouble authenticating with your application from an SPA that executes on a separate subdomain, you have likely misconfigured your CORS (Cross-Origin Resource Sharing) or session cookie settings.

The `config/cors.php` configuration file is not published by default. If you need to customize Laravel's CORS options, you should publish the complete `cors` configuration file using the `config:publish` Artisan command:

```
1php artisan config:publish cors
```

Next, you should ensure that your application's CORS configuration is returning the `Access-Control-Allow-Credentials` header with a value of `True`. This may be accomplished by setting the `supports_credentials` option within your application's `config/cors.php` configuration file to `true`.

In addition, you should enable the `withCredentials` and `withXSRFToken` options on your application's global `axios` instance. This can be performed in your `resources/js/app.js` file. If you are not using Axios to make HTTP requests from your frontend, you should perform the equivalent configuration on your own HTTP client:

```
1axios.defaults.withCredentials = true;

2axios.defaults.withXSRFToken = true;
```

Finally, you should ensure your application's session cookie domain configuration supports any subdomain of your root domain. You may accomplish this by prefixing the domain with a leading `.` within your application's `config/session.php` configuration file:

```
1'domain' => '.domain.com',
```

### [Authenticating](#spa-authenticating)

#### [CSRF Protection](#csrf-protection)

To authenticate your SPA, your SPA's "login" page should first make a request to the `/sanctum/csrf-cookie` endpoint to initialize CSRF protection for the application:

```
1axios.get('/sanctum/csrf-cookie').then(response => {

2    // Login...

3});
```

During this request, Laravel will set an `XSRF-TOKEN` cookie containing the current CSRF token. This token should then be URL decoded and passed in an `X-XSRF-TOKEN` header on subsequent requests, which some HTTP client libraries like Axios and the Angular HttpClient will do automatically for you. If your JavaScript HTTP library does not set the value for you, you will need to manually set the `X-XSRF-TOKEN` header to match the URL decoded value of the `XSRF-TOKEN` cookie that is set by this route.

#### [Logging In](#logging-in)

Once CSRF protection has been initialized, you should make a `POST` request to your Laravel application's `/login` route. This `/login` route may be [implemented manually](/docs/13.x/authentication#authenticating-users) or using a headless authentication package like [Laravel Fortify](/docs/13.x/fortify).

If the login request is successful, you will be authenticated and subsequent requests to your application's routes will automatically be authenticated via the session cookie that the Laravel application issued to your client. In addition, since your application already made a request to the `/sanctum/csrf-cookie` route, subsequent requests should automatically receive CSRF protection as long as your JavaScript HTTP client sends the value of the `XSRF-TOKEN` cookie in the `X-XSRF-TOKEN` header.

Of course, if your user's session expires due to lack of activity, subsequent requests to the Laravel application may receive a 401 or 419 HTTP error response. In this case, you should redirect the user to your SPA's login page.

Since this approach to SPA authentication is session based, you may use Laravel's standard authentication services, including ["remember me"](/docs/13.x/authentication#remembering-users) functionality.

You are free to write your own `/login` endpoint; however, you should ensure that it authenticates the user using the standard, [session based authentication services that Laravel provides](/docs/13.x/authentication#authenticating-users). Typically, this means using the `web` authentication guard.

### [Protecting Routes](#protecting-spa-routes)

To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party:

```
1use Illuminate\Http\Request;

2 

3Route::get('/user', function (Request $request) {

4    return $request->user();

5})->middleware('auth:sanctum');
```

### [Authorizing Private Broadcast Channels](#authorizing-private-broadcast-channels)

If your SPA needs to authenticate with [private / presence broadcast channels](/docs/13.x/broadcasting#authorizing-channels), you should remove the `channels` entry from the `withRouting` method contained in your application's `bootstrap/app.php` file. Instead, you should invoke the `withBroadcasting` method so that you may specify the correct middleware for your application's broadcasting routes:

```
1return Application::configure(basePath: dirname(__DIR__))

2    ->withRouting(

3        web: __DIR__.'/../routes/web.php',

4        // ...

5    )

6    ->withBroadcasting(

7        __DIR__.'/../routes/channels.php',

8        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],

9    )
```

Next, in order for Pusher's authorization requests to succeed, you will need to provide a custom Pusher `authorizer` when initializing [Laravel Echo](/docs/13.x/broadcasting#client-side-installation). This allows your application to configure Pusher to use the `axios` instance that is [properly configured for cross-domain requests](#cors-and-cookies):

```
 1window.Echo = new Echo({

 2    broadcaster: "pusher",

 3    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,

 4    encrypted: true,

 5    key: import.meta.env.VITE_PUSHER_APP_KEY,

 6    authorizer: (channel, options) => {

 7        return {

 8            authorize: (socketId, callback) => {

 9                axios.post('/api/broadcasting/auth', {

10                    socket_id: socketId,

11                    channel_name: channel.name

12                })

13                .then(response => {

14                    callback(false, response.data);

15                })

16                .catch(error => {

17                    callback(true, error);

18                });

19            }

20        };

21    },

22})
```

## [Mobile Application Authentication](#mobile-application-authentication)

You may also use Sanctum tokens to authenticate your mobile application's requests to your API. The process for authenticating mobile application requests is similar to authenticating third-party API requests; however, there are small differences in how you will issue the API tokens.

### [Issuing API Tokens](#issuing-mobile-api-tokens)

To get started, create a route that accepts the user's email / username, password, and device name, then exchanges those credentials for a new Sanctum token. The "device name" given to this endpoint is for informational purposes and may be any value you wish. In general, the device name value should be a name the user would recognize, such as "Nuno's iPhone 17".

Typically, you will make a request to the token endpoint from your mobile application's "login" screen. The endpoint will return the plain-text API token which may then be stored on the mobile device and used to make additional API requests:

```
 1use App\Models\User;

 2use Illuminate\Http\Request;

 3use Illuminate\Support\Facades\Hash;

 4use Illuminate\Validation\ValidationException;

 5 

 6Route::post('/sanctum/token', function (Request $request) {

 7    $request->validate([

 8        'email' => 'required|email',

 9        'password' => 'required',

10        'device_name' => 'required',

11    ]);

12 

13    $user = User::where('email', $request->email)->first();

14 

15    if (! $user || ! Hash::check($request->password, $user->password)) {

16        throw ValidationException::withMessages([

17            'email' => ['The provided credentials are incorrect.'],

18        ]);

19    }

20 

21    return $user->createToken($request->device_name)->plainTextToken;

22});
```

When the mobile application uses the token to make an API request to your application, it should pass the token in the `Authorization` header as a `Bearer` token.

When issuing tokens for a mobile application, you are also free to specify [token abilities](#token-abilities).

### [Protecting Routes](#protecting-mobile-api-routes)

As previously documented, you may protect routes so that all incoming requests must be authenticated by attaching the `sanctum` authentication guard to the routes:

```
1Route::get('/user', function (Request $request) {

2    return $request->user();

3})->middleware('auth:sanctum');
```

### [Revoking Tokens](#revoking-mobile-api-tokens)

To allow users to revoke API tokens issued to mobile devices, you may list them by name, along with a "Revoke" button, within an "account settings" portion of your web application's UI. When the user clicks the "Revoke" button, you can delete the token from the database. Remember, you can access a user's API tokens via the `tokens` relationship provided by the `Laravel\Sanctum\HasApiTokens` trait:

```
1// Revoke all tokens...

2$user->tokens()->delete();

3 

4// Revoke a specific token...

5$user->tokens()->where('id', $tokenId)->delete();
```

## [Testing](#testing)

While testing, the `Sanctum::actingAs` method may be used to authenticate a user and specify which abilities should be granted to their token:

Pest

PHPUnit

```
 1use App\Models\User;

 2use Laravel\Sanctum\Sanctum;

 3 

 4test('task list can be retrieved', function () {

 5    Sanctum::actingAs(

 6        User::factory()->create(),

 7        ['view-tasks']

 8    );

 9 

10    $response = $this->get('/api/task');

11 

12    $response->assertOk();

13});
```

```
 1use App\Models\User;

 2use Laravel\Sanctum\Sanctum;

 3 

 4public function test_task_list_can_be_retrieved(): void

 5{

 6    Sanctum::actingAs(

 7        User::factory()->create(),

 8        ['view-tasks']

 9    );

10 

11    $response = $this->get('/api/task');

12 

13    $response->assertOk();

14}
```

If you would like to grant all abilities to the token, you should include `*` in the ability list provided to the `actingAs` method:

```
1Sanctum::actingAs(

2    User::factory()->create(),

3    ['*']

4);
```
