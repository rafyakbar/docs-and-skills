# Resetting Passwords

- [Introduction](#introduction)
  * [Configuration](#configuration)
  * [Driver Prerequisites](#driver-prerequisites)
  * [Model Preparation](#model-preparation)
  * [Configuring Trusted Hosts](#configuring-trusted-hosts)
- [Routing](#routing)
  * [Requesting the Password Reset Link](#requesting-the-password-reset-link)
  * [Resetting the Password](#resetting-the-password)
- [Deleting Expired Tokens](#deleting-expired-tokens)
- [Customization](#password-customization)

## [Introduction](#introduction)

Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this by hand for every application you create, Laravel provides convenient services for sending password reset links and secure resetting passwords.

Want to get started fast? Install a Laravel [application starter kit](/docs/13.x/starter-kits) in a fresh Laravel application. Laravel's starter kits will take care of scaffolding your entire authentication system, including resetting forgotten passwords.

### [Configuration](#configuration)

Your application's password reset configuration file is stored at `config/auth.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `database` password reset driver.

The password reset `driver` configuration option defines where password reset data will be stored. Laravel includes two drivers:

- `database` - password reset data is stored in a relational database.
- `cache` - password reset data is stored in one of your cache-based stores.

### [Driver Prerequisites](#driver-prerequisites)

#### [Database](#database)

When using the default `database` driver, a table must be created to store your application's password reset tokens. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` database migration.

#### [Cache](#cache)

There is also a cache driver available for handling password resets, which does not require a dedicated database table. Entries are keyed by the user's email address, so ensure you are not using email addresses as a cache key elsewhere in your application:

```
1'passwords' => [

2    'users' => [

3        'driver' => 'cache',

4        'provider' => 'users',

5        'store' => 'passwords', // Optional...

6        'expire' => 60,

7        'throttle' => 60,

8    ],

9],
```

To prevent a call to `artisan cache:clear` from flushing your password reset data, you can optionally specify a separate cache store with the `store` configuration key. The value should correspond to a store configured in your `config/cache.php` configuration value.

### [Model Preparation](#model-preparation)

Before using the password reset features of Laravel, your application's `App\Models\User` model must use the `Illuminate\Notifications\Notifiable` trait. Typically, this trait is already included on the default `App\Models\User` model that is created with new Laravel applications.

Next, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface.

### [Configuring Trusted Hosts](#configuring-trusted-hosts)

By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request.

Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given hostname. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain hostnames, you may do so by using the `trustHosts` middleware method in your application's `bootstrap/app.php` file. This is particularly important when your application offers password reset functionality.

To learn more about this middleware method, please consult the [TrustHosts middleware documentation](/docs/13.x/requests#configuring-trusted-hosts).

## [Routing](#routing)

To properly implement support for allowing users to reset their passwords, we will need to define several routes. First, we will need a pair of routes to handle allowing the user to request a password reset link via their email address. Second, we will need a pair of routes to handle actually resetting the password once the user visits the password reset link that is emailed to them and completes the password reset form.

### [Requesting the Password Reset Link](#requesting-the-password-reset-link)

#### [The Password Reset Link Request Form](#the-password-reset-link-request-form)

First, we will define the routes that are needed to request password reset links. To get started, we will define a route that returns a view with the password reset link request form:

```
1Route::get('/forgot-password', function () {

2    return view('auth.forgot-password');

3})->middleware('guest')->name('password.request');
```

The view that is returned by this route should have a form containing an `email` field, which will allow the user to request a password reset link for a given email address.

#### [Handling the Form Submission](#password-reset-link-handling-the-form-submission)

Next, we will define a route that handles the form submission request from the "forgot password" view. This route will be responsible for validating the email address and sending the password reset request to the corresponding user:

```
 1use Illuminate\Http\Request;

 2use Illuminate\Support\Facades\Password;

 3 

 4Route::post('/forgot-password', function (Request $request) {

 5    $request->validate(['email' => 'required|email']);

 6 

 7    $status = Password::sendResetLink(

 8        $request->only('email')

 9    );

10 

11    return $status === Password::ResetLinkSent

12        ? back()->with(['status' => __($status)])

13        : back()->withErrors(['email' => __($status)]);

14})->middleware('guest')->name('password.email');
```

Before moving on, let's examine this route in more detail. First, the request's `email` attribute is validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to send a password reset link to the user. The password broker will take care of retrieving the user by the given field (in this case, the email address) and sending the user a password reset link via Laravel's built-in [notification system](/docs/13.x/notifications).

The `sendResetLink` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/13.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file.

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

You may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `sendResetLink` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/13.x/authentication#adding-custom-user-providers).

When manually implementing password resets, you are required to define the contents of the views and routes yourself. If you would like scaffolding that includes all necessary authentication and verification logic, check out the [Laravel application starter kits](/docs/13.x/starter-kits).

### [Resetting the Password](#resetting-the-password)

#### [The Password Reset Form](#the-password-reset-form)

Next, we will define the routes necessary to actually reset the password once the user clicks on the password reset link that has been emailed to them and provides a new password. First, let's define the route that will display the reset password form that is displayed when the user clicks the reset password link. This route will receive a `token` parameter that we will use later to verify the password reset request:

```
1Route::get('/reset-password/{token}', function (string $token) {

2    return view('auth.reset-password', ['token' => $token]);

3})->middleware('guest')->name('password.reset');
```

The view that is returned by this route should display a form containing an `email` field, a `password` field, a `password_confirmation` field, and a hidden `token` field, which should contain the value of the secret `$token` received by our route.

#### [Handling the Form Submission](#password-reset-handling-the-form-submission)

Of course, we need to define a route to actually handle the password reset form submission. This route will be responsible for validating the incoming request and updating the user's password in the database:

```
 1use App\Models\User;

 2use Illuminate\Auth\Events\PasswordReset;

 3use Illuminate\Http\Request;

 4use Illuminate\Support\Facades\Hash;

 5use Illuminate\Support\Facades\Password;

 6use Illuminate\Support\Str;

 7 

 8Route::post('/reset-password', function (Request $request) {

 9    $request->validate([

10        'token' => 'required',

11        'email' => 'required|email',

12        'password' => 'required|min:8|confirmed',

13    ]);

14 

15    $status = Password::reset(

16        $request->only('email', 'password', 'password_confirmation', 'token'),

17        function (User $user, string $password) {

18            $user->forceFill([

19                'password' => Hash::make($password)

20            ])->setRememberToken(Str::random(60));

21 

22            $user->save();

23 

24            event(new PasswordReset($user));

25        }

26    );

27 

28    return $status === Password::PasswordReset

29        ? redirect()->route('login')->with('status', __($status))

30        : back()->withErrors(['email' => [__($status)]]);

31})->middleware('guest')->name('password.update');
```

Before moving on, let's examine this route in more detail. First, the request's `token`, `email`, and `password` attributes are validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to validate the password reset request credentials.

If the token, email address, and password given to the password broker are valid, the closure passed to the `reset` method will be invoked. Within this closure, which receives the user instance and the plain-text password provided to the password reset form, we may update the user's password in the database.

The `reset` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/13.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. If your application does not contain a `lang` directory, you may create it using the `lang:publish` Artisan command.

Before moving on, you may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `reset` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/13.x/authentication#adding-custom-user-providers).

## [Deleting Expired Tokens](#deleting-expired-tokens)

If you are using the `database` driver, password reset tokens that have expired will still be present within your database. However, you may easily delete these records using the `auth:clear-resets` Artisan command:

```
1php artisan auth:clear-resets
```

If you would like to automate this process, consider adding the command to your application's [scheduler](/docs/13.x/scheduling):

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

## [Customization](#password-customization)

#### [Reset Link Customization](#reset-link-customization)

You may customize the password reset link URL using the `createUrlUsing` method provided by the `ResetPassword` notification class. This method accepts a closure which receives the user instance that is receiving the notification as well as the password reset link token. Typically, you should call this method from the `boot` method of your application's `AppServiceProvider`:

```
 1use App\Models\User;

 2use Illuminate\Auth\Notifications\ResetPassword;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    ResetPassword::createUrlUsing(function (User $user, string $token) {

10        return 'https://example.com/reset-password?token='.$token;

11    });

12}
```

#### [Reset Email Customization](#reset-email-customization)

You may easily modify the notification class used to send the password reset link to the user. To get started, override the `sendPasswordResetNotification` method on your `App\Models\User` model. Within this method, you may send the notification using any [notification class](/docs/13.x/notifications) of your own creation. The password reset `$token` is the first argument received by the method. You may use this `$token` to build the password reset URL of your choice and send your notification to the user:

```
 1use App\Notifications\ResetPasswordNotification;

 2 

 3/**

 4 * Send a password reset notification to the user.

 5 *

 6 * @param  string  $token

 7 */

 8public function sendPasswordResetNotification($token): void

 9{

10    $url = 'https://example.com/reset-password?token='.$token;

11 

12    $this->notify(new ResetPasswordNotification($url));

13}
```
