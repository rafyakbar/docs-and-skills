# Laravel Envoy

- [Introduction](#introduction)
- [Installation](#installation)
- [Writing Tasks](#writing-tasks)
  * [Defining Tasks](#defining-tasks)
  * [Multiple Servers](#multiple-servers)
  * [Setup](#setup)
  * [Variables](#variables)
  * [Stories](#stories)
  * [Hooks](#completion-hooks)
- [Running Tasks](#running-tasks)
  * [Confirming Task Execution](#confirming-task-execution)
- [Notifications](#notifications)
  * [Slack](#slack)
  * [Discord](#discord)
  * [Telegram](#telegram)
  * [Microsoft Teams](#microsoft-teams)

## [Introduction](#introduction)

[Laravel Envoy](https://github.com/laravel/envoy) is a tool for executing common tasks you run on your remote servers. Using [Blade](/docs/13.x/blade) style syntax, you can easily set up tasks for deployment, Artisan commands, and more. Currently, Envoy only supports the Mac and Linux operating systems. However, Windows support is achievable using [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

## [Installation](#installation)

First, install Envoy into your project using the Composer package manager:

```
1composer require laravel/envoy --dev
```

Once Envoy has been installed, the Envoy binary will be available in your application's `vendor/bin` directory:

```
1php vendor/bin/envoy
```

## [Writing Tasks](#writing-tasks)

### [Defining Tasks](#defining-tasks)

Tasks are the basic building block of Envoy. Tasks define the shell commands that should execute on your remote servers when the task is invoked. For example, you might define a task that executes the `php artisan queue:restart` command on all of your application's queue worker servers.

All of your Envoy tasks should be defined in an `Envoy.blade.php` file at the root of your application. Here's an example to get you started:

```
1@servers(['web' => ['[[email protected]](/cdn-cgi/l/email-protection)'], 'workers' => ['[[email protected]](/cdn-cgi/l/email-protection)']])

2 

3@task('restart-queues', ['on' => 'workers'])

4    cd /home/user/example.com

5    php artisan queue:restart

6@endtask
```

As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers via the `on` option of your task declarations. The `@servers` declaration should always be placed on a single line. Within your `@task` declarations, you should place the shell commands that should execute on your servers when the task is invoked.

#### [Local Tasks](#local-tasks)

You can force a script to run on your local computer by specifying the server's IP address as `127.0.0.1`:

```
1@servers(['localhost' => '127.0.0.1'])
```

#### [Importing Envoy Tasks](#importing-envoy-tasks)

Using the `@import` directive, you may import other Envoy files so their stories and tasks are added to yours. After the files have been imported, you may execute the tasks they contain as if they were defined in your own Envoy file:

```
1@import('vendor/package/Envoy.blade.php')
```

### [Multiple Servers](#multiple-servers)

Envoy allows you to easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers you may list each of the servers in the task's `on` array:

```
1@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

2 

3@task('deploy', ['on' => ['web-1', 'web-2']])

4    cd /home/user/example.com

5    git pull origin {{ $branch }}

6    php artisan migrate --force

7@endtask
```

#### [Parallel Execution](#parallel-execution)

By default, tasks will be executed on each server serially. In other words, a task will finish running on the first server before proceeding to execute on the second server. If you would like to run a task across multiple servers in parallel, add the `parallel` option to your task declaration:

```
1@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

2 

3@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])

4    cd /home/user/example.com

5    git pull origin {{ $branch }}

6    php artisan migrate --force

7@endtask
```

### [Setup](#setup)

Sometimes, you may need to execute arbitrary PHP code before running your Envoy tasks. You may use the `@setup` directive to define a block of PHP code that should execute before your tasks:

```
1@setup

2    $now = new DateTime;

3@endsetup
```

If you need to require other PHP files before your task is executed, you may use the `@include` directive at the top of your `Envoy.blade.php` file:

```
1@include('vendor/autoload.php')

2 

3@task('restart-queues')

4    # ...

5@endtask
```

### [Variables](#variables)

If needed, you may pass arguments to Envoy tasks by specifying them on the command line when invoking Envoy:

```
1php vendor/bin/envoy run deploy --branch=master
```

You may access the options within your tasks using Blade's "echo" syntax. You may also define Blade `if` statements and loops within your tasks. For example, let's verify the presence of the `$branch` variable before executing the `git pull` command:

```
 1@servers(['web' => ['[[email protected]](/cdn-cgi/l/email-protection)']])

 2 

 3@task('deploy', ['on' => 'web'])

 4    cd /home/user/example.com

 5 

 6    @if ($branch)

 7        git pull origin {{ $branch }}

 8    @endif

 9 

10    php artisan migrate --force

11@endtask
```

### [Stories](#stories)

Stories group a set of tasks under a single, convenient name. For instance, a `deploy` story may run the `update-code` and `install-dependencies` tasks by listing the task names within its definition:

```
 1@servers(['web' => ['[[email protected]](/cdn-cgi/l/email-protection)']])

 2 

 3@story('deploy')

 4    update-code

 5    install-dependencies

 6@endstory

 7 

 8@task('update-code')

 9    cd /home/user/example.com

10    git pull origin master

11@endtask

12 

13@task('install-dependencies')

14    cd /home/user/example.com

15    composer install

16@endtask
```

Once the story has been written, you may invoke it in the same way you would invoke a task:

```
1php vendor/bin/envoy run deploy
```

### [Hooks](#completion-hooks)

When tasks and stories run, a number of hooks are executed. The hook types supported by Envoy are `@before`, `@after`, `@error`, `@success`, and `@finished`. All of the code in these hooks is interpreted as PHP and executed locally, not on the remote servers that your tasks interact with.

You may define as many of each of these hooks as you like. They will be executed in the order that they appear in your Envoy script.

#### [`@before`](#hook-before)

Before each task execution, all of the `@before` hooks registered in your Envoy script will execute. The `@before` hooks receive the name of the task that will be executed:

```
1@before

2    if ($task === 'deploy') {

3        // ...

4    }

5@endbefore
```

#### [`@after`](#completion-after)

After each task execution, all of the `@after` hooks registered in your Envoy script will execute. The `@after` hooks receive the name of the task that was executed:

```
1@after

2    if ($task === 'deploy') {

3        // ...

4    }

5@endafter
```

#### [`@error`](#completion-error)

After every task failure (exits with a status code greater than `0`), all of the `@error` hooks registered in your Envoy script will execute. The `@error` hooks receive the name of the task that was executed:

```
1@error

2    if ($task === 'deploy') {

3        // ...

4    }

5@enderror
```

#### [`@success`](#completion-success)

If all tasks have executed without errors, all of the `@success` hooks registered in your Envoy script will execute:

```
1@success

2    // ...

3@endsuccess
```

#### [`@finished`](#completion-finished)

After all tasks have been executed (regardless of exit status), all of the `@finished` hooks will be executed. The `@finished` hooks receive the status code of the completed task, which may be `null` or an `integer` greater than or equal to `0`:

```
1@finished

2    if ($exitCode > 0) {

3        // There were errors in one of the tasks...

4    }

5@endfinished
```

## [Running Tasks](#running-tasks)

To run a task or story that is defined in your application's `Envoy.blade.php` file, execute Envoy's `run` command, passing the name of the task or story you would like to execute. Envoy will execute the task and display the output from your remote servers as the task is running:

```
1php vendor/bin/envoy run deploy
```

### [Confirming Task Execution](#confirming-task-execution)

If you would like to be prompted for confirmation before running a given task on your servers, you should add the `confirm` directive to your task declaration. This option is particularly useful for destructive operations:

```
1@task('deploy', ['on' => 'web', 'confirm' => true])

2    cd /home/user/example.com

3    git pull origin {{ $branch }}

4    php artisan migrate

5@endtask
```

## [Notifications](#notifications)

### [Slack](#slack)

Envoy supports sending notifications to [Slack](https://slack.com) after each task is executed. The `@slack` directive accepts a Slack hook URL and a channel / user name. You may retrieve your webhook URL by creating an "Incoming WebHooks" integration in your Slack control panel.

You should pass the entire webhook URL as the first argument given to the `@slack` directive. The second argument given to the `@slack` directive should be a channel name (`#channel`) or a user name (`@user`):

```
1@finished

2    @slack('webhook-url', '#bots')

3@endfinished
```

By default, Envoy notifications will send a message to the notification channel describing the task that was executed. However, you may overwrite this message with your own custom message by passing a third argument to the `@slack` directive:

```
1@finished

2    @slack('webhook-url', '#bots', 'Hello, Slack.')

3@endfinished
```

### [Discord](#discord)

Envoy also supports sending notifications to [Discord](https://discord.com) after each task is executed. The `@discord` directive accepts a Discord hook URL and a message. You may retrieve your webhook URL by creating a "Webhook" in your Server Settings and choosing which channel the webhook should post to. You should pass the entire Webhook URL into the `@discord` directive:

```
1@finished

2    @discord('discord-webhook-url')

3@endfinished
```

### [Telegram](#telegram)

Envoy also supports sending notifications to [Telegram](https://telegram.org) after each task is executed. The `@telegram` directive accepts a Telegram Bot ID and a Chat ID. You may retrieve your Bot ID by creating a new bot using [BotFather](https://t.me/botfather). You can retrieve a valid Chat ID using [@username_to_id_bot](https://t.me/username_to_id_bot). You should pass the entire Bot ID and Chat ID into the `@telegram` directive:

```
1@finished

2    @telegram('bot-id','chat-id')

3@endfinished
```

### [Microsoft Teams](#microsoft-teams)

Envoy also supports sending notifications to [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) after each task is executed. The `@microsoftTeams` directive accepts a Teams Webhook (required), a message, theme color (success, info, warning, error), and an array of options. You may retrieve your Teams Webhook by creating a new [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). The Teams API has many other attributes to customize your message box like title, summary, and sections. You can find more information on the [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). You should pass the entire Webhook URL into the `@microsoftTeams` directive:

```
1@finished

2    @microsoftTeams('webhook-url')

3@endfinished
```
