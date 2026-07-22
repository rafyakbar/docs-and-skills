# Laravel Cashier (Paddle)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
  * [Paddle Sandbox](#paddle-sandbox)
- [Configuration](#configuration)
  * [Billable Model](#billable-model)
  * [API Keys](#api-keys)
  * [Paddle JS](#paddle-js)
  * [Currency Configuration](#currency-configuration)
  * [Overriding Default Models](#overriding-default-models)
- [Quickstart](#quickstart)
  * [Selling Products](#quickstart-selling-products)
  * [Selling Subscriptions](#quickstart-selling-subscriptions)
- [Checkout Sessions](#checkout-sessions)
  * [Overlay Checkout](#overlay-checkout)
  * [Inline Checkout](#inline-checkout)
  * [Guest Checkouts](#guest-checkouts)
- [Price Previews](#price-previews)
  * [Customer Price Previews](#customer-price-previews)
  * [Discounts](#price-discounts)
- [Customers](#customers)
  * [Customer Defaults](#customer-defaults)
  * [Retrieving Customers](#retrieving-customers)
  * [Creating Customers](#creating-customers)
- [Subscriptions](#subscriptions)
  * [Creating Subscriptions](#creating-subscriptions)
  * [Checking Subscription Status](#checking-subscription-status)
  * [Subscription Single Charges](#subscription-single-charges)
  * [Updating Payment Information](#updating-payment-information)
  * [Changing Plans](#changing-plans)
  * [Subscription Quantity](#subscription-quantity)
  * [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)
  * [Multiple Subscriptions](#multiple-subscriptions)
  * [Pausing Subscriptions](#pausing-subscriptions)
  * [Canceling Subscriptions](#canceling-subscriptions)
- [Subscription Trials](#subscription-trials)
  * [With Payment Method Up Front](#with-payment-method-up-front)
  * [Without Payment Method Up Front](#without-payment-method-up-front)
  * [Extend or Activate a Trial](#extend-or-activate-a-trial)
- [Handling Paddle Webhooks](#handling-paddle-webhooks)
  * [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
  * [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
  * [Charging for Products](#charging-for-products)
  * [Refunding Transactions](#refunding-transactions)
  * [Crediting Transactions](#crediting-transactions)
- [Transactions](#transactions)
  * [Past and Upcoming Payments](#past-and-upcoming-payments)
- [Testing](#testing)

## [Introduction](#introduction)

This documentation is for Cashier Paddle 2.x's integration with Paddle Billing. If you're still using Paddle Classic, you should use [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x).

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) provides an expressive, fluent interface to [Paddle's](https://paddle.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading. In addition to basic subscription management, Cashier can handle: swapping subscriptions, subscription "quantities", subscription pausing, cancelation grace periods, and more.

Before digging into Cashier Paddle, we recommend you also review Paddle's [concept guides](https://developer.paddle.com/concepts/overview) and [API documentation](https://developer.paddle.com/api-reference/overview).

## [Upgrading Cashier](#upgrading-cashier)

When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md).

## [Installation](#installation)

First, install the Cashier package for Paddle using the Composer package manager:

```
1composer require laravel/cashier-paddle
```

Next, you should publish the Cashier migration files using the `vendor:publish` Artisan command:

```
1php artisan vendor:publish --tag="cashier-migrations"
```

Then, you should run your application's database migrations. The Cashier migrations will create a new `customers` table. In addition, new `subscriptions` and `subscription_items` tables will be created to store all of your customer's subscriptions. Lastly, a new `transactions` table will be created to store all of the Paddle transactions associated with your customers:

```
1php artisan migrate
```

To ensure Cashier properly handles all Paddle events, remember to [set up Cashier's webhook handling](#handling-paddle-webhooks).

### [Paddle Sandbox](#paddle-sandbox)

During local and staging development, you should [register a Paddle Sandbox account](https://sandbox-login.paddle.com/signup). This account will give you a sandboxed environment to test and develop your applications without making actual payments. You may use Paddle's [test card numbers](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method) to simulate various payment scenarios.

When using the Paddle Sandbox environment, you should set the `PADDLE_SANDBOX` environment variable to `true` within your application's `.env` file:

```
1PADDLE_SANDBOX=true
```

After you have finished developing your application you may [apply for a Paddle vendor account](https://paddle.com). Before your application is placed into production, Paddle will need to approve your application's domain.

## [Configuration](#configuration)

### [Billable Model](#billable-model)

Before using Cashier, you must add the `Billable` trait to your user model definition. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions and updating payment method information:

```
1use Laravel\Paddle\Billable;

2 

3class User extends Authenticatable

4{

5    use Billable;

6}
```

If you have billable entities that are not users, you may also add the trait to those classes:

```
1use Illuminate\Database\Eloquent\Model;

2use Laravel\Paddle\Billable;

3 

4class Team extends Model

5{

6    use Billable;

7}
```

### [API Keys](#api-keys)

Next, you should configure your Paddle keys in your application's `.env` file. You can retrieve your Paddle API keys from the Paddle control panel:

```
1PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token

2PADDLE_API_KEY=your-paddle-api-key

3PADDLE_RETAIN_KEY=your-paddle-retain-key

4PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"

5PADDLE_SANDBOX=true
```

The `PADDLE_SANDBOX` environment variable should be set to `true` when you are using [Paddle's Sandbox environment](#paddle-sandbox). The `PADDLE_SANDBOX` variable should be set to `false` if you are deploying your application to production and are using Paddle's live vendor environment.

The `PADDLE_RETAIN_KEY` is optional and should only be set if you're using Paddle with [Retain](https://developer.paddle.com/concepts/retain/overview).

### [Paddle JS](#paddle-js)

Paddle relies on its own JavaScript library to initiate the Paddle checkout widget. You can load the JavaScript library by placing the `@paddleJS` Blade directive right before your application layout's closing `</head>` tag:

```
1<head>

2    ...

3 

4    @paddleJS

5</head>
```

### [Currency Configuration](#currency-configuration)

You can specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale:

```
1CASHIER_CURRENCY_LOCALE=nl_BE
```

In order to use locales other than `en`, ensure the `ext-intl` PHP extension is installed and configured on your server.

### [Overriding Default Models](#overriding-default-models)

You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model:

```
1use Laravel\Paddle\Subscription as CashierSubscription;

2 

3class Subscription extends CashierSubscription

4{

5    // ...

6}
```

After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Paddle\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use App\Models\Cashier\Subscription;

 2use App\Models\Cashier\Transaction;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Cashier::useSubscriptionModel(Subscription::class);

10    Cashier::useTransactionModel(Transaction::class);

11}
```

## [Quickstart](#quickstart)

### [Selling Products](#quickstart-selling-products)

Before utilizing Paddle Checkout, you should define Products with fixed prices in your Paddle dashboard. In addition, you should [configure Paddle's webhook handling](#handling-paddle-webhooks).

Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Paddle's Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout), you can easily build modern, robust payment integrations.

To charge customers for non-recurring, single-charge products, we'll utilize Cashier to charge customers with Paddle's Checkout Overlay, where they will provide their payment details and confirm their purchase. Once the payment has been made via the Checkout Overlay, the customer will be redirected to a success URL of your choosing within your application:

```
1use Illuminate\Http\Request;

2 

3Route::get('/buy', function (Request $request) {

4    $checkout = $request->user()->checkout('pri_deluxe_album')

5        ->returnTo(route('dashboard'));

6 

7    return view('buy', ['checkout' => $checkout]);

8})->name('checkout');
```

As you can see in the example above, we will utilize Cashier's provided `checkout` method to create a checkout object to present the customer the Paddle Checkout Overlay for a given "price identifier". When using Paddle, "prices" refer to [defined prices for specific products](https://developer.paddle.com/build/products/create-products-prices).

If necessary, the `checkout` method will automatically create a customer in Paddle and connect that Paddle customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success page where you can display an informational message to the customer.

In the `buy` view, we will include a button to display the Checkout Overlay. The `paddle-button` Blade component is included with Cashier Paddle; however, you may also [manually render an overlay checkout](#manually-rendering-an-overlay-checkout):

```
1<x-paddle-button :checkout="$checkout" class="px-8 py-4">

2    Buy Product

3</x-paddle-button>
```

#### [Providing Meta Data to Paddle Checkout](#providing-meta-data-to-paddle-checkout)

When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Paddle's Checkout Overlay to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application.

To accomplish this, you may provide an array of custom data to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application:

```
 1use App\Models\Cart;

 2use App\Models\Order;

 3use Illuminate\Http\Request;

 4 

 5Route::get('/cart/{cart}/checkout', function (Request $request, Cart $cart) {

 6    $order = Order::create([

 7        'cart_id' => $cart->id,

 8        'price_ids' => $cart->price_ids,

 9        'status' => 'incomplete',

10    ]);

11 

12    $checkout = $request->user()->checkout($order->price_ids)

13        ->customData(['order_id' => $order->id]);

14 

15    return view('billing', ['checkout' => $checkout]);

16})->name('checkout');
```

As you can see in the example above, when a user begins the checkout process, we will provide all of the cart / order's associated Paddle price identifiers to the `checkout` method. Of course, your application is responsible for associating these items with the "shopping cart" or order as a customer adds them. We also provide the order's ID to the Paddle Checkout Overlay via the `customData` method.

Of course, you will likely want to mark the order as "complete" once the customer has finished the checkout process. To accomplish this, you may listen to the webhooks dispatched by Paddle and raised via events by Cashier to store order information in your database.

To get started, listen for the `TransactionCompleted` event dispatched by Cashier. Typically, you should register the event listener in the `boot` method of your application's `AppServiceProvider`:

```
 1use App\Listeners\CompleteOrder;

 2use Illuminate\Support\Facades\Event;

 3use Laravel\Paddle\Events\TransactionCompleted;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Event::listen(TransactionCompleted::class, CompleteOrder::class);

11}
```

In this example, the `CompleteOrder` listener might look like the following:

```
 1namespace App\Listeners;

 2 

 3use App\Models\Order;

 4use Laravel\Paddle\Cashier;

 5use Laravel\Paddle\Events\TransactionCompleted;

 6 

 7class CompleteOrder

 8{

 9    /**

10     * Handle the incoming Cashier webhook event.

11     */

12    public function handle(TransactionCompleted $event): void

13    {

14        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

15 

16        $order = Order::findOrFail($orderId);

17 

18        $order->update(['status' => 'completed']);

19    }

20}
```

Please refer to Paddle's documentation for more information on the [data contained by the `transaction.completed` event](https://developer.paddle.com/webhooks/transactions/transaction-completed).

### [Selling Subscriptions](#quickstart-selling-subscriptions)

Before utilizing Paddle Checkout, you should define Products with fixed prices in your Paddle dashboard. In addition, you should [configure Paddle's webhook handling](#handling-paddle-webhooks).

Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Paddle's Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout), you can easily build modern, robust payment integrations.

To learn how to sell subscriptions using Cashier and Paddle's Checkout Overlay, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Paddle dashboard. In addition, our subscription service might offer an "Expert" plan as `pro_expert`.

First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button will invoke a Paddle Checkout Overlay for their chosen plan. To get started, let's initiate a checkout session via the `checkout` method:

```
1use Illuminate\Http\Request;

2 

3Route::get('/subscribe', function (Request $request) {

4    $checkout = $request->user()->checkout('price_basic_monthly')

5        ->returnTo(route('dashboard'));

6 

7    return view('subscribe', ['checkout' => $checkout]);

8})->name('subscribe');
```

In the `subscribe` view, we will include a button to display the Checkout Overlay. The `paddle-button` Blade component is included with Cashier Paddle; however, you may also [manually render an overlay checkout](#manually-rendering-an-overlay-checkout):

```
1<x-paddle-button :checkout="$checkout" class="px-8 py-4">

2    Subscribe

3</x-paddle-button>
```

Now, when the Subscribe button is clicked, the customer will be able to enter their payment details and initiate their subscription. To know when their subscription has actually started (since some payment methods require a few seconds to process), you should also [configure Cashier's webhook handling](#handling-paddle-webhooks).

Now that customers can start subscriptions, we need to restrict certain portions of our application so that only subscribed users can access them. Of course, we can always determine a user's current subscription status via the `subscribed` method provided by Cashier's `Billable` trait:

```
1@if ($user->subscribed())

2    <p>You are subscribed.</p>

3@endif
```

We can even easily determine if a user is subscribed to specific product or price:

```
1@if ($user->subscribedToProduct('pro_basic'))

2    <p>You are subscribed to our Basic product.</p>

3@endif

4 

5@if ($user->subscribedToPrice('price_basic_monthly'))

6    <p>You are subscribed to our monthly Basic plan.</p>

7@endif
```

#### [Building a Subscribed Middleware](#quickstart-building-a-subscribed-middleware)

For convenience, you may wish to create a [middleware](/docs/13.x/middleware) which determines if the incoming request is from a subscribed user. Once this middleware has been defined, you may easily assign it to a route to prevent users that are not subscribed from accessing the route:

```
 1<?php

 2 

 3namespace App\Http\Middleware;

 4 

 5use Closure;

 6use Illuminate\Http\Request;

 7use Symfony\Component\HttpFoundation\Response;

 8 

 9class Subscribed

10{

11    /**

12     * Handle an incoming request.

13     */

14    public function handle(Request $request, Closure $next): Response

15    {

16        if (! $request->user()?->subscribed()) {

17            // Redirect user to billing page and ask them to subscribe...

18            return redirect('/subscribe');

19        }

20 

21        return $next($request);

22    }

23}
```

Once the middleware has been defined, you may assign it to a route:

```
1use App\Http\Middleware\Subscribed;

2 

3Route::get('/dashboard', function () {

4    // ...

5})->middleware([Subscribed::class]);
```

#### [Allowing Customers to Manage Their Billing Plan](#quickstart-allowing-customers-to-manage-their-billing-plan)

Of course, customers may want to change their subscription plan to another product or "tier". In our example from above, we'd want to allow the customer to change their plan from a monthly subscription to a yearly subscription. For this you'll need to implement something like a button that leads to the below route:

```
1use Illuminate\Http\Request;

2 

3Route::put('/subscription/{price}/swap', function (Request $request, $price) {

4    $user->subscription()->swap($price); // With "$price" being "price_basic_yearly" for this example.

5 

6    return redirect()->route('dashboard');

7})->name('subscription.swap');
```

Besides swapping plans you'll also need to allow your customers to cancel their subscription. Like swapping plans, provide a button that leads to the following route:

```
1use Illuminate\Http\Request;

2 

3Route::put('/subscription/cancel', function (Request $request, $price) {

4    $user->subscription()->cancel();

5 

6    return redirect()->route('dashboard');

7})->name('subscription.cancel');
```

And now your subscription will get canceled at the end of its billing period.

As long as you have configured Cashier's webhook handling, Cashier will automatically keep your application's Cashier-related database tables in sync by inspecting the incoming webhooks from Paddle. So, for example, when you cancel a customer's subscription via Paddle's dashboard, Cashier will receive the corresponding webhook and mark the subscription as "canceled" in your application's database.

## [Checkout Sessions](#checkout-sessions)

Most operations to bill customers are performed using "checkouts" via Paddle's [Checkout Overlay widget](https://developer.paddle.com/build/checkout/build-overlay-checkout) or by utilizing [inline checkout](https://developer.paddle.com/build/checkout/build-branded-inline-checkout).

Before processing checkout payments using Paddle, you should define your application's [default payment link](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link) in your Paddle checkout settings dashboard.

### [Overlay Checkout](#overlay-checkout)

Before displaying the Checkout Overlay widget, you must generate a checkout session using Cashier. A checkout session will inform the checkout widget of the billing operation that should be performed:

```
1use Illuminate\Http\Request;

2 

3Route::get('/buy', function (Request $request) {

4    $checkout = $user->checkout('pri_34567')

5        ->returnTo(route('dashboard'));

6 

7    return view('billing', ['checkout' => $checkout]);

8});
```

Cashier includes a `paddle-button` [Blade component](/docs/13.x/blade#components). You may pass the checkout session to this component as a "prop". Then, when this button is clicked, Paddle's checkout widget will be displayed:

```
1<x-paddle-button :checkout="$checkout" class="px-8 py-4">

2    Subscribe

3</x-paddle-button>
```

By default, this will display the widget using Paddle's default styling. You can customize the widget by adding [Paddle supported attributes](https://developer.paddle.com/paddlejs/html-data-attributes) like the `data-theme='light'` attribute to the component:

```
1<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">

2    Subscribe

3</x-paddle-button>
```

The Paddle checkout widget is asynchronous. Once the user creates a subscription within the widget, Paddle will send your application a webhook so that you may properly update the subscription state in your application's database. Therefore, it's important that you properly [set up webhooks](#handling-paddle-webhooks) to accommodate for state changes from Paddle.

After a subscription state change, the delay for receiving the corresponding webhook is typically minimal but you should account for this in your application by considering that your user's subscription might not be immediately available after completing the checkout.

#### [Manually Rendering an Overlay Checkout](#manually-rendering-an-overlay-checkout)

You may also manually render an overlay checkout without using Laravel's built-in Blade components. To get started, generate the checkout session [as demonstrated in previous examples](#overlay-checkout):

```
1use Illuminate\Http\Request;

2 

3Route::get('/buy', function (Request $request) {

4    $checkout = $user->checkout('pri_34567')

5        ->returnTo(route('dashboard'));

6 

7    return view('billing', ['checkout' => $checkout]);

8});
```

Next, you may use Paddle.js to initialize the checkout. In this example, we will create a link that is assigned the `paddle_button` class. Paddle.js will detect this class and display the overlay checkout when the link is clicked:

```
 1<?php

 2$items = $checkout->getItems();

 3$customer = $checkout->getCustomer();

 4$custom = $checkout->getCustomData();

 5?>

 6 

 7<a

 8    href='#!'

 9    class='paddle_button'

10    data-items='{!! json_encode($items) !!}'

11    @if ($customer) data-customer-id='{{ $customer->paddle_id }}' @endif

12    @if ($custom) data-custom-data='{{ json_encode($custom) }}' @endif

13    @if ($returnUrl = $checkout->getReturnUrl()) data-success-url='{{ $returnUrl }}' @endif

14>

15    Buy Product

16</a>
```

### [Inline Checkout](#inline-checkout)

If you don't want to make use of Paddle's "overlay" style checkout widget, Paddle also provides the option to display the widget inline. While this approach does not allow you to adjust any of the checkout's HTML fields, it allows you to embed the widget within your application.

To make it easy for you to get started with inline checkout, Cashier includes a `paddle-checkout` Blade component. To get started, you should [generate a checkout session](#overlay-checkout):

```
1use Illuminate\Http\Request;

2 

3Route::get('/buy', function (Request $request) {

4    $checkout = $user->checkout('pri_34567')

5        ->returnTo(route('dashboard'));

6 

7    return view('billing', ['checkout' => $checkout]);

8});
```

Then, you may pass the checkout session to the component's `checkout` attribute:

```
1<x-paddle-checkout :checkout="$checkout" class="w-full" />
```

To adjust the height of the inline checkout component, you may pass the `height` attribute to the Blade component:

```
1<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```

Please consult Paddle's [guide on Inline Checkout](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) and [available checkout settings](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings) for further details on the inline checkout's customization options.

#### [Manually Rendering an Inline Checkout](#manually-rendering-an-inline-checkout)

You may also manually render an inline checkout without using Laravel's built-in Blade components. To get started, generate the checkout session [as demonstrated in previous examples](#inline-checkout):

```
1use Illuminate\Http\Request;

2 

3Route::get('/buy', function (Request $request) {

4    $checkout = $user->checkout('pri_34567')

5        ->returnTo(route('dashboard'));

6 

7    return view('billing', ['checkout' => $checkout]);

8});
```

Next, you may use Paddle.js to initialize the checkout. In this example, we will demonstrate this using [Alpine.js](https://github.com/alpinejs/alpine); however, you are free to modify this example for your own frontend stack:

```
 1<?php

 2$options = $checkout->options();

 3 

 4$options['settings']['frameTarget'] = 'paddle-checkout';

 5$options['settings']['frameInitialHeight'] = 366;

 6?>

 7 

 8<div class="paddle-checkout" x-data="{}" x-init="

 9    Paddle.Checkout.open(@json($options));

10">

11</div>
```

### [Guest Checkouts](#guest-checkouts)

Sometimes, you may need to create a checkout session for users that do not need an account with your application. To do so, you may use the `guest` method:

```
1use Illuminate\Http\Request;

2use Laravel\Paddle\Checkout;

3 

4Route::get('/buy', function (Request $request) {

5    $checkout = Checkout::guest(['pri_34567'])

6        ->returnTo(route('home'));

7 

8    return view('billing', ['checkout' => $checkout]);

9});
```

Then, you may provide the checkout session to the [Paddle button](#overlay-checkout) or [inline checkout](#inline-checkout) Blade components.

## [Price Previews](#price-previews)

Paddle allows you to customize prices per currency, essentially allowing you to configure different prices for different countries. Cashier Paddle allows you to retrieve all of these prices using the `previewPrices` method. This method accepts the price IDs you wish to retrieve prices for:

```
1use Laravel\Paddle\Cashier;

2 

3$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```

The currency will be determined based on the IP address of the request; however, you may optionally provide a specific country to retrieve prices for:

```
1use Laravel\Paddle\Cashier;

2 

3$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [

4    'country_code' => 'BE',

5    'postal_code' => '1234',

6]]);
```

After retrieving the prices you may display them however you wish:

```
1<ul>

2    @foreach ($prices as $price)

3        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>

4    @endforeach

5</ul>
```

You may also display the subtotal price and tax amount separately:

```
1<ul>

2    @foreach ($prices as $price)

3        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>

4    @endforeach

5</ul>
```

For more information, [checkout Paddle's API documentation regarding price previews](https://developer.paddle.com/api-reference/pricing-preview/preview-prices).

### [Customer Price Previews](#customer-price-previews)

If a user is already a customer and you would like to display the prices that apply to that customer, you may do so by retrieving the prices directly from the customer instance:

```
1use App\Models\User;

2 

3$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```

Internally, Cashier will use the user's customer ID to retrieve the prices in their currency. So, for example, a user living in the United States will see prices in US dollars while a user in Belgium will see prices in Euros. If no matching currency can be found, the default currency of the product will be used. You can customize all prices of a product or subscription plan in the Paddle control panel.

### [Discounts](#price-discounts)

You may also choose to display prices after a discount. When calling the `previewPrices` method, you provide the discount ID via the `discount_id` option:

```
1use Laravel\Paddle\Cashier;

2 

3$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [

4    'discount_id' => 'dsc_123'

5]);
```

Then, display the calculated prices:

```
1<ul>

2    @foreach ($prices as $price)

3        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>

4    @endforeach

5</ul>
```

## [Customers](#customers)

### [Customer Defaults](#customer-defaults)

Cashier allows you to define some useful defaults for your customers when creating checkout sessions. Setting these defaults allow you to pre-fill a customer's email address and name so that they can immediately move on to the payment portion of the checkout widget. You can set these defaults by overriding the following methods on your billable model:

```
 1/**

 2 * Get the customer's name to associate with Paddle.

 3 */

 4public function paddleName(): string|null

 5{

 6    return $this->name;

 7}

 8 

 9/**

10 * Get the customer's email address to associate with Paddle.

11 */

12public function paddleEmail(): string|null

13{

14    return $this->email;

15}
```

These defaults will be used for every action in Cashier that generates a [checkout session](#checkout-sessions).

### [Retrieving Customers](#retrieving-customers)

You can retrieve a customer by their Paddle Customer ID using the `Cashier::findBillable` method. This method will return an instance of the billable model:

```
1use Laravel\Paddle\Cashier;

2 

3$user = Cashier::findBillable($customerId);
```

### [Creating Customers](#creating-customers)

Occasionally, you may wish to create a Paddle customer without beginning a subscription. You may accomplish this using the `createAsCustomer` method:

```
1$customer = $user->createAsCustomer();
```

An instance of `Laravel\Paddle\Customer` is returned. Once the customer has been created in Paddle, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Paddle API](https://developer.paddle.com/api-reference/customers/create-customer):

```
1$customer = $user->createAsCustomer($options);
```

## [Subscriptions](#subscriptions)

### [Creating Subscriptions](#creating-subscriptions)

To create a subscription, first retrieve an instance of your billable model from your database, which will typically be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `subscribe` method to create the model's checkout session:

```
1use Illuminate\Http\Request;

2 

3Route::get('/user/subscribe', function (Request $request) {

4    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')

5        ->returnTo(route('home'));

6 

7    return view('billing', ['checkout' => $checkout]);

8});
```

The first argument given to the `subscribe` method is the specific price the user is subscribing to. This value should correspond to the price's identifier in Paddle. The `returnTo` method accepts a URL that your user will be redirected to after they successfully complete the checkout. The second argument passed to the `subscribe` method should be the internal "type" of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription type is only for internal application usage and is not meant to be displayed to users. In addition, it should not contain spaces and it should never be changed after creating the subscription.

You may also provide an array of custom metadata regarding the subscription using the `customData` method:

```
1$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')

2    ->customData(['key' => 'value'])

3    ->returnTo(route('home'));
```

Once a subscription checkout session has been created, the checkout session may be provided to the `paddle-button` [Blade component](#overlay-checkout) that is included with Cashier Paddle:

```
1<x-paddle-button :checkout="$checkout" class="px-8 py-4">

2    Subscribe

3</x-paddle-button>
```

After the user has finished their checkout, a `subscription_created` webhook will be dispatched from Paddle. Cashier will receive this webhook and set up the subscription for your customer. In order to make sure all webhooks are properly received and handled by your application, ensure you have properly [set up webhook handling](#handling-paddle-webhooks).

### [Checking Subscription Status](#checking-subscription-status)

Once a user is subscribed to your application, you may check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the user has a valid subscription, even if the subscription is currently within its trial period:

```
1if ($user->subscribed()) {

2    // ...

3}
```

If your application offers multiple subscriptions, you may specify the subscription when invoking the `subscribed` method:

```
1if ($user->subscribed('default')) {

2    // ...

3}
```

The `subscribed` method also makes a great candidate for a [route middleware](/docs/13.x/middleware), allowing you to filter access to routes and controllers based on the user's subscription status:

```
 1<?php

 2 

 3namespace App\Http\Middleware;

 4 

 5use Closure;

 6use Illuminate\Http\Request;

 7use Symfony\Component\HttpFoundation\Response;

 8 

 9class EnsureUserIsSubscribed

10{

11    /**

12     * Handle an incoming request.

13     *

14     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next

15     */

16    public function handle(Request $request, Closure $next): Response

17    {

18        if ($request->user() && ! $request->user()->subscribed()) {

19            // This user is not a paying customer...

20            return redirect('/billing');

21        }

22 

23        return $next($request);

24    }

25}
```

If you would like to determine if a user is still within their trial period, you may use the `onTrial` method. This method can be useful for determining if you should display a warning to the user that they are still on their trial period:

```
1if ($user->subscription()->onTrial()) {

2    // ...

3}
```

The `subscribedToPrice` method may be used to determine if the user is subscribed to a given plan based on a given Paddle price ID. In this example, we will determine if the user's `default` subscription is actively subscribed to the monthly price:

```
1if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {

2    // ...

3}
```

The `recurring` method may be used to determine if the user is currently on an active subscription and is no longer within their trial period or on a grace period:

```
1if ($user->subscription()->recurring()) {

2    // ...

3}
```

#### [Canceled Subscription Status](#canceled-subscription-status)

To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method:

```
1if ($user->subscription()->canceled()) {

2    // ...

3}
```

You may also determine if a user has canceled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. In addition, the `subscribed` method will still return `true` during this time:

```
1if ($user->subscription()->onGracePeriod()) {

2    // ...

3}
```

#### [Past Due Status](#past-due-status)

If a payment fails for a subscription, it will be marked as `past_due`. When your subscription is in this state it will not be active until the customer has updated their payment information. You may determine if a subscription is past due using the `pastDue` method on the subscription instance:

```
1if ($user->subscription()->pastDue()) {

2    // ...

3}
```

When a subscription is past due, you should instruct the user to [update their payment information](#updating-payment-information).

If you would like subscriptions to still be considered valid when they are `past_due`, you may use the `keepPastDueSubscriptionsActive` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`:

```
1use Laravel\Paddle\Cashier;

2 

3/**

4 * Register any application services.

5 */

6public function register(): void

7{

8    Cashier::keepPastDueSubscriptionsActive();

9}
```

When a subscription is in a `past_due` state it cannot be changed until payment information has been updated. Therefore, the `swap` and `updateQuantity` methods will throw an exception when the subscription is in a `past_due` state.

#### [Subscription Scopes](#subscription-scopes)

Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state:

```
1// Get all valid subscriptions...

2$subscriptions = Subscription::query()->valid()->get();

3 

4// Get all of the canceled subscriptions for a user...

5$subscriptions = $user->subscriptions()->canceled()->get();
```

A complete list of available scopes is available below:

```
 1Subscription::query()->valid();

 2Subscription::query()->onTrial();

 3Subscription::query()->expiredTrial();

 4Subscription::query()->notOnTrial();

 5Subscription::query()->active();

 6Subscription::query()->recurring();

 7Subscription::query()->pastDue();

 8Subscription::query()->paused();

 9Subscription::query()->notPaused();

10Subscription::query()->onPausedGracePeriod();

11Subscription::query()->notOnPausedGracePeriod();

12Subscription::query()->canceled();

13Subscription::query()->notCanceled();

14Subscription::query()->onGracePeriod();

15Subscription::query()->notOnGracePeriod();
```

### [Subscription Single Charges](#subscription-single-charges)

Subscription single charges allow you to charge subscribers with a one-time charge on top of their subscriptions. You must provide one or multiple price ID's when invoking the `charge` method:

```
1// Charge a single price...

2$response = $user->subscription()->charge('pri_123');

3 

4// Charge multiple prices at once...

5$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```

The `charge` method will not actually charge the customer until the next billing interval of their subscription. If you would like to bill the customer immediately, you may use the `chargeAndInvoice` method instead:

```
1$response = $user->subscription()->chargeAndInvoice('pri_123');
```

### [Updating Payment Information](#updating-payment-information)

Paddle always saves a payment method per subscription. If you want to update the default payment method for a subscription, you should redirect your customer to Paddle's hosted payment method update page using the `redirectToUpdatePaymentMethod` method on the subscription model:

```
1use Illuminate\Http\Request;

2 

3Route::get('/update-payment-method', function (Request $request) {

4    $user = $request->user();

5 

6    return $user->subscription()->redirectToUpdatePaymentMethod();

7});
```

When a user has finished updating their information, a `subscription_updated` webhook will be dispatched by Paddle and the subscription details will be updated in your application's database.

### [Changing Plans](#changing-plans)

After a user has subscribed to your application, they may occasionally want to change to a new subscription plan. To update the subscription plan for a user, you should pass the Paddle price's identifier to the subscription's `swap` method:

```
1use App\Models\User;

2 

3$user = User::find(1);

4 

5$user->subscription()->swap($premium = 'pri_456');
```

If you would like to swap plans and immediately invoice the user instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method:

```
1$user = User::find(1);

2 

3$user->subscription()->swapAndInvoice($premium = 'pri_456');
```

#### [Prorations](#prorations)

By default, Paddle prorates charges when swapping between plans. The `noProrate` method may be used to update the subscriptions without prorating the charges:

```
1$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```

If you would like to disable proration and invoice customers immediately, you may use the `swapAndInvoice` method in combination with `noProrate`:

```
1$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```

Or, to not bill your customer for a subscription change, you may utilize the `doNotBill` method:

```
1$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```

For more information on Paddle's proration policies, please consult Paddle's [proration documentation](https://developer.paddle.com/concepts/subscriptions/proration).

### [Subscription Quantity](#subscription-quantity)

Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. To easily increment or decrement your subscription's quantity, use the `incrementQuantity` and `decrementQuantity` methods:

```
 1$user = User::find(1);

 2 

 3$user->subscription()->incrementQuantity();

 4 

 5// Add five to the subscription's current quantity...

 6$user->subscription()->incrementQuantity(5);

 7 

 8$user->subscription()->decrementQuantity();

 9 

10// Subtract five from the subscription's current quantity...

11$user->subscription()->decrementQuantity(5);
```

Alternatively, you may set a specific quantity using the `updateQuantity` method:

```
1$user->subscription()->updateQuantity(10);
```

The `noProrate` method may be used to update the subscription's quantity without prorating the charges:

```
1$user->subscription()->noProrate()->updateQuantity(10);
```

#### [Quantities for Subscriptions With Multiple Products](#quantities-for-subscription-with-multiple-products)

If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods:

```
1$user->subscription()->incrementQuantity(1, 'price_chat');
```

### [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)

[Subscription with multiple products](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month.

When creating subscription checkout sessions, you may specify multiple products for a given subscription by passing an array of prices as the first argument to the `subscribe` method:

```
 1use Illuminate\Http\Request;

 2 

 3Route::post('/user/subscribe', function (Request $request) {

 4    $checkout = $request->user()->subscribe([

 5        'price_monthly',

 6        'price_chat',

 7    ]);

 8 

 9    return view('billing', ['checkout' => $checkout]);

10});
```

In the example above, the customer will have two prices attached to their `default` subscription. Both prices will be charged on their respective billing intervals. If necessary, you may pass an associative array of key / value pairs to indicate a specific quantity for each price:

```
1$user = User::find(1);

2 

3$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```

If you would like to add another price to an existing subscription, you must use the subscription's `swap` method. When invoking the `swap` method, you should also include the subscription's current prices and quantities as well:

```
1$user = User::find(1);

2 

3$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```

The example above will add the new price, but the customer will not be billed for it until their next billing cycle. If you would like to bill the customer immediately you may use the `swapAndInvoice` method:

```
1$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```

You may remove prices from subscriptions using the `swap` method and omitting the price you want to remove:

```
1$user->subscription()->swap(['price_original' => 2]);
```

You may not remove the last price on a subscription. Instead, you should simply cancel the subscription.

### [Multiple Subscriptions](#multiple-subscriptions)

Paddle allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans.

When your application creates subscriptions, you may provide the type of the subscription to the `subscribe` method as the second argument. The type may be any string that represents the type of subscription the user is initiating:

```
1use Illuminate\Http\Request;

2 

3Route::post('/swimming/subscribe', function (Request $request) {

4    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

5 

6    return view('billing', ['checkout' => $checkout]);

7});
```

In this example, we initiated a monthly swimming subscription for the customer. However, they may want to swap to a yearly subscription at a later time. When adjusting the customer's subscription, we can simply swap the price on the `swimming` subscription:

```
1$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```

Of course, you may also cancel the subscription entirely:

```
1$user->subscription('swimming')->cancel();
```

### [Pausing Subscriptions](#pausing-subscriptions)

To pause a subscription, call the `pause` method on the user's subscription:

```
1$user->subscription()->pause();
```

When a subscription is paused, Cashier will automatically set the `paused_at` column in your database. This column is used to determine when the `paused` method should begin returning `true`. For example, if a customer pauses a subscription on March 1st, but the subscription was not scheduled to recur until March 5th, the `paused` method will continue to return `false` until March 5th. This is because a user is typically allowed to continue using an application until the end of their billing cycle.

By default, pausing happens at the next billing interval so the customer can use the remainder of the period they paid for. If you want to pause a subscription immediately, you may use the `pauseNow` method:

```
1$user->subscription()->pauseNow();
```

Using the `pauseUntil` method, you can pause the subscription until a specific moment in time:

```
1$user->subscription()->pauseUntil(now()->plus(months: 1));
```

Or, you may use the `pauseNowUntil` method to immediately pause the subscription until a given point in time:

```
1$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```

You may determine if a user has paused their subscription but are still on their "grace period" using the `onPausedGracePeriod` method:

```
1if ($user->subscription()->onPausedGracePeriod()) {

2    // ...

3}
```

To resume a paused subscription, you may invoke the `resume` method on the subscription:

```
1$user->subscription()->resume();
```

A subscription cannot be modified while it is paused. If you want to swap to a different plan or update quantities you must resume the subscription first.

### [Canceling Subscriptions](#canceling-subscriptions)

To cancel a subscription, call the `cancel` method on the user's subscription:

```
1$user->subscription()->cancel();
```

When a subscription is canceled, Cashier will automatically set the `ends_at` column in your database. This column is used to determine when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle.

You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method:

```
1if ($user->subscription()->onGracePeriod()) {

2    // ...

3}
```

If you wish to cancel a subscription immediately, you may call the `cancelNow` method on the subscription:

```
1$user->subscription()->cancelNow();
```

To stop a subscription on its grace period from canceling, you may invoke the `stopCancelation` method:

```
1$user->subscription()->stopCancelation();
```

Paddle's subscriptions cannot be resumed after cancelation. If your customer wishes to resume their subscription, they will have to create a new subscription.

## [Subscription Trials](#subscription-trials)

### [With Payment Method Up Front](#with-payment-method-up-front)

If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use set a trial time in the Paddle dashboard on the price your customer is subscribing to. Then, initiate the checkout session as normal:

```
1use Illuminate\Http\Request;

2 

3Route::get('/user/subscribe', function (Request $request) {

4    $checkout = $request->user()

5        ->subscribe('pri_monthly')

6        ->returnTo(route('home'));

7 

8    return view('billing', ['checkout' => $checkout]);

9});
```

When your application receives the `subscription_created` event, Cashier will set the trial period ending date on the subscription record within your application's database as well as instruct Paddle to not begin billing the customer until after this date.

If the customer's subscription is not canceled before the trial ending date they will be charged as soon as the trial expires, so you should be sure to notify your users of their trial ending date.

You may determine if the user is within their trial period using either the `onTrial` method of the user instance:

```
1if ($user->onTrial()) {

2    // ...

3}
```

To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods:

```
1if ($user->hasExpiredTrial()) {

2    // ...

3}
```

To determine if a user is on trial for a specific subscription type, you may provide the type to the `onTrial` or `hasExpiredTrial` methods:

```
1if ($user->onTrial('default')) {

2    // ...

3}

4 

5if ($user->hasExpiredTrial('default')) {

6    // ...

7}
```

### [Without Payment Method Up Front](#without-payment-method-up-front)

If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the customer record attached to your user to your desired trial ending date. This is typically done during user registration:

```
1use App\Models\User;

2 

3$user = User::create([

4    // ...

5]);

6 

7$user->createAsCustomer([

8    'trial_ends_at' => now()->plus(days: 10)

9]);
```

Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the `User` instance will return `true` if the current date is not past the value of `trial_ends_at`:

```
1if ($user->onTrial()) {

2    // User is within their trial period...

3}
```

Once you are ready to create an actual subscription for the user, you may use the `subscribe` method as usual:

```
1use Illuminate\Http\Request;

2 

3Route::get('/user/subscribe', function (Request $request) {

4    $checkout = $request->user()

5        ->subscribe('pri_monthly')

6        ->returnTo(route('home'));

7 

8    return view('billing', ['checkout' => $checkout]);

9});
```

To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription type parameter if you would like to get the trial ending date for a specific subscription other than the default one:

```
1if ($user->onTrial('default')) {

2    $trialEndsAt = $user->trialEndsAt();

3}
```

You may use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not created an actual subscription yet:

```
1if ($user->onGenericTrial()) {

2    // User is within their "generic" trial period...

3}
```

### [Extend or Activate a Trial](#extend-or-activate-a-trial)

You can extend an existing trial period on a subscription by invoking the `extendTrial` method and specifying the moment in time that the trial should end:

```
1$user->subscription()->extendTrial(now()->plus(days: 5));
```

Or, you may immediately activate a subscription by ending its trial by calling the `activate` method on the subscription:

```
1$user->subscription()->activate();
```

## [Handling Paddle Webhooks](#handling-paddle-webhooks)

Paddle can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is registered by the Cashier service provider. This controller will handle all incoming webhook requests.

By default, this controller will automatically handle canceling subscriptions that have too many failed charges, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Paddle webhook event you like.

To ensure your application can handle Paddle webhooks, be sure to [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/notifications-v2). By default, Cashier's webhook controller responds to the `/paddle/webhook` URL path. The full list of all webhooks you should enable in the Paddle control panel are:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

Make sure you protect incoming requests with Cashier's included [webhook signature verification](/docs/13.x/cashier-paddle#verifying-webhook-signatures) middleware.

#### [Webhooks and CSRF Protection](#webhooks-csrf-protection)

Since Paddle webhooks need to bypass Laravel's [CSRF protection](/docs/13.x/csrf), you should ensure that Laravel does not attempt to verify the CSRF token for incoming Paddle webhooks. To accomplish this, you should exclude `paddle/*` from CSRF protection in your application's `bootstrap/app.php` file:

```
1->withMiddleware(function (Middleware $middleware): void {

2    $middleware->preventRequestForgery(except: [

3        'paddle/*',

4    ]);

5})
```

#### [Webhooks and Local Development](#webhooks-local-development)

For Paddle to be able to send your application webhooks during local development, you will need to expose your application via a site sharing service such as [Ngrok](https://ngrok.com/) or [Expose](https://expose.dev/docs/introduction). If you are developing your application locally using [Laravel Sail](/docs/13.x/sail), you may use Sail's [site sharing command](/docs/13.x/sail#sharing-your-site).

### [Defining Webhook Event Handlers](#defining-webhook-event-handlers)

Cashier automatically handles subscription cancelation on failed charges and other common Paddle webhooks. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

Both events contain the full payload of the Paddle webhook. For example, if you wish to handle the `transaction.billed` webhook, you may register a [listener](/docs/13.x/events#defining-listeners) that will handle the event:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use Laravel\Paddle\Events\WebhookReceived;

 6 

 7class PaddleEventListener

 8{

 9    /**

10     * Handle received Paddle webhooks.

11     */

12    public function handle(WebhookReceived $event): void

13    {

14        if ($event->payload['event_type'] === 'transaction.billed') {

15            // Handle the incoming event...

16        }

17    }

18}
```

Cashier also emit events dedicated to the type of the received webhook. In addition to the full payload from Paddle, they also contain the relevant models that were used to process the webhook such as the billable model, the subscription, or the receipt:

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

You can also override the default, built-in webhook route by defining the `CASHIER_WEBHOOK` environment variable in your application's `.env` file. This value should be the full URL to your webhook route and needs to match the URL set in your Paddle control panel:

```
1CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```

### [Verifying Webhook Signatures](#verifying-webhook-signatures)

To secure your webhooks, you may use [Paddle's webhook signatures](https://developer.paddle.com/webhooks/signature-verification). For convenience, Cashier automatically includes a middleware which validates that the incoming Paddle webhook request is valid.

To enable webhook verification, ensure that the `PADDLE_WEBHOOK_SECRET` environment variable is defined in your application's `.env` file. The webhook secret may be retrieved from your Paddle account dashboard.

## [Single Charges](#single-charges)

### [Charging for Products](#charging-for-products)

If you would like to initiate a product purchase for a customer, you may use the `checkout` method on a billable model instance to generate a checkout session for the purchase. The `checkout` method accepts one or multiple price ID's. If necessary, an associative array may be used to provide the quantity of the product that is being purchased:

```
1use Illuminate\Http\Request;

2 

3Route::get('/buy', function (Request $request) {

4    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

5 

6    return view('buy', ['checkout' => $checkout]);

7});
```

After generating the checkout session, you may use Cashier's provided `paddle-button` [Blade component](#overlay-checkout) to allow the user to view the Paddle checkout widget and complete the purchase:

```
1<x-paddle-button :checkout="$checkout" class="px-8 py-4">

2    Buy

3</x-paddle-button>
```

A checkout session has a `customData` method, allowing you to pass any custom data you wish to the underlying transaction creation. Please consult [the Paddle documentation](https://developer.paddle.com/build/transactions/custom-data) to learn more about the options available to you when passing custom data:

```
1$checkout = $user->checkout('pri_tshirt')

2    ->customData([

3        'custom_option' => $value,

4    ]);
```

### [Refunding Transactions](#refunding-transactions)

Refunding transactions will return the refunded amount to your customer's payment method that was used at the time of purchase. If you need to refund a Paddle purchase, you may use the `refund` method on a `Cashier\Paddle\Transaction` model. This method accepts a reason as the first argument, one or more price ID's to refund with optional amounts as an associative array. You may retrieve the transactions for a given billable model using the `transactions` method.

For example, imagine we want to refund a specific transaction for prices `pri_123` and `pri_456`. We want to fully refund `pri_123`, but only refund two dollars for `pri_456`:

```
 1use App\Models\User;

 2 

 3$user = User::find(1);

 4 

 5$transaction = $user->transactions()->first();

 6 

 7$response = $transaction->refund('Accidental charge', [

 8    'pri_123', // Fully refund this price...

 9    'pri_456' => 200, // Only partially refund this price...

10]);
```

The example above refunds specific line items in a transaction. If you want to refund the entire transaction, simply provide a reason:

```
1$response = $transaction->refund('Accidental charge');
```

For more information on refunds, please consult [Paddle's refund documentation](https://developer.paddle.com/build/transactions/create-transaction-adjustments).

Refunds must always be approved by Paddle before fully processing.

### [Crediting Transactions](#crediting-transactions)

Just like refunding, you can also credit transactions. Crediting transactions will add the funds to the customer's balance so it may be used for future purchases. Crediting transactions can only be done for manually-collected transactions and not for automatically-collected transactions (like subscriptions) since Paddle handles subscription credits automatically:

```
1$transaction = $user->transactions()->first();

2 

3// Credit a specific line item fully...

4$response = $transaction->credit('Compensation', 'pri_123');
```

For more info, [see Paddle's documentation on crediting](https://developer.paddle.com/build/transactions/create-transaction-adjustments).

Credits can only be applied for manually-collected transactions. Automatically-collected transactions are credited by Paddle themselves.

## [Transactions](#transactions)

You may easily retrieve an array of a billable model's transactions via the `transactions` property:

```
1use App\Models\User;

2 

3$user = User::find(1);

4 

5$transactions = $user->transactions;
```

Transactions represent payments for your products and purchases and are accompanied by invoices. Only completed transactions are stored in your application's database.

When listing the transactions for a customer, you may use the transaction instance's methods to display the relevant payment information. For example, you may wish to list every transaction in a table, allowing the user to easily download any of the invoices:

```
 1<table>

 2    @foreach ($transactions as $transaction)

 3        <tr>

 4            <td>{{ $transaction->billed_at->toFormattedDateString() }}</td>

 5            <td>{{ $transaction->total() }}</td>

 6            <td>{{ $transaction->tax() }}</td>

 7            <td><a href="{{ route('download-invoice', $transaction->id) }}" target="_blank">Download</a></td>

 8        </tr>

 9    @endforeach

10</table>
```

The `download-invoice` route may look like the following:

```
1use Illuminate\Http\Request;

2use Laravel\Paddle\Transaction;

3 

4Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {

5    return $transaction->redirectToInvoicePdf();

6})->name('download-invoice');
```

### [Past and Upcoming Payments](#past-and-upcoming-payments)

You may use the `lastPayment` and `nextPayment` methods to retrieve and display a customer's past or upcoming payments for recurring subscriptions:

```
1use App\Models\User;

2 

3$user = User::find(1);

4 

5$subscription = $user->subscription();

6 

7$lastPayment = $subscription->lastPayment();

8$nextPayment = $subscription->nextPayment();
```

Both of these methods will return an instance of `Laravel\Paddle\Payment`; however, `lastPayment` will return `null` when transactions have not been synced by webhooks yet, while `nextPayment` will return `null` when the billing cycle has ended (such as when a subscription has been canceled):

```
1Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

## [Testing](#testing)

While testing, you should manually test your billing flow to make sure your integration works as expected.

For automated tests, including those executed within a CI environment, you may use [Laravel's HTTP Client](/docs/13.x/http-client#testing) to fake HTTP calls made to Paddle. Although this does not test the actual responses from Paddle, it does provide a way to test your application without actually calling Paddle's API.
