# Events

- [Introduction](#introduction)
- [Generating Events and Listeners](#generating-events-and-listeners)
- [Registering Events and Listeners](#registering-events-and-listeners)
  * [Event Discovery](#event-discovery)
  * [Manually Registering Events](#manually-registering-events)
  * [Closure Listeners](#closure-listeners)
- [Defining Events](#defining-events)
- [Defining Listeners](#defining-listeners)
- [Queued Event Listeners](#queued-event-listeners)
  * [Manually Interacting With the Queue](#manually-interacting-with-the-queue)
  * [Queued Event Listeners and Database Transactions](#queued-event-listeners-and-database-transactions)
  * [Queued Listener Middleware](#queued-listener-middleware)
  * [Encrypted Queued Listeners](#encrypted-queued-listeners)
  * [Unique Event Listeners](#unique-event-listeners)
    + [Keeping Listeners Unique Until Processing Begins](#keeping-listeners-unique-until-processing-begins)
    + [Unique Listener Locks](#unique-listener-locks)
  * [Handling Failed Jobs](#handling-failed-jobs)
- [Dispatching Events](#dispatching-events)
  * [Dispatching Events After Database Transactions](#dispatching-events-after-database-transactions)
  * [Deferring Events](#deferring-events)
- [Event Subscribers](#event-subscribers)
  * [Writing Event Subscribers](#writing-event-subscribers)
  * [Registering Event Subscribers](#registering-event-subscribers)
- [Testing](#testing)
  * [Faking a Subset of Events](#faking-a-subset-of-events)
  * [Scoped Events Fakes](#scoped-event-fakes)

## [Introduction](#introduction)

Laravel's events provide a simple observer pattern implementation, allowing you to subscribe and listen for various events that occur within your application. Event classes are typically stored in the `app/Events` directory, while their listeners are stored in `app/Listeners`. Don't worry if you don't see these directories in your application as they will be created for you as you generate events and listeners using Artisan console commands.

Events serve as a great way to decouple various aspects of your application, since a single event can have multiple listeners that do not depend on each other. For example, you may wish to send a Slack notification to your user each time an order has shipped. Instead of coupling your order processing code to your Slack notification code, you can raise an `App\Events\OrderShipped` event which a listener can receive and use to dispatch a Slack notification.

## [Generating Events and Listeners](#generating-events-and-listeners)

To quickly generate events and listeners, you may use the `make:event` and `make:listener` Artisan commands:

```
1php artisan make:event PodcastProcessed

2 

3php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

For convenience, you may also invoke the `make:event` and `make:listener` Artisan commands without additional arguments. When you do so, Laravel will automatically prompt you for the class name and, when creating a listener, the event it should listen to:

```
1php artisan make:event

2 

3php artisan make:listener
```

## [Registering Events and Listeners](#registering-events-and-listeners)

### [Event Discovery](#event-discovery)

By default, Laravel will automatically find and register your event listeners by scanning your application's `Listeners` directory. When Laravel finds any listener class method that begins with `handle` or `__invoke`, Laravel will register those methods as event listeners for the event that is type-hinted in the method's signature:

```
 1use App\Events\PodcastProcessed;

 2 

 3class SendPodcastNotification

 4{

 5    /**

 6     * Handle the event.

 7     */

 8    public function handle(PodcastProcessed $event): void

 9    {

10        // ...

11    }

12}
```

You may listen to multiple events using PHP's union types:

```
1/**

2 * Handle the event.

3 */

4public function handle(PodcastProcessed|PodcastPublished $event): void

5{

6    // ...

7}
```

If you plan to store your listeners in a different directory or within multiple directories, you may instruct Laravel to scan those directories using the `withEvents` method in your application's `bootstrap/app.php` file:

```
1->withEvents(discover: [

2    __DIR__.'/../app/Domain/Orders/Listeners',

3])
```

You may scan for listeners in multiple similar directories using the `*` character as a wildcard:

```
1->withEvents(discover: [

2    __DIR__.'/../app/Domain/*/Listeners',

3])
```

The `event:list` command may be used to list all of the listeners registered within your application:

```
1php artisan event:list
```

#### [Event Discovery in Production](#event-discovery-in-production)

To give your application a speed boost, you should cache a manifest of all of your application's listeners using the `optimize` or `event:cache` Artisan commands. Typically, this command should be run as part of your application's [deployment process](/docs/13.x/deployment#optimization). This manifest will be used by the framework to speed up the event registration process. The `event:clear` command may be used to destroy the event cache.

#### [Dynamic Event Discovery](#dynamic-event-discovery)

To dynamically control whether a given listener is discovered, you may implement the `ShouldBeDiscovered` interface on the listener class and define a `shouldBeDiscovered` method that returns a boolean value. If the method returns `false`, the listener will not be registered during event discovery:

```
 1use Illuminate\Contracts\Events\ShouldBeDiscovered;

 2 

 3class SendPodcastNotification implements ShouldBeDiscovered

 4{

 5    /**

 6     * Handle the event.

 7     */

 8    public function handle(PodcastProcessed $event): void

 9    {

10        // ...

11    }

12 

13    /**

14     * Determine if the listener should be discovered.

15     */

16    public static function shouldBeDiscovered(): bool

17    {

18        return app()->environment('production');

19    }

20}
```

### [Manually Registering Events](#manually-registering-events)

Using the `Event` facade, you may manually register events and their corresponding listeners within the `boot` method of your application's `AppServiceProvider`:

```
 1use App\Domain\Orders\Events\PodcastProcessed;

 2use App\Domain\Orders\Listeners\SendPodcastNotification;

 3use Illuminate\Support\Facades\Event;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Event::listen(

11        PodcastProcessed::class,

12        SendPodcastNotification::class,

13    );

14}
```

The `event:list` command may be used to list all of the listeners registered within your application:

```
1php artisan event:list
```

### [Closure Listeners](#closure-listeners)

Typically, listeners are defined as classes; however, you may also manually register closure-based event listeners in the `boot` method of your application's `AppServiceProvider`:

```
 1use App\Events\PodcastProcessed;

 2use Illuminate\Support\Facades\Event;

 3 

 4/**

 5 * Bootstrap any application services.

 6 */

 7public function boot(): void

 8{

 9    Event::listen(function (PodcastProcessed $event) {

10        // ...

11    });

12}
```

#### [Queueable Anonymous Event Listeners](#queueable-anonymous-event-listeners)

When registering closure-based event listeners, you may wrap the listener closure within the `Illuminate\Events\queueable` function to instruct Laravel to execute the listener using the [queue](/docs/13.x/queues):

```
 1use App\Events\PodcastProcessed;

 2use function Illuminate\Events\queueable;

 3use Illuminate\Support\Facades\Event;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Event::listen(queueable(function (PodcastProcessed $event) {

11        // ...

12    }));

13}
```

Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener:

```
1Event::listen(queueable(function (PodcastProcessed $event) {

2    // ...

3})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener. This closure will receive the event instance and the `Throwable` instance that caused the listener's failure:

```
 1use App\Events\PodcastProcessed;

 2use function Illuminate\Events\queueable;

 3use Illuminate\Support\Facades\Event;

 4use Throwable;

 5 

 6Event::listen(queueable(function (PodcastProcessed $event) {

 7    // ...

 8})->catch(function (PodcastProcessed $event, Throwable $e) {

 9    // The queued listener failed...

10}));
```

#### [Wildcard Event Listeners](#wildcard-event-listeners)

You may also register listeners using the `*` character as a wildcard parameter, allowing you to catch multiple events on the same listener. Wildcard listeners receive the event name as their first argument and the entire event data array as their second argument:

```
1Event::listen('event.*', function (string $eventName, array $data) {

2    // ...

3});
```

## [Defining Events](#defining-events)

An event class is essentially a data container which holds the information related to the event. For example, let's assume an `App\Events\OrderShipped` event receives an [Eloquent ORM](/docs/13.x/eloquent) object:

```
 1<?php

 2 

 3namespace App\Events;

 4 

 5use App\Models\Order;

 6use Illuminate\Broadcasting\InteractsWithSockets;

 7use Illuminate\Foundation\Events\Dispatchable;

 8use Illuminate\Queue\SerializesModels;

 9 

10class OrderShipped

11{

12    use Dispatchable, InteractsWithSockets, SerializesModels;

13 

14    /**

15     * Create a new event instance.

16     */

17    public function __construct(

18        public Order $order,

19    ) {}

20}
```

As you can see, this event class contains no logic. It is a container for the `App\Models\Order` instance that was purchased. The `SerializesModels` trait used by the event will gracefully serialize any Eloquent models if the event object is serialized using PHP's `serialize` function, such as when utilizing [queued listeners](#queued-event-listeners).

## [Defining Listeners](#defining-listeners)

Next, let's take a look at the listener for our example event. Event listeners receive event instances in their `handle` method. The `make:listener` Artisan command, when invoked with the `--event` option, will automatically import the proper event class and type-hint the event in the `handle` method. Within the `handle` method, you may perform any actions necessary to respond to the event:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6 

 7class SendShipmentNotification

 8{

 9    /**

10     * Create the event listener.

11     */

12    public function __construct() {}

13 

14    /**

15     * Handle the event.

16     */

17    public function handle(OrderShipped $event): void

18    {

19        // Access the order using $event->order...

20    }

21}
```

Your event listeners may also type-hint any dependencies they need on their constructors. All event listeners are resolved via the Laravel [service container](/docs/13.x/container), so dependencies will be injected automatically.

#### [Stopping The Propagation Of An Event](#stopping-the-propagation-of-an-event)

Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so by returning `false` from your listener's `handle` method.

## [Queued Event Listeners](#queued-event-listeners)

Queueing listeners can be beneficial if your listener is going to perform a slow task such as sending an email or making an HTTP request. Before using queued listeners, make sure to [configure your queue](/docs/13.x/queues) and start a queue worker on your server or local development environment.

To specify that a listener should be queued, add the `ShouldQueue` interface to the listener class. Listeners generated by the `make:listener` Artisan commands already have this interface imported into the current namespace so you can use it immediately:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7 

 8class SendShipmentNotification implements ShouldQueue

 9{

10    // ...

11}
```

That's it! Now, when an event handled by this listener is dispatched, the listener will automatically be queued by the event dispatcher using Laravel's [queue system](/docs/13.x/queues). If no exceptions are thrown when the listener is executed by the queue, the queued job will automatically be deleted after it has finished processing.

#### [Customizing The Queue Connection, Name, & Delay](#customizing-the-queue-connection-queue-name)

If you would like to customize the queue connection, queue name, or queue delay time of an event listener, you may use the `Connection`, `Queue`, and `Delay` attributes on your listener class:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Queue\Attributes\Connection;

 8use Illuminate\Queue\Attributes\Delay;

 9use Illuminate\Queue\Attributes\Queue;

10 

11#[Connection('sqs')]

12#[Queue('listeners')]

13#[Delay(60)]

14class SendShipmentNotification implements ShouldQueue

15{

16    // ...

17}
```

If you would like to define the listener's queue connection, queue name, or delay at runtime, you may define `viaConnection`, `viaQueue`, or `withDelay` methods on the listener:

```
 1/**

 2 * Get the name of the listener's queue connection.

 3 */

 4public function viaConnection(): string

 5{

 6    return 'sqs';

 7}

 8 

 9/**

10 * Get the name of the listener's queue.

11 */

12public function viaQueue(): string

13{

14    return 'listeners';

15}

16 

17/**

18 * Get the number of seconds before the job should be processed.

19 */

20public function withDelay(OrderShipped $event): int

21{

22    return $event->highPriority ? 0 : 60;

23}
```

#### [Conditionally Queueing Listeners](#conditionally-queueing-listeners)

Sometimes, you may need to determine whether a listener should be queued based on some data that are only available at runtime. To accomplish this, a `shouldQueue` method may be added to a listener to determine whether the listener should be queued. If the `shouldQueue` method returns `false`, the listener will not be queued:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderCreated;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7 

 8class RewardGiftCard implements ShouldQueue

 9{

10    /**

11     * Reward a gift card to the customer.

12     */

13    public function handle(OrderCreated $event): void

14    {

15        // ...

16    }

17 

18    /**

19     * Determine whether the listener should be queued.

20     */

21    public function shouldQueue(OrderCreated $event): bool

22    {

23        return $event->order->subtotal >= 5000;

24    }

25}
```

### [Manually Interacting With the Queue](#manually-interacting-with-the-queue)

If you need to manually access the listener's underlying queue job's `delete` and `release` methods, you may do so using the `Illuminate\Queue\InteractsWithQueue` trait. This trait is imported by default on generated listeners and provides access to these methods:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Queue\InteractsWithQueue;

 8 

 9class SendShipmentNotification implements ShouldQueue

10{

11    use InteractsWithQueue;

12 

13    /**

14     * Handle the event.

15     */

16    public function handle(OrderShipped $event): void

17    {

18        if ($condition) {

19            $this->release(30);

20        }

21    }

22}
```

### [Queued Event Listeners and Database Transactions](#queued-event-listeners-and-database-transactions)

When queued listeners are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your listener depends on these models, unexpected errors can occur when the job that dispatches the queued listener is processed.

If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued listener should be dispatched after all open database transactions have been committed by implementing the `ShouldQueueAfterCommit` interface on the listener class:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;

 6use Illuminate\Queue\InteractsWithQueue;

 7 

 8class SendShipmentNotification implements ShouldQueueAfterCommit

 9{

10    use InteractsWithQueue;

11}
```

To learn more about working around these issues, please review the documentation regarding [queued jobs and database transactions](/docs/13.x/queues#jobs-and-database-transactions).

### [Queued Listener Middleware](#queued-listener-middleware)

Queued listeners can also utilize [job middleware](/docs/13.x/queues#job-middleware). Job middleware allow you to wrap custom logic around the execution of queued listeners, reducing boilerplate in the listeners themselves. After creating job middleware, they may be attached to a listener by returning them from the listener's `middleware` method:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use App\Jobs\Middleware\RateLimited;

 7use Illuminate\Contracts\Queue\ShouldQueue;

 8 

 9class SendShipmentNotification implements ShouldQueue

10{

11    /**

12     * Handle the event.

13     */

14    public function handle(OrderShipped $event): void

15    {

16        // Process the event...

17    }

18 

19    /**

20     * Get the middleware the listener should pass through.

21     *

22     * @return array<int, object>

23     */

24    public function middleware(OrderShipped $event): array

25    {

26        return [new RateLimited];

27    }

28}
```

#### [Encrypted Queued Listeners](#encrypted-queued-listeners)

Laravel allows you to ensure the privacy and integrity of a queued listener's data via [encryption](/docs/13.x/encryption). To get started, simply add the `ShouldBeEncrypted` interface to the listener class. Once this interface has been added to the class, Laravel will automatically encrypt your listener before pushing it onto a queue:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldBeEncrypted;

 7use Illuminate\Contracts\Queue\ShouldQueue;

 8 

 9class SendShipmentNotification implements ShouldQueue, ShouldBeEncrypted

10{

11    // ...

12}
```

### [Unique Event Listeners](#unique-event-listeners)

Unique listeners require a cache driver that supports [locks](/docs/13.x/cache#atomic-locks). Currently, the `memcached`, `redis`, `dynamodb`, `database`, `file`, and `array` cache drivers support atomic locks.

Sometimes, you may want to ensure that only one instance of a specific listener is on the queue at any point in time. You may do so by implementing the `ShouldBeUnique` interface on your listener class:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\LicenseSaved;

 6use Illuminate\Contracts\Queue\ShouldBeUnique;

 7use Illuminate\Contracts\Queue\ShouldQueue;

 8 

 9class AcquireProductKey implements ShouldQueue, ShouldBeUnique

10{

11    public function __invoke(LicenseSaved $event): void

12    {

13        // ...

14    }

15}
```

In the example above, the `AcquireProductKey` listener is unique. So, the listener will not be queued if another instance of the listener is already on the queue and has not finished processing. This ensures that only one product key is acquired for each license, even if the license is saved multiple times in quick succession.

In certain cases, you may want to define a specific "key" that makes the listener unique or you may want to specify a timeout beyond which the listener no longer stays unique. To accomplish this, you may define `uniqueId` and `uniqueFor` properties or methods on your listener class. The methods receive the event instance, allowing you to use event data to construct the return value:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\LicenseSaved;

 6use Illuminate\Contracts\Queue\ShouldBeUnique;

 7use Illuminate\Contracts\Queue\ShouldQueue;

 8 

 9class AcquireProductKey implements ShouldQueue, ShouldBeUnique

10{

11    /**

12     * The number of seconds after which the listener's unique lock will be released.

13     *

14     * @var int

15     */

16    public $uniqueFor = 3600;

17 

18    public function __invoke(LicenseSaved $event): void

19    {

20        // ...

21    }

22 

23    /**

24     * Get the unique ID for the listener.

25     */

26    public function uniqueId(LicenseSaved $event): string

27    {

28        return 'listener:'.$event->license->id;

29    }

30}
```

In the example above, the `AcquireProductKey` listener is unique by license ID. So, any new dispatches of the listener for the same license will be ignored until the existing listener has completed processing. This prevents duplicate product keys from being acquired for the same license. In addition, if the existing listener is not processed within one hour, the unique lock will be released and another listener with the same unique key can be queued.

If your application dispatches events from multiple web servers or containers, you should ensure that all of your servers are communicating with the same central cache server so that Laravel can accurately determine if a listener is unique.

#### [Keeping Listeners Unique Until Processing Begins](#keeping-listeners-unique-until-processing-begins)

By default, unique listeners are "unlocked" after a listener completes processing or fails all of its retry attempts. However, there may be situations where you would like your listener to unlock immediately before it is processed. To accomplish this, your listener should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\LicenseSaved;

 6use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

 7use Illuminate\Contracts\Queue\ShouldQueue;

 8 

 9class AcquireProductKey implements ShouldQueue, ShouldBeUniqueUntilProcessing

10{

11    // ...

12}
```

#### [Unique Listener Locks](#unique-listener-locks)

Behind the scenes, when a `ShouldBeUnique` listener is dispatched, Laravel attempts to acquire a [lock](/docs/13.x/cache#atomic-locks) with the `uniqueId` key. If the lock is already held, the listener is not dispatched. This lock is released when the listener completes processing or fails all of its retry attempts. By default, Laravel will use the default cache driver to obtain this lock. However, if you wish to use another driver for acquiring the lock, you may define a `uniqueVia` method that returns the cache driver that should be used:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\LicenseSaved;

 6use Illuminate\Contracts\Cache\Repository;

 7use Illuminate\Support\Facades\Cache;

 8 

 9class AcquireProductKey implements ShouldQueue, ShouldBeUnique

10{

11    // ...

12 

13    /**

14     * Get the cache driver for the unique listener lock.

15     */

16    public function uniqueVia(LicenseSaved $event): Repository

17    {

18        return Cache::driver('redis');

19    }

20}
```

If you only need to limit the concurrent processing of a listener, use the [WithoutOverlapping](/docs/13.x/queues#preventing-job-overlaps) job middleware instead.

### [Handling Failed Jobs](#handling-failed-jobs)

Sometimes your queued event listeners may fail. If the queued listener exceeds the maximum number of attempts as defined by your queue worker, the `failed` method will be called on your listener. The `failed` method receives the event instance and the `Throwable` that caused the failure:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Queue\InteractsWithQueue;

 8use Throwable;

 9 

10class SendShipmentNotification implements ShouldQueue

11{

12    use InteractsWithQueue;

13 

14    /**

15     * Handle the event.

16     */

17    public function handle(OrderShipped $event): void

18    {

19        // ...

20    }

21 

22    /**

23     * Handle a job failure.

24     */

25    public function failed(OrderShipped $event, Throwable $exception): void

26    {

27        // ...

28    }

29}
```

#### [Specifying Queued Listener Maximum Attempts](#specifying-queued-listener-maximum-attempts)

If one of your queued listeners is encountering an error, you likely do not want it to keep retrying indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a listener may be attempted.

You may use the `Tries` attribute on your listener class to specify how many times the listener may be attempted before it is considered to have failed:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Queue\Attributes\Tries;

 8use Illuminate\Queue\InteractsWithQueue;

 9 

10#[Tries(5)]

11class SendShipmentNotification implements ShouldQueue

12{

13    use InteractsWithQueue;

14 

15    // ...

16}
```

As an alternative to defining how many times a listener may be attempted before it fails, you may define a time at which the listener should no longer be attempted. This allows a listener to be attempted any number of times within a given time frame. To define the time at which a listener should no longer be attempted, add a `retryUntil` method to your listener class. This method should return a `DateTimeInterface` instance:

```
1use DateTimeInterface;

2 

3/**

4 * Determine the time at which the listener should timeout.

5 */

6public function retryUntil(): DateTimeInterface

7{

8    return now()->plus(minutes: 5);

9}
```

If both `retryUntil` and `tries` are defined, Laravel gives precedence to the `retryUntil` method.

#### [Specifying Queued Listener Backoff](#specifying-queued-listener-backoff)

If you would like to configure how many seconds Laravel should wait before retrying a listener that has encountered an exception, you may use the `Backoff` attribute on your listener class:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use Illuminate\Contracts\Queue\ShouldQueue;

 6use Illuminate\Queue\Attributes\Backoff;

 7 

 8#[Backoff(3)]

 9class SendShipmentNotification implements ShouldQueue

10{

11    // ...

12}
```

If you require more complex logic for determining the listeners's backoff time, you may define a `backoff` method on your listener class:

```
1/**

2 * Calculate the number of seconds to wait before retrying the queued listener.

3 */

4public function backoff(OrderShipped $event): int

5{

6    return 3;

7}
```

You may easily configure "exponential" backoffs by returning an array of backoff values from the `backoff` method. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining:

```
1/**

2 * Calculate the number of seconds to wait before retrying the queued listener.

3 *

4 * @return list<int>

5 */

6public function backoff(OrderShipped $event): array

7{

8    return [1, 5, 10];

9}
```

#### [Specifying Queued Listener Max Exceptions](#specifying-queued-listener-max-exceptions)

Sometimes you may wish to specify that a queued listener may be attempted many times, but should fail if the retries are triggered by a given number of unhandled exceptions (as opposed to being released by the `release` method directly). To accomplish this, you may use the `Tries` and `MaxExceptions` attributes on your listener class:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Queue\Attributes\MaxExceptions;

 8use Illuminate\Queue\Attributes\Tries;

 9use Illuminate\Queue\InteractsWithQueue;

10 

11#[Tries(25)]

12#[MaxExceptions(3)]

13class SendShipmentNotification implements ShouldQueue

14{

15    use InteractsWithQueue;

16 

17    /**

18     * Handle the event.

19     */

20    public function handle(OrderShipped $event): void

21    {

22        // Process the event...

23    }

24}
```

In this example, the listener will be retried up to 25 times. However, the listener will fail if three unhandled exceptions are thrown by the listener.

#### [Specifying Queued Listener Timeout](#specifying-queued-listener-timeout)

Often, you know roughly how long you expect your queued listeners to take. For this reason, Laravel allows you to specify a "timeout" value. If a listener is processing for longer than the number of seconds specified by the timeout value, the worker processing the listener will exit with an error. You may define the maximum number of seconds a listener should be allowed to run by using the `Timeout` attribute on your listener class:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Queue\Attributes\Timeout;

 8 

 9#[Timeout(120)]

10class SendShipmentNotification implements ShouldQueue

11{

12    // ...

13}
```

If you would like to indicate that a listener should be marked as failed on timeout, you may use the `FailOnTimeout` attribute on the listener class:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use App\Events\OrderShipped;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Queue\Attributes\FailOnTimeout;

 8 

 9#[FailOnTimeout]

10class SendShipmentNotification implements ShouldQueue

11{

12    // ...

13}
```

## [Dispatching Events](#dispatching-events)

To dispatch an event, you may call the static `dispatch` method on the event. This method is made available on the event by the `Illuminate\Foundation\Events\Dispatchable` trait. Any arguments passed to the `dispatch` method will be passed to the event's constructor:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Events\OrderShipped;

 6use App\Models\Order;

 7use Illuminate\Http\RedirectResponse;

 8use Illuminate\Http\Request;

 9 

10class OrderShipmentController extends Controller

11{

12    /**

13     * Ship the given order.

14     */

15    public function store(Request $request): RedirectResponse

16    {

17        $order = Order::findOrFail($request->order_id);

18 

19        // Order shipment logic...

20 

21        OrderShipped::dispatch($order);

22 

23        return redirect('/orders');

24    }

25}
```

If you would like to conditionally dispatch an event, you may use the `dispatchIf` and `dispatchUnless` methods:

```
1OrderShipped::dispatchIf($condition, $order);

2 

3OrderShipped::dispatchUnless($condition, $order);
```

When testing, it can be helpful to assert that certain events were dispatched without actually triggering their listeners. Laravel's [built-in testing helpers](#testing) make it a cinch.

### [Dispatching Events After Database Transactions](#dispatching-events-after-database-transactions)

Sometimes, you may want to instruct Laravel to only dispatch an event after the active database transaction has committed. To do so, you may implement the `ShouldDispatchAfterCommit` interface on the event class.

This interface instructs Laravel to not dispatch the event until the current database transaction is committed. If the transaction fails, the event will be discarded. If no database transaction is in progress when the event is dispatched, the event will be dispatched immediately:

```
 1<?php

 2 

 3namespace App\Events;

 4 

 5use App\Models\Order;

 6use Illuminate\Broadcasting\InteractsWithSockets;

 7use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;

 8use Illuminate\Foundation\Events\Dispatchable;

 9use Illuminate\Queue\SerializesModels;

10 

11class OrderShipped implements ShouldDispatchAfterCommit

12{

13    use Dispatchable, InteractsWithSockets, SerializesModels;

14 

15    /**

16     * Create a new event instance.

17     */

18    public function __construct(

19        public Order $order,

20    ) {}

21}
```

### [Deferring Events](#deferring-events)

Deferred events allow you to delay the dispatching of model events and execution of event listeners until after a specific block of code has completed. This is particularly useful when you need to ensure that all related records are created before event listeners are triggered.

To defer events, provide a closure to the `Event::defer()` method:

```
1use App\Models\User;

2use Illuminate\Support\Facades\Event;

3 

4Event::defer(function () {

5    $user = User::create(['name' => 'Victoria Otwell']);

6 

7    $user->posts()->create(['title' => 'My first post!']);

8});
```

All events triggered within the closure will be dispatched after the closure is executed. This ensures that event listeners have access to all related records that were created during the deferred execution. If an exception occurs within the closure, the deferred events will not be dispatched.

To defer only specific events, pass an array of events as the second argument to the `defer` method:

```
1use App\Models\User;

2use Illuminate\Support\Facades\Event;

3 

4Event::defer(function () {

5    $user = User::create(['name' => 'Victoria Otwell']);

6 

7    $user->posts()->create(['title' => 'My first post!']);

8}, ['eloquent.created: '.User::class]);
```

## [Event Subscribers](#event-subscribers)

### [Writing Event Subscribers](#writing-event-subscribers)

Event subscribers are classes that may subscribe to multiple events from within the subscriber class itself, allowing you to define several event handlers within a single class. Subscribers should define a `subscribe` method, which receives an event dispatcher instance. You may call the `listen` method on the given dispatcher to register event listeners:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use Illuminate\Auth\Events\Login;

 6use Illuminate\Auth\Events\Logout;

 7use Illuminate\Events\Dispatcher;

 8 

 9class UserEventSubscriber

10{

11    /**

12     * Handle user login events.

13     */

14    public function handleUserLogin(Login $event): void {}

15 

16    /**

17     * Handle user logout events.

18     */

19    public function handleUserLogout(Logout $event): void {}

20 

21    /**

22     * Register the listeners for the subscriber.

23     */

24    public function subscribe(Dispatcher $events): void

25    {

26        $events->listen(

27            Login::class,

28            [UserEventSubscriber::class, 'handleUserLogin']

29        );

30 

31        $events->listen(

32            Logout::class,

33            [UserEventSubscriber::class, 'handleUserLogout']

34        );

35    }

36}
```

If your event listener methods are defined within the subscriber itself, you may find it more convenient to return an array of events and method names from the subscriber's `subscribe` method. Laravel will automatically determine the subscriber's class name when registering the event listeners:

```
 1<?php

 2 

 3namespace App\Listeners;

 4 

 5use Illuminate\Auth\Events\Login;

 6use Illuminate\Auth\Events\Logout;

 7use Illuminate\Events\Dispatcher;

 8 

 9class UserEventSubscriber

10{

11    /**

12     * Handle user login events.

13     */

14    public function handleUserLogin(Login $event): void {}

15 

16    /**

17     * Handle user logout events.

18     */

19    public function handleUserLogout(Logout $event): void {}

20 

21    /**

22     * Register the listeners for the subscriber.

23     *

24     * @return array<string, string>

25     */

26    public function subscribe(Dispatcher $events): array

27    {

28        return [

29            Login::class => 'handleUserLogin',

30            Logout::class => 'handleUserLogout',

31        ];

32    }

33}
```

### [Registering Event Subscribers](#registering-event-subscribers)

After writing the subscriber, Laravel will automatically register handler methods within the subscriber if they follow Laravel's [event discovery conventions](#event-discovery). Otherwise, you may manually register your subscriber using the `subscribe` method of the `Event` facade. Typically, this should be done within the `boot` method of your application's `AppServiceProvider`:

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use App\Listeners\UserEventSubscriber;

 6use Illuminate\Support\Facades\Event;

 7use Illuminate\Support\ServiceProvider;

 8 

 9class AppServiceProvider extends ServiceProvider

10{

11    /**

12     * Bootstrap any application services.

13     */

14    public function boot(): void

15    {

16        Event::subscribe(UserEventSubscriber::class);

17    }

18}
```

## [Testing](#testing)

When testing code that dispatches events, you may wish to instruct Laravel to not actually execute the event's listeners, since the listener's code can be tested directly and separately of the code that dispatches the corresponding event. Of course, to test the listener itself, you may instantiate a listener instance and invoke the `handle` method directly in your test.

Using the `Event` facade's `fake` method, you may prevent listeners from executing, execute the code under test, and then assert which events were dispatched by your application using the `assertDispatched`, `assertNotDispatched`, and `assertNothingDispatched` methods:

Pest

PHPUnit

```
 1<?php

 2 

 3use App\Events\OrderFailedToShip;

 4use App\Events\OrderShipped;

 5use Illuminate\Support\Facades\Event;

 6 

 7test('orders can be shipped', function () {

 8    Event::fake();

 9 

10    // Perform order shipping...

11 

12    // Assert that an event was dispatched...

13    Event::assertDispatched(OrderShipped::class);

14 

15    // Assert an event was dispatched twice...

16    Event::assertDispatched(OrderShipped::class, 2);

17 

18    // Assert an event was dispatched once...

19    Event::assertDispatchedOnce(OrderShipped::class);

20 

21    // Assert an event was not dispatched...

22    Event::assertNotDispatched(OrderFailedToShip::class);

23 

24    // Assert that no events were dispatched...

25    Event::assertNothingDispatched();

26});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use App\Events\OrderFailedToShip;

 6use App\Events\OrderShipped;

 7use Illuminate\Support\Facades\Event;

 8use Tests\TestCase;

 9 

10class ExampleTest extends TestCase

11{

12    /**

13     * Test order shipping.

14     */

15    public function test_orders_can_be_shipped(): void

16    {

17        Event::fake();

18 

19        // Perform order shipping...

20 

21        // Assert that an event was dispatched...

22        Event::assertDispatched(OrderShipped::class);

23 

24        // Assert an event was dispatched twice...

25        Event::assertDispatched(OrderShipped::class, 2);

26 

27        // Assert an event was dispatched once...

28        Event::assertDispatchedOnce(OrderShipped::class);

29 

30        // Assert an event was not dispatched...

31        Event::assertNotDispatched(OrderFailedToShip::class);

32 

33        // Assert that no events were dispatched...

34        Event::assertNothingDispatched();

35    }

36}
```

You may pass a closure to the `assertDispatched` or `assertNotDispatched` methods in order to assert that an event was dispatched that passes a given "truth test". If at least one event was dispatched that passes the given truth test then the assertion will be successful:

```
1Event::assertDispatched(function (OrderShipped $event) use ($order) {

2    return $event->order->id === $order->id;

3});
```

If you would simply like to assert that an event listener is listening to a given event, you may use the `assertListening` method:

```
1Event::assertListening(

2    OrderShipped::class,

3    SendShipmentNotification::class

4);
```

After calling `Event::fake()`, no event listeners will be executed. So, if your tests use model factories that rely on events, such as creating a UUID during a model's `creating` event, you should call `Event::fake()` **after** using your factories.

### [Faking a Subset of Events](#faking-a-subset-of-events)

If you only want to fake event listeners for a specific set of events, you may pass them to the `fake` or `fakeFor` method:

Pest

PHPUnit

```
 1test('orders can be processed', function () {

 2    Event::fake([

 3        OrderCreated::class,

 4    ]);

 5 

 6    $order = Order::factory()->create();

 7 

 8    Event::assertDispatched(OrderCreated::class);

 9 

10    // Other events are dispatched as normal...

11    $order->update([

12        // ...

13    ]);

14});
```

```
 1/**

 2 * Test order process.

 3 */

 4public function test_orders_can_be_processed(): void

 5{

 6    Event::fake([

 7        OrderCreated::class,

 8    ]);

 9 

10    $order = Order::factory()->create();

11 

12    Event::assertDispatched(OrderCreated::class);

13 

14    // Other events are dispatched as normal...

15    $order->update([

16        // ...

17    ]);

18}
```

You may fake all events except for a set of specified events using the `except` method:

```
1Event::fake()->except([

2    OrderCreated::class,

3]);
```

### [Scoped Event Fakes](#scoped-event-fakes)

If you only want to fake event listeners for a portion of your test, you may use the `fakeFor` method:

Pest

PHPUnit

```
 1<?php

 2 

 3use App\Events\OrderCreated;

 4use App\Models\Order;

 5use Illuminate\Support\Facades\Event;

 6 

 7test('orders can be processed', function () {

 8    $order = Event::fakeFor(function () {

 9        $order = Order::factory()->create();

10 

11        Event::assertDispatched(OrderCreated::class);

12 

13        return $order;

14    });

15 

16    // Events are dispatched as normal and observers will run...

17    $order->update([

18        // ...

19    ]);

20});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use App\Events\OrderCreated;

 6use App\Models\Order;

 7use Illuminate\Support\Facades\Event;

 8use Tests\TestCase;

 9 

10class ExampleTest extends TestCase

11{

12    /**

13     * Test order process.

14     */

15    public function test_orders_can_be_processed(): void

16    {

17        $order = Event::fakeFor(function () {

18            $order = Order::factory()->create();

19 

20            Event::assertDispatched(OrderCreated::class);

21 

22            return $order;

23        });

24 

25        // Events are dispatched as normal and observers will run...

26        $order->update([

27            // ...

28        ]);

29    }

30}
```
