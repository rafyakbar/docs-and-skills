# Rate Limiting

- [Introduction](#introduction)
  * [Cache Configuration](#cache-configuration)
- [Basic Usage](#basic-usage)
  * [Manually Incrementing Attempts](#manually-incrementing-attempts)
  * [Clearing Attempts](#clearing-attempts)

## [Introduction](#introduction)

Laravel includes a simple to use rate limiting abstraction which, in conjunction with your application's [cache](cache), provides an easy way to limit any action during a specified window of time.

If you are interested in rate limiting incoming HTTP requests, please consult the [rate limiter middleware documentation](/docs/13.x/routing#rate-limiting).

### [Cache Configuration](#cache-configuration)

Typically, the rate limiter utilizes your default application cache as defined by the `default` key within your application's `cache` configuration file. However, you may specify which cache driver the rate limiter should use by defining a `limiter` key within your application's `cache` configuration file:

```
1'default' => env('CACHE_STORE', 'database'),

2 

3'limiter' => 'redis',
```

## [Basic Usage](#basic-usage)

The `Illuminate\Support\Facades\RateLimiter` facade may be used to interact with the rate limiter. The simplest method offered by the rate limiter is the `attempt` method, which rate limits a given callback for a given number of seconds.

The `attempt` method returns `false` when the callback has no remaining attempts available; otherwise, the `attempt` method will return the callback's result or `true`. The first argument accepted by the `attempt` method is a rate limiter "key", which may be any string of your choosing that represents the action being rate limited:

```
 1use Illuminate\Support\Facades\RateLimiter;

 2 

 3$executed = RateLimiter::attempt(

 4    'send-message:'.$user->id,

 5    $perMinute = 5,

 6    function() {

 7        // Send message...

 8    }

 9);

10 

11if (! $executed) {

12    return 'Too many messages sent!';

13}
```

If necessary, you may provide a fourth argument to the `attempt` method, which is the "decay rate", or the number of seconds until the available attempts are reset. For example, we can modify the example above to allow five attempts every two minutes:

```
1$executed = RateLimiter::attempt(

2    'send-message:'.$user->id,

3    $perTwoMinutes = 5,

4    function() {

5        // Send message...

6    },

7    $decayRate = 120,

8);
```

### [Manually Incrementing Attempts](#manually-incrementing-attempts)

If you would like to manually interact with the rate limiter, a variety of other methods are available. For example, you may invoke the `tooManyAttempts` method to determine if a given rate limiter key has exceeded its maximum number of allowed attempts per minute:

```
1use Illuminate\Support\Facades\RateLimiter;

2 

3if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {

4    return 'Too many attempts!';

5}

6 

7RateLimiter::increment('send-message:'.$user->id);

8 

9// Send message...
```

When rate limiting an endpoint that may receive many simultaneous requests, you may wish to check the value returned by the `increment` method instead of using `tooManyAttempts` and `increment` as separate operations. When using the `redis`, `memcached`, or `database` cache stores, this value is incremented atomically, ensuring each concurrent request receives a unique count:

```
1use Illuminate\Support\Facades\RateLimiter;

2 

3$perMinute = 5;

4 

5if (RateLimiter::increment('send-message:'.$user->id) > $perMinute) {

6    return 'Too many attempts!';

7}

8 

9// Send message...
```

Alternatively, you may use the `remaining` method to retrieve the number of attempts remaining for a given key. If a given key has retries remaining, you may invoke the `increment` method to increment the number of total attempts:

```
1use Illuminate\Support\Facades\RateLimiter;

2 

3if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {

4    RateLimiter::increment('send-message:'.$user->id);

5 

6    // Send message...

7}
```

If you would like to increment the value for a given rate limiter key by more than one, you may provide the desired amount to the `increment` method:

```
1RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

#### [Determining Limiter Availability](#determining-limiter-availability)

When a key has no more attempts left, the `availableIn` method returns the number of seconds remaining until more attempts will be available:

```
 1use Illuminate\Support\Facades\RateLimiter;

 2 

 3if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {

 4    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

 5 

 6    return 'You may try again in '.$seconds.' seconds.';

 7}

 8 

 9RateLimiter::increment('send-message:'.$user->id);

10 

11// Send message...
```

### [Clearing Attempts](#clearing-attempts)

You may reset the number of attempts for a given rate limiter key using the `clear` method. For example, you may reset the number of attempts when a given message is read by the receiver:

```
 1use App\Models\Message;

 2use Illuminate\Support\Facades\RateLimiter;

 3 

 4/**

 5 * Mark the message as read.

 6 */

 7public function read(Message $message): Message

 8{

 9    $message->markAsRead();

10 

11    RateLimiter::clear('send-message:'.$message->user_id);

12 

13    return $message;

14}
```
