# Laravel 13.x Documentation Reference

Crawled from [https://laravel.com/docs/13.x/releases](https://laravel.com/docs/13.x/releases)

## Table of Contents

- [Prologue](#prologue)
- [Getting Started](#getting-started)
- [Architecture Concepts](#architecture-concepts)
- [The Basics](#the-basics)
- [Digging Deeper](#digging-deeper)
- [Security](#security)
- [Database](#database)
- [Eloquent ORM](#eloquent-orm)
- [AI](#ai)
- [Testing](#testing)
- [Packages (Official)](#packages-official)

---

## Prologue

Introductory documentation covering Laravel's versioning strategy, upgrade paths between major releases, and guidelines for contributing to the framework itself.

- **001** [Release Notes](references/001_release-notes.md) — Laravel and its other first-party packages follow Semantic Versioning. Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes.
- **002** [Upgrade Guide](references/002_upgrade-guide.md) — We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. To save time, you may use Shift. Shift is a community-maintained service that automates Laravel upgrades.
- **003** [Contribution Guide](references/003_contribution-guide.md) — To encourage active collaboration, Laravel strongly encourages pull requests, not just bug reports. Pull requests will only be reviewed when marked as "ready for review" (not in the "draft" state) and all tests for new features are passing. Lingering, non-active pull requests left in the "draft" state will be closed after a few days.

## Getting Started

Guides for setting up a new Laravel application, from installation and configuration to directory structure, frontend choices, starter kits, and production deployment.

- **004** [Installation](references/004_installation.md) — Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details.
- **005** [Configuration](references/005_configuration.md) — All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.
- **006** [Agentic Development](references/006_agentic-development.md) — Laravel is uniquely positioned to be the best framework for AI assisted and agentic development. The rise of AI coding agents like Claude Code, OpenCode, Cursor, and GitHub Copilot has transformed how developers write code. These tools can generate entire features,.
- **007** [Directory Structure](references/007_directory-structure.md) — The default Laravel application structure is intended to provide a great starting point for both large and small applications. But you are free to organize your application however you like. Laravel imposes almost no restrictions on where any given class is located - as long as Composer can autoload the class.
- **008** [Frontend](references/008_frontend.md) — Laravel is a backend framework that provides all of the features you need to build modern web applications, such as routing, validation, caching, queues, file storage, and more. However, we believe it's important to offer developers a beautiful full-stack experience, including powerful.
- **009** [Starter Kits](references/009_starter-kits.md) — To give you a head start building your new Laravel application, we are happy to offer application starter kits. These starter kits give you a head start on building your next Laravel application, and include the routes, controllers, and views you need to register and authenticate your application's users. The starter kits use [Laravel Fortify](/docs/13.x/fortify.
- **010** [Deployment](references/010_deployment.md) — When you're ready to deploy your Laravel application to production, there are some important things you can do to make sure your application is running as efficiently as possible. In this document, we'll cover some great starting points for making sure your Laravel application is deployed properly.

## Architecture Concepts

Core architectural patterns underpinning Laravel: the request lifecycle, service container for dependency injection, service providers, and facades.

- **011** [Request Lifecycle](references/011_request-lifecycle.md) — When using any tool in the "real world", you feel more confident if you understand how that tool works. Application development is no different. When you understand how your development tools function, you feel more comfortable and confident using them.
- **012** [Service Container](references/012_service-container.md) — The Laravel service container is a powerful tool for managing class dependencies and performing dependency injection. Dependency injection is a fancy phrase that essentially means this: class dependencies are "injected" into the class via the constructor or, in some cases, "setter" methods.
- **013** [Service Providers](references/013_service-providers.md) — Service providers are the central place of all Laravel application bootstrapping. Your own application, as well as all of Laravel's core services, are bootstrapped via service providers.
- **014** [Facades](references/014_facades.md) — Throughout the Laravel documentation, you will see examples of code that interacts with Laravel's features via "facades". Facades provide a "static" interface to classes that are available in the application's service container. Laravel ships with many facades which provide access to almost all of Laravel's features.

## The Basics

Fundamental HTTP-layer components: routing, middleware, CSRF protection, controllers, request/response handling, views, Blade templating, asset bundling with Vite, URL generation, sessions, validation, error handling, logging, and the Artisan console.

- **015** [Routing](references/015_routing.md) — The most basic Laravel routes accept a URI and a closure, providing a very simple and expressive method of defining routes and behavior without complicated routing configuration files:.
- **016** [Middleware](references/016_middleware.md) — Middleware provide a convenient mechanism for inspecting and filtering HTTP requests entering your application. For example, Laravel includes a middleware that verifies the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to your application's login screen. However, if the user is authenticated, the middleware will allow the request.
- **017** [CSRF Protection](references/017_csrf-protection.md) — Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of an authenticated user. Thankfully, Laravel makes it easy to protect your application from cross-site request forgery (CSRF) attacks.
- **018** [Controllers](references/018_controllers.md) — Instead of defining all of your request handling logic as closures in your route files, you may wish to organize this behavior using "controller" classes. Controllers can group related request handling logic into a single class. For example, a `UserController` class might handle all incoming requests related to users, including showing, creating, updating, and deleting users. By default, controlle.
- **019** [Requests](references/019_requests.md) — Laravel's `Illuminate\Http\Request` class provides an object-oriented way to interact with the current HTTP request being handled by your application as well as retrieve the input, cookies, and files that were submitted with the request.
- **020** [Responses](references/020_responses.md) — All routes and controllers should return a response to be sent back to the user's browser. Laravel provides several different ways to return responses. The most basic response is returning a string from a route or controller. The framework will automatically convert the string into a full HTTP response:.
- **021** [Views](references/021_views.md) — Of course, it's not practical to return entire HTML documents strings directly from your routes and controllers. Thankfully, views provide a convenient way to place all of our HTML in separate files.
- **022** [Blade Templates](references/022_blade-templates.md) — Blade is the simple, yet powerful templating engine that is included with Laravel. Unlike some PHP templating engines, Blade does not restrict you from using plain PHP code in your templates. In fact, all Blade templates are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade template files use the `.blade.php` fi.
- **023** [Asset Bundling](references/023_asset-bundling.md) — Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production.
- **024** [URL Generation](references/024_url-generation.md) — Laravel provides several helpers to assist you in generating URLs for your application. These helpers are primarily helpful when building links in your templates and API responses, or when generating redirect responses to another part of your application.
- **025** [Session](references/025_session.md) — Since HTTP driven applications are stateless, sessions provide a way to store information about the user across multiple requests. That user information is typically placed in a persistent store / backend that can be accessed from subsequent requests.
- **026** [Validation](references/026_validation.md) — Laravel provides several different approaches to validate your application's incoming data. It is most common to use the `validate` method available on all incoming HTTP requests. However, we will discuss other approaches to validation as well.
- **027** [Error Handling](references/027_error-handling.md) — When you start a new Laravel project, error and exception handling is already configured for you; however, at any point, you may use the `withExceptions` method in your application's `bootstrap/app.php` to manage how exceptions are reported and rendered by your application.
- **028** [Logging](references/028_logging.md) — To help you learn more about what's happening within your application, Laravel provides robust logging services that allow you to log messages to files, the system error log, and even to Slack to notify your entire team.
- **029** [Artisan Console](references/029_artisan-console.md) — Artisan is the command line interface included with Laravel. Artisan exists at the root of your application as the `artisan` script and provides a number of helpful commands that can assist you while you build your application. To view a list of all available Artisan commands, you may use the `list` command:.

## Digging Deeper

Advanced framework features including broadcasting, caching, collections, concurrency, context, contracts, events, file storage, helpers, HTTP client, image manipulation, localization, mail, notifications, package development, processes, queues, rate limiting, search, string utilities, and task scheduling.

- **030** [Broadcasting](references/030_broadcasting.md) — In many modern web applications, WebSockets are used to implement realtime, live-updating user interfaces. When some data is updated on the server, a message is typically sent over a WebSocket connection to be handled by the client. WebSockets provide a more efficient alternative to continually polling your application's server for data changes that should be reflected in your UI.
- **031** [Cache](references/031_cache.md) — Some of the data retrieval or processing tasks performed by your application could be CPU intensive or take several seconds to complete. When this is the case, it is common to cache the retrieved data for a time so it can be retrieved quickly on subsequent requests for the same data. The cached data is usually stored in a very fast data store such as Memcached or [Redis](h.
- **032** [Collections](references/032_collections.md) — The `Illuminate\Support\Collection` class provides a fluent, convenient wrapper for working with arrays of data. For example, check out the following code. We'll use the `collect` helper to create a new collection instance from the array, run the `strtoupper` function on each element, and then remove all empty elements:.
- **033** [Concurrency](references/033_concurrency.md) — Sometimes you may need to execute several slow tasks which do not depend on one another. In many cases, significant performance improvements can be realized by executing the tasks concurrently. Laravel's `Concurrency` facade provides a simple, convenient API for executing closures concurrently.
- **034** [Context](references/034_context.md) — Laravel's "context" capabilities enable you to capture, retrieve, and share information throughout requests, jobs, and commands executing within your application. This captured information is also included in logs written by your application, giving you deeper insight into the surrounding code execution history that occurred before a log entry was written and allowing you to trace execution flows.
- **035** [Contracts](references/035_contracts.md) — Laravel's "contracts" are a set of interfaces that define the core services provided by the framework. For example, an `Illuminate\Contracts\Queue\Queue` contract defines the methods needed for queueing jobs, while the `Illuminate\Contracts\Mail\Mailer` contract defines the methods needed for sending e-mail.
- **036** [Events](references/036_events.md) — + Keeping Listeners Unique Until Processing Begins.
- **037** [File Storage](references/037_file-storage.md) — Laravel provides a powerful filesystem abstraction thanks to the wonderful Flysystem PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple drivers for working with local filesystems, SFTP, and Amazon S3. Even better, it's amazingly simple to switch between these storage options between your local development machine and produc.
- **038** [Helpers](references/038_helpers.md) — Laravel includes a variety of global "helper" PHP functions. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient.
- **039** [HTTP Client](references/039_http-client.md) — Laravel provides an expressive, minimal API around the Guzzle HTTP client, allowing you to quickly make outgoing HTTP requests to communicate with other web applications. Laravel's wrapper around Guzzle is focused on its most common use cases and a wonderful developer experience.
- **040** [Images](references/040_images.md) — Laravel provides a fluent image manipulation API that allows you to resize, crop, encode, and store images using the same expressive conventions found throughout the framework. Laravel's image features are powered by Intervention Image and support the GD and Imagick PHP extensions.
- **041** [Localization](references/041_localization.md) — By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.
- **042** [Mail](references/042_mail.md) — Sending email doesn't have to be complicated. Laravel provides a clean, simple email API powered by the popular Symfony Mailer component. Laravel and Symfony Mailer provide drivers for sending email via SMTP, Cloudflare, Mailgun, Postmark, Resend, Amazon SES, and `sendmail`, allowing you to quickly get started sending mail through a local or cloud-bas.
- **043** [Notifications](references/043_notifications.md) — In addition to support for sending email, Laravel provides support for sending notifications across a variety of delivery channels, including email, SMS (via Vonage, formerly known as Nexmo), and Slack. In addition, a variety of [community built notification channels](https://laravel-notification-channels.com/ab.
- **044** [Package Development](references/044_package-development.md) — Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like Carbon or a package that allows you to associate files with Eloquent models like Spatie's Laravel Media Library.
- **045** [Processes](references/045_processes.md) — Laravel provides an expressive, minimal API around the Symfony Process component, allowing you to conveniently invoke external processes from your Laravel application. Laravel's process features are focused on the most common use cases and a wonderful developer experience.
- **046** [Queues](references/046_queues.md) — While building your web application, you may have some tasks, such as parsing and storing an uploaded CSV file, that take too long to perform during a typical web request. Thankfully, Laravel allows you to easily create queued jobs that may be processed in the background. By moving time intensive tasks to a queue, your application can respond to web requests with blazing speed and provide a better.
- **047** [Rate Limiting](references/047_rate-limiting.md) — Laravel includes a simple to use rate limiting abstraction which, in conjunction with your application's cache, provides an easy way to limit any action during a specified window of time.
- **048** [Search](references/048_search.md) — Almost every application needs search. Whether your users are searching a knowledge base for relevant articles, exploring a product catalog, or asking natural-language questions against a corpus of documents, Laravel provides built-in tools to handle each of these scenarios — and you often don't need any external services to get there.
- **049** [Strings](references/049_strings.md) — Laravel includes a variety of functions for manipulating string values. Many of these functions are used by the framework itself; however, you are free to use them in your own applications if you find them convenient.
- **050** [Task Scheduling](references/050_task-scheduling.md) — In the past, you may have written a cron configuration entry for each task you needed to schedule on your server. However, this can quickly become a pain because your task schedule is no longer in source control and you must SSH into your server to view your existing cron entries or add additional entries.

## Security

Authentication, authorization, email verification, encryption, hashing, and password reset — everything needed to secure a Laravel application.

- **051** [Authentication](references/051_authentication.md) — Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily.
- **052** [Authorization](references/052_authorization.md) — In addition to providing built-in authentication services, Laravel also provides a simple way to authorize user actions against a given resource. For example, even though a user is authenticated, they may not be authorized to update or delete certain Eloquent models or database records managed by your application. Laravel's authorization features provide an easy, organ.
- **053** [Email Verification](references/053_email-verification.md) — Many web applications require users to verify their email addresses before using the application. Rather than forcing you to re-implement this feature by hand for each application you create, Laravel provides convenient built-in services for sending and verifying email verification requests.
- **054** [Encryption](references/054_encryption.md) — Laravel's encryption services provide a simple, convenient interface for encrypting and decrypting text via OpenSSL using AES-256 and AES-128 encryption. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value cannot be modified or tampered with once encrypted.
- **055** [Hashing](references/055_hashing.md) — The Laravel `Hash` facade provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the Laravel application starter kits, Bcrypt will be used for registration and authentication by default.
- **056** [Password Reset](references/056_password-reset.md) — Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this by hand for every application you create, Laravel provides convenient services for sending password reset links and secure resetting passwords.

## Database

Database interaction layer: getting started with configuration, the query builder, pagination, migrations, seeding, Redis, and MongoDB integration.

- **057** [Getting Started](references/057_getting-started.md) — Almost every modern web application interacts with a database. Laravel makes interacting with databases extremely simple across a variety of supported databases using raw SQL, a fluent query builder, and the Eloquent ORM. Currently, Laravel provides first-party support for five databases:.
- **058** [Query Builder](references/058_query-builder.md) — Laravel's database query builder provides a convenient, fluent interface to creating and running database queries. It can be used to perform most database operations in your application and works perfectly with all of Laravel's supported database systems.
- **059** [Pagination](references/059_pagination.md) — In other frameworks, pagination can be very painful. We hope Laravel's approach to pagination will be a breath of fresh air. Laravel's paginator is integrated with the query builder and Eloquent ORM and provides convenient, easy-to-use pagination of database records with zero configuration.
- **060** [Migrations](references/060_migrations.md) — Migrations are like version control for your database, allowing your team to define and share the application's database schema definition. If you have ever had to tell a teammate to manually add a column to their local database schema after pulling in your changes from source control, you've faced the problem that database migrations solve.
- **061** [Seeding](references/061_seeding.md) — Laravel includes the ability to seed your database with data using seed classes. All seed classes are stored in the `database/seeders` directory. By default, a `DatabaseSeeder` class is defined for you. From this class, you may use the `call` method to run other seed classes, allowing you to control the seeding order.
- **062** [Redis](references/062_redis.md) — Before using Redis with Laravel, we encourage you to install and use the PhpRedis PHP extension via PECL. The extension is more complex to install compared to "user-land" PHP packages but may yield better performance for applications that make heavy use of Redis. If you are using Laravel Sail, this extension is already installed in your ap.
- **063** [MongoDB](references/063_mongodb.md) — Instead of storing data in tables of rows or columns like SQL databases, each record in a MongoDB database is a document described in BSON, a binary representation of the data. Applications can then retrieve this information in a JSON format. It supports a wide variety of data types, including documents, arrays, embedded documents, and binary data.

## Eloquent ORM

Laravel's active-record ORM: getting started, defining relationships, Eloquent collections, mutators and casting, API resources, serialization, and model factories.

- **064** [Getting Started](references/064_getting-started.md) — Laravel includes Eloquent, an object-relational mapper (ORM) that makes it enjoyable to interact with your database. When using Eloquent, each database table has a corresponding "Model" that is used to interact with that table. In addition to retrieving records from the database table, Eloquent models allow you to insert, update, and delete records from the table as well.
- **065** [Relationships](references/065_relationships.md) — Database tables are often related to one another. For example, a blog post may have many comments or an order could be related to the user who placed it. Eloquent makes managing and working with these relationships easy, and supports a variety of common relationships:.
- **066** [Collections](references/066_collections.md) — All Eloquent methods that return more than one model result will return instances of the `Illuminate\Database\Eloquent\Collection` class, including results retrieved via the `get` method or accessed via a relationship. The Eloquent collection object extends Laravel's base collection, so it naturally inherits dozens of methods used to fluently work with the underlying arra.
- **067** [Mutators / Casts](references/067_mutators-casts.md) — Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the Laravel encrypter to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON st.
- **068** [API Resources](references/068_api-resources.md) — When building an API, you may need a transformation layer that sits between your Eloquent models and the JSON responses that are actually returned to your application's users. For example, you may wish to display certain attributes for a subset of users and not others, or you may wish to always include certain relationships in the JSON representation of your models. Eloquent's resource classes all.
- **069** [Serialization](references/069_serialization.md) — When building APIs using Laravel, you will often need to convert your models and relationships to arrays or JSON. Eloquent includes convenient methods for making these conversions, as well as controlling which attributes are included in the serialized representation of your models.
- **070** [Factories](references/070_factories.md) — When testing your application or seeding your database, you may need to insert a few records into your database. Instead of manually specifying the value of each column, Laravel allows you to define a set of default attributes for each of your Eloquent models using model factories.

## AI

Laravel's AI tooling: the AI SDK for integrating LLM providers, MCP (Model Context Protocol) for agent tooling, and Boost for AI-assisted development workflows.

- **071** [AI SDK](references/071_ai-sdk.md) — The Laravel AI SDK provides a unified, expressive API for interacting with AI providers such as OpenAI, Anthropic, Gemini, and more. With the AI SDK, you can build intelligent agents with tools and structured output, generate images, synthesize and transcribe audio, create vector embeddings, and much more — all using a consistent, Laravel-friendly interface.
- **072** [MCP](references/072_mcp.md) — To get started, install Laravel MCP into your project using the Composer package manager:.
- **073** [Boost](references/073_boost.md) — Laravel Boost accelerates AI-assisted development by providing the essential guidelines and agent skills that help AI agents write high-quality Laravel applications that adhere to Laravel best practices.

## Testing

Testing fundamentals: HTTP tests, console tests, browser tests with Laravel Dusk, database testing helpers, and mocking techniques for isolated unit tests.

- **074** [Getting Started](references/074_getting-started.md) — Laravel is built with testing in mind. In fact, support for testing with Pest and PHPUnit is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications.
- **075** [HTTP Tests](references/075_http-tests.md) — Laravel provides a very fluent API for making HTTP requests to your application and examining the responses. For example, take a look at the feature test defined below:.
- **076** [Console Tests](references/076_console-tests.md) — In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's custom console commands.
- **077** [Browser Tests](references/077_browser-tests.md) — To get started, you should install Google Chrome and add the `laravel/dusk` Composer dependency to your project:.
- **078** [Database](references/078_database.md) — Laravel provides a variety of helpful tools and assertions to make it easier to test your database driven applications. In addition, Laravel model factories and seeders make it painless to create test database records using your application's Eloquent models and relationships. We'll discuss all of these powerful features in the following documentation.
- **079** [Mocking](references/079_mocking.md) — When testing Laravel applications, you may wish to "mock" certain aspects of your application so they are not actually executed during a given test. For example, when testing a controller that dispatches an event, you may wish to mock the event listeners so they are not actually executed during the test. This allows you to only test the controller's HTTP response without worrying about the executi.

## Packages (Official)

First-party Laravel packages: Cashier (Stripe & Paddle), Envoy, Fortify, Folio, Homestead, Horizon, Mix, Octane, Passport, Pennant, Pint, Precognition, Prompts, Pulse, Reverb, Sail, Sanctum, Scout, Socialite, Telescope, and Valet.

- **080** [Cashier (Stripe)](references/080_cashier-(stripe).md) — When upgrading to a new version of Cashier, it's important that you carefully review the upgrade guide.
- **081** [Cashier (Paddle)](references/081_cashier-(paddle).md) — This documentation is for Cashier Paddle 2.x's integration with Paddle Billing. If you're still using Paddle Classic, you should use Cashier Paddle 1.x.
- **082** [Envoy](references/082_envoy.md) — First, install Envoy into your project using the Composer package manager:.
- **083** [Fortify](references/083_fortify.md) — Since Fortify does not provide its own user interface, it is meant to be paired with your own user interface which makes requests to the routes it registers. We will discuss exactly how to make requests to these routes in the remainder of this documentation.
- **084** [Folio](references/084_folio.md) — For example, to create a page that is accessible at the `/greeting` URL, just create a `greeting.blade.php` file in your application's `resources/views/pages` directory:.
- **085** [Homestead](references/085_homestead.md) — Laravel Homestead is a legacy package that is no longer actively maintained. Laravel Sail may be used as a modern alternative.
- **086** [Horizon](references/086_horizon.md) — Before digging into Laravel Horizon, you should familiarize yourself with Laravel's base queue services. Horizon augments Laravel's queue with additional features that may be confusing if you are not already familiar with the basic queue features offered by Laravel.
- **087** [Mix](references/087_mix.md) — Laravel Mix is a legacy package that is no longer actively maintained. Vite may be used as a modern alternative.
- **088** [Octane](references/088_octane.md) — Octane may be installed via the Composer package manager:.
- **089** [Passport](references/089_passport.md) — This documentation assumes you are already familiar with OAuth2. If you do not know anything about OAuth2, consider familiarizing yourself with the general terminology and features of OAuth2 before continuing.
- **090** [Pennant](references/090_pennant.md) — First, install Pennant into your project using the Composer package manager:.
- **091** [Pint](references/091_pint.md) — Pint is automatically installed with all new Laravel applications so you may start using it immediately. By default, Pint does not require any configuration and will fix code style issues in your code by following the opinionated coding style of Laravel.
- **092** [Precognition](references/092_precognition.md) — Laravel Precognition allows you to anticipate the outcome of a future HTTP request. One of the primary use cases of Precognition is the ability to provide "live" validation for your frontend JavaScript application without having to duplicate your application's backend validation rules.
- **093** [Prompts](references/093_prompts.md) — Laravel Prompts is perfect for accepting user input in your Artisan console commands, but it may also be used in any command-line PHP project.
- **094** [Pulse](references/094_pulse.md) — For in-depth debugging of individual events, check out Laravel Telescope.
- **095** [Reverb](references/095_reverb.md) — You may install Reverb using the `install:broadcasting` Artisan command:.
- **096** [Sail](references/096_sail.md) — At its heart, Sail is the `compose.yaml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `compose.yaml` file.
- **097** [Sanctum](references/097_sanctum.md) — Laravel Sanctum exists to solve two separate problems. Let's discuss each before digging deeper into the library.
- **098** [Scout](references/098_scout.md) — Scout ships with a built-in `database` engine that uses MySQL / PostgreSQL full-text indexes and `LIKE` clauses to search your existing database — no external service required. For most applications, this is all you need. For an overview of all search options available in Laravel, consult the search documentation.
- **099** [Socialite](references/099_socialite.md) — In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using Laravel Socialite. Socialite currently supports authentication via Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, and Slack.
- **100** [Telescope](references/100_telescope.md) — You may use the Composer package manager to install Telescope into your Laravel project:.
- **101** [Valet](references/101_valet.md) — Looking for an even easier way to develop Laravel applications on macOS or Windows? Check out Laravel Herd. Herd includes everything you need to get started with Laravel development, including Valet, PHP, and Composer.

---

> **Generated by Laravel 13.x Documentation Crawler**  
> Total pages: 101  
> Source: [laravel.com/docs/13.x](https://laravel.com/docs/13.x)