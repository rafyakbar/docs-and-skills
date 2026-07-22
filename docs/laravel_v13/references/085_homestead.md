# Laravel Homestead

- [Introduction](#introduction)
- [Installation and Setup](#installation-and-setup)
  * [First Steps](#first-steps)
  * [Configuring Homestead](#configuring-homestead)
  * [Configuring Nginx Sites](#configuring-nginx-sites)
  * [Configuring Services](#configuring-services)
  * [Launching the Vagrant Box](#launching-the-vagrant-box)
  * [Per Project Installation](#per-project-installation)
  * [Installing Optional Features](#installing-optional-features)
  * [Aliases](#aliases)
- [Updating Homestead](#updating-homestead)
- [Daily Usage](#daily-usage)
  * [Connecting via SSH](#connecting-via-ssh)
  * [Adding Additional Sites](#adding-additional-sites)
  * [Environment Variables](#environment-variables)
  * [Ports](#ports)
  * [PHP Versions](#php-versions)
  * [Connecting to Databases](#connecting-to-databases)
  * [Database Backups](#database-backups)
  * [Configuring Cron Schedules](#configuring-cron-schedules)
  * [Configuring Mailpit](#configuring-mailpit)
  * [Configuring Minio](#configuring-minio)
  * [Laravel Dusk](#laravel-dusk)
  * [Sharing Your Environment](#sharing-your-environment)
- [Debugging and Profiling](#debugging-and-profiling)
  * [Debugging Web Requests With Xdebug](#debugging-web-requests)
  * [Debugging CLI Applications](#debugging-cli-applications)
  * [Profiling Applications With Blackfire](#profiling-applications-with-blackfire)
- [Network Interfaces](#network-interfaces)
- [Extending Homestead](#extending-homestead)
- [Provider Specific Settings](#provider-specific-settings)
  * [VirtualBox](#provider-specific-virtualbox)

## [Introduction](#introduction)

Laravel Homestead is a legacy package that is no longer actively maintained. [Laravel Sail](/docs/13.x/sail) may be used as a modern alternative.

Laravel strives to make the entire PHP development experience delightful, including your local development environment. [Laravel Homestead](https://github.com/laravel/homestead) is an official, pre-packaged Vagrant box that provides you a wonderful development environment without requiring you to install PHP, a web server, or any other server software on your local machine.

[Vagrant](https://www.vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines. Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes!

Homestead runs on any Windows, macOS, or Linux system and includes Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, and all of the other software you need to develop amazing Laravel applications.

If you are using Windows, you may need to enable hardware virtualization (VT-x). It can usually be enabled via your BIOS. If you are using Hyper-V on a UEFI system you may additionally need to disable Hyper-V in order to access VT-x.

### [Included Software](#included-software)

- Ubuntu 22.04
- Git
- PHP 8.3
- PHP 8.2
- PHP 8.1
- PHP 8.0
- PHP 7.4
- PHP 7.3
- PHP 7.2
- PHP 7.1
- PHP 7.0
- PHP 5.6
- Nginx
- MySQL 8.0
- lmm
- Sqlite3
- PostgreSQL 15
- Composer
- Docker
- Node (With Yarn, Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- Mailpit
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli

### [Optional Software](#optional-software)

- Apache
- Blackfire
- Cassandra
- Chronograf
- CouchDB
- Crystal & Lucky Framework
- Elasticsearch
- EventStoreDB
- Flyway
- Gearman
- Go
- Grafana
- InfluxDB
- Logstash
- MariaDB
- Meilisearch
- MinIO
- MongoDB
- Neo4j
- Oh My Zsh
- Open Resty
- PM2
- Python
- R
- RabbitMQ
- Rust
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader (PHP extension)
- Webdriver & Laravel Dusk Utilities

## [Installation and Setup](#installation-and-setup)

### [First Steps](#first-steps)

Before launching your Homestead environment, you must install [Vagrant](https://developer.hashicorp.com/vagrant/downloads) as well as one of the following supported providers:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

All of these software packages provide easy-to-use visual installers for all popular operating systems.

To use the Parallels provider, you will need to install [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels). It is free of charge.

#### [Installing Homestead](#installing-homestead)

You may install Homestead by cloning the Homestead repository onto your host machine. Consider cloning the repository into a `Homestead` folder within your "home" directory, as the Homestead virtual machine will serve as the host to all of your Laravel applications. Throughout this documentation, we will refer to this directory as your "Homestead directory":

```
1git clone https://github.com/laravel/homestead.git ~/Homestead
```

After cloning the Laravel Homestead repository, you should checkout the `release` branch. This branch always contains the latest stable release of Homestead:

```
1cd ~/Homestead

2 

3git checkout release
```

Next, execute the `bash init.sh` command from the Homestead directory to create the `Homestead.yaml` configuration file. The `Homestead.yaml` file is where you will configure all of the settings for your Homestead installation. This file will be placed in the Homestead directory:

```
1# macOS / Linux...

2bash init.sh

3 

4# Windows...

5init.bat
```

### [Configuring Homestead](#configuring-homestead)

#### [Setting Your Provider](#setting-your-provider)

The `provider` key in your `Homestead.yaml` file indicates which Vagrant provider should be used: `virtualbox` or `parallels`:

```
1provider: virtualbox
```

If you are using Apple Silicon the Parallels provider is required.

#### [Configuring Shared Folders](#configuring-shared-folders)

The `folders` property of the `Homestead.yaml` file lists all of the folders you wish to share with your Homestead environment. As files within these folders are changed, they will be kept in sync between your local machine and the Homestead virtual environment. You may configure as many shared folders as necessary:

```
1folders:

2    - map: ~/code/project1

3      to: /home/vagrant/project1
```

Windows users should not use the `~/` path syntax and instead should use the full path to their project, such as `C:\Users\user\Code\project1`.

You should always map individual applications to their own folder mapping instead of mapping a single large directory that contains all of your applications. When you map a folder, the virtual machine must keep track of all disk IO for *every* file in the folder. You may experience reduced performance if you have a large number of files in a folder:

```
1folders:

2    - map: ~/code/project1

3      to: /home/vagrant/project1

4    - map: ~/code/project2

5      to: /home/vagrant/project2
```

You should never mount `.` (the current directory) when using Homestead. This causes Vagrant to not map the current folder to `/vagrant` and will break optional features and cause unexpected results while provisioning.

To enable [NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs), you may add a `type` option to your folder mapping:

```
1folders:

2    - map: ~/code/project1

3      to: /home/vagrant/project1

4      type: "nfs"
```

When using NFS on Windows, you should consider installing the [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) plug-in. This plug-in will maintain the correct user / group permissions for files and directories within the Homestead virtual machine.

You may also pass any options supported by Vagrant's [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) by listing them under the `options` key:

```
1folders:

2    - map: ~/code/project1

3      to: /home/vagrant/project1

4      type: "rsync"

5      options:

6          rsync__args: ["--verbose", "--archive", "--delete", "-zz"]

7          rsync__exclude: ["node_modules"]
```

### [Configuring Nginx Sites](#configuring-nginx-sites)

Not familiar with Nginx? No problem. Your `Homestead.yaml` file's `sites` property allows you to easily map a "domain" to a folder on your Homestead environment. A sample site configuration is included in the `Homestead.yaml` file. Again, you may add as many sites to your Homestead environment as necessary. Homestead can serve as a convenient, virtualized environment for every Laravel application you are working on:

```
1sites:

2    - map: homestead.test

3      to: /home/vagrant/project1/public
```

If you change the `sites` property after provisioning the Homestead virtual machine, you should execute the `vagrant reload --provision` command in your terminal to update the Nginx configuration on the virtual machine.

Homestead scripts are built to be as idempotent as possible. However, if you are experiencing issues while provisioning you should destroy and rebuild the machine by executing the `vagrant destroy && vagrant up` command.

#### [Hostname Resolution](#hostname-resolution)

Homestead publishes hostnames using `mDNS` for automatic host resolution. If you set `hostname: homestead` in your `Homestead.yaml` file, the host will be available at `homestead.local`. macOS, iOS, and Linux desktop distributions include `mDNS` support by default. If you are using Windows, you must install [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US).

Using automatic hostnames works best for [per project installations](#per-project-installation) of Homestead. If you host multiple sites on a single Homestead instance, you may add the "domains" for your web sites to the `hosts` file on your machine. The `hosts` file will redirect requests for your Homestead sites into your Homestead virtual machine. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following:

```
1192.168.56.56  homestead.test
```

Make sure the IP address listed is the one set in your `Homestead.yaml` file. Once you have added the domain to your `hosts` file and launched the Vagrant box you will be able to access the site via your web browser:

```
1http://homestead.test
```

### [Configuring Services](#configuring-services)

Homestead starts several services by default; however, you may customize which services are enabled or disabled during provisioning. For example, you may enable PostgreSQL and disable MySQL by modifying the `services` option within your `Homestead.yaml` file:

```
1services:

2    - enabled:

3        - "postgresql"

4    - disabled:

5        - "mysql"
```

The specified services will be started or stopped based on their order in the `enabled` and `disabled` directives.

### [Launching the Vagrant Box](#launching-the-vagrant-box)

Once you have edited the `Homestead.yaml` to your liking, run the `vagrant up` command from your Homestead directory. Vagrant will boot the virtual machine and automatically configure your shared folders and Nginx sites.

To destroy the machine, you may use the `vagrant destroy` command.

### [Per Project Installation](#per-project-installation)

Instead of installing Homestead globally and sharing the same Homestead virtual machine across all of your projects, you may instead configure a Homestead instance for each project you manage. Installing Homestead per project may be beneficial if you wish to ship a `Vagrantfile` with your project, allowing others working on the project to `vagrant up` immediately after cloning the project's repository.

You may install Homestead into your project using the Composer package manager:

```
1composer require laravel/homestead --dev
```

Once Homestead has been installed, invoke Homestead's `make` command to generate the `Vagrantfile` and `Homestead.yaml` file for your project. These files will be placed in the root of your project. The `make` command will automatically configure the `sites` and `folders` directives in the `Homestead.yaml` file:

```
1# macOS / Linux...

2php vendor/bin/homestead make

3 

4# Windows...

5vendor\\bin\\homestead make
```

Next, run the `vagrant up` command in your terminal and access your project at `http://homestead.test` in your browser. Remember, you will still need to add an `/etc/hosts` file entry for `homestead.test` or the domain of your choice if you are not using automatic [hostname resolution](#hostname-resolution).

### [Installing Optional Features](#installing-optional-features)

Optional software is installed using the `features` option within your `Homestead.yaml` file. Most features can be enabled or disabled with a boolean value, while some features allow multiple configuration options:

```
 1features:

 2    - blackfire:

 3        server_id: "server_id"

 4        server_token: "server_value"

 5        client_id: "client_id"

 6        client_token: "client_value"

 7    - cassandra: true

 8    - chronograf: true

 9    - couchdb: true

10    - crystal: true

11    - dragonflydb: true

12    - elasticsearch:

13        version: 7.9.0

14    - eventstore: true

15        version: 21.2.0

16    - flyway: true

17    - gearman: true

18    - golang: true

19    - grafana: true

20    - influxdb: true

21    - logstash: true

22    - mariadb: true

23    - meilisearch: true

24    - minio: true

25    - mongodb: true

26    - neo4j: true

27    - ohmyzsh: true

28    - openresty: true

29    - pm2: true

30    - python: true

31    - r-base: true

32    - rabbitmq: true

33    - rustc: true

34    - rvm: true

35    - solr: true

36    - timescaledb: true

37    - trader: true

38    - webdriver: true
```

#### [Elasticsearch](#elasticsearch)

You may specify a supported version of Elasticsearch, which must be an exact version number (major.minor.patch). The default installation will create a cluster named 'homestead'. You should never give Elasticsearch more than half of the operating system's memory, so make sure your Homestead virtual machine has at least twice the Elasticsearch allocation.

Check out the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current) to learn how to customize your configuration.

#### [MariaDB](#mariadb)

Enabling MariaDB will remove MySQL and install MariaDB. MariaDB typically serves as a drop-in replacement for MySQL, so you should still use the `mysql` database driver in your application's database configuration.

#### [MongoDB](#mongodb)

The default MongoDB installation will set the database username to `homestead` and the corresponding password to `secret`.

#### [Neo4j](#neo4j)

The default Neo4j installation will set the database username to `homestead` and the corresponding password to `secret`. To access the Neo4j browser, visit `http://homestead.test:7474` via your web browser. The ports `7687` (Bolt), `7474` (HTTP), and `7473` (HTTPS) are ready to serve requests from the Neo4j client.

### [Aliases](#aliases)

You may add Bash aliases to your Homestead virtual machine by modifying the `aliases` file within your Homestead directory:

```
1alias c='clear'

2alias ..='cd ..'
```

After you have updated the `aliases` file, you should re-provision the Homestead virtual machine using the `vagrant reload --provision` command. This will ensure that your new aliases are available on the machine.

## [Updating Homestead](#updating-homestead)

Before you begin updating Homestead you should ensure you have removed your current virtual machine by running the following command in your Homestead directory:

```
1vagrant destroy
```

Next, you need to update the Homestead source code. If you cloned the repository, you can execute the following commands at the location you originally cloned the repository:

```
1git fetch

2 

3git pull origin release
```

These commands pull the latest Homestead code from the GitHub repository, fetch the latest tags, and then check out the latest tagged release. You can find the latest stable release version on Homestead's [GitHub releases page](https://github.com/laravel/homestead/releases).

If you have installed Homestead via your project's `composer.json` file, you should ensure your `composer.json` file contains `"laravel/homestead": "^12"` and update your dependencies:

```
1composer update
```

Next, you should update the Vagrant box using the `vagrant box update` command:

```
1vagrant box update
```

After updating the Vagrant box, you should run the `bash init.sh` command from the Homestead directory in order to update Homestead's additional configuration files. You will be asked whether you wish to overwrite your existing `Homestead.yaml`, `after.sh`, and `aliases` files:

```
1# macOS / Linux...

2bash init.sh

3 

4# Windows...

5init.bat
```

Finally, you will need to regenerate your Homestead virtual machine to utilize the latest Vagrant installation:

```
1vagrant up
```

## [Daily Usage](#daily-usage)

### [Connecting via SSH](#connecting-via-ssh)

You can SSH into your virtual machine by executing the `vagrant ssh` terminal command from your Homestead directory.

### [Adding Additional Sites](#adding-additional-sites)

Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your other Laravel projects. You can run as many Laravel projects as you wish on a single Homestead environment. To add an additional site, add the site to your `Homestead.yaml` file.

```
1sites:

2    - map: homestead.test

3      to: /home/vagrant/project1/public

4    - map: another.test

5      to: /home/vagrant/project2/public
```

You should ensure that you have configured a [folder mapping](#configuring-shared-folders) for the project's directory before adding the site.

If Vagrant is not automatically managing your "hosts" file, you may need to add the new site to that file as well. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`:

```
1192.168.56.56  homestead.test

2192.168.56.56  another.test
```

Once the site has been added, execute the `vagrant reload --provision` terminal command from your Homestead directory.

#### [Site Types](#site-types)

Homestead supports several "types" of sites which allow you to easily run projects that are not based on Laravel. For example, we may easily add a Statamic application to Homestead using the `statamic` site type:

```
1sites:

2    - map: statamic.test

3      to: /home/vagrant/my-symfony-project/web

4      type: "statamic"
```

The available site types are: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (the default), `proxy` (for nginx), `silverstripe`, `statamic`, `symfony2`, `symfony4`, and `zf`.

#### [Site Parameters](#site-parameters)

You may add additional Nginx `fastcgi_param` values to your site via the `params` site directive:

```
1sites:

2    - map: homestead.test

3      to: /home/vagrant/project1/public

4      params:

5          - key: FOO

6            value: BAR
```

### [Environment Variables](#environment-variables)

You can define global environment variables by adding them to your `Homestead.yaml` file:

```
1variables:

2    - key: APP_ENV

3      value: local

4    - key: FOO

5      value: bar
```

After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command. This will update the PHP-FPM configuration for all of the installed PHP versions and also update the environment for the `vagrant` user.

### [Ports](#ports)

By default, the following ports are forwarded to your Homestead environment:

- **HTTP:** 8000 → Forwards To 80
- **HTTPS:** 44300 → Forwards To 443

#### [Forwarding Additional Ports](#forwarding-additional-ports)

If you wish, you may forward additional ports to the Vagrant box by defining a `ports` configuration entry within your `Homestead.yaml` file. After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command:

```
1ports:

2    - send: 50000

3      to: 5000

4    - send: 7777

5      to: 777

6      protocol: udp
```

Below is a list of additional Homestead service ports that you may wish to map from your host machine to your Vagrant box:

- **SSH:** 2222 → To 22
- **ngrok UI:** 4040 → To 4040
- **MySQL:** 33060 → To 3306
- **PostgreSQL:** 54320 → To 5432
- **MongoDB:** 27017 → To 27017
- **Mailpit:** 8025 → To 8025
- **Minio:** 9600 → To 9600

### [PHP Versions](#php-versions)

Homestead supports running multiple versions of PHP on the same virtual machine. You may specify which version of PHP to use for a given site within your `Homestead.yaml` file. The available PHP versions are: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", and "8.3", (the default):

```
1sites:

2    - map: homestead.test

3      to: /home/vagrant/project1/public

4      php: "7.1"
```

[Within your Homestead virtual machine](#connecting-via-ssh), you may use any of the supported PHP versions via the CLI:

```
 1php5.6 artisan list

 2php7.0 artisan list

 3php7.1 artisan list

 4php7.2 artisan list

 5php7.3 artisan list

 6php7.4 artisan list

 7php8.0 artisan list

 8php8.1 artisan list

 9php8.2 artisan list

10php8.3 artisan list
```

You may change the default version of PHP used by the CLI by issuing the following commands from within your Homestead virtual machine:

```
 1php56

 2php70

 3php71

 4php72

 5php73

 6php74

 7php80

 8php81

 9php82

10php83
```

### [Connecting to Databases](#connecting-to-databases)

A `homestead` database is configured for both MySQL and PostgreSQL out of the box. To connect to your MySQL or PostgreSQL database from your host machine's database client, you should connect to `127.0.0.1` on port `33060` (MySQL) or `54320` (PostgreSQL). The username and password for both databases is `homestead` / `secret`.

You should only use these non-standard ports when connecting to the databases from your host machine. You will use the default 3306 and 5432 ports in your Laravel application's `database` configuration file since Laravel is running *within* the virtual machine.

### [Database Backups](#database-backups)

Homestead can automatically backup your database when your Homestead virtual machine is destroyed. To utilize this feature, you must be using Vagrant 2.1.0 or greater. Or, if you are using an older version of Vagrant, you must install the `vagrant-triggers` plug-in. To enable automatic database backups, add the following line to your `Homestead.yaml` file:

```
1backup: true
```

Once configured, Homestead will export your databases to `.backup/mysql_backup` and `.backup/postgres_backup` directories when the `vagrant destroy` command is executed. These directories can be found in the folder where you installed Homestead or in the root of your project if you are using the [per project installation](#per-project-installation) method.

### [Configuring Cron Schedules](#configuring-cron-schedules)

Laravel provides a convenient way to [schedule cron jobs](/docs/13.x/scheduling) by scheduling a single `schedule:run` Artisan command to run every minute. The `schedule:run` command will examine the job schedule defined in your `routes/console.php` file to determine which scheduled tasks to run.

If you would like the `schedule:run` command to be run for a Homestead site, you may set the `schedule` option to `true` when defining the site:

```
1sites:

2    - map: homestead.test

3      to: /home/vagrant/project1/public

4      schedule: true
```

The cron job for the site will be defined in the `/etc/cron.d` directory of the Homestead virtual machine.

### [Configuring Mailpit](#configuring-mailpit)

[Mailpit](https://github.com/axllent/mailpit) allows you to intercept your outgoing email and examine it without actually sending the mail to its recipients. To get started, update your application's `.env` file to use the following mail settings:

```
1MAIL_MAILER=smtp

2MAIL_HOST=localhost

3MAIL_PORT=1025

4MAIL_USERNAME=null

5MAIL_PASSWORD=null

6MAIL_ENCRYPTION=null
```

Once Mailpit has been configured, you may access the Mailpit dashboard at `http://localhost:8025`.

### [Configuring Minio](#configuring-minio)

[Minio](https://github.com/minio/minio) is an open source object storage server with an Amazon S3 compatible API. To install Minio, update your `Homestead.yaml` file with the following configuration option in the [features](#installing-optional-features) section:

```
1minio: true
```

By default, Minio is available on port 9600. You may access the Minio control panel by visiting `http://localhost:9600`. The default access key is `homestead`, while the default secret key is `secretkey`. When accessing Minio, you should always use region `us-east-1`.

In order to use Minio, ensure your `.env` file has the following options:

```
1AWS_USE_PATH_STYLE_ENDPOINT=true

2AWS_ENDPOINT=http://localhost:9600

3AWS_ACCESS_KEY_ID=homestead

4AWS_SECRET_ACCESS_KEY=secretkey

5AWS_DEFAULT_REGION=us-east-1
```

To provision Minio powered "S3" buckets, add a `buckets` directive to your `Homestead.yaml` file. After defining your buckets, you should execute the `vagrant reload --provision` command in your terminal:

```
1buckets:

2    - name: your-bucket

3      policy: public

4    - name: your-private-bucket

5      policy: none
```

Supported `policy` values include: `none`, `download`, `upload`, and `public`.

### [Laravel Dusk](#laravel-dusk)

In order to run [Laravel Dusk](/docs/13.x/dusk) tests within Homestead, you should enable the [webdriver feature](#installing-optional-features) in your Homestead configuration:

```
1features:

2    - webdriver: true
```

After enabling the `webdriver` feature, you should execute the `vagrant reload --provision` command in your terminal.

### [Sharing Your Environment](#sharing-your-environment)

Sometimes you may wish to share what you're currently working on with coworkers or a client. Vagrant has built-in support for this via the `vagrant share` command; however, this will not work if you have multiple sites configured in your `Homestead.yaml` file.

To solve this problem, Homestead includes its own `share` command. To get started, [SSH into your Homestead virtual machine](#connecting-via-ssh) via `vagrant ssh` and execute the `share homestead.test` command. This command will share the `homestead.test` site from your `Homestead.yaml` configuration file. You may substitute any of your other configured sites for `homestead.test`:

```
1share homestead.test
```

After running the command, you will see an Ngrok screen appear which contains the activity log and the publicly accessible URLs for the shared site. If you would like to specify a custom region, subdomain, or other Ngrok runtime option, you may add them to your `share` command:

```
1share homestead.test -region=eu -subdomain=laravel
```

If you need to share content over HTTPS rather than HTTP, using the `sshare` command instead of `share` will enable you to do so.

Remember, Vagrant is inherently insecure and you are exposing your virtual machine to the Internet when running the `share` command.

## [Debugging and Profiling](#debugging-and-profiling)

### [Debugging Web Requests With Xdebug](#debugging-web-requests)

Homestead includes support for step debugging using [Xdebug](https://xdebug.org). For example, you can access a page in your browser and PHP will connect to your IDE to allow inspection and modification of the running code.

By default, Xdebug is already running and ready to accept connections. If you need to enable Xdebug on the CLI, execute the `sudo phpenmod xdebug` command within your Homestead virtual machine. Next, follow your IDE's instructions to enable debugging. Finally, configure your browser to trigger Xdebug with an extension or [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/).

Xdebug causes PHP to run significantly slower. To disable Xdebug, run `sudo phpdismod xdebug` within your Homestead virtual machine and restart the FPM service.

#### [Autostarting Xdebug](#autostarting-xdebug)

When debugging functional tests that make requests to the web server, it is easier to autostart debugging rather than modifying tests to pass through a custom header or cookie to trigger debugging. To force Xdebug to start automatically, modify the `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` file inside your Homestead virtual machine and add the following configuration:

```
1; If Homestead.yaml contains a different subnet for the IP address, this address may be different...

2xdebug.client_host = 192.168.10.1

3xdebug.mode = debug

4xdebug.start_with_request = yes
```

### [Debugging CLI Applications](#debugging-cli-applications)

To debug a PHP CLI application, use the `xphp` shell alias inside your Homestead virtual machine:

```
1xphp /path/to/script
```

### [Profiling Applications With Blackfire](#profiling-applications-with-blackfire)

[Blackfire](https://blackfire.io/docs/introduction) is a service for profiling web requests and CLI applications. It offers an interactive user interface which displays profile data in call-graphs and timelines. It is built for use in development, staging, and production, with no overhead for end users. In addition, Blackfire provides performance, quality, and security checks on code and `php.ini` configuration settings.

The [Blackfire Player](https://blackfire.io/docs/player/index) is an open-source Web Crawling, Web Testing, and Web Scraping application which can work jointly with Blackfire in order to script profiling scenarios.

To enable Blackfire, use the "features" setting in your Homestead configuration file:

```
1features:

2    - blackfire:

3        server_id: "server_id"

4        server_token: "server_value"

5        client_id: "client_id"

6        client_token: "client_value"
```

Blackfire server credentials and client credentials [require a Blackfire account](https://blackfire.io/signup). Blackfire offers various options to profile an application, including a CLI tool and browser extension. Please [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index).

## [Network Interfaces](#network-interfaces)

The `networks` property of the `Homestead.yaml` file configures network interfaces for your Homestead virtual machine. You may configure as many interfaces as necessary:

```
1networks:

2    - type: "private_network"

3      ip: "192.168.10.20"
```

To enable a [bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) interface, configure a `bridge` setting for the network and change the network type to `public_network`:

```
1networks:

2    - type: "public_network"

3      ip: "192.168.10.20"

4      bridge: "en1: Wi-Fi (AirPort)"
```

To enable [DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp), just remove the `ip` option from your configuration:

```
1networks:

2    - type: "public_network"

3      bridge: "en1: Wi-Fi (AirPort)"
```

To update what device the network is using, you may add a `dev` option to the network's configuration. The default `dev` value is `eth0`:

```
1networks:

2    - type: "public_network"

3      ip: "192.168.10.20"

4      bridge: "en1: Wi-Fi (AirPort)"

5      dev: "enp2s0"
```

## [Extending Homestead](#extending-homestead)

You may extend Homestead using the `after.sh` script in the root of your Homestead directory. Within this file, you may add any shell commands that are necessary to properly configure and customize your virtual machine.

When customizing Homestead, Ubuntu may ask you if you would like to keep a package's original configuration or overwrite it with a new configuration file. To avoid this, you should use the following command when installing packages in order to avoid overwriting any configuration previously written by Homestead:

```
1sudo apt-get -y \

2    -o Dpkg::Options::="--force-confdef" \

3    -o Dpkg::Options::="--force-confold" \

4    install package-name
```

### [User Customizations](#user-customizations)

When using Homestead with your team, you may want to tweak Homestead to better fit your personal development style. To accomplish this, you may create a `user-customizations.sh` file in the root of your Homestead directory (the same directory containing your `Homestead.yaml` file). Within this file, you may make any customization you would like; however, the `user-customizations.sh` should not be version controlled.

## [Provider Specific Settings](#provider-specific-settings)

### [VirtualBox](#provider-specific-virtualbox)

#### [`natdnshostresolver`](#natdnshostresolver)

By default, Homestead configures the `natdnshostresolver` setting to `on`. This allows Homestead to use your host operating system's DNS settings. If you would like to override this behavior, add the following configuration options to your `Homestead.yaml` file:

```
1provider: virtualbox

2natdnshostresolver: 'off'
```
