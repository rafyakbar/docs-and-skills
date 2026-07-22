# Task Scheduling

- [Introduction](#introduction)
- [Defining Schedules](#defining-schedules)
  * [Scheduling Artisan Commands](#scheduling-artisan-commands)
  * [Scheduling Queued Jobs](#scheduling-queued-jobs)
  * [Scheduling Shell Commands](#scheduling-shell-commands)
  * [Schedule Frequency Options](#schedule-frequency-options)
  * [Timezones](#timezones)
  * [Preventing Task Overlaps](#preventing-task-overlaps)
  * [Running Tasks on One Server](#running-tasks-on-one-server)
  * [Background Tasks](#background-tasks)
  * [Maintenance Mode](#maintenance-mode)
  * [Pausing Scheduled Tasks](#pausing-scheduled-tasks)
  * [Schedule Groups](#schedule-groups)
- [Running the Scheduler](#running-the-scheduler)
  * [Sub-Minute Scheduled Tasks](#sub-minute-scheduled-tasks)
  * [Running the Scheduler Locally](#running-the-scheduler-locally)
- [Task Output](#task-output)
- [Task Hooks](#task-hooks)
- [Events](#events)

## [Introduction](#introduction)

In the past, you may have written a cron configuration entry for each task you needed to schedule on your server. However, this can quickly become a pain because your task schedule is no longer in source control and you must SSH into your server to view your existing cron entries or add additional entries.

Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is typically defined in your application's `routes/console.php` file.

## [Defining Schedules](#defining-schedules)

You may define all of your scheduled tasks in your application's `routes/console.php` file. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table:

```
1<?php

2 

3use Illuminate\Support\Facades\DB;

4use Illuminate\Support\Facades\Schedule;

5 

6Schedule::call(function () {

7    DB::table('recent_users')->delete();

8})->daily();
```

In addition to scheduling using closures, you may also schedule [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Invokable objects are simple PHP classes that contain an `__invoke` method:

```
1Schedule::call(new DeleteRecentUsers)->daily();
```

If you prefer to reserve your `routes/console.php` file for command definitions only, you may use the `withSchedule` method in your application's `bootstrap/app.php` file to define your scheduled tasks. This method accepts a closure that receives an instance of the scheduler:

```
1use Illuminate\Console\Scheduling\Schedule;

2 

3->withSchedule(function (Schedule $schedule) {

4    $schedule->call(new DeleteRecentUsers)->daily();

5})
```

If you would like to view an overview of your scheduled tasks and the next time they are scheduled to run, you may use the `schedule:list` Artisan command:

```
1php artisan schedule:list
```

### [Scheduling Artisan Commands](#scheduling-artisan-commands)

In addition to scheduling closures, you may also schedule [Artisan commands](/docs/13.x/artisan) and system commands. For example, you may use the `command` method to schedule an Artisan command using either the command's name or class.

When scheduling Artisan commands using the command's class name, you may pass an array of additional command-line arguments that should be provided to the command when it is invoked:

```
1use App\Console\Commands\SendEmailsCommand;

2use Illuminate\Support\Facades\Schedule;

3 

4Schedule::command('emails:send Taylor --force')->daily();

5 

6Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

#### [Scheduling Artisan Closure Commands](#scheduling-artisan-closure-commands)

If you want to schedule an Artisan command defined by a closure, you may chain the scheduling related methods after the command's definition:

```
1Artisan::command('delete:recent-users', function () {

2    DB::table('recent_users')->delete();

3})->purpose('Delete recent users')->daily();
```

If you need to pass arguments to the closure command, you may provide them to the `schedule` method:

```
1Artisan::command('emails:send {user} {--force}', function ($user) {

2    // ...

3})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

### [Scheduling Queued Jobs](#scheduling-queued-jobs)

The `job` method may be used to schedule a [queued job](/docs/13.x/queues). This method provides a convenient way to schedule queued jobs without using the `call` method to define closures to queue the job:

```
1use App\Jobs\Heartbeat;

2use Illuminate\Support\Facades\Schedule;

3 

4Schedule::job(new Heartbeat)->everyFiveMinutes();
```

Optional second and third arguments may be provided to the `job` method which specifies the queue name and queue connection that should be used to queue the job:

```
1use App\Jobs\Heartbeat;

2use Illuminate\Support\Facades\Schedule;

3 

4// Dispatch the job to the "heartbeats" queue on the "sqs" connection...

5Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

### [Scheduling Shell Commands](#scheduling-shell-commands)

The `exec` method may be used to issue a command to the operating system:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::exec('node /home/forge/script.js')->daily();
```

### [Schedule Frequency Options](#schedule-frequency-options)

We've already seen a few examples of how you may configure a task to run at specified intervals. However, there are many more task schedule frequencies that you may assign to a task:

| Method                             | Description                                              |
| ---------------------------------- | -------------------------------------------------------- |
| `->cron('* * * * *');`             | Run the task on a custom cron schedule.                  |
| `->everySecond();`                 | Run the task every second.                               |
| `->everyTwoSeconds();`             | Run the task every two seconds.                          |
| `->everyFiveSeconds();`            | Run the task every five seconds.                         |
| `->everyTenSeconds();`             | Run the task every ten seconds.                          |
| `->everyFifteenSeconds();`         | Run the task every fifteen seconds.                      |
| `->everyTwentySeconds();`          | Run the task every twenty seconds.                       |
| `->everyThirtySeconds();`          | Run the task every thirty seconds.                       |
| `->everyMinute();`                 | Run the task every minute.                               |
| `->everyTwoMinutes();`             | Run the task every two minutes.                          |
| `->everyThreeMinutes();`           | Run the task every three minutes.                        |
| `->everyFourMinutes();`            | Run the task every four minutes.                         |
| `->everyFiveMinutes();`            | Run the task every five minutes.                         |
| `->everyTenMinutes();`             | Run the task every ten minutes.                          |
| `->everyFifteenMinutes();`         | Run the task every fifteen minutes.                      |
| `->everyThirtyMinutes();`          | Run the task every thirty minutes.                       |
| `->hourly();`                      | Run the task every hour.                                 |
| `->hourlyAt(17);`                  | Run the task every hour at 17 minutes past the hour.     |
| `->everyOddHour($minutes = 0);`    | Run the task every odd hour.                             |
| `->everyTwoHours($minutes = 0);`   | Run the task every two hours.                            |
| `->everyThreeHours($minutes = 0);` | Run the task every three hours.                          |
| `->everyFourHours($minutes = 0);`  | Run the task every four hours.                           |
| `->everySixHours($minutes = 0);`   | Run the task every six hours.                            |
| `->daily();`                       | Run the task every day at midnight.                      |
| `->dailyAt('13:00');`              | Run the task every day at 13:00.                         |
| `->twiceDaily(1, 13);`             | Run the task daily at 1:00 & 13:00.                      |
| `->twiceDailyAt(1, 13, 15);`       | Run the task daily at 1:15 & 13:15.                      |
| `->daysOfMonth([1, 10, 20]);`      | Run the task on specific days of the month.              |
| `->weekly();`                      | Run the task every Sunday at 00:00.                      |
| `->weeklyOn(1, '8:00');`           | Run the task every week on Monday at 8:00.               |
| `->monthly();`                     | Run the task on the first day of every month at 00:00.   |
| `->monthlyOn(4, '15:00');`         | Run the task every month on the 4th at 15:00.            |
| `->twiceMonthly(1, 16, '13:00');`  | Run the task monthly on the 1st and 16th at 13:00.       |
| `->lastDayOfMonth('15:00');`       | Run the task on the last day of the month at 15:00.      |
| `->quarterly();`                   | Run the task on the first day of every quarter at 00:00. |
| `->quarterlyOn(4, '14:00');`       | Run the task every quarter on the 4th at 14:00.          |
| `->yearly();`                      | Run the task on the first day of every year at 00:00.    |
| `->yearlyOn(6, 1, '17:00');`       | Run the task every year on June 1st at 17:00.            |
| `->timezone('America/New_York');`  | Set the timezone for the task.                           |

These methods may be combined with additional constraints to create even more finely tuned schedules that only run on certain days of the week. For example, you may schedule a command to run weekly on Monday:

```
 1use Illuminate\Support\Facades\Schedule;

 2 

 3// Run once per week on Monday at 1 PM...

 4Schedule::call(function () {

 5    // ...

 6})->weekly()->mondays()->at('13:00');

 7 

 8// Run hourly from 8 AM to 5 PM on weekdays...

 9Schedule::command('foo')

10    ->weekdays()

11    ->hourly()

12    ->timezone('America/Chicago')

13    ->between('8:00', '17:00');
```

A list of additional schedule constraints may be found below:

| Method                                   | Description                                            |
| ---------------------------------------- | ------------------------------------------------------ |
| `->weekdays();`                          | Limit the task to weekdays.                            |
| `->weekends();`                          | Limit the task to weekends.                            |
| `->sundays();`                           | Limit the task to Sunday.                              |
| `->mondays();`                           | Limit the task to Monday.                              |
| `->tuesdays();`                          | Limit the task to Tuesday.                             |
| `->wednesdays();`                        | Limit the task to Wednesday.                           |
| `->thursdays();`                         | Limit the task to Thursday.                            |
| `->fridays();`                           | Limit the task to Friday.                              |
| `->saturdays();`                         | Limit the task to Saturday.                            |
| `->days(array|mixed);`                   | Limit the task to specific days.                       |
| `->between($startTime, $endTime);`       | Limit the task to run between start and end times.     |
| `->unlessBetween($startTime, $endTime);` | Limit the task to not run between start and end times. |
| `->when(Closure);`                       | Limit the task based on a truth test.                  |
| `->environments($env);`                  | Limit the task to specific environments.               |

#### [Day Constraints](#day-constraints)

The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('emails:send')

4    ->hourly()

5    ->days([0, 3]);
```

Alternatively, you may use the constants available on the `Illuminate\Console\Scheduling\Schedule` class when defining the days on which a task should run:

```
1use Illuminate\Support\Facades;

2use Illuminate\Console\Scheduling\Schedule;

3 

4Facades\Schedule::command('emails:send')

5    ->hourly()

6    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

#### [Between Time Constraints](#between-time-constraints)

The `between` method may be used to limit the execution of a task based on the time of day:

```
1Schedule::command('emails:send')

2    ->hourly()

3    ->between('7:00', '22:00');
```

Similarly, the `unlessBetween` method can be used to exclude the execution of a task for a period of time:

```
1Schedule::command('emails:send')

2    ->hourly()

3    ->unlessBetween('23:00', '4:00');
```

#### [Truth Test Constraints](#truth-test-constraints)

The `when` method may be used to limit the execution of a task based on the result of a given truth test. In other words, if the given closure returns `true`, the task will execute as long as no other constraining conditions prevent the task from running:

```
1Schedule::command('emails:send')->daily()->when(function () {

2    return true;

3});
```

The `skip` method may be seen as the inverse of `when`. If the `skip` method returns `true`, the scheduled task will not be executed:

```
1Schedule::command('emails:send')->daily()->skip(function () {

2    return true;

3});
```

When using chained `when` methods, the scheduled command will only execute if all `when` conditions return `true`.

#### [Environment Constraints](#environment-constraints)

The `environments` method may be used to execute tasks only on the given environments (as defined by the `APP_ENV` [environment variable](/docs/13.x/configuration#environment-configuration)):

```
1Schedule::command('emails:send')

2    ->daily()

3    ->environments(['staging', 'production']);
```

### [Timezones](#timezones)

Using the `timezone` method, you may specify that a scheduled task's time should be interpreted within a given timezone:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('report:generate')

4    ->timezone('America/New_York')

5    ->at('2:00')
```

If you are repeatedly assigning the same timezone to all of your scheduled tasks, you can specify which timezone should be assigned to all schedules by defining a `schedule_timezone` option within your application's `app` configuration file:

```
1'timezone' => 'UTC',

2 

3'schedule_timezone' => 'America/Chicago',
```

Remember that some timezones utilize daylight saving time. When daylight saving time changes occur, your scheduled task may run twice or even not run at all. For this reason, we recommend avoiding timezone scheduling when possible.

### [Preventing Task Overlaps](#preventing-task-overlaps)

By default, scheduled tasks will be run even if the previous instance of the task is still running. To prevent this, you may use the `withoutOverlapping` method:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('emails:send')->withoutOverlapping();
```

In this example, the `emails:send` [Artisan command](/docs/13.x/artisan) will be run every minute if it is not already running. The `withoutOverlapping` method is especially useful if you have tasks that vary drastically in their execution time, preventing you from predicting exactly how long a given task will take.

If needed, you may specify how many minutes must pass before the "without overlapping" lock expires. By default, the lock will expire after 24 hours:

```
1Schedule::command('emails:send')->withoutOverlapping(10);
```

Behind the scenes, the `withoutOverlapping` method utilizes your application's [cache](/docs/13.x/cache) to obtain locks. If necessary, you can clear these cache locks using the `schedule:clear-cache` Artisan command. This is typically only necessary if a task becomes stuck due to an unexpected server problem.

### [Running Tasks on One Server](#running-tasks-on-one-server)

To utilize this feature, your application must be using the `database`, `memcached`, `dynamodb`, or `redis` cache driver as your application's default cache driver. In addition, all servers must be communicating with the same central cache server.

If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good!

To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('report:generate')

4    ->fridays()

5    ->at('17:00')

6    ->onOneServer();
```

You may use the `useCache` method to customize the cache store used by the scheduler to obtain the atomic locks necessary for single-server tasks:

```
1Schedule::useCache('database');
```

#### [Naming Single Server Jobs](#naming-unique-jobs)

Sometimes you may need to schedule the same job to be dispatched with different parameters, while still instructing Laravel to run each permutation of the job on a single server. To accomplish this, you may assign each schedule definition a unique name via the `name` method:

```
1Schedule::job(new CheckUptime('https://laravel.com'))

2    ->name('check_uptime:laravel.com')

3    ->everyFiveMinutes()

4    ->onOneServer();

5 

6Schedule::job(new CheckUptime('https://vapor.laravel.com'))

7    ->name('check_uptime:vapor.laravel.com')

8    ->everyFiveMinutes()

9    ->onOneServer();
```

Similarly, scheduled closures must be assigned a name if they are intended to be run on one server:

```
1Schedule::call(fn () => User::resetApiRequestCount())

2    ->name('reset-api-request-count')

3    ->daily()

4    ->onOneServer();
```

### [Background Tasks](#background-tasks)

By default, multiple tasks scheduled at the same time will execute sequentially based on the order they are defined in your `schedule` method. If you have long-running tasks, this may cause subsequent tasks to start much later than anticipated. If you would like to run tasks in the background so that they may all run simultaneously, you may use the `runInBackground` method:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('analytics:report')

4    ->daily()

5    ->runInBackground();
```

The `runInBackground` method may only be used when scheduling tasks via the `command` and `exec` methods.

### [Maintenance Mode](#maintenance-mode)

Your application's scheduled tasks will not run when the application is in [maintenance mode](/docs/13.x/configuration#maintenance-mode), since we don't want your tasks to interfere with any unfinished maintenance you may be performing on your server. However, if you would like to force a task to run even in maintenance mode, you may call the `evenInMaintenanceMode` method when defining the task:

```
1Schedule::command('emails:send')->evenInMaintenanceMode();
```

### [Pausing Scheduled Tasks](#pausing-scheduled-tasks)

You may temporarily pause scheduled task processing without changing your deployed code by using the `schedule:pause` Artisan command:

```
1php artisan schedule:pause
```

While the scheduler is paused, no scheduled tasks will run. You may resume scheduled task processing using the `schedule:continue` command:

```
1php artisan schedule:continue
```

If a task should still run while the scheduler is paused, you may mark it with the `evenWhenPaused` method:

```
1Schedule::command('emails:send')->evenWhenPaused();
```

### [Schedule Groups](#schedule-groups)

When defining multiple scheduled tasks with similar configurations, you can use Laravel's task grouping feature to avoid repeating the same settings for each task. Grouping tasks simplifies your code and ensures consistency across related tasks.

To create a group of scheduled tasks, invoke the desired task configuration methods, followed by the `group` method. The `group` method accepts a closure that is responsible for defining the tasks that share the specified configuration:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::daily()

4    ->onOneServer()

5    ->timezone('America/New_York')

6    ->group(function () {

7        Schedule::command('emails:send --force');

8        Schedule::command('emails:prune');

9    });
```

## [Running the Scheduler](#running-the-scheduler)

Now that we have learned how to define scheduled tasks, let's discuss how to actually run them on our server. The `schedule:run` Artisan command will evaluate all of your scheduled tasks and determine if they need to run based on the server's current time.

So, when using Laravel's scheduler, we only need to add a single cron configuration entry to our server that runs the `schedule:run` command every minute. If you do not know how to add cron entries to your server, consider using a managed platform such as [Laravel Cloud](https://cloud.laravel.com) which can manage the scheduled task execution for you:

```
1* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

### [Sub-Minute Scheduled Tasks](#sub-minute-scheduled-tasks)

On most operating systems, cron jobs are limited to running a maximum of once per minute. However, Laravel's scheduler allows you to schedule tasks to run at more frequent intervals, even as often as once per second:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::call(function () {

4    DB::table('recent_users')->delete();

5})->everySecond();
```

When sub-minute tasks are defined within your application, the `schedule:run` command will continue running until the end of the current minute instead of exiting immediately. This allows the command to invoke all required sub-minute tasks throughout the minute.

Since sub-minute tasks that take longer than expected to run could delay the execution of later sub-minute tasks, it is recommended that all sub-minute tasks dispatch queued jobs or background commands to handle the actual task processing:

```
1use App\Jobs\DeleteRecentUsers;

2 

3Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

4 

5Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

#### [Interrupting Sub-Minute Tasks](#interrupting-sub-minute-tasks)

As the `schedule:run` command runs for the entire minute of invocation when sub-minute tasks are defined, you may sometimes need to interrupt the command when deploying your application. Otherwise, an instance of the `schedule:run` command that is already running would continue using your application's previously deployed code until the current minute ends.

To interrupt in-progress `schedule:run` invocations, you may add the `schedule:interrupt` command to your application's deployment script. This command should be invoked after your application is finished deploying:

```
1php artisan schedule:interrupt
```

### [Running the Scheduler Locally](#running-the-scheduler-locally)

Typically, you would not add a scheduler cron entry to your local development machine. Instead, you may use the `schedule:work` Artisan command. This command will run in the foreground and invoke the scheduler every minute until you terminate the command. When sub-minute tasks are defined, the scheduler will continue running within each minute to process those tasks:

```
1php artisan schedule:work
```

## [Task Output](#task-output)

The Laravel scheduler provides several convenient methods for working with the output generated by scheduled tasks. First, using the `sendOutputTo` method, you may send the output to a file for later inspection:

```
1use Illuminate\Support\Facades\Schedule;

2 

3Schedule::command('emails:send')

4    ->daily()

5    ->sendOutputTo($filePath);
```

If you would like to append the output to a given file, you may use the `appendOutputTo` method:

```
1Schedule::command('emails:send')

2    ->daily()

3    ->appendOutputTo($filePath);
```

Using the `emailOutputTo` method, you may email the output to an email address of your choice. Before emailing the output of a task, you should configure Laravel's [email services](/docs/13.x/mail):

```
1Schedule::command('report:generate')

2    ->daily()

3    ->sendOutputTo($filePath)

4    ->emailOutputTo('[[email protected]](/cdn-cgi/l/email-protection)');
```

If you only want to email the output if the scheduled Artisan or system command terminates with a non-zero exit code, use the `emailOutputOnFailure` method:

```
1Schedule::command('report:generate')

2    ->daily()

3    ->emailOutputOnFailure('[[email protected]](/cdn-cgi/l/email-protection)');
```

The `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, and `appendOutputTo` methods are exclusive to the `command` and `exec` methods.

## [Task Hooks](#task-hooks)

Using the `before` and `after` methods, you may specify code to be executed before and after the scheduled task is executed:

```
 1use Illuminate\Support\Facades\Schedule;

 2 

 3Schedule::command('emails:send')

 4    ->daily()

 5    ->before(function () {

 6        // The task is about to execute...

 7    })

 8    ->after(function () {

 9        // The task has executed...

10    });
```

The `onSuccess` and `onFailure` methods allow you to specify code to be executed if the scheduled task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code:

```
1Schedule::command('emails:send')

2    ->daily()

3    ->onSuccess(function () {

4        // The task succeeded...

5    })

6    ->onFailure(function () {

7        // The task failed...

8    });
```

If output is available from your command, you may access it in your `after`, `onSuccess` or `onFailure` hooks by type-hinting an `Illuminate\Support\Stringable` instance as the `$output` argument of your hook's closure definition:

```
 1use Illuminate\Support\Stringable;

 2 

 3Schedule::command('emails:send')

 4    ->daily()

 5    ->onSuccess(function (Stringable $output) {

 6        // The task succeeded...

 7    })

 8    ->onFailure(function (Stringable $output) {

 9        // The task failed...

10    });
```

#### [Pinging URLs](#pinging-urls)

Using the `pingBefore` and `thenPing` methods, the scheduler can automatically ping a given URL before or after a task is executed. This method is useful for notifying an external service, such as [Envoyer](https://envoyer.io), that your scheduled task is beginning or has finished execution:

```
1Schedule::command('emails:send')

2    ->daily()

3    ->pingBefore($url)

4    ->thenPing($url);
```

The `pingOnSuccess` and `pingOnFailure` methods may be used to ping a given URL only if the task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code:

```
1Schedule::command('emails:send')

2    ->daily()

3    ->pingOnSuccess($successUrl)

4    ->pingOnFailure($failureUrl);
```

The `pingBeforeIf`,`thenPingIf`,`pingOnSuccessIf`, and `pingOnFailureIf` methods may be used to ping a given URL only if a given condition is `true`:

```
1Schedule::command('emails:send')

2    ->daily()

3    ->pingBeforeIf($condition, $url)

4    ->thenPingIf($condition, $url);

5 

6Schedule::command('emails:send')

7    ->daily()

8    ->pingOnSuccessIf($condition, $successUrl)

9    ->pingOnFailureIf($condition, $failureUrl);
```

## [Events](#events)

Laravel dispatches a variety of [events](/docs/13.x/events) during the scheduling process. You may [define listeners](/docs/13.x/events) for any of the following events:

| Event Name                                                  |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |
