# Validation

- [Introduction](#introduction)
- [Validation Quickstart](#validation-quickstart)
  * [Defining the Routes](#quick-defining-the-routes)
  * [Creating the Controller](#quick-creating-the-controller)
  * [Writing the Validation Logic](#quick-writing-the-validation-logic)
  * [Displaying the Validation Errors](#quick-displaying-the-validation-errors)
  * [Repopulating Forms](#repopulating-forms)
  * [A Note on Optional Fields](#a-note-on-optional-fields)
  * [Validation Error Response Format](#validation-error-response-format)
- [Form Request Validation](#form-request-validation)
  * [Creating Form Requests](#creating-form-requests)
  * [Authorizing Form Requests](#authorizing-form-requests)
  * [Customizing the Error Messages](#customizing-the-error-messages)
  * [Preparing Input for Validation](#preparing-input-for-validation)
- [Manually Creating Validators](#manually-creating-validators)
  * [Automatic Redirection](#automatic-redirection)
  * [Named Error Bags](#named-error-bags)
  * [Customizing the Error Messages](#manual-customizing-the-error-messages)
  * [Performing Additional Validation](#performing-additional-validation)
- [Working With Validated Input](#working-with-validated-input)
- [Working With Error Messages](#working-with-error-messages)
  * [Specifying Custom Messages in Language Files](#specifying-custom-messages-in-language-files)
  * [Specifying Attributes in Language Files](#specifying-attribute-in-language-files)
  * [Specifying Values in Language Files](#specifying-values-in-language-files)
- [Available Validation Rules](#available-validation-rules)
- [Conditionally Adding Rules](#conditionally-adding-rules)
- [Validating Arrays](#validating-arrays)
  * [Validating Nested Array Input](#validating-nested-array-input)
  * [Error Message Indexes and Positions](#error-message-indexes-and-positions)
- [Validating Files](#validating-files)
- [Validating Passwords](#validating-passwords)
- [Custom Validation Rules](#custom-validation-rules)
  * [Using Rule Objects](#using-rule-objects)
  * [Using Closures](#using-closures)
  * [Implicit Rules](#implicit-rules)

## [Introduction](#introduction)

Laravel provides several different approaches to validate your application's incoming data. It is most common to use the `validate` method available on all incoming HTTP requests. However, we will discuss other approaches to validation as well.

Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features.

## [Validation Quickstart](#validation-quickstart)

To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel:

### [Defining the Routes](#quick-defining-the-routes)

First, let's assume we have the following routes defined in our `routes/web.php` file:

```
1use App\Http\Controllers\PostController;

2 

3Route::get('/post/create', [PostController::class, 'create']);

4Route::post('/post', [PostController::class, 'store']);
```

The `GET` route will display a form for the user to create a new blog post, while the `POST` route will store the new blog post in the database.

### [Creating the Controller](#quick-creating-the-controller)

Next, let's take a look at a simple controller that handles incoming requests to these routes. We'll leave the `store` method empty for now:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Http\RedirectResponse;

 6use Illuminate\Http\Request;

 7use Illuminate\View\View;

 8 

 9class PostController extends Controller

10{

11    /**

12     * Show the form to create a new blog post.

13     */

14    public function create(): View

15    {

16        return view('post.create');

17    }

18 

19    /**

20     * Store a new blog post.

21     */

22    public function store(Request $request): RedirectResponse

23    {

24        // Validate and store the blog post...

25 

26        $post = /** ... */

27 

28        return to_route('post.show', ['post' => $post->id]);

29    }

30}
```

### [Writing the Validation Logic](#quick-writing-the-validation-logic)

Now we are ready to fill in our `store` method with the logic to validate the new blog post. To do this, we will use the `validate` method provided by the `Illuminate\Http\Request` object. If the validation rules pass, your code will keep executing normally; however, if validation fails, an `Illuminate\Validation\ValidationException` exception will be thrown and the proper error response will automatically be sent back to the user.

If validation fails during a traditional HTTP request, a redirect response to the previous URL will be generated. If the incoming request is an XHR request, a [JSON response containing the validation error messages](#validation-error-response-format) will be returned.

To get a better understanding of the `validate` method, let's jump back into the `store` method:

```
 1/**

 2 * Store a new blog post.

 3 */

 4public function store(Request $request): RedirectResponse

 5{

 6    $validated = $request->validate([

 7        'title' => ['required', 'unique:posts', 'max:255'],

 8        'body' => ['required'],

 9    ]);

10 

11    // The blog post is valid...

12 

13    return redirect('/posts');

14}
```

As you can see, the validation rules are passed into the `validate` method. Don't worry - all available validation rules are [documented](#available-validation-rules). Again, if the validation fails, the proper response will automatically be generated. If the validation passes, our controller will continue executing normally.

In addition, you may use the `validateWithBag` method to validate a request and store any error messages within a [named error bag](#named-error-bags):

```
1$validated = $request->validateWithBag('post', [

2    'title' => ['required', 'unique:posts', 'max:255'],

3    'body' => ['required'],

4]);
```

#### [Stopping on First Validation Failure](#stopping-on-first-validation-failure)

Sometimes you may wish to stop running validation rules on an attribute after the first validation failure. To do so, assign the `bail` rule to the attribute:

```
1$request->validate([

2    'title' => ['bail', 'required', 'unique:posts', 'max:255'],

3    'body' => ['required'],

4]);
```

In this example, if the `unique` rule on the `title` attribute fails, the `max` rule will not be checked. Rules will be validated in the order they are assigned.

#### [A Note on Nested Attributes](#a-note-on-nested-attributes)

If the incoming HTTP request contains "nested" field data, you may specify these fields in your validation rules using "dot" syntax:

```
1$request->validate([

2    'title' => ['required', 'unique:posts', 'max:255'],

3    'author.name' => ['required'],

4    'author.description' => ['required'],

5]);
```

On the other hand, if your field name contains a literal period, you can explicitly prevent this from being interpreted as "dot" syntax by escaping the period with a backslash:

```
1$request->validate([

2    'title' => ['required', 'unique:posts', 'max:255'],

3    'v1\.0' => ['required'],

4]);
```

### [Displaying the Validation Errors](#quick-displaying-the-validation-errors)

So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/13.x/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/13.x/session#flash-data).

An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages).

So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view:

```
 1<!-- /resources/views/post/create.blade.php -->

 2 

 3<h1>Create Post</h1>

 4 

 5@if ($errors->any())

 6    <div class="alert alert-danger">

 7        <ul>

 8            @foreach ($errors->all() as $error)

 9                <li>{{ $error }}</li>

10            @endforeach

11        </ul>

12    </div>

13@endif

14 

15<!-- Create Post Form -->
```

#### [Customizing the Error Messages](#quick-customizing-the-error-messages)

Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command.

Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application.

In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/13.x/localization).

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

#### [XHR Requests and Validation](#quick-xhr-requests-and-validation)

In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a [JSON response containing all of the validation errors](#validation-error-response-format). This JSON response will be sent with a 422 HTTP status code.

#### [The `@error` Directive](#the-at-error-directive)

You may use the `@error` [Blade](/docs/13.x/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message:

```
 1<!-- /resources/views/post/create.blade.php -->

 2 

 3<label for="title">Post Title</label>

 4 

 5<input

 6    id="title"

 7    type="text"

 8    name="title"

 9    class="@error('title') is-invalid @enderror"

10/>

11 

12@error('title')

13    <div class="alert alert-danger">{{ $message }}</div>

14@enderror
```

If you are using [named error bags](#named-error-bags), you may pass the name of the error bag as the second argument to the `@error` directive:

```
1<input ... class="@error('title', 'post') is-invalid @enderror">
```

### [Repopulating Forms](#repopulating-forms)

When Laravel generates a redirect response due to a validation error, the framework will automatically [flash all of the request's input to the session](/docs/13.x/session#flash-data). This is done so that you may conveniently access the input during the next request and repopulate the form that the user attempted to submit.

To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/13.x/session):

```
1$title = $request->old('title');
```

Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/13.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned:

```
1<input type="text" name="title" value="{{ old('title') }}">
```

### [A Note on Optional Fields](#a-note-on-optional-fields)

By default, Laravel includes the `TrimStrings` and `ConvertEmptyStringsToNull` middleware in your application's global middleware stack. Because of this, you will often need to mark your "optional" request fields as `nullable` if you do not want the validator to consider `null` values as invalid. For example:

```
1$request->validate([

2    'title' => ['required', 'unique:posts', 'max:255'],

3    'body' => ['required'],

4    'publish_at' => ['nullable', 'date'],

5]);
```

In this example, we are specifying that the `publish_at` field may be either `null` or a valid date representation. If the `nullable` modifier is not added to the rule definition, the validator would consider `null` an invalid date.

### [Validation Error Response Format](#validation-error-response-format)

When your application throws a `Illuminate\Validation\ValidationException` exception and the incoming HTTP request is expecting a JSON response, Laravel will automatically format the error messages for you and return a `422 Unprocessable Entity` HTTP response.

Below, you can review an example of the JSON response format for validation errors. Note that nested error keys are flattened into "dot" notation format:

```
 1{

 2    "message": "The team name must be a string. (and 4 more errors)",

 3    "errors": {

 4        "team_name": [

 5            "The team name must be a string.",

 6            "The team name must be at least 1 characters."

 7        ],

 8        "authorization.role": [

 9            "The selected authorization.role is invalid."

10        ],

11        "users.0.email": [

12            "The users.0.email field is required."

13        ],

14        "users.2.email": [

15            "The users.2.email must be a valid email address."

16        ]

17    }

18}
```

## [Form Request Validation](#form-request-validation)

### [Creating Form Requests](#creating-form-requests)

For more complex validation scenarios, you may wish to create a "form request". Form requests are custom request classes that encapsulate their own validation and authorization logic. To create a form request class, you may use the `make:request` Artisan CLI command:

```
1php artisan make:request StorePostRequest
```

The generated form request class will be placed in the `app/Http/Requests` directory. If this directory does not exist, it will be created when you run the `make:request` command. Each form request generated by Laravel has two methods: `authorize` and `rules`.

As you might have guessed, the `authorize` method is responsible for determining if the currently authenticated user can perform the action represented by the request, while the `rules` method returns the validation rules that should apply to the request's data:

```
 1/**

 2 * Get the validation rules that apply to the request.

 3 *

 4 * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>

 5 */

 6public function rules(): array

 7{

 8    return [

 9        'title' => ['required', 'unique:posts', 'max:255'],

10        'body' => ['required'],

11    ];

12}
```

You may type-hint any dependencies you require within the `rules` method's signature. They will automatically be resolved via the Laravel [service container](/docs/13.x/container).

So, how are the validation rules evaluated? All you need to do is type-hint the request on your controller method. The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic:

```
 1/**

 2 * Store a new blog post.

 3 */

 4public function store(StorePostRequest $request): RedirectResponse

 5{

 6    // The incoming request is valid...

 7 

 8    // Retrieve the validated input data...

 9    $validated = $request->validated();

10 

11    // Retrieve a portion of the validated input data...

12    $validated = $request->safe()->only(['name', 'email']);

13    $validated = $request->safe()->except(['name', 'email']);

14 

15    // Store the blog post...

16 

17    return redirect('/posts');

18}
```

If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an XHR request, an HTTP response with a 422 status code will be returned to the user including a [JSON representation of the validation errors](#validation-error-response-format).

Need to add real-time form request validation to your Inertia powered Laravel frontend? Check out [Laravel Precognition](/docs/13.x/precognition).

#### [Performing Additional Validation](#performing-additional-validation-on-form-requests)

Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the form request's `after` method.

The `after` method should return an array of callables or closures which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary:

```
 1use Illuminate\Validation\Validator;

 2 

 3/**

 4 * Get the "after" validation callables for the request.

 5 */

 6public function after(): array

 7{

 8    return [

 9        function (Validator $validator) {

10            if ($this->somethingElseIsInvalid()) {

11                $validator->errors()->add(

12                    'field',

13                    'Something is wrong with this field!'

14                );

15            }

16        }

17    ];

18}
```

As noted, the array returned by the `after` method may also contain invokable classes. The `__invoke` method of these classes will receive an `Illuminate\Validation\Validator` instance:

```
 1use App\Validation\ValidateShippingTime;

 2use App\Validation\ValidateUserStatus;

 3use Illuminate\Validation\Validator;

 4 

 5/**

 6 * Get the "after" validation callables for the request.

 7 */

 8public function after(): array

 9{

10    return [

11        new ValidateUserStatus,

12        new ValidateShippingTime,

13        function (Validator $validator) {

14            //

15        }

16    ];

17}
```

#### [Stopping on the First Validation Failure](#request-stopping-on-first-validation-rule-failure)

By adding the `StopOnFirstFailure` attribute to your request class, you may inform the validator that it should stop validating all attributes once a single validation failure has occurred:

```
 1<?php

 2 

 3namespace App\Http\Requests;

 4 

 5use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;

 6use Illuminate\Foundation\Http\FormRequest;

 7 

 8#[StopOnFirstFailure]

 9class StorePostRequest extends FormRequest

10{

11    // ...

12}
```

#### [Failing on Unknown Fields](#request-failing-on-unknown-fields)

By adding the `FailOnUnknownFields` attribute to your request class, you may instruct Laravel to reject any incoming fields that are not defined by your request's validation rules:

```
 1<?php

 2 

 3namespace App\Http\Requests;

 4 

 5use Illuminate\Foundation\Http\Attributes\FailOnUnknownFields;

 6use Illuminate\Foundation\Http\FormRequest;

 7 

 8#[FailOnUnknownFields]

 9class StorePostRequest extends FormRequest

10{

11    public function rules(): array

12    {

13        return [

14            'title' => ['required', 'string'],

15            'body' => ['required', 'string'],

16        ];

17    }

18}
```

You may also enable this behavior globally for all form requests from your `AppServiceProvider`:

```
1use Illuminate\Foundation\Http\FormRequest;

2 

3/**

4 * Bootstrap any application services.

5 */

6public function boot(): void

7{

8    FormRequest::failOnUnknownFields();

9}
```

If needed, you may disable this behavior for a specific request by passing `false` to the attribute:

```
1#[FailOnUnknownFields(false)]

2class PublicWebhookRequest extends FormRequest

3{

4    // ...

5}
```

Rejecting unknown fields can provide additional protection against mass-assignment style issues by preventing unexpected input keys from flowing deeper into your application. However, you should still configure your model's `$fillable` / `$guarded` properties and only persist trusted, validated input.

#### [Customizing the Redirect Location](#customizing-the-redirect-location)

When form request validation fails, a redirect response will be generated to send the user back to their previous location. However, you are free to customize this behavior. To do so, you may use the `RedirectTo` attribute on your form request:

```
 1<?php

 2 

 3namespace App\Http\Requests;

 4 

 5use Illuminate\Foundation\Http\Attributes\RedirectTo;

 6use Illuminate\Foundation\Http\FormRequest;

 7 

 8#[RedirectTo('/dashboard')]

 9class StorePostRequest extends FormRequest

10{

11    // ...

12}
```

Or, if you would like to redirect users to a named route, you may use the `RedirectToRoute` attribute instead:

```
 1<?php

 2 

 3namespace App\Http\Requests;

 4 

 5use Illuminate\Foundation\Http\Attributes\RedirectToRoute;

 6use Illuminate\Foundation\Http\FormRequest;

 7 

 8#[RedirectToRoute('dashboard')]

 9class StorePostRequest extends FormRequest

10{

11    // ...

12}
```

#### [Customizing the Error Bag](#customizing-the-error-bag)

When form request validation fails, the errors are flashed to the `default` error bag. If you need to store the errors in a different [named error bag](#named-error-bags), you may use the `ErrorBag` attribute on your form request:

```
 1<?php

 2 

 3namespace App\Http\Requests;

 4 

 5use Illuminate\Foundation\Http\Attributes\ErrorBag;

 6use Illuminate\Foundation\Http\FormRequest;

 7 

 8#[ErrorBag('login')]

 9class LoginRequest extends FormRequest

10{

11    // ...

12}
```

### [Authorizing Form Requests](#authorizing-form-requests)

The form request class also contains an `authorize` method. Within this method, you may determine if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update. Most likely, you will interact with your [authorization gates and policies](/docs/13.x/authorization) within this method:

```
 1use App\Models\Comment;

 2 

 3/**

 4 * Determine if the user is authorized to make this request.

 5 */

 6public function authorize(): bool

 7{

 8    $comment = Comment::find($this->route('comment'));

 9 

10    return $comment && $this->user()->can('update', $comment);

11}
```

Since all form requests extend the base Laravel request class, we may use the `user` method to access the currently authenticated user. Also, note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below:

```
1Route::post('/comment/{comment}');
```

Therefore, if your application is taking advantage of [route model binding](/docs/13.x/routing#route-model-binding), your code may be made even more succinct by accessing the resolved model as a property of the request:

```
1return $this->user()->can('update', $this->comment);
```

If the `authorize` method returns `false`, an HTTP response with a 403 status code will automatically be returned and your controller method will not execute.

If you plan to handle authorization logic for the request in another part of your application, you may remove the `authorize` method completely, or simply return `true`:

```
1/**

2 * Determine if the user is authorized to make this request.

3 */

4public function authorize(): bool

5{

6    return true;

7}
```

You may type-hint any dependencies you need within the `authorize` method's signature. They will automatically be resolved via the Laravel [service container](/docs/13.x/container).

### [Customizing the Error Messages](#customizing-the-error-messages)

You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages:

```
 1/**

 2 * Get the error messages for the defined validation rules.

 3 *

 4 * @return array<string, string>

 5 */

 6public function messages(): array

 7{

 8    return [

 9        'title.required' => 'A title is required',

10        'body.required' => 'A message is required',

11    ];

12}
```

#### [Customizing the Validation Attributes](#customizing-the-validation-attributes)

Many of Laravel's built-in validation rule error messages contain an `:attribute` placeholder. If you would like the `:attribute` placeholder of your validation message to be replaced with a custom attribute name, you may specify the custom names by overriding the `attributes` method. This method should return an array of attribute / name pairs:

```
 1/**

 2 * Get custom attributes for validator errors.

 3 *

 4 * @return array<string, string>

 5 */

 6public function attributes(): array

 7{

 8    return [

 9        'email' => 'email address',

10    ];

11}
```

### [Preparing Input for Validation](#preparing-input-for-validation)

If you need to prepare or sanitize any data from the request before you apply your validation rules, you may use the `prepareForValidation` method:

```
 1use Illuminate\Support\Str;

 2 

 3/**

 4 * Prepare the data for validation.

 5 */

 6protected function prepareForValidation(): void

 7{

 8    $this->merge([

 9        'slug' => Str::slug($this->slug),

10    ]);

11}
```

Likewise, if you need to normalize any request data after validation is complete, you may use the `passedValidation` method:

```
1/**

2 * Handle a passed validation attempt.

3 */

4protected function passedValidation(): void

5{

6    $this->replace(['name' => 'Taylor']);

7}
```

## [Manually Creating Validators](#manually-creating-validators)

If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/13.x/facades). The `make` method on the facade generates a new validator instance:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Http\RedirectResponse;

 6use Illuminate\Http\Request;

 7use Illuminate\Support\Facades\Validator;

 8 

 9class PostController extends Controller

10{

11    /**

12     * Store a new blog post.

13     */

14    public function store(Request $request): RedirectResponse

15    {

16        $validator = Validator::make($request->all(), [

17            'title' => ['required', 'unique:posts', 'max:255'],

18            'body' => ['required'],

19        ]);

20 

21        if ($validator->fails()) {

22            return redirect('/post/create')

23                ->withErrors($validator)

24                ->withInput();

25        }

26 

27        // Retrieve the validated input...

28        $validated = $validator->validated();

29 

30        // Retrieve a portion of the validated input...

31        $validated = $validator->safe()->only(['name', 'email']);

32        $validated = $validator->safe()->except(['name', 'email']);

33 

34        // Store the blog post...

35 

36        return redirect('/posts');

37    }

38}
```

The first argument passed to the `make` method is the data under validation. The second argument is an array of the validation rules that should be applied to the data.

After determining whether the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`.

#### Stopping on First Validation Failure

The `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred:

```
1if ($validator->stopOnFirstFailure()->fails()) {

2    // ...

3}
```

### [Automatic Redirection](#automatic-redirection)

If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the HTTP request's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an XHR request, a [JSON response will be returned](#validation-error-response-format):

```
1Validator::make($request->all(), [

2    'title' => ['required', 'unique:posts', 'max:255'],

3    'body' => ['required'],

4])->validate();
```

You may use the `validateWithBag` method to store the error messages in a [named error bag](#named-error-bags) if validation fails:

```
1Validator::make($request->all(), [

2    'title' => ['required', 'unique:posts', 'max:255'],

3    'body' => ['required'],

4])->validateWithBag('post');
```

### [Named Error Bags](#named-error-bags)

If you have multiple forms on a single page, you may wish to name the `MessageBag` containing the validation errors, allowing you to retrieve the error messages for a specific form. To achieve this, pass a name as the second argument to `withErrors`:

```
1return redirect('/register')->withErrors($validator, 'login');
```

You may then access the named `MessageBag` instance from the `$errors` variable:

```
1{{ $errors->login->first('email') }}
```

### [Customizing the Error Messages](#manual-customizing-the-error-messages)

If needed, you may provide custom error messages that a validator instance should use instead of the default error messages provided by Laravel. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method:

```
1$validator = Validator::make($input, $rules, $messages = [

2    'required' => 'The :attribute field is required.',

3]);
```

In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example:

```
1$messages = [

2    'same' => 'The :attribute and :other must match.',

3    'size' => 'The :attribute must be exactly :size.',

4    'between' => 'The :attribute value :input is not between :min - :max.',

5    'in' => 'The :attribute must be one of the following types: :values',

6];
```

#### [Specifying a Custom Message for a Given Attribute](#specifying-a-custom-message-for-a-given-attribute)

Sometimes you may wish to specify a custom error message only for a specific attribute. You may do so using "dot" notation. Specify the attribute's name first, followed by the rule:

```
1$messages = [

2    'email.required' => 'We need to know your email address!',

3];
```

#### [Specifying Custom Attribute Values](#specifying-custom-attribute-values)

Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. To customize the values used to replace these placeholders for specific fields, you may pass an array of custom attributes as the fourth argument to the `Validator::make` method:

```
1$validator = Validator::make($input, $rules, $messages, [

2    'email' => 'email address',

3]);
```

### [Performing Additional Validation](#performing-additional-validation)

Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the validator's `after` method. The `after` method accepts a closure or an array of callables which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary:

```
 1use Illuminate\Support\Facades\Validator;

 2 

 3$validator = Validator::make(/* ... */);

 4 

 5$validator->after(function ($validator) {

 6    if ($this->somethingElseIsInvalid()) {

 7        $validator->errors()->add(

 8            'field', 'Something is wrong with this field!'

 9        );

10    }

11});

12 

13if ($validator->fails()) {

14    // ...

15}
```

As noted, the `after` method also accepts an array of callables, which is particularly convenient if your "after validation" logic is encapsulated in invokable classes, which will receive an `Illuminate\Validation\Validator` instance via their `__invoke` method:

```
 1use App\Validation\ValidateShippingTime;

 2use App\Validation\ValidateUserStatus;

 3 

 4$validator->after([

 5    new ValidateUserStatus,

 6    new ValidateShippingTime,

 7    function ($validator) {

 8        // ...

 9    },

10]);
```

## [Working With Validated Input](#working-with-validated-input)

After validating incoming request data using a form request or a manually created validator instance, you may wish to retrieve the incoming request data that actually underwent validation. This can be accomplished in several ways. First, you may call the `validated` method on a form request or validator instance. This method returns an array of the data that was validated:

```
1$validated = $request->validated();

2 

3$validated = $validator->validated();
```

Alternatively, you may call the `safe` method on a form request or validator instance. This method returns an instance of `Illuminate\Support\ValidatedInput`. This object exposes `only`, `except`, and `all` methods to retrieve a subset of the validated data or the entire array of validated data:

```
1$validated = $request->safe()->only(['name', 'email']);

2 

3$validated = $request->safe()->except(['name', 'email']);

4 

5$validated = $request->safe()->all();
```

In addition, the `Illuminate\Support\ValidatedInput` instance may be iterated over and accessed like an array:

```
1// Validated data may be iterated...

2foreach ($request->safe() as $key => $value) {

3    // ...

4}

5 

6// Validated data may be accessed as an array...

7$validated = $request->safe();

8 

9$email = $validated['email'];
```

If you would like to add additional fields to the validated data, you may call the `merge` method:

```
1$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

If you would like to retrieve the validated data as a [collection](/docs/13.x/collections) instance, you may call the `collect` method:

```
1$collection = $request->safe()->collect();
```

## [Working With Error Messages](#working-with-error-messages)

After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class.

#### [Retrieving the First Error Message for a Field](#retrieving-the-first-error-message-for-a-field)

To retrieve the first error message for a given field, use the `first` method:

```
1$errors = $validator->errors();

2 

3echo $errors->first('email');
```

#### [Retrieving All Error Messages for a Field](#retrieving-all-error-messages-for-a-field)

If you need to retrieve an array of all the messages for a given field, use the `get` method:

```
1foreach ($errors->get('email') as $message) {

2    // ...

3}
```

If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character:

```
1foreach ($errors->get('attachments.*') as $message) {

2    // ...

3}
```

#### [Retrieving All Error Messages for All Fields](#retrieving-all-error-messages-for-all-fields)

To retrieve an array of all messages for all fields, use the `all` method:

```
1foreach ($errors->all() as $message) {

2    // ...

3}
```

#### [Determining if Messages Exist for a Field](#determining-if-messages-exist-for-a-field)

The `has` method may be used to determine if any error messages exist for a given field:

```
1if ($errors->has('email')) {

2    // ...

3}
```

### [Specifying Custom Messages in Language Files](#specifying-custom-messages-in-language-files)

Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command.

Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application.

In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/13.x/localization).

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

#### [Custom Messages for Specific Attributes](#custom-messages-for-specific-attributes)

You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `lang/xx/validation.php` language file:

```
1'custom' => [

2    'email' => [

3        'required' => 'We need to know your email address!',

4        'max' => 'Your email address is too long!'

5    ],

6],
```

### [Specifying Attributes in Language Files](#specifying-attribute-in-language-files)

Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. If you would like the `:attribute` portion of your validation message to be replaced with a custom value, you may specify the custom attribute name in the `attributes` array of your `lang/xx/validation.php` language file:

```
1'attributes' => [

2    'email' => 'email address',

3],
```

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

### [Specifying Values in Language Files](#specifying-values-in-language-files)

Some of Laravel's built-in validation rule error messages contain a `:value` placeholder that is replaced with the current value of the request attribute. However, you may occasionally need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`:

```
1Validator::make($request->all(), [

2    'credit_card_number' => ['required_if:payment_type,cc']

3]);
```

If this validation rule fails, it will produce the following error message:

```
1The credit card number field is required when payment type is cc.
```

Instead of displaying `cc` as the payment type value, you may specify a more user-friendly value representation in your `lang/xx/validation.php` language file by defining a `values` array:

```
1'values' => [

2    'payment_type' => [

3        'cc' => 'credit card'

4    ],

5],
```

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

After defining this value, the validation rule will produce the following error message:

```
1The credit card number field is required when payment type is credit card.
```

## [Available Validation Rules](#available-validation-rules)

Below is a list of all available validation rules and their function:

#### Booleans

[Accepted](#rule-accepted) [Accepted If](#rule-accepted-if) [Boolean](#rule-boolean) [Declined](#rule-declined) [Declined If](#rule-declined-if)

#### Strings

[Active URL](#rule-active-url) [Alpha](#rule-alpha) [Alpha Dash](#rule-alpha-dash) [Alpha Numeric](#rule-alpha-num) [Ascii](#rule-ascii) [Confirmed](#rule-confirmed) [Current Password](#rule-current-password) [Different](#rule-different) [Doesnt Start With](#rule-doesnt-start-with) [Doesnt End With](#rule-doesnt-end-with) [Email](#rule-email) [Ends With](#rule-ends-with) [Enum](#rule-enum) [Hex Color](#rule-hex-color) [In](#rule-in) [IP Address](#rule-ip) [JSON](#rule-json) [Lowercase](#rule-lowercase) [MAC Address](#rule-mac) [Max](#rule-max) [Min](#rule-min) [Not In](#rule-not-in) [Regular Expression](#rule-regex) [Not Regular Expression](#rule-not-regex) [Same](#rule-same) [Size](#rule-size) [Starts With](#rule-starts-with) [String](#rule-string) [Uppercase](#rule-uppercase) [URL](#rule-url) [ULID](#rule-ulid) [UUID](#rule-uuid)

#### Numbers

[Between](#rule-between) [Decimal](#rule-decimal) [Different](#rule-different) [Digits](#rule-digits) [Digits Between](#rule-digits-between) [Greater Than](#rule-gt) [Greater Than Or Equal](#rule-gte) [Integer](#rule-integer) [Less Than](#rule-lt) [Less Than Or Equal](#rule-lte) [Max](#rule-max) [Max Digits](#rule-max-digits) [Min](#rule-min) [Min Digits](#rule-min-digits) [Multiple Of](#rule-multiple-of) [Numeric](#rule-numeric) [Same](#rule-same) [Size](#rule-size)

#### Arrays

[Array](#rule-array) [Between](#rule-between) [Contains](#rule-contains) [Doesnt Contain](#rule-doesnt-contain) [Distinct](#rule-distinct) [In Array](#rule-in-array) [In Array Keys](#rule-in-array-keys) [List](#rule-list) [Max](#rule-max) [Min](#rule-min) [Size](#rule-size)

#### Dates

[After](#rule-after) [After Or Equal](#rule-after-or-equal) [Before](#rule-before) [Before Or Equal](#rule-before-or-equal) [Date](#rule-date) [Date Equals](#rule-date-equals) [Date Format](#rule-date-format) [Different](#rule-different) [Timezone](#rule-timezone)

#### Files

[Between](#rule-between) [Dimensions](#rule-dimensions) [Encoding](#rule-encoding) [Extensions](#rule-extensions) [File](#rule-file) [Image](#rule-image) [Max](#rule-max) [Min](#rule-min) [MIME Types](#rule-mimetypes) [MIME Type By File Extension](#rule-mimes) [Size](#rule-size)

#### Database

[Exists](#rule-exists) [Unique](#rule-unique)

#### Utilities

[Any Of](#rule-anyof) [Bail](#rule-bail) [Exclude](#rule-exclude) [Exclude If](#rule-exclude-if) [Exclude Unless](#rule-exclude-unless) [Exclude With](#rule-exclude-with) [Exclude Without](#rule-exclude-without) [Filled](#rule-filled) [Missing](#rule-missing) [Missing If](#rule-missing-if) [Missing Unless](#rule-missing-unless) [Missing With](#rule-missing-with) [Missing With All](#rule-missing-with-all) [Nullable](#rule-nullable) [Present](#rule-present) [Present If](#rule-present-if) [Present Unless](#rule-present-unless) [Present With](#rule-present-with) [Present With All](#rule-present-with-all) [Prohibited](#rule-prohibited) [Prohibited If](#rule-prohibited-if) [Prohibited If Accepted](#rule-prohibited-if-accepted) [Prohibited If Declined](#rule-prohibited-if-declined) [Prohibited Unless](#rule-prohibited-unless) [Prohibits](#rule-prohibits) [Required](#rule-required) [Required If](#rule-required-if) [Required If Accepted](#rule-required-if-accepted) [Required If Declined](#rule-required-if-declined) [Required Unless](#rule-required-unless) [Required With](#rule-required-with) [Required With All](#rule-required-with-all) [Required Without](#rule-required-without) [Required Without All](#rule-required-without-all) [Required Array Keys](#rule-required-array-keys) [Sometimes](#validating-when-present)

#### [accepted](#rule-accepted)

The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. This is useful for validating "Terms of Service" acceptance or similar fields.

#### [accepted_if:anotherfield,value,...](#rule-accepted-if)

The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"` if another field under validation is equal to a specified value. This is useful for validating "Terms of Service" acceptance or similar fields.

#### [active_url](#rule-active-url)

The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function. The hostname of the provided URL is extracted using the `parse_url` PHP function before being passed to `dns_get_record`.

#### [after:*date*](#rule-after)

The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function in order to be converted to a valid `DateTime` instance:

```
1'start_date' => ['required', 'date', 'after:tomorrow']
```

Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date:

```
1'finish_date' => ['required', 'date', 'after:start_date']
```

For convenience, date-based rules may be constructed using the fluent `date` rule builder:

```
1use Illuminate\Validation\Rule;

2 

3'start_date' => [

4    'required',

5    Rule::date()->after(today()->addDays(7)),

6],
```

The `afterToday` and `todayOrAfter` methods may be used to fluently express the date and must be after today, or today or after, respectively:

```
1'start_date' => [

2    'required',

3    Rule::date()->afterToday(),

4],
```

#### [after_or_equal:*date*](#rule-after-or-equal)

The field under validation must be a value after or equal to the given date. For more information, see the [after](#rule-after) rule.

For convenience, date-based rules may be constructed using the fluent `date` rule builder:

```
1use Illuminate\Validation\Rule;

2 

3'start_date' => [

4    'required',

5    Rule::date()->afterOrEqual(today()->addDays(7)),

6],
```

#### [anyOf](#rule-anyof)

The `Rule::anyOf` validation rule allows you to specify that the field under validation must satisfy any of the given validation rulesets. For example, the following rule will validate that the `username` field is either an email address or an alpha-numeric string (including dashes) that is at least 6 characters long:

```
1use Illuminate\Validation\Rule;

2 

3'username' => [

4    'required',

5    Rule::anyOf([

6        ['string', 'email'],

7        ['string', 'alpha_dash', 'min:6'],

8    ]),

9],
```

#### [alpha](#rule-alpha)

The field under validation must be entirely Unicode alphabetic characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) and [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=).

To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule:

```
1'username' => ['alpha:ascii'],
```

#### [alpha_dash](#rule-alpha-dash)

The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), as well as ASCII dashes (`-`) and ASCII underscores (`_`).

To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule:

```
1'username' => ['alpha_dash:ascii'],
```

#### [alpha_num](#rule-alpha-num)

The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), and [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=).

To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule:

```
1'username' => ['alpha_num:ascii'],
```

#### [array](#rule-array)

The field under validation must be a PHP `array`.

When additional values are provided to the `array` rule, each key in the input array must be present within the list of values provided to the rule. In the following example, the `admin` key in the input array is invalid since it is not contained in the list of values provided to the `array` rule:

```
 1use Illuminate\Support\Facades\Validator;

 2 

 3$input = [

 4    'user' => [

 5        'name' => 'Taylor Otwell',

 6        'username' => 'taylorotwell',

 7        'admin' => true,

 8    ],

 9];

10 

11Validator::make($input, [

12    'user' => ['array:name,username'],

13]);
```

In general, you should always specify the array keys that are allowed to be present within your array.

#### [ascii](#rule-ascii)

The field under validation must be entirely 7-bit ASCII characters.

#### [bail](#rule-bail)

Stop running validation rules for the field after the first validation failure.

While the `bail` rule will only stop validating a specific field when it encounters a validation failure, the `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred:

```
1if ($validator->stopOnFirstFailure()->fails()) {

2    // ...

3}
```

#### [before:*date*](#rule-before)

The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [after](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`.

For convenience, date-based rules may also be constructed using the fluent `date` rule builder:

```
1use Illuminate\Validation\Rule;

2 

3'start_date' => [

4    'required',

5    Rule::date()->before(today()->subDays(7)),

6],
```

The `beforeToday` and `todayOrBefore` methods may be used to fluently express the date and must be before today, or today or before, respectively:

```
1'start_date' => [

2    'required',

3    Rule::date()->beforeToday(),

4],
```

#### [before_or_equal:*date*](#rule-before-or-equal)

The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [after](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`.

For convenience, date-based rules may also be constructed using the fluent `date` rule builder:

```
1use Illuminate\Validation\Rule;

2 

3'start_date' => [

4    'required',

5    Rule::date()->beforeOrEqual(today()->subDays(7)),

6],
```

#### [between:*min*,*max*](#rule-between)

The field under validation must have a size between the given *min* and *max* (inclusive). Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule.

#### [boolean](#rule-boolean)

The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`.

You may use the `strict` parameter to only consider the field valid if its value is `true` or `false`:

```
1'foo' => ['boolean:strict']
```

#### [confirmed](#rule-confirmed)

The field under validation must have a matching field of `{field}_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input.

You may also pass a custom confirmation field name. For example, `confirmed:repeat_username` will expect the field `repeat_username` to match the field under validation.

#### [contains:*foo*,*bar*,...](#rule-contains)

The field under validation must be an array that contains all of the given parameter values. Since this rule often requires you to `implode` an array, the `Rule::contains` method may be used to fluently construct the rule:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($data, [

 5    'roles' => [

 6        'required',

 7        'array',

 8        Rule::contains(['admin', 'editor']),

 9    ],

10]);
```

#### [doesnt_contain:*foo*,*bar*,...](#rule-doesnt-contain)

The field under validation must be an array that does not contain any of the given parameter values. Since this rule often requires you to `implode` an array, the `Rule::doesntContain` method may be used to fluently construct the rule:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($data, [

 5    'roles' => [

 6        'required',

 7        'array',

 8        Rule::doesntContain(['admin', 'editor']),

 9    ],

10]);
```

#### [current_password](#rule-current-password)

The field under validation must match the authenticated user's password. You may specify an [authentication guard](/docs/13.x/authentication) using the rule's first parameter:

```
1'password' => ['current_password:api']
```

#### [date](#rule-date)

The field under validation must be a valid, non-relative date according to the `strtotime` PHP function.

#### [date_equals:*date*](#rule-date-equals)

The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance.

#### [date_format:*format*,...](#rule-date-format)

The field under validation must match one of the given *formats*. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class.

For convenience, date-based rules may be constructed using the fluent `date` rule builder:

```
1use Illuminate\Validation\Rule;

2 

3'start_date' => [

4    'required',

5    Rule::date()->format('Y-m-d'),

6],
```

#### [decimal:*min*,*max*](#rule-decimal)

The field under validation must be numeric and must contain the specified number of decimal places:

```
1// Must have exactly two decimal places (9.99)...

2'price' => ['decimal:2']

3 

4// Must have between 2 and 4 decimal places...

5'price' => ['decimal:2,4']
```

#### [declined](#rule-declined)

The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

#### [declined_if:anotherfield,value,...](#rule-declined-if)

The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"` if another field under validation is equal to a specified value.

#### [different:*field*](#rule-different)

The field under validation must have a different value than *field*.

#### [digits:*value*](#rule-digits)

The integer under validation must have an exact length of *value*.

#### [digits_between:*min*,*max*](#rule-digits-between)

The integer under validation must have a length between the given *min* and *max*.

#### [dimensions](#rule-dimensions)

The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters:

```
1'avatar' => ['dimensions:min_width=100,min_height=200']
```

Available constraints are: *min_width*, *max_width*, *min_height*, *max_height*, *width*, *height*, *ratio*, *min_ratio*, *max_ratio*.

A *ratio* constraint should be represented as width divided by height. This can be specified either by a fraction like `3/2` or a float like `1.5`:

```
1'avatar' => ['dimensions:ratio=3/2']
```

The *min_ratio* and *max_ratio* constraints may be used to define a range of acceptable aspect ratios:

```
1'avatar' => ['dimensions:min_ratio=1/2,max_ratio=3/2']
```

Since this rule requires several arguments, it is often more convenient to use the `Rule::dimensions` method to fluently construct the rule:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($data, [

 5    'avatar' => [

 6        'required',

 7        Rule::dimensions()

 8            ->maxWidth(1000)

 9            ->maxHeight(500)

10            ->ratio(3 / 2),

11    ],

12]);
```

You may also use the `minRatio`, `maxRatio`, and `ratioBetween` methods to fluently define ratio constraints:

```
1Rule::dimensions()->ratioBetween(min: 1 / 2, max: 3 / 2)
```

#### [distinct](#rule-distinct)

When validating arrays, the field under validation must not have any duplicate values:

```
1'foo.*.id' => ['distinct']
```

Distinct uses loose variable comparisons by default. To use strict comparisons, you may add the `strict` parameter to your validation rule definition:

```
1'foo.*.id' => ['distinct:strict']
```

You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences:

```
1'foo.*.id' => ['distinct:ignore_case']
```

#### [doesnt_start_with:*foo*,*bar*,...](#rule-doesnt-start-with)

The field under validation must not start with one of the given values.

#### [doesnt_end_with:*foo*,*bar*,...](#rule-doesnt-end-with)

The field under validation must not end with one of the given values.

#### [email](#rule-email)

The field under validation must be formatted as an email address. This validation rule utilizes the [egulias/email-validator](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well:

```
1'email' => ['email:rfc,dns']
```

The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply:

- `rfc`: `RFCValidation` - Validate the email address according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs).
- `strict`: `NoRFCWarningsValidation` - Validate the email according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs), failing when warnings are found (e.g. trailing periods and multiple consecutive periods).
- `dns`: `DNSCheckValidation` - Ensure the email address's domain has a valid MX record.
- `spoof`: `SpoofCheckValidation` - Ensure the email address does not contain homograph or deceptive Unicode characters.
- `filter`: `FilterEmailValidation` - Ensure the email address is valid according to PHP's `filter_var` function.
- `filter_unicode`: `FilterEmailValidation::unicode()` - Ensure the email address is valid according to PHP's `filter_var` function, allowing some Unicode characters.

For convenience, email validation rules may be built using the fluent rule builder:

```
 1use Illuminate\Validation\Rule;

 2 

 3$request->validate([

 4    'email' => [

 5        'required',

 6        Rule::email()

 7            ->rfcCompliant(strict: false)

 8            ->validateMxRecord()

 9            ->preventSpoofing()

10    ],

11]);
```

The `dns` and `spoof` validators require the PHP `intl` extension.

#### [encoding:*encoding_type*](#rule-encoding)

The field under validation must match the specified character encoding. This rule uses PHP's `mb_check_encoding` function to verify the encoding of the given file or string value. For convenience, the `encoding` rule may be constructed using Laravel's fluent file rule builder:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rules\File;

 3 

 4Validator::validate($input, [

 5    'attachment' => [

 6        'required',

 7        File::types(['csv'])

 8            ->encoding('utf-8'),

 9    ],

10]);
```

#### [ends_with:*foo*,*bar*,...](#rule-ends-with)

The field under validation must end with one of the given values.

#### [enum](#rule-enum)

The `Enum` rule is a class-based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument. When validating primitive values, a backed Enum should be provided to the `Enum` rule:

```
1use App\Enums\ServerStatus;

2use Illuminate\Validation\Rule;

3 

4$request->validate([

5    'status' => [Rule::enum(ServerStatus::class)],

6]);
```

The `Enum` rule's `only` and `except` methods may be used to limit which enum cases should be considered valid:

```
1Rule::enum(ServerStatus::class)

2    ->only([ServerStatus::Pending, ServerStatus::Active]);

3 

4Rule::enum(ServerStatus::class)

5    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

The `when` method may be used to conditionally modify the `Enum` rule:

```
1use Illuminate\Support\Facades\Auth;

2use Illuminate\Validation\Rule;

3 

4Rule::enum(ServerStatus::class)

5    ->when(

6        Auth::user()->isAdmin(),

7        fn ($rule) => $rule->only(...),

8        fn ($rule) => $rule->only(...),

9    );
```

#### [exclude](#rule-exclude)

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods.

#### [exclude_if:*anotherfield*,*value*](#rule-exclude-if)

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the *anotherfield* field is equal to *value*.

If complex conditional exclusion logic is required, you may utilize the `Rule::excludeIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be excluded:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($request->all(), [

 5    'role_id' => [Rule::excludeIf($request->user()->is_admin)],

 6]);

 7 

 8Validator::make($request->all(), [

 9    'role_id' => [Rule::excludeIf(fn () => $request->user()->is_admin)],

10]);
```

#### [exclude_unless:*anotherfield*,*value*](#rule-exclude-unless)

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods unless *anotherfield*'s field is equal to *value*. If *value* is `null` (`exclude_unless:name,null`), the field under validation will be excluded unless the comparison field is `null` or the comparison field is missing from the request data.

If complex conditional exclusion logic is required, you may utilize the `Rule::excludeUnless` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should not be excluded:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($request->all(), [

 5    'role_id' => [Rule::excludeUnless($request->user()->is_admin)],

 6]);

 7 

 8Validator::make($request->all(), [

 9    'role_id' => [Rule::excludeUnless(fn () => $request->user()->is_admin)],

10]);
```

#### [exclude_with:*anotherfield*](#rule-exclude-with)

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the *anotherfield* field is present.

#### [exclude_without:*anotherfield*](#rule-exclude-without)

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the *anotherfield* field is not present.

#### [exists:*table*,*column*](#rule-exists)

The field under validation must exist in a given database table.

#### [Basic Usage of Exists Rule](#basic-usage-of-exists-rule)

```
1'state' => ['exists:states']
```

If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value.

#### [Specifying a Custom Column Name](#specifying-a-custom-column-name)

You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name:

```
1'state' => ['exists:states,abbreviation']
```

Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name:

```
1'email' => ['exists:connection.staff,email']
```

Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name:

```
1'user_id' => ['exists:App\Models\User,id']
```

If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule.

```
 1use Illuminate\Database\Query\Builder;

 2use Illuminate\Support\Facades\Validator;

 3use Illuminate\Validation\Rule;

 4 

 5Validator::make($data, [

 6    'email' => [

 7        'required',

 8        Rule::exists('staff')->where(function (Builder $query) {

 9            $query->where('account_id', 1);

10        }),

11    ],

12]);
```

You may explicitly specify the database column name that should be used by the `exists` rule generated by the `Rule::exists` method by providing the column name as the second argument to the `exists` method:

```
1'state' => [Rule::exists('states', 'abbreviation')],
```

Sometimes, you may wish to validate whether an array of values exists in the database. You can do so by adding both the `exists` and [array](#rule-array) rules to the field being validated:

```
1'states' => ['array', Rule::exists('states', 'abbreviation')],
```

When both of these rules are assigned to a field, Laravel will automatically build a single query to determine if all of the given values exist in the specified table.

#### [extensions:*foo*,*bar*,...](#rule-extensions)

The file under validation must have a user-assigned extension corresponding to one of the listed extensions:

```
1'photo' => ['required', 'extensions:jpg,png'],
```

You should never rely on validating a file by its user-assigned extension alone. This rule should typically always be used in combination with the [mimes](#rule-mimes) or [mimetypes](#rule-mimetypes) rules.

#### [file](#rule-file)

The field under validation must be a successfully uploaded file.

#### [filled](#rule-filled)

The field under validation must not be empty when it is present.

#### [gt:*field*](#rule-gt)

The field under validation must be greater than the given *field* or *value*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

#### [gte:*field*](#rule-gte)

The field under validation must be greater than or equal to the given *field* or *value*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

#### [hex_color](#rule-hex-color)

The field under validation must contain a valid color value in [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) format.

#### [image](#rule-image)

The file under validation must be an image (jpg, jpeg, png, bmp, gif, or webp).

By default, the image rule does not allow SVG files due to the possibility of XSS vulnerabilities. If you need to allow SVG files, you may provide the `allow_svg` directive to the `image` rule (`image:allow_svg`).

#### [in:*foo*,*bar*,...](#rule-in)

The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule:

```
1use Illuminate\Support\Facades\Validator;

2use Illuminate\Validation\Rule;

3 

4Validator::make($data, [

5    'zones' => [

6        'required',

7        Rule::in(['first-zone', 'second-zone']),

8    ],

9]);
```

When the `in` rule is combined with the `array` rule, each value in the input array must be present within the list of values provided to the `in` rule. In the following example, the `LAS` airport code in the input array is invalid since it is not contained in the list of airports provided to the `in` rule:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4$input = [

 5    'airports' => ['NYC', 'LAS'],

 6];

 7 

 8Validator::make($input, [

 9    'airports' => [

10        'required',

11        'array',

12    ],

13    'airports.*' => Rule::in(['NYC', 'LIT']),

14]);
```

#### [in_array:*anotherfield*.*](#rule-in-array)

The field under validation must exist in *anotherfield*'s values.

#### [in_array_keys:*value*.*](#rule-in-array-keys)

The field under validation must be an array having at least one of the given *values* as a key within the array:

```
1'config' => ['array', 'in_array_keys:timezone']
```

#### [integer](#rule-integer)

The field under validation must be an integer.

You may use the `strict` parameter to only consider the field valid if its type is `integer`. Strings with integer values will be considered invalid:

```
1'age' => ['integer:strict']
```

This validation rule does not verify that the input is of the "integer" variable type, only that the input is of a type accepted by PHP's `FILTER_VALIDATE_INT` rule. If you need to validate the input as being a number please use this rule in combination with [the `numeric` validation rule](#rule-numeric).

#### [ip](#rule-ip)

The field under validation must be an IP address.

#### [ipv4](#ipv4)

The field under validation must be an IPv4 address.

#### [ipv6](#ipv6)

The field under validation must be an IPv6 address.

#### [json](#rule-json)

The field under validation must be a valid JSON string.

#### [lt:*field*](#rule-lt)

The field under validation must be less than the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

#### [lte:*field*](#rule-lte)

The field under validation must be less than or equal to the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

#### [lowercase](#rule-lowercase)

The field under validation must be lowercase.

#### [list](#rule-list)

The field under validation must be an array that is a list. An array is considered a list if its keys consist of consecutive numbers from 0 to `count($array) - 1`.

#### [mac_address](#rule-mac)

The field under validation must be a MAC address.

#### [max:*value*](#rule-max)

The field under validation must be less than or equal to a maximum *value*. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule.

#### [max_digits:*value*](#rule-max-digits)

The integer under validation must have a maximum length of *value*.

#### [mimetypes:*text/plain*,...](#rule-mimetypes)

The file under validation must match one of the given MIME types:

```
1'video' => ['mimetypes:video/avi,video/mpeg,video/quicktime'],

2 

3'media' => ['mimetypes:image/*,video/*'],
```

To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type.

#### [mimes:*foo*,*bar*,...](#rule-mimes)

The file under validation must have a MIME type corresponding to one of the listed extensions:

```
1'photo' => ['mimes:jpg,bmp,png']
```

Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location:

<https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types>

#### [MIME Types and Extensions](#mime-types-and-extensions)

This validation rule does not verify agreement between the MIME type and the extension the user assigned to the file. For example, the `mimes:png` validation rule would consider a file containing valid PNG content to be a valid PNG image, even if the file is named `photo.txt`. If you would like to validate the user-assigned extension of the file, you may use the [extensions](#rule-extensions) rule.

#### [min:*value*](#rule-min)

The field under validation must have a minimum *value*. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule.

#### [min_digits:*value*](#rule-min-digits)

The integer under validation must have a minimum length of *value*.

#### [multiple_of:*value*](#rule-multiple-of)

The field under validation must be a multiple of *value*.

#### [missing](#rule-missing)

The field under validation must not be present in the input data.

#### [missing_if:*anotherfield*,*value*,...](#rule-missing-if)

The field under validation must not be present if the *anotherfield* field is equal to any *value*.

#### [missing_unless:*anotherfield*,*value*](#rule-missing-unless)

The field under validation must not be present unless the *anotherfield* field is equal to any *value*.

#### [missing_with:*foo*,*bar*,...](#rule-missing-with)

The field under validation must not be present *only if* any of the other specified fields are present.

#### [missing_with_all:*foo*,*bar*,...](#rule-missing-with-all)

The field under validation must not be present *only if* all of the other specified fields are present.

#### [not_in:*foo*,*bar*,...](#rule-not-in)

The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule:

```
1use Illuminate\Validation\Rule;

2 

3Validator::make($data, [

4    'toppings' => [

5        'required',

6        Rule::notIn(['sprinkles', 'cherries']),

7    ],

8]);
```

#### [not_regex:*pattern*](#rule-not-regex)

The field under validation must not match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => ['not_regex:/^.+$/i']`.

#### [nullable](#rule-nullable)

The field under validation may be `null`.

#### [numeric](#rule-numeric)

The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php).

You may use the `strict` parameter to only consider the field valid if its value is an integer or float type. Numeric strings will be considered invalid:

```
1'amount' => ['numeric:strict']
```

#### [present](#rule-present)

The field under validation must exist in the input data.

#### [present_if:*anotherfield*,*value*,...](#rule-present-if)

The field under validation must be present if the *anotherfield* field is equal to any *value*.

#### [present_unless:*anotherfield*,*value*](#rule-present-unless)

The field under validation must be present unless the *anotherfield* field is equal to any *value*.

#### [present_with:*foo*,*bar*,...](#rule-present-with)

The field under validation must be present *only if* any of the other specified fields are present.

#### [present_with_all:*foo*,*bar*,...](#rule-present-with-all)

The field under validation must be present *only if* all of the other specified fields are present.

#### [prohibited](#rule-prohibited)

The field under validation must be missing or empty. A field is "empty" if it meets one of the following criteria:

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

#### [prohibited_if:*anotherfield*,*value*,...](#rule-prohibited-if)

The field under validation must be missing or empty if the *anotherfield* field is equal to any *value*. A field is "empty" if it meets one of the following criteria:

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be prohibited:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($request->all(), [

 5    'role_id' => [Rule::prohibitedIf($request->user()->is_admin)],

 6]);

 7 

 8Validator::make($request->all(), [

 9    'role_id' => [Rule::prohibitedIf(fn () => $request->user()->is_admin)],

10]);
```

#### [prohibited_if_accepted:*anotherfield*,...](#rule-prohibited-if-accepted)

The field under validation must be missing or empty if the *anotherfield* field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`.

#### [prohibited_if_declined:*anotherfield*,...](#rule-prohibited-if-declined)

The field under validation must be missing or empty if the *anotherfield* field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

#### [prohibited_unless:*anotherfield*,*value*,...](#rule-prohibited-unless)

The field under validation must be missing or empty unless the *anotherfield* field is equal to any *value*. A field is "empty" if it meets one of the following criteria:

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedUnless` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should not be prohibited:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($request->all(), [

 5    'role_id' => [Rule::prohibitedUnless($request->user()->is_admin)],

 6]);

 7 

 8Validator::make($request->all(), [

 9    'role_id' => [Rule::prohibitedUnless(fn () => $request->user()->is_admin)],

10]);
```

#### [prohibits:*anotherfield*,...](#rule-prohibits)

If the field under validation is not missing or empty, all fields in *anotherfield* must be missing or empty. A field is "empty" if it meets one of the following criteria:

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

#### [regex:*pattern*](#rule-regex)

The field under validation must match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => ['regex:/^.+@.+$/i']`.

#### [required](#rule-required)

The field under validation must be present in the input data and not empty. A field is "empty" if it meets one of the following criteria:

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with no path.

#### [required_if:*anotherfield*,*value*,...](#rule-required-if)

The field under validation must be present and not empty if the *anotherfield* field is equal to any *value*.

If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($request->all(), [

 5    'role_id' => [Rule::requiredIf($request->user()->is_admin)],

 6]);

 7 

 8Validator::make($request->all(), [

 9    'role_id' => [Rule::requiredIf(fn () => $request->user()->is_admin)],

10]);
```

#### [required_if_accepted:*anotherfield*,...](#rule-required-if-accepted)

The field under validation must be present and not empty if the *anotherfield* field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`.

#### [required_if_declined:*anotherfield*,...](#rule-required-if-declined)

The field under validation must be present and not empty if the *anotherfield* field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

#### [required_unless:*anotherfield*,*value*,...](#rule-required-unless)

The field under validation must be present and not empty unless the *anotherfield* field is equal to any *value*. This also means *anotherfield* must be present in the request data unless *value* is `null`. If *value* is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data.

If you would like to construct a more complex condition for the `required_unless` rule, you may use the `Rule::requiredUnless` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is not required:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3 

 4Validator::make($request->all(), [

 5    'role_id' => [Rule::requiredUnless($request->user()->is_admin)],

 6]);

 7 

 8Validator::make($request->all(), [

 9    'role_id' => [Rule::requiredUnless(fn () => $request->user()->is_admin)],

10]);
```

#### [required_with:*foo*,*bar*,...](#rule-required-with)

The field under validation must be present and not empty *only if* any of the other specified fields are present and not empty.

#### [required_with_all:*foo*,*bar*,...](#rule-required-with-all)

The field under validation must be present and not empty *only if* all of the other specified fields are present and not empty.

#### [required_without:*foo*,*bar*,...](#rule-required-without)

The field under validation must be present and not empty *only when* any of the other specified fields are empty or not present.

#### [required_without_all:*foo*,*bar*,...](#rule-required-without-all)

The field under validation must be present and not empty *only when* all of the other specified fields are empty or not present.

#### [required_array_keys:*foo*,*bar*,...](#rule-required-array-keys)

The field under validation must be an array and must contain at least the specified keys.

#### [same:*field*](#rule-same)

The given *field* must match the field under validation.

#### [size:*value*](#rule-size)

The field under validation must have a size matching the given *value*. For string data, *value* corresponds to the number of characters. For numeric data, *value* corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, *size* corresponds to the `count` of the array. For files, *size* corresponds to the file size in kilobytes. Let's look at some examples:

```
 1// Validate that a string is exactly 12 characters long...

 2'title' => ['size:12'];

 3 

 4// Validate that a provided integer equals 10...

 5'seats' => ['integer', 'size:10'];

 6 

 7// Validate that an array has exactly 5 elements...

 8'tags' => ['array', 'size:5'];

 9 

10// Validate that an uploaded file is exactly 512 kilobytes...

11'image' => ['file', 'size:512'];
```

#### [starts_with:*foo*,*bar*,...](#rule-starts-with)

The field under validation must start with one of the given values.

#### [string](#rule-string)

The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field.

For convenience, string validation rules may also be constructed using the fluent `Rule::string()` rule builder:

```
1use Illuminate\Validation\Rule;

2 

3'title' => [

4    'required',

5    Rule::string()

6        ->min(3)

7        ->max(255)

8        ->alphaDash(ascii: true),

9],
```

The string rule builder provides methods for common string constraints, including `alpha`, `alphaDash`, `alphaNumeric`, `ascii`, `between`, `doesntEndWith`, `doesntStartWith`, `endsWith`, `exactly`, `lowercase`, `max`, `min`, `startsWith`, and `uppercase`. Since the rule builder is conditionable, you may also use the `when` and `unless` methods to conditionally apply constraints.

#### [timezone](#rule-timezone)

The field under validation must be a valid timezone identifier according to the `DateTimeZone::listIdentifiers` method.

The arguments [accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php) may also be provided to this validation rule:

```
1'timezone' => ['required', 'timezone:all'];

2 

3'timezone' => ['required', 'timezone:Africa'];

4 

5'timezone' => ['required', 'timezone:per_country,US'];
```

#### [unique:*table*,*column*](#rule-unique)

The field under validation must not exist within the given database table.

**Specifying a Custom Table / Column Name:**

Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name:

```
1'email' => ['unique:App\Models\User,email_address']
```

The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used.

```
1'email' => ['unique:users,email_address']
```

**Specifying a Custom Database Connection**

Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name:

```
1'email' => ['unique:connection.users,email_address']
```

**Forcing a Unique Rule to Ignore a Given ID:**

Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question.

To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule.

```
1use Illuminate\Support\Facades\Validator;

2use Illuminate\Validation\Rule;

3 

4Validator::make($data, [

5    'email' => [

6        'required',

7        Rule::unique('users')->ignore($user->id),

8    ],

9]);
```

You should never pass any user controlled request input into the `ignore` method. Instead, you should only pass a system generated unique ID such as an auto-incrementing ID or UUID from an Eloquent model instance. Otherwise, your application will be vulnerable to an SQL injection attack.

Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model:

```
1Rule::unique('users')->ignore($user)
```

If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method:

```
1Rule::unique('users')->ignore($user->id, 'user_id')
```

By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method:

```
1Rule::unique('users', 'email_address')->ignore($user->id)
```

**Adding Additional Where Clauses:**

You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`:

```
1'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Ignoring Soft Deleted Records in Unique Checks:**

By default, the unique rule includes soft deleted records when determining uniqueness. To exclude soft deleted records from the uniqueness check, you may invoke the `withoutTrashed` method:

```
1Rule::unique('users')->withoutTrashed();
```

If your model uses a column name other than `deleted_at` for soft deleted records, you may provide the column name when invoking the `withoutTrashed` method:

```
1Rule::unique('users')->withoutTrashed('was_deleted_at');
```

#### [uppercase](#rule-uppercase)

The field under validation must be uppercase.

#### [url](#rule-url)

The field under validation must be a valid URL.

If you would like to specify the URL protocols that should be considered valid, you may pass the protocols as validation rule parameters:

```
1'url' => ['url:http,https'],

2 

3'game' => ['url:minecraft,steam'],
```

#### [ulid](#rule-ulid)

The field under validation must be a valid [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID).

#### [uuid](#rule-uuid)

The field under validation must be a valid RFC 9562 (version 1, 3, 4, 5, 6, 7, or 8) universally unique identifier (UUID).

You may also validate that the given UUID matches a UUID specification by version:

```
1'uuid' => ['uuid:4']
```

## [Conditionally Adding Rules](#conditionally-adding-rules)

#### [Skipping Validation When Fields Have Certain Values](#skipping-validation-when-fields-have-certain-values)

You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`:

```
1use Illuminate\Support\Facades\Validator;

2 

3$validator = Validator::make($data, [

4    'has_appointment' => ['required', 'boolean'],

5    'appointment_date' => ['exclude_if:has_appointment,false', 'required', 'date'],

6    'doctor_name' => ['exclude_if:has_appointment,false', 'required', 'string'],

7]);
```

Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value:

```
1$validator = Validator::make($data, [

2    'has_appointment' => ['required', 'boolean'],

3    'appointment_date' => ['exclude_unless:has_appointment,true', 'required', 'date'],

4    'doctor_name' => ['exclude_unless:has_appointment,true', 'required', 'string'],

5]);
```

#### [Validating When Present](#validating-when-present)

In some situations, you may wish to run validation checks against a field **only** if that field is present in the data being validated. To quickly accomplish this, add the `sometimes` rule to your rule list:

```
1$validator = Validator::make($data, [

2    'email' => ['sometimes', 'required', 'email'],

3]);
```

In the example above, the `email` field will only be validated if it is present in the `$data` array.

If you are attempting to validate a field that should always be present but may be empty, check out [this note on optional fields](#a-note-on-optional-fields).

#### [Complex Conditional Validation](#complex-conditional-validation)

Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your *static rules* that never change:

```
1use Illuminate\Support\Facades\Validator;

2 

3$validator = Validator::make($request->all(), [

4    'email' => ['required', 'email'],

5    'games' => ['required', 'integer', 'min:0'],

6]);
```

Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance.

```
1use Illuminate\Support\Fluent;

2 

3$validator->sometimes('reason', ['required', 'max:500'], function (Fluent $input) {

4    return $input->games >= 100;

5});
```

The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once:

```
1$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {

2    return $input->games >= 100;

3});
```

The `$input` parameter passed to your closure will be an instance of `Illuminate\Support\Fluent` and may be used to access your input and files under validation.

#### [Complex Conditional Array Validation](#complex-conditional-array-validation)

Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated:

```
 1$input = [

 2    'channels' => [

 3        [

 4            'type' => 'email',

 5            'address' => '[[email protected]](/cdn-cgi/l/email-protection)',

 6        ],

 7        [

 8            'type' => 'url',

 9            'address' => 'https://example.com',

10        ],

11    ],

12];

13 

14$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {

15    return $item->type === 'email';

16});

17 

18$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {

19    return $item->type !== 'email';

20});
```

Like the `$input` parameter passed to the closure, the `$item` parameter is an instance of `Illuminate\Support\Fluent` when the attribute data is an array; otherwise, it is a string.

## [Validating Arrays](#validating-arrays)

As discussed in the [array validation rule documentation](#rule-array), the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail:

```
 1use Illuminate\Support\Facades\Validator;

 2 

 3$input = [

 4    'user' => [

 5        'name' => 'Taylor Otwell',

 6        'username' => 'taylorotwell',

 7        'admin' => true,

 8    ],

 9];

10 

11Validator::make($input, [

12    'user' => ['array:name,username'],

13]);
```

In general, you should always specify the array keys that are allowed to be present within your array. Otherwise, the validator's `validate` and `validated` methods will return all of the validated data, including the array and all of its keys, even if those keys were not validated by other nested array validation rules.

### [Validating Nested Array Input](#validating-nested-array-input)

Validating nested array-based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so:

```
1use Illuminate\Support\Facades\Validator;

2 

3$validator = Validator::make($request->all(), [

4    'photos.profile' => ['required', 'image'],

5]);
```

You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following:

```
1$validator = Validator::make($request->all(), [

2    'users.*.email' => ['email', 'unique:users'],

3    'users.*.first_name' => ['required_with:users.*.last_name'],

4]);
```

Likewise, you may use the `*` character when specifying [custom validation messages in your language files](#custom-messages-for-specific-attributes), making it a breeze to use a single validation message for array-based fields:

```
1'custom' => [

2    'users.*.email' => [

3        'unique' => 'Each user must have a unique email address',

4    ]

5],
```

#### [Accessing Nested Array Data](#accessing-nested-array-data)

Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may accomplish this using the `Rule::forEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element:

```
 1use App\Rules\HasPermission;

 2use Illuminate\Support\Facades\Validator;

 3use Illuminate\Validation\Rule;

 4 

 5$validator = Validator::make($request->all(), [

 6    'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {

 7        return [

 8            Rule::exists(Company::class, 'id'),

 9            new HasPermission('manage-company', $value),

10        ];

11    }),

12]);
```

### [Error Message Indexes and Positions](#error-message-indexes-and-positions)

When validating arrays, you may want to reference the index or position of a particular item that failed validation within the error message displayed by your application. To accomplish this, you may include the `:index` (starts from `0`), `:position` (starts from `1`), or `:ordinal-position` (starts from `1st`) placeholders within your [custom validation message](#manual-customizing-the-error-messages):

```
 1use Illuminate\Support\Facades\Validator;

 2 

 3$input = [

 4    'photos' => [

 5        [

 6            'name' => 'BeachVacation.jpg',

 7            'description' => 'A photo of my beach vacation!',

 8        ],

 9        [

10            'name' => 'GrandCanyon.jpg',

11            'description' => '',

12        ],

13    ],

14];

15 

16Validator::validate($input, [

17    'photos.*.description' => ['required'],

18], [

19    'photos.*.description.required' => 'Please describe photo #:position.',

20]);
```

Given the example above, validation will fail and the user will be presented with the following error of *"Please describe photo #2."*

If necessary, you may reference more deeply nested indexes and positions via `second-index`, `second-position`, `third-index`, `third-position`, etc.

```
1'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

## [Validating Files](#validating-files)

Laravel provides a variety of validation rules that may be used to validate uploaded files, such as `mimes`, `image`, `min`, and `max`. While you are free to specify these rules individually when validating files, Laravel also offers a fluent file validation rule builder that you may find convenient:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rules\File;

 3 

 4Validator::validate($input, [

 5    'attachment' => [

 6        'required',

 7        File::types(['mp3', 'wav'])

 8            ->min(1024)

 9            ->max(12 * 1024),

10    ],

11]);
```

#### [Validating File Types](#validating-files-file-types)

Even though you only need to specify the extensions when invoking the `types` method, this method actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location:

<https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types>

#### [Validating File Sizes](#validating-files-file-sizes)

For convenience, minimum and maximum file sizes may be specified as a string with a suffix indicating the file size units. The `kb`, `mb`, `gb`, and `tb` suffixes are supported:

```
1File::types(['mp3', 'wav'])

2    ->min('1kb')

3    ->max('10mb');
```

#### [Validating Image Files](#validating-files-image-files)

If your application accepts images uploaded by your users, you may use the `File` rule's `image` constructor method to ensure that the file under validation is an image (jpg, jpeg, png, bmp, gif, or webp).

In addition, the `dimensions` rule may be used to limit the dimensions of the image:

```
 1use Illuminate\Support\Facades\Validator;

 2use Illuminate\Validation\Rule;

 3use Illuminate\Validation\Rules\File;

 4 

 5Validator::validate($input, [

 6    'photo' => [

 7        'required',

 8        File::image()

 9            ->min(1024)

10            ->max(12 * 1024)

11            ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)),

12    ],

13]);
```

More information regarding validating image dimensions may be found in the [dimension rule documentation](#rule-dimensions).

By default, the `image` rule does not allow SVG files due to the possibility of XSS vulnerabilities. If you need to allow SVG files, you may pass `allowSvg: true` to the `image` rule: `File::image(allowSvg: true)`.

#### [Validating Image Dimensions](#validating-files-image-dimensions)

You may also validate the dimensions of an image. For example, to validate that an uploaded image is at least 1000 pixels wide and 500 pixels tall, you may use the `dimensions` rule:

```
1use Illuminate\Validation\Rule;

2use Illuminate\Validation\Rules\File;

3 

4File::image()->dimensions(

5    Rule::dimensions()

6        ->maxWidth(1000)

7        ->maxHeight(500)

8)
```

More information regarding validating image dimensions may be found in the [dimension rule documentation](#rule-dimensions).

## [Validating Passwords](#validating-passwords)

To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object:

```
1use Illuminate\Support\Facades\Validator;

2use Illuminate\Validation\Rules\Password;

3 

4$validator = Validator::make($request->all(), [

5    'password' => ['required', 'confirmed', Password::min(8)],

6]);
```

The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing:

```
 1// Require at least 8 characters...

 2Password::min(8)

 3 

 4// Require at least one letter...

 5Password::min(8)->letters()

 6 

 7// Require at least one uppercase and one lowercase letter...

 8Password::min(8)->mixedCase()

 9 

10// Require at least one number...

11Password::min(8)->numbers()

12 

13// Require at least one symbol...

14Password::min(8)->symbols()
```

In addition, you may ensure that a password has not been compromised in a public password data breach leak using the `uncompromised` method:

```
1Password::min(8)->uncompromised()
```

Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security.

By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method:

```
1// Ensure the password appears less than 3 times in the same data leak...

2Password::min(8)->uncompromised(3);
```

Of course, you may chain all the methods in the examples above:

```
1Password::min(8)

2    ->letters()

3    ->mixedCase()

4    ->numbers()

5    ->symbols()

6    ->uncompromised()
```

You may convert a `Password` rule object to a string suitable for the HTML `passwordrules` attribute using the `toPasswordRulesString` method:

```
1<input

2    type="password"

3    name="password"

4    autocomplete="new-password"

5    passwordrules="{{ Password::defaults()->toPasswordRulesString() }}"

6/>
```

#### [Defining Default Password Rules](#defining-default-password-rules)

You may find it convenient to specify the default validation rules for passwords in a single location of your application. You can easily accomplish this using the `Password::defaults` method, which accepts a closure. The closure given to the `defaults` method should return the default configuration of the Password rule. Typically, the `defaults` rule should be called within the `boot` method of one of your application's service providers:

```
 1use Illuminate\Validation\Rules\Password;

 2 

 3/**

 4 * Bootstrap any application services.

 5 */

 6public function boot(): void

 7{

 8    Password::defaults(function () {

 9        $rule = Password::min(8);

10 

11        return $this->app->isProduction()

12            ? $rule->mixedCase()->uncompromised()

13            : $rule;

14    });

15}
```

Then, when you would like to apply the default rules to a particular password undergoing validation, you may invoke the `defaults` method with no arguments:

```
1'password' => ['required', Password::defaults()],
```

Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this:

```
1use App\Rules\ZxcvbnRule;

2 

3Password::defaults(function () {

4    $rule = Password::min(8)->rules([new ZxcvbnRule]);

5 

6    // ...

7});
```

## [Custom Validation Rules](#custom-validation-rules)

### [Using Rule Objects](#using-rule-objects)

Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using rule objects. To generate a new rule object, you may use the `make:rule` Artisan command. Let's use this command to generate a rule that verifies a string is uppercase. Laravel will place the new rule in the `app/Rules` directory. If this directory does not exist, Laravel will create it when you execute the Artisan command to create your rule:

```
1php artisan make:rule Uppercase
```

Once the rule has been created, we are ready to define its behavior. A rule object contains a single method: `validate`. This method receives the attribute name, its value, and a callback that should be invoked on failure with the validation error message:

```
 1<?php

 2 

 3namespace App\Rules;

 4 

 5use Closure;

 6use Illuminate\Contracts\Validation\ValidationRule;

 7 

 8class Uppercase implements ValidationRule

 9{

10    /**

11     * Run the validation rule.

12     */

13    public function validate(string $attribute, mixed $value, Closure $fail): void

14    {

15        if (strtoupper($value) !== $value) {

16            $fail('The :attribute must be uppercase.');

17        }

18    }

19}
```

Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules:

```
1use App\Rules\Uppercase;

2 

3$request->validate([

4    'name' => ['required', 'string', new Uppercase],

5]);
```

#### Translating Validation Messages

Instead of providing a literal error message to the `$fail` closure, you may also provide a [translation string key](/docs/13.x/localization) and instruct Laravel to translate the error message:

```
1if (strtoupper($value) !== $value) {

2    $fail('validation.uppercase')->translate();

3}
```

If necessary, you may provide placeholder replacements and the preferred language as the first and second arguments to the `translate` method:

```
1$fail('validation.location')->translate([

2    'value' => $this->value,

3], 'fr');
```

#### Accessing Additional Data

If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation:

```
 1<?php

 2 

 3namespace App\Rules;

 4 

 5use Illuminate\Contracts\Validation\DataAwareRule;

 6use Illuminate\Contracts\Validation\ValidationRule;

 7 

 8class Uppercase implements DataAwareRule, ValidationRule

 9{

10    /**

11     * All of the data under validation.

12     *

13     * @var array<string, mixed>

14     */

15    protected $data = [];

16 

17    // ...

18 

19    /**

20     * Set the data under validation.

21     *

22     * @param  array<string, mixed>  $data

23     */

24    public function setData(array $data): static

25    {

26        $this->data = $data;

27 

28        return $this;

29    }

30}
```

Or, if your validation rule requires access to the validator instance performing the validation, you may implement the `ValidatorAwareRule` interface:

```
 1<?php

 2 

 3namespace App\Rules;

 4 

 5use Illuminate\Contracts\Validation\ValidationRule;

 6use Illuminate\Contracts\Validation\ValidatorAwareRule;

 7use Illuminate\Validation\Validator;

 8 

 9class Uppercase implements ValidationRule, ValidatorAwareRule

10{

11    /**

12     * The validator instance.

13     *

14     * @var \Illuminate\Validation\Validator

15     */

16    protected $validator;

17 

18    // ...

19 

20    /**

21     * Set the current validator.

22     */

23    public function setValidator(Validator $validator): static

24    {

25        $this->validator = $validator;

26 

27        return $this;

28    }

29}
```

### [Using Closures](#using-closures)

If you only need the functionality of a custom rule once throughout your application, you may use a closure instead of a rule object. The closure receives the attribute's name, the attribute's value, and a `$fail` callback that should be called if validation fails:

```
 1use Illuminate\Support\Facades\Validator;

 2use Closure;

 3 

 4$validator = Validator::make($request->all(), [

 5    'title' => [

 6        'required',

 7        'max:255',

 8        function (string $attribute, mixed $value, Closure $fail) {

 9            if ($value === 'foo') {

10                $fail("The {$attribute} is invalid.");

11            }

12        },

13    ],

14]);
```

### [Implicit Rules](#implicit-rules)

By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom rules, are not run. For example, the [unique](#rule-unique) rule will not be run against an empty string:

```
1use Illuminate\Support\Facades\Validator;

2 

3$rules = ['name' => ['unique:users,name']];

4 

5$input = ['name' => ''];

6 

7Validator::make($input, $rules)->passes(); // true
```

For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To quickly generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option:

```
1php artisan make:rule Uppercase --implicit
```

An "implicit" rule only *implies* that the attribute is required. Whether it actually invalidates a missing or empty attribute is up to you.
