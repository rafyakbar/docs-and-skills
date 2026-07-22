# Laravel Cashier (Stripe)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
- [Configuration](#configuration)
  * [Billable Model](#billable-model)
  * [API Keys](#api-keys)
  * [Currency Configuration](#currency-configuration)
  * [Tax Configuration](#tax-configuration)
  * [Logging](#logging)
  * [Using Custom Models](#using-custom-models)
- [Quickstart](#quickstart)
  * [Selling Products](#quickstart-selling-products)
  * [Selling Subscriptions](#quickstart-selling-subscriptions)
- [Customers](#customers)
  * [Retrieving Customers](#retrieving-customers)
  * [Creating Customers](#creating-customers)
  * [Updating Customers](#updating-customers)
  * [Balances](#balances)
  * [Tax IDs](#tax-ids)
  * [Syncing Customer Data With Stripe](#syncing-customer-data-with-stripe)
  * [Billing Portal](#billing-portal)
- [Payment Methods](#payment-methods)
  * [Storing Payment Methods](#storing-payment-methods)
  * [Retrieving Payment Methods](#retrieving-payment-methods)
  * [Payment Method Presence](#payment-method-presence)
  * [Updating the Default Payment Method](#updating-the-default-payment-method)
  * [Adding Payment Methods](#adding-payment-methods)
  * [Deleting Payment Methods](#deleting-payment-methods)
- [Subscriptions](#subscriptions)
  * [Creating Subscriptions](#creating-subscriptions)
  * [Checking Subscription Status](#checking-subscription-status)
  * [Changing Prices](#changing-prices)
  * [Subscription Quantity](#subscription-quantity)
  * [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)
  * [Multiple Subscriptions](#multiple-subscriptions)
  * [Usage Based Billing](#usage-based-billing)
  * [Subscription Taxes](#subscription-taxes)
  * [Subscription Anchor Date](#subscription-anchor-date)
  * [Canceling Subscriptions](#cancelling-subscriptions)
  * [Resuming Subscriptions](#resuming-subscriptions)
- [Subscription Trials](#subscription-trials)
  * [With Payment Method Up Front](#with-payment-method-up-front)
  * [Without Payment Method Up Front](#without-payment-method-up-front)
  * [Extending Trials](#extending-trials)
- [Handling Stripe Webhooks](#handling-stripe-webhooks)
  * [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
  * [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
  * [Simple Charge](#simple-charge)
  * [Charge With Invoice](#charge-with-invoice)
  * [Creating Payment Intents](#creating-payment-intents)
  * [Refunding Charges](#refunding-charges)
- [Invoices](#invoices)
  * [Retrieving Invoices](#retrieving-invoices)
  * [Upcoming Invoices](#upcoming-invoices)
  * [Previewing Subscription Invoices](#previewing-subscription-invoices)
  * [Generating Invoice PDFs](#generating-invoice-pdfs)
- [Checkout](#checkout)
  * [Product Checkouts](#product-checkouts)
  * [Single Charge Checkouts](#single-charge-checkouts)
  * [Subscription Checkouts](#subscription-checkouts)
  * [Collecting Tax IDs](#collecting-tax-ids)
  * [Guest Checkouts](#guest-checkouts)
- [Handling Failed Payments](#handling-failed-payments)
  * [Confirming Payments](#confirming-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
  * [Payments Requiring Additional Confirmation](#payments-requiring-additional-confirmation)
  * [Off-session Payment Notifications](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [Testing](#testing)

## [Introduction](#introduction)

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs.

## [Upgrading Cashier](#upgrading-cashier)

When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md).

To prevent breaking changes, Cashier uses a fixed Stripe API version. Cashier 16 utilizes Stripe API version `2025-06-30.basil`. The Stripe API version will be updated on minor releases in order to make use of new Stripe features and improvements.

## [Installation](#installation)

First, install the Cashier package for Stripe using the Composer package manager:

```
1composer require laravel/cashier
```

After installing the package, publish Cashier's migrations using the `vendor:publish` Artisan command:

```
1php artisan vendor:publish --tag="cashier-migrations"
```

Then, migrate your database:

```
1php artisan migrate
```

Cashier's migrations will add several columns to your `users` table. They will also create a new `subscriptions` table to hold all of your customer's subscriptions and a `subscription_items` table for subscriptions with multiple prices.

If you wish, you can also publish Cashier's configuration file using the `vendor:publish` Artisan command:

```
1php artisan vendor:publish --tag="cashier-config"
```

Lastly, to ensure Cashier properly handles all Stripe events, remember to [configure Cashier's webhook handling](#handling-stripe-webhooks).

Stripe recommends that any column used for storing Stripe identifiers should be case-sensitive. Therefore, you should ensure the column collation for the `stripe_id` column is set to `utf8_bin` when using MySQL. More information regarding this can be found in the [Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible).

## [Configuration](#configuration)

### [Billable Model](#billable-model)

Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information:

```
1use Laravel\Cashier\Billable;

2 

3class User extends Authenticatable

4{

5    use Billable;

6}
```

Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class:

```
 1use App\Models\Cashier\User;

 2use Laravel\Cashier\Cashier;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Cashier::useCustomerModel(User::class);

10}
```

If you're using a model other than Laravel's supplied `App\Models\User` model, you'll need to publish and alter the [Cashier migrations](#installation) provided to match your alternative model's table name.

### [API Keys](#api-keys)

Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel:

```
1STRIPE_KEY=your-stripe-key

2STRIPE_SECRET=your-stripe-secret

3STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

You should ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is defined in your application's `.env` file, as this variable is used to ensure that incoming webhooks are actually from Stripe.

### [Currency Configuration](#currency-configuration)

The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file:

```
1CASHIER_CURRENCY=eur
```

In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale:

```
1CASHIER_CURRENCY_LOCALE=nl_BE
```

In order to use locales other than `en`, ensure the `ext-intl` PHP extension is installed and configured on your server.

### [Tax Configuration](#tax-configuration)

Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
1use Laravel\Cashier\Cashier;

2 

3/**

4 * Bootstrap any application services.

5 */

6public function boot(): void

7{

8    Cashier::calculateTaxes();

9}
```

Once tax calculation has been enabled, any new subscriptions and any one-off invoices that are generated will receive automatic tax calculation.

For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this.

### [Logging](#logging)

Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file:

```
1CASHIER_LOGGER=stack
```

Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel.

### [Using Custom Models](#using-custom-models)

You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model:

```
1use Laravel\Cashier\Subscription as CashierSubscription;

2 

3class Subscription extends CashierSubscription

4{

5    // ...

6}
```

After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

```
 1use App\Models\Cashier\Subscription;

 2use App\Models\Cashier\SubscriptionItem;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Cashier::useSubscriptionModel(Subscription::class);

10    Cashier::useSubscriptionItemModel(SubscriptionItem::class);

11}
```

## [Quickstart](#quickstart)

### [Selling Products](#quickstart-selling-products)

Before utilizing Stripe Checkout, you should define Products with fixed prices in your Stripe dashboard. In addition, you should [configure Cashier's webhook handling](#handling-stripe-webhooks).

Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations.

To charge customers for non-recurring, single-charge products, we'll utilize Cashier to direct customers to Stripe Checkout, where they will provide their payment details and confirm their purchase. Once the payment has been made via Checkout, the customer will be redirected to a success URL of your choosing within your application:

```
 1use Illuminate\Http\Request;

 2 

 3Route::get('/checkout', function (Request $request) {

 4    $stripePriceId = 'price_deluxe_album';

 5 

 6    $quantity = 1;

 7 

 8    return $request->user()->checkout([$stripePriceId => $quantity], [

 9        'success_url' => route('checkout-success'),

10        'cancel_url' => route('checkout-cancel'),

11    ]);

12})->name('checkout');

13 

14Route::view('/checkout/success', 'checkout.success')->name('checkout-success');

15Route::view('/checkout/cancel', 'checkout.cancel')->name('checkout-cancel');
```

As you can see in the example above, we will utilize Cashier's provided `checkout` method to redirect the customer to Stripe Checkout for a given "price identifier". When using Stripe, "prices" refer to [defined prices for specific products](https://stripe.com/docs/products-prices/how-products-and-prices-work).

If necessary, the `checkout` method will automatically create a customer in Stripe and connect that Stripe customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success or cancellation page where you can display an informational message to the customer.

#### [Providing Meta Data to Stripe Checkout](#providing-meta-data-to-stripe-checkout)

When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Stripe Checkout to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application.

To accomplish this, you may provide an array of `metadata` to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application:

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

12    return $request->user()->checkout($order->price_ids, [

13        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',

14        'cancel_url' => route('checkout-cancel'),

15        'metadata' => ['order_id' => $order->id],

16    ]);

17})->name('checkout');
```

As you can see in the example above, when a user begins the checkout process, we will provide all of the cart / order's associated Stripe price identifiers to the `checkout` method. Of course, your application is responsible for associating these items with the "shopping cart" or order as a customer adds them. We also provide the order's ID to the Stripe Checkout session via the `metadata` array. Finally, we have added the `CHECKOUT_SESSION_ID` template variable to the Checkout success route. When Stripe redirects customers back to your application, this template variable will automatically be populated with the Checkout session ID.

Next, let's build the Checkout success route. This is the route that users will be redirected to after their purchase has been completed via Stripe Checkout. Within this route, we can retrieve the Stripe Checkout session ID and the associated Stripe Checkout instance in order to access our provided meta data and update our customer's order accordingly:

```
 1use App\Models\Order;

 2use Illuminate\Http\Request;

 3use Laravel\Cashier\Cashier;

 4 

 5Route::get('/checkout/success', function (Request $request) {

 6    $sessionId = $request->get('session_id');

 7 

 8    if ($sessionId === null) {

 9        return;

10    }

11 

12    $session = Cashier::stripe()->checkout->sessions->retrieve($sessionId);

13 

14    if ($session->payment_status !== 'paid') {

15        return;

16    }

17 

18    $orderId = $session['metadata']['order_id'] ?? null;

19 

20    $order = Order::findOrFail($orderId);

21 

22    $order->update(['status' => 'completed']);

23 

24    return view('checkout-success', ['order' => $order]);

25})->name('checkout-success');
```

Please refer to Stripe's documentation for more information on the [data contained by the Checkout session object](https://stripe.com/docs/api/checkout/sessions/object).

### [Selling Subscriptions](#quickstart-selling-subscriptions)

Before utilizing Stripe Checkout, you should define Products with fixed prices in your Stripe dashboard. In addition, you should [configure Cashier's webhook handling](#handling-stripe-webhooks).

Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations.

To learn how to sell subscriptions using Cashier and Stripe Checkout, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Stripe dashboard. In addition, our subscription service might offer an Expert plan as `pro_expert`.

First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button or link should direct the user to a Laravel route which creates the Stripe Checkout session for their chosen plan:

```
 1use Illuminate\Http\Request;

 2 

 3Route::get('/subscription-checkout', function (Request $request) {

 4    return $request->user()

 5        ->newSubscription('default', 'price_basic_monthly')

 6        ->trialDays(5)

 7        ->allowPromotionCodes()

 8        ->checkout([

 9            'success_url' => route('your-success-route'),

10            'cancel_url' => route('your-cancel-route'),

11        ]);

12});
```

As you can see in the example above, we will redirect the customer to a Stripe Checkout session which will allow them to subscribe to our Basic plan. After a successful checkout or cancellation, the customer will be redirected back to the URL we provided to the `checkout` method. To know when their subscription has actually started (since some payment methods require a few seconds to process), we'll also need to [configure Cashier's webhook handling](#handling-stripe-webhooks).

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

18            return redirect('/billing');

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

Of course, customers may want to change their subscription plan to another product or "tier". The easiest way to allow this is by directing customers to Stripe's [Customer Billing Portal](https://stripe.com/docs/no-code/customer-portal), which provides a hosted user interface that allows customers to download invoices, update their payment method, and change subscription plans.

First, define a link or button within your application that directs users to a Laravel route which we will utilize to initiate a Billing Portal session:

```
1<a href="{{ route('billing') }}">

2    Billing

3</a>
```

Next, let's define the route that initiates a Stripe Customer Billing Portal session and redirects the user to the Portal. The `redirectToBillingPortal` method accepts the URL that users should be returned to when exiting the Portal:

```
1use Illuminate\Http\Request;

2 

3Route::get('/billing', function (Request $request) {

4    return $request->user()->redirectToBillingPortal(route('dashboard'));

5})->middleware(['auth'])->name('billing');
```

As long as you have configured Cashier's webhook handling, Cashier will automatically keep your application's Cashier-related database tables in sync by inspecting the incoming webhooks from Stripe. So, for example, when a user cancels their subscription via Stripe's Customer Billing Portal, Cashier will receive the corresponding webhook and mark the subscription as "canceled" in your application's database.

## [Customers](#customers)

### [Retrieving Customers](#retrieving-customers)

You can retrieve a customer by their Stripe ID using the `Cashier::findBillable` method. This method will return an instance of the billable model:

```
1use Laravel\Cashier\Cashier;

2 

3$user = Cashier::findBillable($stripeId);
```

### [Creating Customers](#creating-customers)

Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method:

```
1$stripeCustomer = $user->createAsStripeCustomer();
```

Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create):

```
1$stripeCustomer = $user->createAsStripeCustomer($options);
```

You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model:

```
1$stripeCustomer = $user->asStripeCustomer();
```

The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist:

```
1$stripeCustomer = $user->createOrGetStripeCustomer();
```

### [Updating Customers](#updating-customers)

Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update):

```
1$stripeCustomer = $user->updateStripeCustomer($options);
```

### [Balances](#balances)

Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency:

```
1$balance = $user->balance();
```

To credit a customer's balance, you may provide a value to the `creditBalance` method. If you wish, you may also provide a description:

```
1$user->creditBalance(500, 'Premium customer top-up.');
```

Providing a value to the `debitBalance` method will debit the customer's balance:

```
1$user->debitBalance(300, 'Bad usage penalty.');
```

The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review:

```
 1// Retrieve all transactions...

 2$transactions = $user->balanceTransactions();

 3 

 4foreach ($transactions as $transaction) {

 5    // Transaction amount...

 6    $amount = $transaction->amount(); // $2.31

 7 

 8    // Retrieve the related invoice when available...

 9    $invoice = $transaction->invoice();

10}
```

### [Tax IDs](#tax-ids)

Cashier offers an easy way to manage a customer's tax IDs. For example, the `taxIds` method may be used to retrieve all of the [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object) that are assigned to a customer as a collection:

```
1$taxIds = $user->taxIds();
```

You can also retrieve a specific tax ID for a customer by its identifier:

```
1$taxId = $user->findTaxId('txi_belgium');
```

You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method:

```
1$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```

The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks).

You may delete a tax ID using the `deleteTaxId` method:

```
1$user->deleteTaxId('txi_belgium');
```

### [Syncing Customer Data With Stripe](#syncing-customer-data-with-stripe)

Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's.

To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model:

```
 1use App\Models\User;

 2use function Illuminate\Events\queueable;

 3 

 4/**

 5 * The "booted" method of the model.

 6 */

 7protected static function booted(): void

 8{

 9    static::updated(queueable(function (User $customer) {

10        if ($customer->hasStripeId()) {

11            $customer->syncStripeCustomerDetails();

12        }

13    }));

14}
```

Now, every time your customer model is updated, its information will be synced with Stripe. For convenience, Cashier will automatically sync your customer's information with Stripe on the initial creation of the customer.

You may customize the columns used for syncing customer information to Stripe by overriding a variety of methods provided by Cashier. For example, you may override the `stripeName` method to customize the attribute that should be considered the customer's "name" when Cashier syncs customer information to Stripe:

```
1/**

2 * Get the customer name that should be synced to Stripe.

3 */

4public function stripeName(): string|null

5{

6    return $this->company_name;

7}
```

Similarly, you may override the `stripeEmail`, `stripePhone` (20 character maximum), `stripeAddress`, and `stripePreferredLocales` methods. These methods will sync information to their corresponding customer parameters when [updating the Stripe customer object](https://stripe.com/docs/api/customers/update). If you wish to take total control over the customer information sync process, you may override the `syncStripeCustomerDetails` method.

### [Billing Portal](#billing-portal)

Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route:

```
1use Illuminate\Http\Request;

2 

3Route::get('/billing-portal', function (Request $request) {

4    return $request->user()->redirectToBillingPortal();

5});
```

By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method:

```
1use Illuminate\Http\Request;

2 

3Route::get('/billing-portal', function (Request $request) {

4    return $request->user()->redirectToBillingPortal(route('billing'));

5});
```

If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method:

```
1$url = $request->user()->billingPortalUrl(route('billing'));
```

## [Payment Methods](#payment-methods)

### [Storing Payment Methods](#storing-payment-methods)

In order to create subscriptions or perform "one-off" charges with Stripe, your application will need to securely collect payment details from the customer. The approach used to accomplish this differs based on whether you plan to store the payment method for future subscriptions or immediately process a single charge, so we will examine both below.

Stripe's [Payment Element](https://stripe.com/docs/payments/payment-element) may be used to support multiple payment methods, such as cards, Apple Pay, Google Pay, and iDEAL.

#### [Payment Element for Subscriptions](#payment-element-for-subscriptions)

First, create a Setup Intent and pass it to your view:

```
1return view('subscribe', [

2    'intent' => $user->createSetupIntent()

3]);
```

Mount the Payment Element using the Setup Intent's `client_secret`:

```
 1<div id="payment-element"></div>

 2<button id="submit">Subscribe</button>

 3 

 4<script src="https://js.stripe.com/v3/"></script>

 5<script>

 6    const stripe = Stripe('stripe-public-key');

 7 

 8    const elements = stripe.elements({

 9        clientSecret: '{{ $intent->client_secret }}'

10    });

11 

12    const paymentElement = elements.create('payment');

13 

14    paymentElement.mount('#payment-element');

15 

16    document.getElementById('submit').addEventListener('click', async () => {

17        const { error } = await stripe.confirmSetup({

18            elements,

19            confirmParams: {

20                return_url: '{{ route("subscription.complete") }}',

21            },

22        });

23 

24        if (error) {

25            // Display "error.message" to the user...

26        }

27    });

28</script>
```

After Stripe redirects to your `return_url`, the `setup_intent` ID will be available as a query string parameter. You may use this value to retrieve the payment method and create the subscription:

```
 1use Illuminate\Http\Request;

 2 

 3Route::get('/subscription/complete', function (Request $request) {

 4    $setupIntent = $request->user()->findSetupIntent(

 5        $request->setup_intent

 6    );

 7 

 8    $paymentMethod = $setupIntent->payment_method;

 9 

10    $request->user()

11        ->newSubscription('default', 'price_xxx')

12        ->create($paymentMethod);

13 

14    return redirect('/dashboard');

15})->name('subscription.complete');
```

If you are using the Payment Element to update a customer's default payment method instead of creating a subscription, you may pass the payment method identifier to the [`updateDefaultPaymentMethod`](#updating-the-default-payment-method) method.

#### [Payment Element for Single Charges](#payment-element-for-single-charges)

For one-off payments, create a Payment Intent using Cashier's `pay` method. Typically, you should store the Payment Intent ID on your application's corresponding order so that the order can be retrieved after Stripe redirects the customer back to your application. The following example assumes your application has an `Order` model with `user_id`, `amount`, `status`, and `stripe_payment_intent_id` columns:

```
 1use App\Models\Order;

 2use Illuminate\Http\Request;

 3 

 4Route::post('/pay', function (Request $request) {

 5    $amount = 1000;

 6 

 7    $payment = $request->user()->pay($amount);

 8 

 9    $order = Order::create([

10        'user_id' => $request->user()->id,

11        'amount' => $amount,

12        'status' => 'pending',

13        'stripe_payment_intent_id' => $payment->id,

14    ]);

15 

16    return view('checkout', [

17        'clientSecret' => $payment->client_secret,

18        'order' => $order,

19    ]);

20});
```

Then, mount the Payment Element and confirm the payment:

```
 1<div id="payment-element"></div>

 2<button id="submit">Pay Now</button>

 3 

 4<script src="https://js.stripe.com/v3/"></script>

 5<script>

 6    const stripe = Stripe('stripe-public-key');

 7 

 8    const elements = stripe.elements({

 9        clientSecret: '{{ $clientSecret }}'

10    });

11 

12    const paymentElement = elements.create('payment');

13 

14    paymentElement.mount('#payment-element');

15 

16    document.getElementById('submit').addEventListener('click', async () => {

17        const { error } = await stripe.confirmPayment({

18            elements,

19            confirmParams: {

20                return_url: '{{ route("payment.complete") }}',

21            },

22        });

23 

24        if (error) {

25            // Display "error.message" to the user...

26        }

27    });

28</script>
```

After the redirect, you may use the `payment_intent` query string parameter to retrieve the corresponding order and Payment Intent. Before fulfilling the order, you should verify that the order belongs to the authenticated customer and that the Payment Intent belongs to the authenticated customer and has succeeded:

```
 1use App\Models\Order;

 2use Illuminate\Http\Request;

 3 

 4Route::get('/payment/complete', function (Request $request) {

 5    $order = Order::where('user_id', $request->user()->id)

 6        ->where('stripe_payment_intent_id', $request->payment_intent)

 7        ->firstOrFail();

 8 

 9    $paymentIntent = $request->user()

10        ->stripe()

11        ->paymentIntents

12        ->retrieve($request->payment_intent);

13 

14    if ($paymentIntent->customer === $request->user()->stripe_id &&

15        $paymentIntent->status === 'succeeded') {

16        $order->update(['status' => 'paid']);

17 

18        // Fulfill the order...

19    }

20 

21    return redirect('/dashboard');

22})->name('payment.complete');
```

### [Retrieving Payment Methods](#retrieving-payment-methods)

The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances:

```
1$paymentMethods = $user->paymentMethods();
```

By default, this method will return payment methods of every type. To retrieve payment methods of a specific type, you may pass the `type` as an argument to the method:

```
1$paymentMethods = $user->paymentMethods('sepa_debit');
```

To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used:

```
1$paymentMethod = $user->defaultPaymentMethod();
```

You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method:

```
1$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```

### [Payment Method Presence](#payment-method-presence)

To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method:

```
1if ($user->hasDefaultPaymentMethod()) {

2    // ...

3}
```

You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account:

```
1if ($user->hasPaymentMethod()) {

2    // ...

3}
```

This method will determine if the billable model has any payment method at all. To determine if a payment method of a specific type exists for the model, you may pass the `type` as an argument to the method:

```
1if ($user->hasPaymentMethod('sepa_debit')) {

2    // ...

3}
```

### [Updating the Default Payment Method](#updating-the-default-payment-method)

The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method:

```
1$user->updateDefaultPaymentMethod($paymentMethod);
```

To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method:

```
1$user->updateDefaultPaymentMethodFromStripe();
```

The default payment method on a customer can only be used for invoicing and creating new subscriptions. Due to limitations imposed by Stripe, it may not be used for single charges.

### [Adding Payment Methods](#adding-payment-methods)

To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier:

```
1$user->addPaymentMethod($paymentMethod);
```

To learn how to retrieve payment method identifiers please review the [payment method storage documentation](#storing-payment-methods).

### [Deleting Payment Methods](#deleting-payment-methods)

To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete:

```
1$paymentMethod->delete();
```

The `deletePaymentMethod` method will delete a specific payment method from the billable model:

```
1$user->deletePaymentMethod('pm_visa');
```

The `deletePaymentMethods` method will delete all of the payment method information for the billable model:

```
1$user->deletePaymentMethods();
```

By default, this method will delete payment methods of every type. To delete payment methods of a specific type you can pass the `type` as an argument to the method:

```
1$user->deletePaymentMethods('sepa_debit');
```

If a user has an active subscription, your application should not allow them to delete their default payment method.

## [Subscriptions](#subscriptions)

Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more.

### [Creating Subscriptions](#creating-subscriptions)

To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription:

```
1use Illuminate\Http\Request;

2 

3Route::post('/user/subscribe', function (Request $request) {

4    $request->user()->newSubscription(

5        'default', 'price_monthly'

6    )->create($request->paymentMethodId);

7 

8    // ...

9});
```

The first argument passed to the `newSubscription` method should be the internal type of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription type is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument is the specific price the user is subscribing to. This value should correspond to the price's identifier in Stripe.

The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information.

Passing a payment method identifier directly to the `create` subscription method will also automatically add it to the user's stored payment methods.

#### [Collecting Recurring Payments via Invoice Emails](#collecting-recurring-payments-via-invoice-emails)

Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices:

```
1$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```

The amount of time a customer has to pay their invoice before their subscription is canceled is determined by the `days_until_due` option. By default, this is 30 days; however, you may provide a specific value for this option if you wish:

```
1$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [

2    'days_until_due' => 30

3]);
```

#### [Quantities](#subscription-quantities)

If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription:

```
1$user->newSubscription('default', 'price_monthly')

2    ->quantity(5)

3    ->create($paymentMethod);
```

#### [Additional Details](#additional-details)

If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method:

```
1$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [

2    'email' => $email,

3], [

4    'metadata' => ['note' => 'Some extra information.'],

5]);
```

#### [Coupons](#coupons)

If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method:

```
1$user->newSubscription('default', 'price_monthly')

2    ->withCoupon('code')

3    ->create($paymentMethod);
```

Or, if you would like to apply a [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes), you may use the `withPromotionCode` method:

```
1$user->newSubscription('default', 'price_monthly')

2    ->withPromotionCode('promo_code_id')

3    ->create($paymentMethod);
```

The given promotion code ID should be the Stripe API ID assigned to the promotion code and not the customer facing promotion code. If you need to find a promotion code ID based on a given customer facing promotion code, you may use the `findPromotionCode` method:

```
1// Find a promotion code ID by its customer facing code...

2$promotionCode = $user->findPromotionCode('SUMMERSALE');

3 

4// Find an active promotion code ID by its customer facing code...

5$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```

In the example above, the returned `$promotionCode` object is an instance of `Laravel\Cashier\PromotionCode`. This class decorates an underlying `Stripe\PromotionCode` object. You can retrieve the coupon related to the promotion code by invoking the `coupon` method:

```
1$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```

The coupon instance allows you to determine the discount amount and whether the coupon represents a fixed discount or percentage based discount:

```
1if ($coupon->isPercentage()) {

2    return $coupon->percentOff().'%'; // 21.5%

3} else {

4    return $coupon->amountOff(); // $5.99

5}
```

You can also retrieve the discounts that are currently applied to a customer or subscription:

```
1$discount = $billable->discount();

2 

3$discount = $subscription->discount();
```

The returned `Laravel\Cashier\Discount` instances decorate an underlying `Stripe\Discount` object instance. You may retrieve the coupon related to this discount by invoking the `coupon` method:

```
1$coupon = $subscription->discount()->coupon();
```

If you would like to apply a new coupon or promotion code to a customer or subscription, you may do so via the `applyCoupon` or `applyPromotionCode` methods:

```
1$billable->applyCoupon('coupon_id');

2$billable->applyPromotionCode('promotion_code_id');

3 

4$subscription->applyCoupon('coupon_id');

5$subscription->applyPromotionCode('promotion_code_id');
```

Remember, you should use the Stripe API ID assigned to the promotion code and not the customer facing promotion code. Only one coupon or promotion code can be applied to a customer or subscription at a given time.

For more info on this subject, please consult the Stripe documentation regarding [coupons](https://stripe.com/docs/billing/subscriptions/coupons) and [promotion codes](https://stripe.com/docs/billing/subscriptions/coupons/codes).

#### [Adding Subscriptions](#adding-subscriptions)

If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder:

```
1use App\Models\User;

2 

3$user = User::find(1);

4 

5$user->newSubscription('default', 'price_monthly')->add();
```

#### [Creating Subscriptions From the Stripe Dashboard](#creating-subscriptions-from-the-stripe-dashboard)

You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a type of `default`. To customize the subscription type that is assigned to dashboard created subscriptions, [define webhook event handlers](#defining-webhook-event-handlers).

In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different types, only one type of subscription may be added through the Stripe dashboard.

Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If a customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database.

### [Checking Subscription Status](#checking-subscription-status)

Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the type of the subscription as its first argument:

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

18        if ($request->user() && ! $request->user()->subscribed('default')) {

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
1if ($user->subscription('default')->onTrial()) {

2    // ...

3}
```

The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard:

```
1if ($user->subscribedToProduct('prod_premium', 'default')) {

2    // ...

3}
```

By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product:

```
1if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {

2    // ...

3}
```

The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID:

```
1if ($user->subscribedToPrice('price_basic_monthly', 'default')) {

2    // ...

3}
```

The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period:

```
1if ($user->subscription('default')->recurring()) {

2    // ...

3}
```

If a user has two subscriptions with the same type, the most recent subscription will always be returned by the `subscription` method. For example, a user might have two subscription records with the type of `default`; however, one of the subscriptions may be an old, expired subscription, while the other is the current, active subscription. The most recent subscription will always be returned while older subscriptions are kept in the database for historical review.

#### [Canceled Subscription Status](#cancelled-subscription-status)

To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method:

```
1if ($user->subscription('default')->canceled()) {

2    // ...

3}
```

You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time:

```
1if ($user->subscription('default')->onGracePeriod()) {

2    // ...

3}
```

To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method:

```
1if ($user->subscription('default')->ended()) {

2    // ...

3}
```

#### [Incomplete and Past Due Status](#incomplete-and-past-due-status)

If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table.

Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance:

```
1if ($user->hasIncompletePayment('default')) {

2    // ...

3}

4 

5if ($user->subscription('default')->hasIncompletePayment()) {

6    // ...

7}
```

When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier:

```
1<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">

2    Please confirm your payment.

3</a>
```

If you would like the subscription to still be considered active when it's in a `past_due` or `incomplete` state, you may use the `keepPastDueSubscriptionsActive` and `keepIncompleteSubscriptionsActive` methods provided by Cashier. Typically, these methods should be called in the `register` method of your `App\Providers\AppServiceProvider`:

```
 1use Laravel\Cashier\Cashier;

 2 

 3/**

 4 * Register any application services.

 5 */

 6public function register(): void

 7{

 8    Cashier::keepPastDueSubscriptionsActive();

 9    Cashier::keepIncompleteSubscriptionsActive();

10}
```

When a subscription is in an `incomplete` state it cannot be changed until the payment is confirmed. Therefore, the `swap` and `updateQuantity` methods will throw an exception when the subscription is in an `incomplete` state.

#### [Subscription Scopes](#subscription-scopes)

Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state:

```
1// Get all active subscriptions...

2$subscriptions = Subscription::query()->active()->get();

3 

4// Get all of the canceled subscriptions for a user...

5$subscriptions = $user->subscriptions()->canceled()->get();
```

A complete list of available scopes is available below:

```
 1Subscription::query()->active();

 2Subscription::query()->canceled();

 3Subscription::query()->ended();

 4Subscription::query()->incomplete();

 5Subscription::query()->notCanceled();

 6Subscription::query()->notOnGracePeriod();

 7Subscription::query()->notOnTrial();

 8Subscription::query()->onGracePeriod();

 9Subscription::query()->onTrial();

10Subscription::query()->pastDue();

11Subscription::query()->recurring();
```

### [Changing Prices](#changing-prices)

After a customer is subscribed to your application, they may occasionally want to change to a new subscription price. To swap a customer to a new price, pass the Stripe price's identifier to the `swap` method. When swapping prices, it is assumed that the user would like to re-activate their subscription if it was previously canceled. The given price identifier should correspond to a Stripe price identifier available in the Stripe dashboard:

```
1use App\Models\User;

2 

3$user = App\Models\User::find(1);

4 

5$user->subscription('default')->swap('price_yearly');
```

If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained.

If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method:

```
1$user->subscription('default')

2    ->skipTrial()

3    ->swap('price_yearly');
```

If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method:

```
1$user = User::find(1);

2 

3$user->subscription('default')->swapAndInvoice('price_yearly');
```

#### [Prorations](#prorations)

By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges:

```
1$user->subscription('default')->noProrate()->swap('price_yearly');
```

For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations).

Executing the `noProrate` method before the `swapAndInvoice` method will have no effect on proration. An invoice will always be issued.

### [Subscription Quantity](#subscription-quantity)

Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity:

```
 1use App\Models\User;

 2 

 3$user = User::find(1);

 4 

 5$user->subscription('default')->incrementQuantity();

 6 

 7// Add five to the subscription's current quantity...

 8$user->subscription('default')->incrementQuantity(5);

 9 

10$user->subscription('default')->decrementQuantity();

11 

12// Subtract five from the subscription's current quantity...

13$user->subscription('default')->decrementQuantity(5);
```

Alternatively, you may set a specific quantity using the `updateQuantity` method:

```
1$user->subscription('default')->updateQuantity(10);
```

The `noProrate` method may be used to update the subscription's quantity without prorating the charges:

```
1$user->subscription('default')->noProrate()->updateQuantity(10);
```

For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities).

#### [Quantities for Subscriptions With Multiple Products](#quantities-for-subscription-with-multiple-products)

If your subscription is a [subscription with multiple products](#subscriptions-with-multiple-products), you should pass the ID of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods:

```
1$user->subscription('default')->incrementQuantity(1, 'price_chat');
```

### [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)

[Subscription with multiple products](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing products to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on product for an additional $15 per month. Information for subscriptions with multiple products is stored in Cashier's `subscription_items` database table.

You may specify multiple products for a given subscription by passing an array of prices as the second argument to the `newSubscription` method:

```
 1use Illuminate\Http\Request;

 2 

 3Route::post('/user/subscribe', function (Request $request) {

 4    $request->user()->newSubscription('default', [

 5        'price_monthly',

 6        'price_chat',

 7    ])->create($request->paymentMethodId);

 8 

 9    // ...

10});
```

In the example above, the customer will have two prices attached to their `default` subscription. Both prices will be charged on their respective billing intervals. If necessary, you may use the `quantity` method to indicate a specific quantity for each price:

```
1$user = User::find(1);

2 

3$user->newSubscription('default', ['price_monthly', 'price_chat'])

4    ->quantity(5, 'price_chat')

5    ->create($paymentMethod);
```

If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method:

```
1$user = User::find(1);

2 

3$user->subscription('default')->addPrice('price_chat');
```

The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method:

```
1$user->subscription('default')->addPriceAndInvoice('price_chat');
```

If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods:

```
1$user = User::find(1);

2 

3$user->subscription('default')->addPrice('price_chat', 5);
```

You may remove prices from subscriptions using the `removePrice` method:

```
1$user->subscription('default')->removePrice('price_chat');
```

You may not remove the last price on a subscription. Instead, you should simply cancel the subscription.

#### [Swapping Prices](#swapping-prices)

You may also change the prices attached to a subscription with multiple products. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on product and you want to upgrade the customer from the `price_basic` to the `price_pro` price:

```
1use App\Models\User;

2 

3$user = User::find(1);

4 

5$user->subscription('default')->swap(['price_pro', 'price_chat']);
```

When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created.

You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities:

```
1$user = User::find(1);

2 

3$user->subscription('default')->swap([

4    'price_pro' => ['quantity' => 5],

5    'price_chat'

6]);
```

If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices:

```
1$user = User::find(1);

2 

3$user->subscription('default')

4    ->findItemOrFail('price_basic')

5    ->swap('price_pro');
```

#### [Proration](#proration)

By default, Stripe will prorate charges when adding or removing prices from a subscription with multiple products. If you would like to make a price adjustment without proration, you should chain the `noProrate` method onto your price operation:

```
1$user->subscription('default')->noProrate()->removePrice('price_chat');
```

#### [Quantities](#swapping-quantities)

If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the ID of the price as an additional argument to the method:

```
1$user = User::find(1);

2 

3$user->subscription('default')->incrementQuantity(5, 'price_chat');

4 

5$user->subscription('default')->decrementQuantity(3, 'price_chat');

6 

7$user->subscription('default')->updateQuantity(10, 'price_chat');
```

When a subscription has multiple prices the `stripe_price` and `quantity` attributes on the `Subscription` model will be `null`. To access the individual price attributes, you should use the `items` relationship available on the `Subscription` model.

#### [Subscription Items](#subscription-items)

When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription:

```
1use App\Models\User;

2 

3$user = User::find(1);

4 

5$subscriptionItem = $user->subscription('default')->items->first();

6 

7// Retrieve the Stripe price and quantity for a specific item...

8$stripePrice = $subscriptionItem->stripe_price;

9$quantity = $subscriptionItem->quantity;
```

You can also retrieve a specific price using the `findItemOrFail` method:

```
1$user = User::find(1);

2 

3$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```

### [Multiple Subscriptions](#multiple-subscriptions)

Stripe allows your customers to have multiple subscriptions simultaneously. For example, you may run a gym that offers a swimming subscription and a weight-lifting subscription, and each subscription may have different pricing. Of course, customers should be able to subscribe to either or both plans.

When your application creates subscriptions, you may provide the type of the subscription to the `newSubscription` method. The type may be any string that represents the type of subscription the user is initiating:

```
1use Illuminate\Http\Request;

2 

3Route::post('/swimming/subscribe', function (Request $request) {

4    $request->user()->newSubscription('swimming')

5        ->price('price_swimming_monthly')

6        ->create($request->paymentMethodId);

7 

8    // ...

9});
```

In this example, we initiated a monthly swimming subscription for the customer. However, they may want to swap to a yearly subscription at a later time. When adjusting the customer's subscription, we can simply swap the price on the `swimming` subscription:

```
1$user->subscription('swimming')->swap('price_swimming_yearly');
```

Of course, you may also cancel the subscription entirely:

```
1$user->subscription('swimming')->cancel();
```

### [Usage Based Billing](#usage-based-billing)

[Usage based billing](https://stripe.com/docs/billing/subscriptions/metered-billing) allows you to charge customers based on their product usage during a billing cycle. For example, you may charge customers based on the number of text messages or emails they send per month.

To start using usage billing, you will first need to create a new product in your Stripe dashboard with a [usage based billing model](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide) and a [meter](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter). After creating the meter, store the associated event name and meter ID, which you will need to report and retrieve usage. Then, use the `meteredPrice` method to add the metered price ID to a customer subscription:

```
1use Illuminate\Http\Request;

2 

3Route::post('/user/subscribe', function (Request $request) {

4    $request->user()->newSubscription('default')

5        ->meteredPrice('price_metered')

6        ->create($request->paymentMethodId);

7 

8    // ...

9});
```

You may also start a metered subscription via [Stripe Checkout](#checkout):

```
1$checkout = Auth::user()

2    ->newSubscription('default', [])

3    ->meteredPrice('price_metered')

4    ->checkout();

5 

6return view('your-checkout-view', [

7    'checkout' => $checkout,

8]);
```

#### [Reporting Usage](#reporting-usage)

As your customer uses your application, you will report their usage to Stripe so that they can be billed accurately. To report the usage of a metered event, you may use the `reportMeterEvent` method on your `Billable` model:

```
1$user = User::find(1);

2 

3$user->reportMeterEvent('emails-sent');
```

By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period:

```
1$user = User::find(1);

2 

3$user->reportMeterEvent('emails-sent', quantity: 15);
```

To retrieve a customer's event summary for a meter, you may use a `Billable` instance's `meterEventSummaries` method:

```
1$user = User::find(1);

2 

3$meterUsage = $user->meterEventSummaries($meterId);

4 

5$meterUsage->first()->aggregated_value // 10
```

Please refer to Stripe's [Meter Event Summary object documentation](https://docs.stripe.com/api/billing/meter-event_summary/object) for more information on meter event summaries.

To [list all meters](https://docs.stripe.com/api/billing/meter/list), you may use a `Billable` instance's `meters` method:

```
1$user = User::find(1);

2 

3$user->meters();
```

### [Subscription Taxes](#subscription-taxes)

Instead of calculating Tax Rates manually, you can [automatically calculate taxes using Stripe Tax](#tax-configuration)

To specify the tax rates a user pays on a subscription, you should implement the `taxRates` method on your billable model and return an array containing the Stripe tax rate IDs. You can define these tax rates in [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates):

```
1/**

2 * The tax rates that should apply to the customer's subscriptions.

3 *

4 * @return array<int, string>

5 */

6public function taxRates(): array

7{

8    return ['txr_id'];

9}
```

The `taxRates` method enables you to apply a tax rate on a customer-by-customer basis, which may be helpful for a user base that spans multiple countries and tax rates.

If you're offering subscriptions with multiple products, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model:

```
 1/**

 2 * The tax rates that should apply to the customer's subscriptions.

 3 *

 4 * @return array<string, array<int, string>>

 5 */

 6public function priceTaxRates(): array

 7{

 8    return [

 9        'price_monthly' => ['txr_id'],

10    ];

11}
```

The `taxRates` method only applies to subscription charges. If you use Cashier to make "one-off" charges, you will need to manually specify the tax rate at that time.

#### [Syncing Tax Rates](#syncing-tax-rates)

When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance:

```
1$user->subscription('default')->syncTaxRates();
```

This will also sync any item tax rates for a subscription with multiple products. If your application is offering subscriptions with multiple products, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes).

#### [Tax Exemption](#tax-exemption)

Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status:

```
1use App\Models\User;

2 

3$user = User::find(1);

4 

5$user->isTaxExempt();

6$user->isNotTaxExempt();

7$user->reverseChargeApplies();
```

These methods are also available on any `Laravel\Cashier\Invoice` object. However, when invoked on an `Invoice` object, the methods will determine the exemption status at the time the invoice was created.

### [Subscription Anchor Date](#subscription-anchor-date)

By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method:

```
 1use Illuminate\Http\Request;

 2 

 3Route::post('/user/subscribe', function (Request $request) {

 4    $anchor = Carbon::parse('first day of next month');

 5 

 6    $request->user()->newSubscription('default', 'price_monthly')

 7        ->anchorBillingCycleOn($anchor->startOfDay())

 8        ->create($request->paymentMethodId);

 9 

10    // ...

11});
```

For more information on managing subscription billing cycles, consult the [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)

### [Cancelling Subscriptions](#cancelling-subscriptions)

To cancel a subscription, call the `cancel` method on the user's subscription:

```
1$user->subscription('default')->cancel();
```

When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`.

For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle.

You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method:

```
1if ($user->subscription('default')->onGracePeriod()) {

2    // ...

3}
```

If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription:

```
1$user->subscription('default')->cancelNow();
```

If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription:

```
1$user->subscription('default')->cancelNowAndInvoice();
```

You may also choose to cancel the subscription at a specific moment in time:

```
1$user->subscription('default')->cancelAt(

2    now()->plus(days: 10)

3);
```

Finally, you should always cancel user subscriptions before deleting the associated user model:

```
1$user->subscription('default')->cancelNow();

2 

3$user->delete();
```

### [Resuming Subscriptions](#resuming-subscriptions)

If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription:

```
1$user->subscription('default')->resume();
```

If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle.

## [Subscription Trials](#subscription-trials)

### [With Payment Method Up Front](#with-payment-method-up-front)

If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions:

```
1use Illuminate\Http\Request;

2 

3Route::post('/user/subscribe', function (Request $request) {

4    $request->user()->newSubscription('default', 'price_monthly')

5        ->trialDays(10)

6        ->create($request->paymentMethodId);

7 

8    // ...

9});
```

This method will set the trial period ending date on the subscription record within the database and instruct Stripe to not begin billing the customer until after this date. When using the `trialDays` method, Cashier will overwrite any default trial period configured for the price in Stripe.

If the customer's subscription is not canceled before the trial ending date they will be charged as soon as the trial expires, so you should be sure to notify your users of their trial ending date.

The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end:

```
1use Illuminate\Support\Carbon;

2 

3$user->newSubscription('default', 'price_monthly')

4    ->trialUntil(Carbon::now()->plus(days: 10))

5    ->create($paymentMethod);
```

You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent:

```
1if ($user->onTrial('default')) {

2    // ...

3}

4 

5if ($user->subscription('default')->onTrial()) {

6    // ...

7}
```

You may use the `endTrial` method to immediately end a subscription trial:

```
1$user->subscription('default')->endTrial();
```

To determine if an existing trial has expired, you may use the `hasExpiredTrial` methods:

```
1if ($user->hasExpiredTrial('default')) {

2    // ...

3}

4 

5if ($user->subscription('default')->hasExpiredTrial()) {

6    // ...

7}
```

#### [Defining Trial Days in Stripe / Cashier](#defining-trial-days-in-stripe-cashier)

You may choose to define how many trial days your price's receive in the Stripe dashboard or always pass them explicitly using Cashier. If you choose to define your price's trial days in Stripe you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `skipTrial()` method.

### [Without Payment Method Up Front](#without-payment-method-up-front)

If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration:

```
1use App\Models\User;

2 

3$user = User::create([

4    // ...

5    'trial_ends_at' => now()->plus(days: 10),

6]);
```

Be sure to add a [date cast](/docs/13.x/eloquent-mutators#date-casting) for the `trial_ends_at` attribute within your billable model's class definition.

Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`:

```
1if ($user->onTrial()) {

2    // User is within their trial period...

3}
```

Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual:

```
1$user = User::find(1);

2 

3$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```

To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription type parameter if you would like to get the trial ending date for a specific subscription other than the default one:

```
1if ($user->onTrial()) {

2    $trialEndsAt = $user->trialEndsAt('main');

3}
```

You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription:

```
1if ($user->onGenericTrial()) {

2    // User is within their "generic" trial period...

3}
```

### [Extending Trials](#extending-trials)

The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice:

```
 1use App\Models\User;

 2 

 3$subscription = User::find(1)->subscription('default');

 4 

 5// End the trial 7 days from now...

 6$subscription->extendTrial(

 7    now()->plus(days: 7)

 8);

 9 

10// Add an additional 5 days to the trial...

11$subscription->extendTrial(

12    $subscription->trial_ends_at->plus(days: 5)

13);
```

## [Handling Stripe Webhooks](#handling-stripe-webhooks)

You may use [the Stripe CLI](https://stripe.com/docs/stripe-cli) to help test webhooks during local development.

Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests.

By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like.

To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

For convenience, Cashier includes a `cashier:webhook` Artisan command. This command will create a webhook in Stripe that listens to all of the events required by Cashier:

```
1php artisan cashier:webhook
```

By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL:

```
1php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option:

```
1php artisan cashier:webhook --api-version="2019-12-03"
```

After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command:

```
1php artisan cashier:webhook --disabled
```

Make sure you protect incoming Stripe webhook requests with Cashier's included [webhook signature verification](#verifying-webhook-signatures) middleware.

#### [Webhooks and CSRF Protection](#webhooks-csrf-protection)

Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/13.x/csrf), you should ensure that Laravel does not attempt to validate the CSRF token for incoming Stripe webhooks. To accomplish this, you should exclude `stripe/*` from CSRF protection in your application's `bootstrap/app.php` file:

```
1->withMiddleware(function (Middleware $middleware): void {

2    $middleware->preventRequestForgery(except: [

3        'stripe/*',

4    ]);

5})
```

### [Defining Webhook Event Handlers](#defining-webhook-event-handlers)

Cashier automatically handles subscription cancellations for failed charges and other common Stripe webhook events. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/13.x/events#defining-listeners) that will handle the event:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use Laravel\Cashier\Events\WebhookReceived;

 6 

 7class StripeEventListener

 8{

 9    /**

10     * Handle received Stripe webhooks.

11     */

12    public function handle(WebhookReceived $event): void

13    {

14        if ($event->payload['type'] === 'invoice.payment_succeeded') {

15            // Handle the incoming event...

16        }

17    }

18}
```

### [Verifying Webhook Signatures](#verifying-webhook-signatures)

To secure your webhooks, you may use [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures). For convenience, Cashier automatically includes a middleware which validates that the incoming Stripe webhook request is valid.

To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard.

## [Single Charges](#single-charges)

### [Simple Charge](#simple-charge)

If you would like to make a one-time charge against a customer using a payment method identifier, you may use the `charge` method on a billable model instance. If you need to collect payment details from a customer before processing a one-time charge, see the [Payment Element for Single Charges](#payment-element-for-single-charges) documentation:

```
1use Illuminate\Http\Request;

2 

3Route::post('/purchase', function (Request $request) {

4    $payment = $request->user()->charge(

5        100, $request->paymentMethodId

6    );

7 

8    // ...

9});
```

The `charge` method accepts an array as its third argument, allowing you to pass any options you wish to the underlying Stripe Payment Intent creation. More information regarding the options available to you when creating Payment Intents may be found in the [Stripe documentation](https://stripe.com/docs/api/payment_intents/create):

```
1$user->charge(100, $paymentMethod, [

2    'custom_option' => $value,

3]);
```

You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model:

```
1use App\Models\User;

2 

3$payment = (new User)->charge(100, $paymentMethod);
```

The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method:

```
1try {

2    $payment = $user->charge(100, $paymentMethod);

3} catch (Exception $e) {

4    // ...

5}
```

The `charge` method accepts the payment amount in the lowest denominator of the currency used by your application. For example, if customers are paying in United States Dollars, amounts should be specified in pennies.

### [Charge With Invoice](#charge-with-invoice)

Sometimes you may need to make a one-time charge and offer a PDF invoice to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts:

```
1$user->invoicePrice('price_tshirt', 5);
```

The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself:

```
1$user->invoicePrice('price_tshirt', 5, [

2    'discounts' => [

3        ['coupon' => 'SUMMER21SALE']

4    ],

5], [

6    'default_tax_rates' => ['txr_id'],

7]);
```

Similarly to `invoicePrice`, you may use the `tabPrice` method to create a one-time charge for multiple items (up to 250 items per invoice) by adding them to the customer's "tab" and then invoicing the customer. For example, we may invoice a customer for five shirts and two mugs:

```
1$user->tabPrice('price_tshirt', 5);

2$user->tabPrice('price_mug', 2);

3$user->invoice();
```

Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method:

```
1$user->invoiceFor('One Time Fee', 500);
```

Although the `invoiceFor` method is available for you to use, it is recommended that you use the `invoicePrice` and `tabPrice` methods with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis.

The `invoice`, `invoicePrice`, and `invoiceFor` methods will create a Stripe invoice which will retry failed billing attempts. If you do not want invoices to retry failed charges, you will need to close them using the Stripe API after the first failed charge.

### [Creating Payment Intents](#creating-payment-intents)

You can create a new Stripe payment intent by invoking the `pay` method on a billable model instance. Calling this method will create a payment intent that is wrapped in a `Laravel\Cashier\Payment` instance:

```
1use Illuminate\Http\Request;

2 

3Route::post('/pay', function (Request $request) {

4    $payment = $request->user()->pay(

5        $request->get('amount')

6    );

7 

8    return $payment->client_secret;

9});
```

After creating the payment intent, you can return the client secret to your application's frontend so that the user can complete the payment in their browser. To read more about building entire payment flows using Stripe payment intents, please consult the [Stripe documentation](https://stripe.com/docs/payments/accept-a-payment?platform=web).

When using the `pay` method, the default payment methods that are enabled within your Stripe dashboard will be available to the customer. Alternatively, if you only want to allow for some specific payment methods to be used, you may use the `payWith` method:

```
1use Illuminate\Http\Request;

2 

3Route::post('/pay', function (Request $request) {

4    $payment = $request->user()->payWith(

5        $request->get('amount'), ['card', 'bancontact']

6    );

7 

8    return $payment->client_secret;

9});
```

The `pay` and `payWith` methods accept the payment amount in the lowest denominator of the currency used by your application. For example, if customers are paying in United States Dollars, amounts should be specified in pennies.

### [Refunding Charges](#refunding-charges)

If you need to refund a Stripe payment, you may use the `refund` method. This method accepts the Stripe Payment Intent ID as its first argument:

```
1$payment = $user->charge(100, $paymentMethodId);

2 

3$user->refund($payment->id);
```

## [Invoices](#invoices)

### [Retrieving Invoices](#retrieving-invoices)

You may easily retrieve an array of a billable model's invoices using the `invoices` method. The `invoices` method returns a collection of `Laravel\Cashier\Invoice` instances:

```
1$invoices = $user->invoices();
```

If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method:

```
1$invoices = $user->invoicesIncludingPending();
```

You may use the `findInvoice` method to retrieve a specific invoice by its ID:

```
1$invoice = $user->findInvoice($invoiceId);
```

#### [Displaying Invoice Information](#displaying-invoice-information)

When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them:

```
1<table>

2    @foreach ($invoices as $invoice)

3        <tr>

4            <td>{{ $invoice->date()->toFormattedDateString() }}</td>

5            <td>{{ $invoice->total() }}</td>

6            <td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>

7        </tr>

8    @endforeach

9</table>
```

### [Upcoming Invoices](#upcoming-invoices)

To retrieve the upcoming invoice for a customer, you may use the `upcomingInvoice` method:

```
1$invoice = $user->upcomingInvoice();
```

Similarly, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription:

```
1$invoice = $user->subscription('default')->upcomingInvoice();
```

### [Previewing Subscription Invoices](#previewing-subscription-invoices)

Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made:

```
1$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```

You may pass an array of prices to the `previewInvoice` method in order to preview invoices with multiple new prices:

```
1$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```

### [Generating Invoice PDFs](#generating-invoice-pdfs)

Before generating invoice PDFs, you should use Composer to install the Dompdf library, which is the default invoice renderer for Cashier:

```
1composer require dompdf/dompdf
```

From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice:

```
1use Illuminate\Http\Request;

2 

3Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {

4    return $request->user()->downloadInvoice($invoiceId);

5});
```

By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. The filename is based on your `app.name` config value. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details:

```
 1return $request->user()->downloadInvoice($invoiceId, [

 2    'vendor' => 'Your Company',

 3    'product' => 'Your Product',

 4    'street' => 'Main Str. 1',

 5    'location' => '2000 Antwerp, Belgium',

 6    'phone' => '+32 499 00 00 00',

 7    'email' => '[[email protected]](/cdn-cgi/l/email-protection)',

 8    'url' => 'https://example.com',

 9    'vendorVat' => 'BE123456789',

10]);
```

The `downloadInvoice` method also allows for a custom filename via its third argument. This filename will automatically be suffixed with `.pdf`:

```
1return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```

#### [Custom Invoice Renderer](#custom-invoice-render)

Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service:

```
 1use Illuminate\Support\Facades\Http;

 2use Laravel\Cashier\Contracts\InvoiceRenderer;

 3use Laravel\Cashier\Invoice;

 4 

 5class ApiInvoiceRenderer implements InvoiceRenderer

 6{

 7    /**

 8     * Render the given invoice and return the raw PDF bytes.

 9     */

10    public function render(Invoice $invoice, array $data = [], array $options = []): string

11    {

12        $html = $invoice->view($data)->render();

13 

14        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();

15    }

16}
```

Once you have implemented the invoice renderer contract, you should update the `cashier.invoices.renderer` configuration value in your application's `config/cashier.php` configuration file. This configuration value should be set to the class name of your custom renderer implementation.

## [Checkout](#checkout)

Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page.

The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout).

### [Product Checkouts](#product-checkouts)

You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID:

```
1use Illuminate\Http\Request;

2 

3Route::get('/product-checkout', function (Request $request) {

4    return $request->user()->checkout('price_tshirt');

5});
```

If needed, you may also specify a product quantity:

```
1use Illuminate\Http\Request;

2 

3Route::get('/product-checkout', function (Request $request) {

4    return $request->user()->checkout(['price_tshirt' => 15]);

5});
```

When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options:

```
1use Illuminate\Http\Request;

2 

3Route::get('/product-checkout', function (Request $request) {

4    return $request->user()->checkout(['price_tshirt' => 1], [

5        'success_url' => route('your-success-route'),

6        'cancel_url' => route('your-cancel-route'),

7    ]);

8});
```

When defining your `success_url` checkout option, you may instruct Stripe to add the checkout session ID as a query string parameter when invoking your URL. To do so, add the literal string `{CHECKOUT_SESSION_ID}` to your `success_url` query string. Stripe will replace this placeholder with the actual checkout session ID:

```
 1use Illuminate\Http\Request;

 2use Stripe\Checkout\Session;

 3use Stripe\Customer;

 4 

 5Route::get('/product-checkout', function (Request $request) {

 6    return $request->user()->checkout(['price_tshirt' => 1], [

 7        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',

 8        'cancel_url' => route('checkout-cancel'),

 9    ]);

10});

11 

12Route::get('/checkout-success', function (Request $request) {

13    $checkoutSession = $request->user()->stripe()->checkout->sessions->retrieve($request->get('session_id'));

14 

15    return view('checkout.success', ['checkoutSession' => $checkoutSession]);

16})->name('checkout-success');
```

#### [Promotion Codes](#checkout-promotion-codes)

By default, Stripe Checkout does not allow [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes). Luckily, there's an easy way to enable these for your Checkout page. To do so, you may invoke the `allowPromotionCodes` method:

```
1use Illuminate\Http\Request;

2 

3Route::get('/product-checkout', function (Request $request) {

4    return $request->user()

5        ->allowPromotionCodes()

6        ->checkout('price_tshirt');

7});
```

### [Single Charge Checkouts](#single-charge-checkouts)

You can also perform a simple charge for an ad-hoc product that has not been created in your Stripe dashboard. To do so you may use the `checkoutCharge` method on a billable model and pass it a chargeable amount, a product name, and an optional quantity. When a customer visits this route they will be redirected to Stripe's Checkout page:

```
1use Illuminate\Http\Request;

2 

3Route::get('/charge-checkout', function (Request $request) {

4    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);

5});
```

When using the `checkoutCharge` method, Stripe will always create a new product and price in your Stripe dashboard. Therefore, we recommend that you create the products up front in your Stripe dashboard and use the `checkout` method instead.

### [Subscription Checkouts](#subscription-checkouts)

Using Stripe Checkout for subscriptions requires you to enable the `customer.subscription.created` webhook in your Stripe dashboard. This webhook will create the subscription record in your database and store all of the relevant subscription items.

You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page:

```
1use Illuminate\Http\Request;

2 

3Route::get('/subscription-checkout', function (Request $request) {

4    return $request->user()

5        ->newSubscription('default', 'price_monthly')

6        ->checkout();

7});
```

Just as with product checkouts, you may customize the success and cancellation URLs:

```
 1use Illuminate\Http\Request;

 2 

 3Route::get('/subscription-checkout', function (Request $request) {

 4    return $request->user()

 5        ->newSubscription('default', 'price_monthly')

 6        ->checkout([

 7            'success_url' => route('your-success-route'),

 8            'cancel_url' => route('your-cancel-route'),

 9        ]);

10});
```

Of course, you can also enable promotion codes for subscription checkouts:

```
1use Illuminate\Http\Request;

2 

3Route::get('/subscription-checkout', function (Request $request) {

4    return $request->user()

5        ->newSubscription('default', 'price_monthly')

6        ->allowPromotionCodes()

7        ->checkout();

8});
```

Unfortunately Stripe Checkout does not support all subscription billing options when starting subscriptions. Using the `anchorBillingCycleOn` method on the subscription builder, setting proration behavior, or setting payment behavior will not have any effect during Stripe Checkout sessions. Please consult [the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create) to review which parameters are available.

#### [Stripe Checkout and Trial Periods](#stripe-checkout-trial-periods)

Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout:

```
1$checkout = Auth::user()->newSubscription('default', 'price_monthly')

2    ->trialDays(3)

3    ->checkout();
```

However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout.

#### [Subscriptions and Webhooks](#stripe-checkout-subscriptions-and-webhooks)

Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending.

### [Collecting Tax IDs](#collecting-tax-ids)

Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session:

```
1$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```

When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number.

If you have already configured [automatic tax collection](#tax-configuration) in your application's service provider then this feature will be enabled automatically and there is no need to invoke the `collectTaxIds` method.

### [Guest Checkouts](#guest-checkouts)

Using the `Checkout::guest` method, you may initiate checkout sessions for guests of your application that do not have an "account":

```
1use Illuminate\Http\Request;

2use Laravel\Cashier\Checkout;

3 

4Route::get('/product-checkout', function (Request $request) {

5    return Checkout::guest()->create('price_tshirt', [

6        'success_url' => route('your-success-route'),

7        'cancel_url' => route('your-cancel-route'),

8    ]);

9});
```

Similarly to when creating checkout sessions for existing users, you may utilize additional methods available on the `Laravel\Cashier\CheckoutBuilder` instance to customize the guest checkout session:

```
 1use Illuminate\Http\Request;

 2use Laravel\Cashier\Checkout;

 3 

 4Route::get('/product-checkout', function (Request $request) {

 5    return Checkout::guest()

 6        ->withPromotionCode('promo-code')

 7        ->create('price_tshirt', [

 8            'success_url' => route('your-success-route'),

 9            'cancel_url' => route('your-cancel-route'),

10        ]);

11});
```

After a guest checkout has been completed, Stripe can dispatch a `checkout.session.completed` webhook event, so make sure to [configure your Stripe webhook](https://dashboard.stripe.com/webhooks) to actually send this event to your application. Once the webhook has been enabled within the Stripe dashboard, you may [handle the webhook with Cashier](#handling-stripe-webhooks). The object contained in the webhook payload will be a [checkout object](https://stripe.com/docs/api/checkout/sessions/object) that you may inspect in order to fulfill your customer's order.

## [Handling Failed Payments](#handling-failed-payments)

Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed.

First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page:

```
 1use Laravel\Cashier\Exceptions\IncompletePayment;

 2 

 3try {

 4    $subscription = $user->newSubscription('default', 'price_monthly')

 5        ->create($paymentMethod);

 6} catch (IncompletePayment $exception) {

 7    return redirect()->route(

 8        'cashier.payment',

 9        [$exception->payment->id, 'redirect' => route('home')]

10    );

11}
```

On the payment confirmation page, the customer will be prompted to enter their credit card information again and perform any additional actions required by Stripe, such as "3D Secure" confirmation. After confirming their payment, the user will be redirected to the URL provided by the `redirect` parameter specified above. Upon redirection, `message` (string) and `success` (integer) query string variables will be added to the URL. The payment page currently supports the following payment method types:

- Credit Cards
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit

Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [set up Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions.

Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions.

Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance:

```
1if ($user->hasIncompletePayment('default')) {

2    // ...

3}

4 

5if ($user->subscription('default')->hasIncompletePayment()) {

6    // ...

7}
```

You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance:

```
 1use Laravel\Cashier\Exceptions\IncompletePayment;

 2 

 3try {

 4    $user->charge(1000, 'pm_card_threeDSecure2Required');

 5} catch (IncompletePayment $exception) {

 6    // Get the payment intent status...

 7    $exception->payment->status;

 8 

 9    // Check specific conditions...

10    if ($exception->payment->requiresPaymentMethod()) {

11        // ...

12    } elseif ($exception->payment->requiresConfirmation()) {

13        // ...

14    }

15}
```

### [Confirming Payments](#confirming-payments)

Some payment methods require additional data in order to confirm payments. For example, SEPA payment methods require additional "mandate" data during the payment process. You may provide this data to Cashier using the `withPaymentConfirmationOptions` method:

```
1$subscription->withPaymentConfirmationOptions([

2    'mandate_data' => '...',

3])->swap('price_xxx');
```

You may consult the [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm) to review all of the options accepted when confirming payments.

## [Strong Customer Authentication](#strong-customer-authentication)

If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications.

Before getting started, review [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication) as well as their [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication).

### [Payments Requiring Additional Confirmation](#payments-requiring-additional-confirmation)

SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions can be found in the documentation on [handling failed payments](#handling-failed-payments).

Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification.

#### [Incomplete and Past Due State](#incomplete-and-past-due-state)

When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion.

For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status).

### [Off-Session Payment Notifications](#off-session-payment-notifications)

Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired:

```
1CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait.

Notifications will be sent even when customers are manually making a payment that requires additional confirmation. Unfortunately, there is no way for Stripe to know that the payment was done manually or "off-session". But, a customer will simply see a "Payment Successful" message if they visit the payment page after already confirming their payment. The customer will not be allowed to accidentally confirm the same payment twice and incur an accidental second charge.

## [Stripe SDK](#stripe-sdk)

Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method:

```
1$stripeSubscription = $subscription->asStripeSubscription();

2 

3$stripeSubscription->application_fee_percent = 5;

4 

5$stripeSubscription->save();
```

You may also use the `updateStripeSubscription` method to update a Stripe subscription directly:

```
1$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```

You may invoke the `stripe` method on the `Cashier` class if you would like to use the `Stripe\StripeClient` client directly. For example, you could use this method to access the `StripeClient` instance and retrieve a list of prices from your Stripe account:

```
1use Laravel\Cashier\Cashier;

2 

3$prices = Cashier::stripe()->prices->all();
```

## [Testing](#testing)

When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own Pest / PHPUnit testing group.

When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior.

To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file:

```
1<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing.

In order to test a variety of billing scenarios, such as credit card denials and failures, you may use the vast range of [testing card numbers and tokens](https://stripe.com/docs/testing) provided by Stripe.
