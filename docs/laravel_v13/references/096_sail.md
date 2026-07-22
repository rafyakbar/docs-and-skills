# Laravel Sail

- [Introduction](#introduction)
- [Installation and Setup](#installation)
  * [Rebuilding Sail Images](#rebuilding-sail-images)
  * [Configuring A Shell Alias](#configuring-a-shell-alias)
- [Starting and Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
  * [Executing PHP Commands](#executing-php-commands)
  * [Executing Composer Commands](#executing-composer-commands)
  * [Executing Artisan Commands](#executing-artisan-commands)
  * [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
  * [MySQL](#mysql)
  * [MongoDB](#mongodb)
  * [Redis](#redis)
  * [Valkey](#valkey)
  * [Meilisearch](#meilisearch)
  * [Typesense](#typesense)
- [File Storage](#file-storage)
- [Running Tests](#running-tests)
  * [Laravel Dusk](#laravel-dusk)
- [Previewing Emails](#previewing-emails)
- [Container CLI](#sail-container-cli)
- [PHP Versions](#sail-php-versions)
  * [Additional PHP Extensions](#sail-php-extensions)
- [Node Versions](#sail-node-versions)
- [Sharing Your Site](#sharing-your-site)
- [Debugging With Xdebug](#debugging-with-xdebug)
  * [Xdebug CLI Usage](#xdebug-cli-usage)
  * [Xdebug Browser Usage](#xdebug-browser-usage)
- [Customization](#sail-customization)

## [Introduction](#introduction)

[Laravel Sail](https://github.com/laravel/sail) is a light-weight command-line interface for interacting with Laravel's default Docker development environment. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

At its heart, Sail is the `compose.yaml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `compose.yaml` file.

Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)).

## [Installation and Setup](#installation)

You may install Sail using the Composer package manager:

```
1composer require laravel/sail --dev
```

After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `compose.yaml` file to the root of your application and modify your `.env` file with the required environment variables in order to connect to the Docker services:

```
1php artisan sail:install
```

Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation:

```
1./vendor/bin/sail up
```

If you are using Docker Desktop for Linux, you should use the `default` Docker context by executing the following command: `docker context use default`. In addition, if you encounter file permission errors within containers, you may need to set the `SUPERVISOR_PHP_USER` environment variable to `root`.

#### [Adding Additional Services](#adding-additional-services)

If you would like to add an additional service to your existing Sail installation, you may run the `sail:add` Artisan command:

```
1php artisan sail:add
```

#### [Using Devcontainers](#using-devcontainers)

If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application:

```
1php artisan sail:install --devcontainer
```

### [Rebuilding Sail Images](#rebuilding-sail-images)

Sometimes you may want to completely rebuild your Sail images to ensure all of the image's packages and software are up to date. You may accomplish this using the `build` command:

```
1docker compose down -v

2 

3sail build --no-cache

4 

5sail up
```

### [Configuring A Shell Alias](#configuring-a-shell-alias)

By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications:

```
1./vendor/bin/sail up
```

However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a shell alias that allows you to execute Sail's commands more easily:

```
1alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

To make sure this is always available, you may add this to your shell configuration file in your home directory, such as `~/.zshrc` or `~/.bashrc`, and then restart your shell.

Once the shell alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias:

```
1sail up
```

## [Starting and Stopping Sail](#starting-and-stopping-sail)

Laravel Sail's `compose.yaml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `compose.yaml` file. The `laravel.test` container is the primary application container that will be serving your application.

Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `compose.yaml` file, you should execute the `up` command:

```
1sail up
```

To start all of the Docker containers in the background, you may start Sail in "detached" mode:

```
1sail up -d
```

Once the application's containers have been started, you may access the project in your web browser at: <http://localhost>.

To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command:

```
1sail stop
```

## [Executing Commands](#executing-sail-commands)

When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands.

**When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail:

```
1# Running Artisan commands locally...

2php artisan queue:work

3 

4# Running Artisan commands within Laravel Sail...

5sail artisan queue:work
```

### [Executing PHP Commands](#executing-php-commands)

PHP commands may be executed using the `php` command. Of course, these commands will execute using the PHP version that is configured for your application. To learn more about the PHP versions available to Laravel Sail, consult the [PHP version documentation](#sail-php-versions):

```
1sail php --version

2 

3sail php script.php
```

### [Executing Composer Commands](#executing-composer-commands)

Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer installation:

```
1sail composer require laravel/sanctum
```

### [Executing Artisan Commands](#executing-artisan-commands)

Laravel Artisan commands may be executed using the `artisan` command:

```
1sail artisan queue:work
```

### [Executing Node / NPM Commands](#executing-node-npm-commands)

Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command:

```
1sail node --version

2 

3sail npm run dev
```

If you wish, you may use Yarn instead of NPM:

```
1sail yarn
```

## [Interacting With Databases](#interacting-with-sail-databases)

### [MySQL](#mysql)

As you may have noticed, your application's `compose.yaml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers.

In addition, the first time the MySQL container starts, it will create two databases for you. The first database is named using the value of your `DB_DATABASE` environment variable and is for your local development. The second is a dedicated testing database named `testing` and will ensure that your tests do not interfere with your development data.

Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`.

To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306 and the access credentials correspond to the values of your `DB_USERNAME` and `DB_PASSWORD` environment variables. Or, you may connect as the `root` user, which also utilizes the value of your `DB_PASSWORD` environment variable as its password.

### [MongoDB](#mongodb)

If you chose to install the [MongoDB](https://www.mongodb.com/) service when installing Sail, your application's `compose.yaml` file contains an entry for a [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) container which provides the MongoDB document database with Atlas features like [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers.

Once you have started your containers, you may connect to the MongoDB instance within your application by setting your `MONGODB_URI` environment variable within your application's `.env` file to `mongodb://mongodb:27017`. Authentication is disabled by default, but you can set the `MONGODB_USERNAME` and `MONGODB_PASSWORD` environment variables to enable authentication before starting the `mongodb` container. Then, add the credentials to the connection string:

```
1MONGODB_USERNAME=user

2MONGODB_PASSWORD=laravel

3MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

For seamless integration of MongoDB with your application, you can install the [official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/).

To connect to your application's MongoDB database from your local machine, you may use a graphical interface such as [Compass](https://www.mongodb.com/products/tools/compass). By default, the MongoDB database is accessible at `localhost` port `27017`.

### [Redis](#redis)

Your application's `compose.yaml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis instance is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`.

To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379.

### [Valkey](#valkey)

If you choose to install Valkey service when installing Sail, your application's `compose.yaml` file will contain an entry for [Valkey](https://valkey.io/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Valkey instance is persisted even when stopping and restarting your containers. You can connect to this container in your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `valkey`.

To connect to your application's Valkey database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Valkey database is accessible at `localhost` port 6379.

### [Meilisearch](#meilisearch)

If you chose to install the [Meilisearch](https://www.meilisearch.com) service when installing Sail, your application's `compose.yaml` file will contain an entry for this powerful search engine that is integrated with [Laravel Scout](/docs/13.x/scout). Once you have started your containers, you may connect to the Meilisearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`.

From your local machine, you may access Meilisearch's web based administration panel by navigating to `http://localhost:7700` in your web browser.

### [Typesense](#typesense)

If you chose to install the [Typesense](https://typesense.org) service when installing Sail, your application's `compose.yaml` file will contain an entry for this lightning fast, open-source search engine that is natively integrated with [Laravel Scout](/docs/13.x/scout#typesense). Once you have started your containers, you may connect to the Typesense instance within your application by setting the following environment variables:

```
1TYPESENSE_HOST=typesense

2TYPESENSE_PORT=8108

3TYPESENSE_PROTOCOL=http

4TYPESENSE_API_KEY=xyz
```

From your local machine, you may access Typesense's API via `http://localhost:8108`.

## [File Storage](#file-storage)

If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [RustFS](https://rustfs.com) service when installing Sail. RustFS provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install RustFS while installing Sail, a RustFS configuration section will be added to your application's `compose.yaml` file.

By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as RustFS by simply modifying the associated environment variables that control its configuration. For example, when using RustFS, your filesystem environment variable configuration should be defined as follows:

```
1FILESYSTEM_DISK=s3

2AWS_ACCESS_KEY_ID=sail

3AWS_SECRET_ACCESS_KEY=password

4AWS_DEFAULT_REGION=us-east-1

5AWS_BUCKET=local

6AWS_ENDPOINT=http://rustfs:9000

7AWS_USE_PATH_STYLE_ENDPOINT=true
```

## [Running Tests](#running-tests)

Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/13.x/testing). Any CLI options that are accepted by Pest / PHPUnit may also be passed to the `test` command:

```
1sail test

2 

3sail test --group orders
```

The Sail `test` command is equivalent to running the `test` Artisan command:

```
1sail artisan test
```

By default, Sail will create a dedicated `testing` database so that your tests do not interfere with the current state of your database. In a default Laravel installation, Sail will also configure your `phpunit.xml` file to use this database when executing your tests:

```
1<env name="DB_DATABASE" value="testing"/>
```

### [Laravel Dusk](#laravel-dusk)

[Laravel Dusk](/docs/13.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `compose.yaml` file:

```
1selenium:

2    image: 'selenium/standalone-chrome'

3    extra_hosts:

4      - 'host.docker.internal:host-gateway'

5    volumes:

6        - '/dev/shm:/dev/shm'

7    networks:

8        - sail
```

Next, ensure that the `laravel.test` service in your application's `compose.yaml` file has a `depends_on` entry for `selenium`:

```
1depends_on:

2    - mysql

3    - redis

4    - selenium
```

Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command:

```
1sail dusk
```

#### [Selenium on Apple Silicon](#selenium-on-apple-silicon)

If your local machine contains an Apple Silicon chip, your `selenium` service must use the `selenium/standalone-chromium` image:

```
1selenium:

2    image: 'selenium/standalone-chromium'

3    extra_hosts:

4        - 'host.docker.internal:host-gateway'

5    volumes:

6        - '/dev/shm:/dev/shm'

7    networks:

8        - sail
```

## [Previewing Emails](#previewing-emails)

Laravel Sail's default `compose.yaml` file contains a service entry for [Mailpit](https://github.com/axllent/mailpit). Mailpit intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, Mailpit's default host is `mailpit` and is available via port 1025:

```
1MAIL_HOST=mailpit

2MAIL_PORT=1025

3MAIL_ENCRYPTION=null
```

When Sail is running, you may access the Mailpit web interface at: <http://localhost:8025>

## [Container CLI](#sail-container-cli)

Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well as execute arbitrary shell commands within the container:

```
1sail shell

2 

3sail root-shell
```

To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command:

```
1sail tinker
```

## [PHP Versions](#sail-php-versions)

Sail currently supports serving your application via PHP 8.5, 8.4, 8.3, 8.2, 8.1, or PHP 8.0. The default PHP version used by Sail is currently PHP 8.5. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `compose.yaml` file:

```
 1# PHP 8.5

 2context: ./vendor/laravel/sail/runtimes/8.5

 3 

 4# PHP 8.4

 5context: ./vendor/laravel/sail/runtimes/8.4

 6 

 7# PHP 8.3

 8context: ./vendor/laravel/sail/runtimes/8.3

 9 

10# PHP 8.2

11context: ./vendor/laravel/sail/runtimes/8.2

12 

13# PHP 8.1

14context: ./vendor/laravel/sail/runtimes/8.1

15 

16# PHP 8.0

17context: ./vendor/laravel/sail/runtimes/8.0
```

In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `compose.yaml` file:

```
1image: sail-8.2/app
```

After updating your application's `compose.yaml` file, you should rebuild your container images:

```
1sail build --no-cache

2 

3sail up
```

### [Additional PHP Extensions](#sail-php-extensions)

Sail's runtime images include a common set of PHP extensions. If your application requires additional extensions, you may install them when building the image by adding a space-separated `PHP_EXTENSIONS` build argument to the `laravel.test` service in your application's `compose.yaml` file:

```
1build:

2    args:

3        WWWGROUP: '${WWWGROUP}'

4        PHP_EXTENSIONS: 'gmp imagick'
```

After updating your application's `compose.yaml` file, you should rebuild your container images.

## [Node Versions](#sail-node-versions)

Sail installs Node 24 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `compose.yaml` file:

```
1build:

2    args:

3        WWWGROUP: '${WWWGROUP}'

4        NODE_VERSION: '18'
```

After updating your application's `compose.yaml` file, you should rebuild your container images:

```
1sail build --no-cache

2 

3sail up
```

## [Sharing Your Site](#sharing-your-site)

Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application:

```
1sail share
```

When sharing your site via the `share` command, you should configure your application's trusted proxies using the `trustProxies` middleware method in your application's `bootstrap/app.php` file. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation:

```
1->withMiddleware(function (Middleware $middleware): void {

2    $middleware->trustProxies(at: '*');

3})
```

If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command:

```
1sail share --subdomain=my-sail-site
```

The `share` command is powered by [Expose](https://github.com/beyondcode/expose), an open source tunneling service by [BeyondCode](https://beyondco.de).

## [Debugging With Xdebug](#debugging-with-xdebug)

Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. To enable Xdebug, ensure you have [published your Sail configuration](#sail-customization). Then, add the following variables to your application's `.env` file to configure Xdebug:

```
1SAIL_XDEBUG_MODE=develop,debug,coverage
```

Next, ensure that your published `php.ini` file includes the following configuration so that Xdebug is activated in the specified modes:

```
1[xdebug]

2xdebug.mode=${XDEBUG_MODE}
```

After modifying the `php.ini` file, remember to rebuild your Docker images so that your changes to the `php.ini` file take effect:

```
1sail build --no-cache
```

#### Linux Host IP Configuration

Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux and you're using Docker 20.10+, `host.docker.internal` is available, and no manual configuration is required.

For Docker versions older than 20.10, `host.docker.internal` is not supported on Linux, and you will need to manually define the host IP. To do this, configure a static IP for your container by defining a custom network in your `compose.yaml` file:

```
 1networks:

 2  custom_network:

 3    ipam:

 4      config:

 5        - subnet: 172.20.0.0/16

 6 

 7services:

 8  laravel.test:

 9    networks:

10      custom_network:

11        ipv4_address: 172.20.0.2
```

Once you have set the static IP, define the SAIL_XDEBUG_CONFIG variable within your application's .env file:

```
1SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

### [Xdebug CLI Usage](#xdebug-cli-usage)

A `sail debug` command may be used to start a debugging session when running an Artisan command:

```
1# Run an Artisan command without Xdebug...

2sail artisan migrate

3 

4# Run an Artisan command with Xdebug...

5sail debug migrate
```

### [Xdebug Browser Usage](#xdebug-browser-usage)

To debug your application while interacting with the application via a web browser, follow the [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application) for initiating an Xdebug session from the web browser.

If you're using PhpStorm, please review JetBrains' documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html).

Laravel Sail relies on `artisan serve` to serve your application. The `artisan serve` command only accepts the `XDEBUG_CONFIG` and `XDEBUG_MODE` variables as of Laravel version 8.53.0. Older versions of Laravel (8.52.0 and below) do not support these variables and will not accept debug connections.

## [Customization](#sail-customization)

Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command:

```
1sail artisan sail:publish
```

After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `compose.yaml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine:

```
1sail build --no-cache
```
