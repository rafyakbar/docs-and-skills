# Laravel Passport

- [Introduction](#introduction)
  * [Passport or Sanctum?](#passport-or-sanctum)
- [Installation](#installation)
  * [Deploying Passport](#deploying-passport)
  * [Upgrading Passport](#upgrading-passport)
- [Configuration](#configuration)
  * [Token Lifetimes](#token-lifetimes)
  * [Overriding Default Models](#overriding-default-models)
  * [Overriding Routes](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
  * [Managing Clients](#managing-clients)
  * [Requesting Tokens](#requesting-tokens)
  * [Managing Tokens](#managing-tokens)
  * [Refreshing Tokens](#refreshing-tokens)
  * [Revoking Tokens](#revoking-tokens)
  * [Purging Tokens](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
  * [Creating the Client](#creating-a-auth-pkce-grant-client)
  * [Requesting Tokens](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
  * [Creating a Device Code Grant Client](#creating-a-device-authorization-grant-client)
  * [Requesting Tokens](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
  * [Creating a Password Grant Client](#creating-a-password-grant-client)
  * [Requesting Tokens](#requesting-password-grant-tokens)
  * [Requesting All Scopes](#requesting-all-scopes)
  * [Customizing the User Provider](#customizing-the-user-provider)
  * [Customizing the Username Field](#customizing-the-username-field)
  * [Customizing the Password Validation](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Tokens](#personal-access-tokens)
  * [Creating a Personal Access Client](#creating-a-personal-access-client)
  * [Customizing the User Provider](#customizing-the-user-provider-for-pat)
  * [Managing Personal Access Tokens](#managing-personal-access-tokens)
- [Protecting Routes](#protecting-routes)
  * [Via Middleware](#via-middleware)
  * [Passing the Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
  * [Defining Scopes](#defining-scopes)
  * [Default Scope](#default-scope)
  * [Assigning Scopes to Tokens](#assigning-scopes-to-tokens)
  * [Checking Scopes](#checking-scopes)
- [SPA Authentication](#spa-authentication)
- [Events](#events)
- [Testing](#testing)

## [Introduction](#introduction)

[Laravel Passport](https://github.com/laravel/passport) provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Andy Millington and Simon Hamp.

This documentation assumes you are already familiar with OAuth2. If you do not know anything about OAuth2, consider familiarizing yourself with the general [terminology](https://oauth2.thephpleague.com/terminology/) and features of OAuth2 before continuing.

### [Passport or Sanctum?](#passport-or-sanctum)

Before getting started, you may wish to determine if your application would be better served by Laravel Passport or [Laravel Sanctum](/docs/13.x/sanctum). If your application absolutely needs to support OAuth2, then you should use Laravel Passport.

However, if you are attempting to authenticate a single-page application, mobile application, or issue API tokens, you should use [Laravel Sanctum](/docs/13.x/sanctum). Laravel Sanctum does not support OAuth2; however, it provides a much simpler API authentication development experience.

## [Installation](#installation)

You may install Laravel Passport via the `install:api` Artisan command:

```
1php artisan install:api --passport
```

This command will publish and run the database migrations necessary for creating the tables your application needs to store OAuth2 clients and access tokens. The command will also create the encryption keys required to generate secure access tokens.

After running the `install:api` command, add the `Laravel\Passport\HasApiTokens` trait and `Laravel\Passport\Contracts\OAuthenticatable` interface to your `App\Models\User` model. This trait will provide a few helper methods to your model which allow you to inspect the authenticated user's token and scopes:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Database\Eloquent\Factories\HasFactory;

 6use Illuminate\Foundation\Auth\User as Authenticatable;

 7use Illuminate\Notifications\Notifiable;

 8use Laravel\Passport\Contracts\OAuthenticatable;

 9use Laravel\Passport\HasApiTokens;

10 

11class User extends Authenticatable implements OAuthenticatable

12{

13    use HasApiTokens, HasFactory, Notifiable;

14}
```

Finally, in your application's `config/auth.php` configuration file, you should define an `api` authentication guard and set the `driver` option to `passport`. This will instruct your application to use Passport's `TokenGuard` when authenticating incoming API requests:

```
 1'guards' => [

 2    'web' => [

 3        'driver' => 'session',

 4        'provider' => 'users',

 5    ],

 6 

 7    'api' => [

 8        'driver' => 'passport',

 9        'provider' => 'users',

10    ],

11],
```

### [Deploying Passport](#deploying-passport)

When deploying Passport to your application's servers for the first time, you will likely need to run the `passport:keys` command. This command generates the encryption keys Passport needs in order to generate access tokens. The generated keys are not typically kept in source control:

```
1php artisan passport:keys
```

If necessary, you may define the path where Passport's keys should be loaded from. You may use the `Passport::loadKeysFrom` method to accomplish this. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
1/**

2 * Bootstrap any application services.

3 */

4public function boot(): void

5{

6    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');

7}
```

#### [Loading Keys From the Environment](#loading-keys-from-the-environment)

Alternatively, you may publish Passport's configuration file using the `vendor:publish` Artisan command:

```
1php artisan vendor:publish --tag=passport-config
```

After the configuration file has been published, you may load your application's encryption keys by defining them as environment variables:

```
1PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----

2<private key here>

3-----END RSA PRIVATE KEY-----"

4 

5PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----

6<public key here>

7-----END PUBLIC KEY-----"
```

### [Upgrading Passport](#upgrading-passport)

When upgrading to a new major version of Passport, it's important that you carefully review [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md).

## [Configuration](#configuration)

### [Token Lifetimes](#token-lifetimes)

By default, Passport issues long-lived access tokens that expire after one year. If you would like to configure a longer / shorter token lifetime, you may use the `tokensExpireIn`, `refreshTokensExpireIn`, and `personalAccessTokensExpireIn` methods. These methods should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use Carbon\CarbonInterval;

 2 

 3/**

 4 * Bootstrap any application services.

 5 */

 6public function boot(): void

 7{

 8    Passport::tokensExpireIn(CarbonInterval::days(15));

 9    Passport::refreshTokensExpireIn(CarbonInterval::days(30));

10    Passport::personalAccessTokensExpireIn(CarbonInterval::months(6));

11}
```

The `expires_at` columns on Passport's database tables are read-only and for display purposes only. When issuing tokens, Passport stores the expiration information within the signed and encrypted tokens. If you need to invalidate a token you should [revoke it](#revoking-tokens).

### [Overriding Default Models](#overriding-default-models)

You are free to extend the models used internally by Passport by defining your own model and extending the corresponding Passport model:

```
1use Laravel\Passport\Client as PassportClient;

2 

3class Client extends PassportClient

4{

5    // ...

6}
```

After defining your model, you may instruct Passport to use your custom model via the `Laravel\Passport\Passport` class. Typically, you should inform Passport about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use App\Models\Passport\AuthCode;

 2use App\Models\Passport\Client;

 3use App\Models\Passport\DeviceCode;

 4use App\Models\Passport\RefreshToken;

 5use App\Models\Passport\Token;

 6use Laravel\Passport\Passport;

 7 

 8/**

 9 * Bootstrap any application services.

10 */

11public function boot(): void

12{

13    Passport::useTokenModel(Token::class);

14    Passport::useRefreshTokenModel(RefreshToken::class);

15    Passport::useAuthCodeModel(AuthCode::class);

16    Passport::useClientModel(Client::class);

17    Passport::useDeviceCodeModel(DeviceCode::class);

18}
```

### [Overriding Routes](#overriding-routes)

Sometimes you may wish to customize the routes defined by Passport. To achieve this, you first need to ignore the routes registered by Passport by adding `Passport::ignoreRoutes` to the `register` method of your application's `AppServiceProvider`:

```
1use Laravel\Passport\Passport;

2 

3/**

4 * Register any application services.

5 */

6public function register(): void

7{

8    Passport::ignoreRoutes();

9}
```

Then, you may copy the routes defined by Passport in [its routes file](https://github.com/laravel/passport/blob/master/routes/web.php) to your application's `routes/web.php` file and modify them to your liking:

```
1Route::group([

2    'as' => 'passport.',

3    'prefix' => config('passport.path', 'oauth'),

4    'namespace' => '\Laravel\Passport\Http\Controllers',

5], function () {

6    // Passport routes...

7});
```

## [Authorization Code Grant](#authorization-code-grant)

Using OAuth2 via authorization codes is how most developers are familiar with OAuth2. When using authorization codes, a client application will redirect a user to your server where they will either approve or deny the request to issue an access token to the client.

To get started, we need to instruct Passport how to return our "authorization" view.

All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use Inertia\Inertia;

 2use Laravel\Passport\Passport;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    // By providing a view name...

10    Passport::authorizationView('auth.oauth.authorize');

11 

12    // By providing a closure...

13    Passport::authorizationView(

14        fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [

15            'request' => $parameters['request'],

16            'authToken' => $parameters['authToken'],

17            'client' => $parameters['client'],

18            'user' => $parameters['user'],

19            'scopes' => $parameters['scopes'],

20        ])

21    );

22}
```

Passport will automatically define the `/oauth/authorize` route that returns this view. Your `auth.oauth.authorize` template should include a form that makes a POST request to the `passport.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.authorizations.deny` route to deny the authorization. The `passport.authorizations.approve` and `passport.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields.

### [Managing Clients](#managing-clients)

Developers building applications that need to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URI that your application can redirect to after users approve their request for authorization.

#### [First-Party Clients](#managing-first-party-clients)

The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create first-party clients or testing your OAuth2 functionality. When you run the `passport:client` command, Passport will prompt you for more information about your client and will provide you with a client ID and secret:

```
1php artisan passport:client
```

If you would like to allow multiple redirect URIs for your client, you may specify them using a comma-delimited list when prompted for the URI by the `passport:client` command. Any URIs which contain commas should be URI encoded:

```
1https://third-party-app.com/callback,https://example.com/oauth/redirect
```

#### [Third-Party Clients](#managing-third-party-clients)

Since your application's users will not be able to utilize the `passport:client` command, you may use `createAuthorizationCodeGrantClient` method of the `Laravel\Passport\ClientRepository` class to register a client for a given user:

```
 1use App\Models\User;

 2use Laravel\Passport\ClientRepository;

 3 

 4$user = User::find($userId);

 5 

 6// Creating an OAuth app client that belongs to the given user...

 7$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(

 8    user: $user,

 9    name: 'Example App',

10    redirectUris: ['https://third-party-app.com/callback'],

11    confidential: false,

12    enableDeviceFlow: true

13);

14 

15// Retrieving all the OAuth app clients that belong to the user...

16$clients = $user->oauthApps()->get();
```

The `createAuthorizationCodeGrantClient` method returns an instance of `Laravel\Passport\Client`. You may display the `$client->id` as the client ID and `$client->plainSecret` as the client secret to the user.

### [Requesting Tokens](#requesting-tokens)

#### [Redirecting for Authorization](#requesting-tokens-redirecting-for-authorization)

Once a client has been created, developers may use their client ID and secret to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route like so:

```
 1use Illuminate\Http\Request;

 2use Illuminate\Support\Str;

 3 

 4Route::get('/redirect', function (Request $request) {

 5    $request->session()->put('state', $state = Str::random(40));

 6 

 7    $query = http_build_query([

 8        'client_id' => 'your-client-id',

 9        'redirect_uri' => 'https://third-party-app.com/callback',

10        'response_type' => 'code',

11        'scope' => 'user:read orders:create',

12        'state' => $state,

13        // 'prompt' => '', // "none", "consent", or "login"

14    ]);

15 

16    return redirect('https://passport-app.test/oauth/authorize?'.$query);

17});
```

The `prompt` parameter may be used to specify the authentication behavior of the Passport application.

If the `prompt` value is `none`, Passport will always throw an authentication error if the user is not already authenticated with the Passport application. If the value is `consent`, Passport will always display the authorization approval screen, even if all scopes were previously granted to the consuming application. When the value is `login`, the Passport application will always prompt the user to re-login to the application, even if they already have an existing session.

If no `prompt` value is provided, the user will be prompted for authorization only if they have not previously authorized access to the consuming application for the requested scopes.

Remember, the `/oauth/authorize` route is already defined by Passport. You do not need to manually define this route.

#### [Approving the Request](#approving-the-request)

When receiving authorization requests, Passport will automatically respond based on the value of `prompt` parameter (if present) and may display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created.

Sometimes you may wish to skip the authorization prompt, such as when authorizing a first-party client. You may accomplish this by [extending the `Client` model](#overriding-default-models) and defining a `skipsAuthorization` method. If `skipsAuthorization` returns `true` the client will be approved and the user will be redirected back to the `redirect_uri` immediately, unless the consuming application has explicitly set the `prompt` parameter when redirecting for authorization:

```
 1<?php

 2 

 3namespace App\Models\Passport;

 4 

 5use Illuminate\Contracts\Auth\Authenticatable;

 6use Laravel\Passport\Client as BaseClient;

 7 

 8class Client extends BaseClient

 9{

10    /**

11     * Determine if the client should skip the authorization prompt.

12     *

13     * @param  \Laravel\Passport\Scope[]  $scopes

14     */

15    public function skipsAuthorization(Authenticatable $user, array $scopes): bool

16    {

17        return $this->firstParty();

18    }

19}
```

#### [Converting Authorization Codes to Access Tokens](#requesting-tokens-converting-authorization-codes-to-access-tokens)

If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should first verify the `state` parameter against the value that was stored prior to the redirect. If the state parameter matches then the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request:

```
 1use Illuminate\Http\Request;

 2use Illuminate\Support\Facades\Http;

 3 

 4Route::get('/callback', function (Request $request) {

 5    $state = $request->session()->pull('state');

 6 

 7    throw_unless(

 8        strlen($state) > 0 && $state === $request->state,

 9        InvalidArgumentException::class,

10        'Invalid state value.'

11    );

12 

13    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [

14        'grant_type' => 'authorization_code',

15        'client_id' => 'your-client-id',

16        'client_secret' => 'your-client-secret',

17        'redirect_uri' => 'https://third-party-app.com/callback',

18        'code' => $request->code,

19    ]);

20 

21    return $response->json();

22});
```

This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

Like the `/oauth/authorize` route, the `/oauth/token` route is defined for you by Passport. There is no need to manually define this route.

### [Managing Tokens](#managing-tokens)

You may retrieve user's authorized tokens using the `tokens` method of the `Laravel\Passport\HasApiTokens` trait. For example, this may be used to offer your users a dashboard to keep track of their connections with third-party applications:

```
 1use App\Models\User;

 2use Illuminate\Database\Eloquent\Collection;

 3use Illuminate\Support\Facades\Date;

 4use Laravel\Passport\Token;

 5 

 6$user = User::find($userId);

 7 

 8// Retrieving all of the valid tokens for the user...

 9$tokens = $user->tokens()

10    ->where('revoked', false)

11    ->where('expires_at', '>', Date::now())

12    ->get();

13 

14// Retrieving all the user's connections to third-party OAuth app clients...

15$connections = $tokens->load('client')

16    ->reject(fn (Token $token) => $token->client->firstParty())

17    ->groupBy('client_id')

18    ->map(fn (Collection $tokens) => [

19        'client' => $tokens->first()->client,

20        'scopes' => $tokens->pluck('scopes')->flatten()->unique()->values()->all(),

21        'tokens_count' => $tokens->count(),

22    ])

23    ->values();
```

### [Refreshing Tokens](#refreshing-tokens)

If your application issues short-lived access tokens, users will need to refresh their access tokens via the refresh token that was provided to them when the access token was issued:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3$response = Http::asForm()->post('https://passport-app.test/oauth/token', [

 4    'grant_type' => 'refresh_token',

 5    'refresh_token' => 'the-refresh-token',

 6    'client_id' => 'your-client-id',

 7    'client_secret' => 'your-client-secret', // Required for confidential clients only...

 8    'scope' => 'user:read orders:create',

 9]);

10 

11return $response->json();
```

This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

### [Revoking Tokens](#revoking-tokens)

You may revoke a token by using the `revoke` method on the `Laravel\Passport\Token` model. You may revoke a token's refresh token using the `revoke` method on the `Laravel\Passport\RefreshToken` model:

```
 1use Laravel\Passport\Passport;

 2use Laravel\Passport\Token;

 3 

 4$token = Passport::token()->find($tokenId);

 5 

 6// Revoke an access token...

 7$token->revoke();

 8 

 9// Revoke the token's refresh token...

10$token->refreshToken?->revoke();

11 

12// Revoke all of the user's tokens...

13User::find($userId)->tokens()->each(function (Token $token) {

14    $token->revoke();

15    $token->refreshToken?->revoke();

16});
```

### [Purging Tokens](#purging-tokens)

When tokens have been revoked or expired, you might want to purge them from the database. Passport's included `passport:purge` Artisan command can do this for you:

```
 1# Purge revoked and expired tokens, auth codes, and device codes...

 2php artisan passport:purge

 3 

 4# Only purge tokens expired for more than 6 hours...

 5php artisan passport:purge --hours=6

 6 

 7# Only purge revoked tokens, auth codes, and device codes...

 8php artisan passport:purge --revoked

 9 

10# Only purge expired tokens, auth codes, and device codes...

11php artisan passport:purge --expired
```

You may also configure a [scheduled job](/docs/13.x/scheduling) in your application's `routes/console.php` file to automatically prune your tokens on a schedule:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('passport:purge')->hourly();
```

## [Authorization Code Grant With PKCE](#code-grant-pkce)

The Authorization Code grant with "Proof Key for Code Exchange" (PKCE) is a secure way to authenticate single page applications or mobile applications to access your API. This grant should be used when you can't guarantee that the client secret will be stored confidentially or in order to mitigate the threat of having the authorization code intercepted by an attacker. A combination of a "code verifier" and a "code challenge" replaces the client secret when exchanging the authorization code for an access token.

### [Creating the Client](#creating-a-auth-pkce-grant-client)

Before your application can issue tokens via the authorization code grant with PKCE, you will need to create a PKCE-enabled client. You may do this using the `passport:client` Artisan command with the `--public` option:

```
1php artisan passport:client --public
```

### [Requesting Tokens](#requesting-auth-pkce-grant-tokens)

#### [Code Verifier and Code Challenge](#code-verifier-code-challenge)

As this authorization grant does not provide a client secret, developers will need to generate a combination of a code verifier and a code challenge in order to request a token.

The code verifier should be a random string of between 43 and 128 characters containing letters, numbers, and `"-"`, `"."`, `"_"`, `"~"` characters, as defined in the [RFC 7636 specification](https://tools.ietf.org/html/rfc7636).

The code challenge should be a Base64 encoded string with URL and filename-safe characters. The trailing `'='` characters should be removed and no line breaks, whitespace, or other additional characters should be present.

```
1$encoded = base64_encode(hash('sha256', $codeVerifier, true));

2 

3$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

#### [Redirecting for Authorization](#code-grant-pkce-redirecting-for-authorization)

Once a client has been created, you may use the client ID and the generated code verifier and code challenge to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route:

```
 1use Illuminate\Http\Request;

 2use Illuminate\Support\Str;

 3 

 4Route::get('/redirect', function (Request $request) {

 5    $request->session()->put('state', $state = Str::random(40));

 6 

 7    $request->session()->put(

 8        'code_verifier', $codeVerifier = Str::random(128)

 9    );

10 

11    $codeChallenge = strtr(rtrim(

12        base64_encode(hash('sha256', $codeVerifier, true))

13    , '='), '+/', '-_');

14 

15    $query = http_build_query([

16        'client_id' => 'your-client-id',

17        'redirect_uri' => 'https://third-party-app.com/callback',

18        'response_type' => 'code',

19        'scope' => 'user:read orders:create',

20        'state' => $state,

21        'code_challenge' => $codeChallenge,

22        'code_challenge_method' => 'S256',

23        // 'prompt' => '', // "none", "consent", or "login"

24    ]);

25 

26    return redirect('https://passport-app.test/oauth/authorize?'.$query);

27});
```

#### [Converting Authorization Codes to Access Tokens](#code-grant-pkce-converting-authorization-codes-to-access-tokens)

If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should verify the `state` parameter against the value that was stored prior to the redirect, as in the standard Authorization Code Grant.

If the state parameter matches, the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request along with the originally generated code verifier:

```
 1use Illuminate\Http\Request;

 2use Illuminate\Support\Facades\Http;

 3 

 4Route::get('/callback', function (Request $request) {

 5    $state = $request->session()->pull('state');

 6 

 7    $codeVerifier = $request->session()->pull('code_verifier');

 8 

 9    throw_unless(

10        strlen($state) > 0 && $state === $request->state,

11        InvalidArgumentException::class

12    );

13 

14    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [

15        'grant_type' => 'authorization_code',

16        'client_id' => 'your-client-id',

17        'redirect_uri' => 'https://third-party-app.com/callback',

18        'code_verifier' => $codeVerifier,

19        'code' => $request->code,

20    ]);

21 

22    return $response->json();

23});
```

## [Device Authorization Grant](#device-authorization-grant)

The OAuth2 device authorization grant allows browserless or limited input devices, such as TVs and game consoles, to obtain an access token by exchanging a "device code". When using device flow, the device client will instruct the user to use a secondary device, such as a computer or a smartphone and connect to your server where they will enter the provided "user code" and either approve or deny the access request.

To get started, we need to instruct Passport how to return our "user code" and "authorization" views.

All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class.

```
 1use Inertia\Inertia;

 2use Laravel\Passport\Passport;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    // By providing a view name...

10    Passport::deviceUserCodeView('auth.oauth.device.user-code');

11    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

12 

13    // By providing a closure...

14    Passport::deviceUserCodeView(

15        fn ($parameters) => Inertia::render('Auth/OAuth/Device/UserCode')

16    );

17 

18    Passport::deviceAuthorizationView(

19        fn ($parameters) => Inertia::render('Auth/OAuth/Device/Authorize', [

20            'request' => $parameters['request'],

21            'authToken' => $parameters['authToken'],

22            'client' => $parameters['client'],

23            'user' => $parameters['user'],

24            'scopes' => $parameters['scopes'],

25        ])

26    );

27 

28    // ...

29}
```

Passport will automatically define routes that return these views. Your `auth.oauth.device.user-code` template should include a form that makes a GET request to the `passport.device.authorizations.authorize` route. The `passport.device.authorizations.authorize` route expects a `user_code` query parameter.

Your `auth.oauth.device.authorize` template should include a form that makes a POST request to the `passport.device.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.device.authorizations.deny` route to deny the authorization. The `passport.device.authorizations.approve` and `passport.device.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields.

### [Creating a Device Authorization Grant Client](#creating-a-device-authorization-grant-client)

Before your application can issue tokens via the device authorization grant, you will need to create a device flow enabled client. You may do this using the `passport:client` Artisan command with the `--device` option. This command will create a first-party device flow enabled client and provide you with a client ID and secret:

```
1php artisan passport:client --device
```

Additionally, you may use `createDeviceAuthorizationGrantClient` method on the `ClientRepository` class to register a third-party client that belongs to the given user:

```
 1use App\Models\User;

 2use Laravel\Passport\ClientRepository;

 3 

 4$user = User::find($userId);

 5 

 6$client = app(ClientRepository::class)->createDeviceAuthorizationGrantClient(

 7    user: $user,

 8    name: 'Example Device',

 9    confidential: false,

10);
```

### [Requesting Tokens](#requesting-device-authorization-grant-tokens)

#### [Requesting a Device Code](#device-code)

Once a client has been created, developers may use their client ID to request a device code from your application. First, the consuming device should make a `POST` request to your application's `/oauth/device/code` route to request a device code:

```
1use Illuminate\Support\Facades\Http;

2 

3$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [

4    'client_id' => 'your-client-id',

5    'scope' => 'user:read orders:create',

6]);

7 

8return $response->json();
```

This will return a JSON response containing `device_code`, `user_code`, `verification_uri`, `interval`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the device code expires. The `interval` attribute contains the number of seconds the consuming device should wait between requests when polling `/oauth/token` route to avoid rate limit errors.

Remember, the `/oauth/device/code` route is already defined by Passport. You do not need to manually define this route.

#### [Displaying the Verification URI and User Code](#user-code)

Once a device code request has been obtained, the consuming device should instruct the user to use another device and visit the provided `verification_uri` and enter the `user_code` in order to approve the authorization request.

#### [Polling Token Request](#polling-token-request)

Since the user will be using a separate device to grant (or deny) access, the consuming device should poll your application's `/oauth/token` route to determine when the user has responded to the request. The consuming device should use the minimum polling `interval` provided in the JSON response when requesting device code to avoid rate limit errors:

```
 1use Illuminate\Support\Facades\Http;

 2use Illuminate\Support\Sleep;

 3 

 4$interval = 5;

 5 

 6do {

 7    Sleep::for($interval)->seconds();

 8 

 9    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [

10        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',

11        'client_id' => 'your-client-id',

12        'client_secret' => 'your-client-secret', // Required for confidential clients only...

13        'device_code' => 'the-device-code',

14    ]);

15 

16    if ($response->json('error') === 'slow_down') {

17        $interval += 5;

18    }

19} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

20 

21return $response->json();
```

If the user has approved the authorization request, this will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires.

## [Password Grant](#password-grant)

We no longer recommend using password grant tokens. Instead, you should choose [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/).

The OAuth2 password grant allows your other first-party clients, such as a mobile application, to obtain an access token using an email address / username and password. This allows you to issue access tokens securely to your first-party clients without requiring your users to go through the entire OAuth2 authorization code redirect flow.

To enable the password grant, call the `enablePasswordGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
1/**

2 * Bootstrap any application services.

3 */

4public function boot(): void

5{

6    Passport::enablePasswordGrant();

7}
```

### [Creating a Password Grant Client](#creating-a-password-grant-client)

Before your application can issue tokens via the password grant, you will need to create a password grant client. You may do this using the `passport:client` Artisan command with the `--password` option.

```
1php artisan passport:client --password
```

### [Requesting Tokens](#requesting-password-grant-tokens)

Once you have enabled the grant and have created a password grant client, you may request an access token by issuing a `POST` request to the `/oauth/token` route with the user's email address and password. Remember, this route is already registered by Passport so there is no need to define it manually. If the request is successful, you will receive an `access_token` and `refresh_token` in the JSON response from the server:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3$response = Http::asForm()->post('https://passport-app.test/oauth/token', [

 4    'grant_type' => 'password',

 5    'client_id' => 'your-client-id',

 6    'client_secret' => 'your-client-secret', // Required for confidential clients only...

 7    'username' => '[[email protected]](/cdn-cgi/l/email-protection)',

 8    'password' => 'my-password',

 9    'scope' => 'user:read orders:create',

10]);

11 

12return $response->json();
```

Remember, access tokens are long-lived by default. However, you are free to [configure your maximum access token lifetime](#configuration) if needed.

### [Requesting All Scopes](#requesting-all-scopes)

When using the password grant or client credentials grant, you may wish to authorize the token for all of the scopes supported by your application. You can do this by requesting the `*` scope. If you request the `*` scope, the `can` method on the token instance will always return `true`. This scope may only be assigned to a token that is issued using the `password` or `client_credentials` grant:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3$response = Http::asForm()->post('https://passport-app.test/oauth/token', [

 4    'grant_type' => 'password',

 5    'client_id' => 'your-client-id',

 6    'client_secret' => 'your-client-secret', // Required for confidential clients only...

 7    'username' => '[[email protected]](/cdn-cgi/l/email-protection)',

 8    'password' => 'my-password',

 9    'scope' => '*',

10]);
```

### [Customizing the User Provider](#customizing-the-user-provider)

If your application uses more than one [authentication user provider](/docs/13.x/authentication#introduction), you may specify which user provider the password grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --password` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized.

### [Customizing the Username Field](#customizing-the-username-field)

When authenticating using the password grant, Passport will use the `email` attribute of your authenticatable model as the "username". However, you may customize this behavior by defining a `findForPassport` method on your model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Foundation\Auth\User as Authenticatable;

 6use Illuminate\Notifications\Notifiable;

 7use Laravel\Passport\Bridge\Client;

 8use Laravel\Passport\Contracts\OAuthenticatable;

 9use Laravel\Passport\HasApiTokens;

10 

11class User extends Authenticatable implements OAuthenticatable

12{

13    use HasApiTokens, Notifiable;

14 

15    /**

16     * Find the user instance for the given username.

17     */

18    public function findForPassport(string $username, Client $client): User

19    {

20        return $this->where('username', $username)->first();

21    }

22}
```

### [Customizing the Password Validation](#customizing-the-password-validation)

When authenticating using the password grant, Passport will use the `password` attribute of your model to validate the given password. If your model does not have a `password` attribute or you wish to customize the password validation logic, you can define a `validateForPassportPasswordGrant` method on your model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Foundation\Auth\User as Authenticatable;

 6use Illuminate\Notifications\Notifiable;

 7use Illuminate\Support\Facades\Hash;

 8use Laravel\Passport\Contracts\OAuthenticatable;

 9use Laravel\Passport\HasApiTokens;

10 

11class User extends Authenticatable implements OAuthenticatable

12{

13    use HasApiTokens, Notifiable;

14 

15    /**

16     * Validate the password of the user for the Passport password grant.

17     */

18    public function validateForPassportPasswordGrant(string $password): bool

19    {

20        return Hash::check($password, $this->password);

21    }

22}
```

## [Implicit Grant](#implicit-grant)

We no longer recommend using implicit grant tokens. Instead, you should choose [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/).

The implicit grant is similar to the authorization code grant; however, the token is returned to the client without exchanging an authorization code. This grant is most commonly used for JavaScript or mobile applications where the client credentials can't be securely stored. To enable the grant, call the `enableImplicitGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
1/**

2 * Bootstrap any application services.

3 */

4public function boot(): void

5{

6    Passport::enableImplicitGrant();

7}
```

Before your application can issue tokens via the implicit grant, you will need to create an implicit grant client. You may do this using the `passport:client` Artisan command with the `--implicit` option.

```
1php artisan passport:client --implicit
```

Once the grant has been enabled and an implicit client has been created, developers may use their client ID to request an access token from your application. The consuming application should make a redirect request to your application's `/oauth/authorize` route like so:

```
 1use Illuminate\Http\Request;

 2 

 3Route::get('/redirect', function (Request $request) {

 4    $request->session()->put('state', $state = Str::random(40));

 5 

 6    $query = http_build_query([

 7        'client_id' => 'your-client-id',

 8        'redirect_uri' => 'https://third-party-app.com/callback',

 9        'response_type' => 'token',

10        'scope' => 'user:read orders:create',

11        'state' => $state,

12        // 'prompt' => '', // "none", "consent", or "login"

13    ]);

14 

15    return redirect('https://passport-app.test/oauth/authorize?'.$query);

16});
```

Remember, the `/oauth/authorize` route is already defined by Passport. You do not need to manually define this route.

## [Client Credentials Grant](#client-credentials-grant)

The client credentials grant is suitable for machine-to-machine authentication. For example, you might use this grant in a scheduled job which is performing maintenance tasks over an API.

Before your application can issue tokens via the client credentials grant, you will need to create a client credentials grant client. You may do this using the `--client` option of the `passport:client` Artisan command:

```
1php artisan passport:client --client
```

Next, assign the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware to a route:

```
1use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

2 

3Route::get('/orders', function (Request $request) {

4    // Access token is valid and the client is resource owner...

5})->middleware(EnsureClientIsResourceOwner::class);
```

To restrict access to the route to specific scopes, you may provide a list of the required scopes to the `using` method`:

```
1Route::get('/orders', function (Request $request) {

2    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...

3})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

The [underlying OAuth2 server](https://oauth2.thephpleague.com/database-setup/#:~:text=Please%20note%20that,the%20bearer%20token.) sets the token's `sub` claim to the client's identifier for client credentials tokens. By default, Passport uses UUIDs for clients, so this cannot collide with a user's integer primary key. However, if you have set `Passport::$clientUuids` to `false`, a client credentials token may inadvertently resolve a user whose ID matches the client's ID. In such cases, using this middleware cannot guarantee that the incoming token is a client credentials token.

### [Retrieving Tokens](#retrieving-tokens)

To retrieve a token using this grant type, make a request to the `oauth/token` endpoint:

```
 1use Illuminate\Support\Facades\Http;

 2 

 3$response = Http::asForm()->post('https://passport-app.test/oauth/token', [

 4    'grant_type' => 'client_credentials',

 5    'client_id' => 'your-client-id',

 6    'client_secret' => 'your-client-secret',

 7    'scope' => 'servers:read servers:create',

 8]);

 9 

10return $response->json()['access_token'];
```

## [Personal Access Tokens](#personal-access-tokens)

Sometimes, your users may want to issue access tokens to themselves without going through the typical authorization code redirect flow. Allowing users to issue tokens to themselves via your application's UI can be useful for allowing users to experiment with your API or may serve as a simpler approach to issuing access tokens in general.

If your application is using Passport primarily to issue personal access tokens, consider using [Laravel Sanctum](/docs/13.x/sanctum), Laravel's light-weight first-party library for issuing API access tokens.

### [Creating a Personal Access Client](#creating-a-personal-access-client)

Before your application can issue personal access tokens, you will need to create a personal access client. You may do this by executing the `passport:client` Artisan command with the `--personal` option. If you have already run the `passport:install` command, you do not need to run this command:

```
1php artisan passport:client --personal
```

### [Customizing the User Provider](#customizing-the-user-provider-for-pat)

If your application uses more than one [authentication user provider](/docs/13.x/authentication#introduction), you may specify which user provider the personal access grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --personal` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized.

### [Managing Personal Access Tokens](#managing-personal-access-tokens)

Once you have created a personal access client, you may issue tokens for a given user using the `createToken` method on the `App\Models\User` model instance. The `createToken` method accepts the name of the token as its first argument and an optional array of [scopes](#token-scopes) as its second argument:

```
 1use App\Models\User;

 2use Illuminate\Support\Facades\Date;

 3use Laravel\Passport\Token;

 4 

 5$user = User::find($userId);

 6 

 7// Creating a token without scopes...

 8$token = $user->createToken('My Token')->accessToken;

 9 

10// Creating a token with scopes...

11$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

12 

13// Creating a token with all scopes...

14$token = $user->createToken('My Token', ['*'])->accessToken;

15 

16// Retrieving all the valid personal access tokens that belong to the user...

17$tokens = $user->tokens()

18    ->with('client')

19    ->where('revoked', false)

20    ->where('expires_at', '>', Date::now())

21    ->get()

22    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

## [Protecting Routes](#protecting-routes)

### [Via Middleware](#via-middleware)

Passport includes an [authentication guard](/docs/13.x/authentication#adding-custom-guards) that will validate access tokens on incoming requests. Once you have configured the `api` guard to use the `passport` driver, you only need to specify the `auth:api` middleware on any routes that should require a valid access token:

```
1Route::get('/user', function () {

2    // Only API authenticated users may access this route...

3})->middleware('auth:api');
```

If you are using the [client credentials grant](#client-credentials-grant), you should use [the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware](#client-credentials-grant) to protect your routes instead of the `auth:api` middleware.

#### [Multiple Authentication Guards](#multiple-authentication-guards)

If your application authenticates different types of users that perhaps use entirely different Eloquent models, you will likely need to define a guard configuration for each user provider type in your application. This allows you to protect requests intended for specific user providers. For example, given the following guard configuration the `config/auth.php` configuration file:

```
 1'guards' => [

 2    'api' => [

 3        'driver' => 'passport',

 4        'provider' => 'users',

 5    ],

 6 

 7    'api-customers' => [

 8        'driver' => 'passport',

 9        'provider' => 'customers',

10    ],

11],
```

The following route will utilize the `api-customers` guard, which uses the `customers` user provider, to authenticate incoming requests:

```
1Route::get('/customer', function () {

2    // ...

3})->middleware('auth:api-customers');
```

For more information on using multiple user providers with Passport, please consult the [personal access tokens documentation](#customizing-the-user-provider-for-pat) and [password grant documentation](#customizing-the-user-provider).

### [Passing the Access Token](#passing-the-access-token)

When calling routes that are protected by Passport, your application's API consumers should specify their access token as a `Bearer` token in the `Authorization` header of their request. For example, when using the `Http` Facade:

```
1use Illuminate\Support\Facades\Http;

2 

3$response = Http::withHeaders([

4    'Accept' => 'application/json',

5    'Authorization' => "Bearer $accessToken",

6])->get('https://passport-app.test/api/user');

7 

8return $response->json();
```

## [Token Scopes](#token-scopes)

Scopes allow your API clients to request a specific set of permissions when requesting authorization to access an account. For example, if you are building an e-commerce application, not all API consumers will need the ability to place orders. Instead, you may allow the consumers to only request authorization to access order shipment statuses. In other words, scopes allow your application's users to limit the actions a third-party application can perform on their behalf.

### [Defining Scopes](#defining-scopes)

You may define your API's scopes using the `Passport::tokensCan` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class. The `tokensCan` method accepts an array of scope names and scope descriptions. The scope description may be anything you wish and will be displayed to users on the authorization approval screen:

```
 1/**

 2 * Bootstrap any application services.

 3 */

 4public function boot(): void

 5{

 6    Passport::tokensCan([

 7        'user:read' => 'Retrieve the user info',

 8        'orders:create' => 'Place orders',

 9        'orders:read:status' => 'Check order status',

10    ]);

11}
```

### [Default Scope](#default-scope)

If a client does not request any specific scopes, you may configure your Passport server to attach default scopes to the token using the `defaultScopes` method. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use Laravel\Passport\Passport;

 2 

 3Passport::tokensCan([

 4    'user:read' => 'Retrieve the user info',

 5    'orders:create' => 'Place orders',

 6    'orders:read:status' => 'Check order status',

 7]);

 8 

 9Passport::defaultScopes([

10    'user:read',

11    'orders:create',

12]);
```

### [Assigning Scopes to Tokens](#assigning-scopes-to-tokens)

#### [When Requesting Authorization Codes](#when-requesting-authorization-codes)

When requesting an access token using the authorization code grant, consumers should specify their desired scopes as the `scope` query string parameter. The `scope` parameter should be a space-delimited list of scopes:

```
 1Route::get('/redirect', function () {

 2    $query = http_build_query([

 3        'client_id' => 'your-client-id',

 4        'redirect_uri' => 'https://third-party-app.com/callback',

 5        'response_type' => 'code',

 6        'scope' => 'user:read orders:create',

 7    ]);

 8 

 9    return redirect('https://passport-app.test/oauth/authorize?'.$query);

10});
```

#### [When Issuing Personal Access Tokens](#when-issuing-personal-access-tokens)

If you are issuing personal access tokens using the `App\Models\User` model's `createToken` method, you may pass the array of desired scopes as the second argument to the method:

```
1$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

### [Checking Scopes](#checking-scopes)

Passport includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given scope.

#### [Check For All Scopes](#check-for-all-scopes)

The `Laravel\Passport\Http\Middleware\CheckToken` middleware may be assigned to a route to verify that the incoming request's access token has all the listed scopes:

```
1use Laravel\Passport\Http\Middleware\CheckToken;

2 

3Route::get('/orders', function () {

4    // Access token has both "orders:read" and "orders:create" scopes...

5})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

#### [Check for Any Scopes](#check-for-any-scopes)

The `Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` middleware may be assigned to a route to verify that the incoming request's access token has *at least one* of the listed scopes:

```
1use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

2 

3Route::get('/orders', function () {

4    // Access token has either "orders:read" or "orders:create" scope...

5})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

#### [Scope Attributes](#scope-attributes)

If your application uses [controller middleware attributes](/docs/13.x/controllers#middleware-attributes), you may use the `Laravel\Passport\Attributes\AuthorizeToken` attribute as a convenient shortcut for Passport's scope middleware:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Laravel\Passport\Attributes\AuthorizeToken;

 6 

 7#[AuthorizeToken('orders:read')]

 8#[AuthorizeToken('orders:create', only: ['store'])]

 9class OrderController

10{

11    #[AuthorizeToken(['orders:read', 'orders:create'], anyScope: true)]

12    public function index()

13    {

14        // Access token has either "orders:read" or "orders:create" scope...

15    }

16 

17    public function store()

18    {

19        // Access token has both "orders:read" and "orders:create" scopes...

20    }

21}
```

By default, the `AuthorizeToken` attribute requires all given scopes. If you pass `anyScope: true`, the request is authorized when the token has at least one of the given scopes.

#### [Checking Scopes on a Token Instance](#checking-scopes-on-a-token-instance)

Once an access token authenticated request has entered your application, you may still check if the token has a given scope using the `tokenCan` method on the authenticated `App\Models\User` instance:

```
1use Illuminate\Http\Request;

2 

3Route::get('/orders', function (Request $request) {

4    if ($request->user()->tokenCan('orders:create')) {

5        // ...

6    }

7});
```

#### [Additional Scope Methods](#additional-scope-methods)

The `scopeIds` method will return an array of all defined IDs / names:

```
1use Laravel\Passport\Passport;

2 

3Passport::scopeIds();
```

The `scopes` method will return an array of all defined scopes as instances of `Laravel\Passport\Scope`:

```
1Passport::scopes();
```

The `scopesFor` method will return an array of `Laravel\Passport\Scope` instances matching the given IDs / names:

```
1Passport::scopesFor(['user:read', 'orders:create']);
```

You may determine if a given scope has been defined using the `hasScope` method:

```
1Passport::hasScope('orders:create');
```

## [SPA Authentication](#spa-authentication)

When building an API, it can be extremely useful to be able to consume your own API from your JavaScript application. This approach to API development allows your own application to consume the same API that you are sharing with the world. The same API may be consumed by your web application, mobile applications, third-party applications, and any SDKs that you may publish on various package managers.

Typically, if you want to consume your API from your JavaScript application, you would need to manually send an access token to the application and pass it with each request to your application. However, Passport includes a middleware that can handle this for you. All you need to do is append the `CreateFreshApiToken` middleware to the `web` middleware group in your application's `bootstrap/app.php` file:

```
1use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

2 

3->withMiddleware(function (Middleware $middleware): void {

4    $middleware->web(append: [

5        CreateFreshApiToken::class,

6    ]);

7})
```

You should ensure that the `CreateFreshApiToken` middleware is the last middleware listed in your middleware stack.

This middleware will attach a `laravel_token` cookie to your outgoing responses. This cookie contains an encrypted JWT that Passport will use to authenticate API requests from your JavaScript application. The JWT has a lifetime equal to your `session.lifetime` configuration value. Now, since the browser will automatically send the cookie with all subsequent requests, you may make requests to your application's API without explicitly passing an access token:

```
1axios.get('/api/user')

2    .then(response => {

3        console.log(response.data);

4    });
```

#### [Customizing the Cookie Name](#customizing-the-cookie-name)

If needed, you can customize the `laravel_token` cookie's name using the `Passport::cookie` method. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
1/**

2 * Bootstrap any application services.

3 */

4public function boot(): void

5{

6    Passport::cookie('custom_name');

7}
```

#### [CSRF Protection](#csrf-protection)

When using this method of authentication, you will need to ensure a valid CSRF token header is included in your requests. The default Laravel JavaScript scaffolding included with the skeleton application and all starter kits includes an [Axios](https://github.com/axios/axios) instance, which will automatically use the encrypted `XSRF-TOKEN` cookie value to send an `X-XSRF-TOKEN` header on same-origin requests.

If you choose to send the `X-CSRF-TOKEN` header instead of `X-XSRF-TOKEN`, you will need to use the unencrypted token provided by `csrf_token()`.

## [Events](#events)

Passport raises events when issuing access tokens and refresh tokens. You may [listen for these events](/docs/13.x/events) to prune or revoke other access tokens in your database:

| Event Name                                    |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

## [Testing](#testing)

Passport's `actingAs` method may be used to specify the currently authenticated user as well as its scopes. The first argument given to the `actingAs` method is the user instance and the second is an array of scopes that should be granted to the user's token:

Pest

PHPUnit

```
 1use App\Models\User;

 2use Laravel\Passport\Passport;

 3 

 4test('orders can be created', function () {

 5    Passport::actingAs(

 6        User::factory()->create(),

 7        ['orders:create']

 8    );

 9 

10    $response = $this->post('/api/orders');

11 

12    $response->assertStatus(201);

13});
```

```
 1use App\Models\User;

 2use Laravel\Passport\Passport;

 3 

 4public function test_orders_can_be_created(): void

 5{

 6    Passport::actingAs(

 7        User::factory()->create(),

 8        ['orders:create']

 9    );

10 

11    $response = $this->post('/api/orders');

12 

13    $response->assertStatus(201);

14}
```

Passport's `actingAsClient` method may be used to specify the currently authenticated client as well as its scopes. The first argument given to the `actingAsClient` method is the client instance and the second is an array of scopes that should be granted to the client's token:

Pest

PHPUnit

```
 1use Laravel\Passport\Client;

 2use Laravel\Passport\Passport;

 3 

 4test('servers can be retrieved', function () {

 5    Passport::actingAsClient(

 6        Client::factory()->create(),

 7        ['servers:read']

 8    );

 9 

10    $response = $this->get('/api/servers');

11 

12    $response->assertStatus(200);

13});
```

```
 1use Laravel\Passport\Client;

 2use Laravel\Passport\Passport;

 3 

 4public function test_servers_can_be_retrieved(): void

 5{

 6    Passport::actingAsClient(

 7        Client::factory()->create(),

 8        ['servers:read']

 9    );

10 

11    $response = $this->get('/api/servers');

12 

13    $response->assertStatus(200);

14}
```
