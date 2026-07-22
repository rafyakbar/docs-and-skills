# Mail

- [Introduction](#introduction)
  * [Configuration](#configuration)
  * [Driver Prerequisites](#driver-prerequisites)
  * [Failover Configuration](#failover-configuration)
  * [Round Robin Configuration](#round-robin-configuration)
- [Generating Mailables](#generating-mailables)
- [Writing Mailables](#writing-mailables)
  * [Configuring the Sender](#configuring-the-sender)
  * [Configuring the View](#configuring-the-view)
  * [View Data](#view-data)
  * [Attachments](#attachments)
  * [Inline Attachments](#inline-attachments)
  * [Attachable Objects](#attachable-objects)
  * [Headers](#headers)
  * [Tags and Metadata](#tags-and-metadata)
  * [Customizing the Symfony Message](#customizing-the-symfony-message)
- [Markdown Mailables](#markdown-mailables)
  * [Generating Markdown Mailables](#generating-markdown-mailables)
  * [Writing Markdown Messages](#writing-markdown-messages)
  * [Customizing the Components](#customizing-the-components)
- [Sending Mail](#sending-mail)
  * [Queueing Mail](#queueing-mail)
- [Rendering Mailables](#rendering-mailables)
  * [Previewing Mailables in the Browser](#previewing-mailables-in-the-browser)
- [Localizing Mailables](#localizing-mailables)
- [Testing](#testing-mailables)
  * [Testing Mailable Content](#testing-mailable-content)
  * [Testing Mailable Sending](#testing-mailable-sending)
- [Mail and Local Development](#mail-and-local-development)
- [Events](#events)
- [Custom Transports](#custom-transports)
  * [Additional Symfony Transports](#additional-symfony-transports)

## [Introduction](#introduction)

Sending email doesn't have to be complicated. Laravel provides a clean, simple email API powered by the popular [Symfony Mailer](https://symfony.com/doc/current/mailer.html) component. Laravel and Symfony Mailer provide drivers for sending email via SMTP, Cloudflare, Mailgun, Postmark, Resend, Amazon SES, and `sendmail`, allowing you to quickly get started sending mail through a local or cloud-based service of your choice.

### [Configuration](#configuration)

Laravel's email services may be configured via your application's `config/mail.php` configuration file. Each mailer configured within this file may have its own unique configuration and even its own unique "transport", allowing your application to use different email services to send certain email messages. For example, your application might use Postmark to send transactional emails while using Amazon SES to send bulk emails.

Within your `mail` configuration file, you will find a `mailers` configuration array. This array contains a sample configuration entry for each of the major mail drivers / transports supported by Laravel, while the `default` configuration value determines which mailer will be used by default when your application needs to send an email message.

### [Driver / Transport Prerequisites](#driver-prerequisites)

The API based drivers such as Mailgun, Postmark, and Resend are often simpler and faster than sending mail via SMTP servers. Whenever possible, we recommend that you use one of these drivers.

#### [Cloudflare Driver](#cloudflare-driver)

To use the Cloudflare driver, install Symfony's HTTP Client via Composer:

```
1composer require symfony/http-client
```

Next, you will need to make two changes in your application's `config/mail.php` configuration file. First, set your default mailer to `cloudflare`:

```
1'default' => env('MAIL_MAILER', 'cloudflare'),
```

Second, add the following configuration array to your array of `mailers`:

```
1'cloudflare' => [

2    'transport' => 'cloudflare',

3],
```

After configuring your application's default mailer, add the following options to your `config/services.php` configuration file:

```
1'cloudflare' => [

2    'account_id' => env('CLOUDFLARE_ACCOUNT_ID'),

3    'key' => env('CLOUDFLARE_KEY'),

4],
```

#### [Mailgun Driver](#mailgun-driver)

To use the Mailgun driver, install Symfony's Mailgun Mailer transport via Composer:

```
1composer require symfony/mailgun-mailer symfony/http-client
```

Next, you will need to make two changes in your application's `config/mail.php` configuration file. First, set your default mailer to `mailgun`:

```
1'default' => env('MAIL_MAILER', 'mailgun'),
```

Second, add the following configuration array to your array of `mailers`:

```
1'mailgun' => [

2    'transport' => 'mailgun',

3    // 'client' => [

4    //     'timeout' => 5,

5    // ],

6],
```

After configuring your application's default mailer, add the following options to your `config/services.php` configuration file:

```
1'mailgun' => [

2    'domain' => env('MAILGUN_DOMAIN'),

3    'secret' => env('MAILGUN_SECRET'),

4    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),

5    'scheme' => 'https',

6],
```

If you are not using the United States [Mailgun region](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview#mailgun-regions), you may define your region's endpoint in the `services` configuration file:

```
1'mailgun' => [

2    'domain' => env('MAILGUN_DOMAIN'),

3    'secret' => env('MAILGUN_SECRET'),

4    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),

5    'scheme' => 'https',

6],
```

#### [Postmark Driver](#postmark-driver)

To use the [Postmark](https://postmarkapp.com/) driver, install Symfony's Postmark Mailer transport via Composer:

```
1composer require symfony/postmark-mailer symfony/http-client
```

Next, set the `default` option in your application's `config/mail.php` configuration file to `postmark`. After configuring your application's default mailer, ensure that your `config/services.php` configuration file contains the following options:

```
1'postmark' => [

2    'key' => env('POSTMARK_API_KEY'),

3],
```

If you would like to specify the Postmark message stream that should be used by a given mailer, you may add the `message_stream_id` configuration option to the mailer's configuration array. This configuration array can be found in your application's `config/mail.php` configuration file:

```
1'postmark' => [

2    'transport' => 'postmark',

3    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),

4    // 'client' => [

5    //     'timeout' => 5,

6    // ],

7],
```

This way you are also able to set up multiple Postmark mailers with different message streams.

#### [Resend Driver](#resend-driver)

To use the [Resend](https://resend.com/) driver, install Resend's PHP SDK via Composer:

```
1composer require resend/resend-php
```

Next, set the `default` option in your application's `config/mail.php` configuration file to `resend`. After configuring your application's default mailer, ensure that your `config/services.php` configuration file contains the following options:

```
1'resend' => [

2    'key' => env('RESEND_API_KEY'),

3],
```

#### [SES Driver](#ses-driver)

To use the Amazon SES driver you must first install the Amazon AWS SDK for PHP. You may install this library via the Composer package manager:

```
1composer require aws/aws-sdk-php
```

Next, set the `default` option in your `config/mail.php` configuration file to `ses` and verify that your `config/services.php` configuration file contains the following options:

```
1'ses' => [

2    'key' => env('AWS_ACCESS_KEY_ID'),

3    'secret' => env('AWS_SECRET_ACCESS_KEY'),

4    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),

5],
```

To utilize AWS [temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) via a session token, you may add a `token` key to your application's SES configuration:

```
1'ses' => [

2    'key' => env('AWS_ACCESS_KEY_ID'),

3    'secret' => env('AWS_SECRET_ACCESS_KEY'),

4    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),

5    'token' => env('AWS_SESSION_TOKEN'),

6],
```

To interact with SES's [subscription management features](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html), you may return the `X-Ses-List-Management-Options` header in the array returned by the [headers](#headers) method of a mail message:

```
 1/**

 2 * Get the message headers.

 3 */

 4public function headers(): Headers

 5{

 6    return new Headers(

 7        text: [

 8            'X-Ses-List-Management-Options' => 'contactListName=MyContactList;topicName=MyTopic',

 9        ],

10    );

11}
```

If you would like to define [additional options](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail) that Laravel should pass to the AWS SDK's `SendEmail` method when sending an email, you may define an `options` array within your `ses` configuration:

```
 1'ses' => [

 2    'key' => env('AWS_ACCESS_KEY_ID'),

 3    'secret' => env('AWS_SECRET_ACCESS_KEY'),

 4    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),

 5    'options' => [

 6        'ConfigurationSetName' => 'MyConfigurationSet',

 7        'EmailTags' => [

 8            ['Name' => 'foo', 'Value' => 'bar'],

 9        ],

10    ],

11],
```

### [Failover Configuration](#failover-configuration)

Sometimes, an external service you have configured to send your application's mail may be down. In these cases, it can be useful to define one or more backup mail delivery configurations that will be used in case your primary delivery driver is down.

To accomplish this, you should define a mailer within your application's `mail` configuration file that uses the `failover` transport. The configuration array for your application's `failover` mailer should contain an array of `mailers` that reference the order in which configured mailers should be chosen for delivery:

```
 1'mailers' => [

 2    'failover' => [

 3        'transport' => 'failover',

 4        'mailers' => [

 5            'postmark',

 6            'mailgun',

 7            'sendmail',

 8        ],

 9        'retry_after' => 60,

10    ],

11 

12    // ...

13],
```

Once you have configured a mailer that uses the `failover` transport, you will need to set the failover mailer as your default mailer in your application's `.env` file to make use of the failover functionality:

```
1MAIL_MAILER=failover
```

### [Round Robin Configuration](#round-robin-configuration)

The `roundrobin` transport allows you to distribute your mailing workload across multiple mailers. To get started, define a mailer within your application's `mail` configuration file that uses the `roundrobin` transport. The configuration array for your application's `roundrobin` mailer should contain an array of `mailers` that reference which configured mailers should be used for delivery:

```
 1'mailers' => [

 2    'roundrobin' => [

 3        'transport' => 'roundrobin',

 4        'mailers' => [

 5            'ses',

 6            'postmark',

 7        ],

 8        'retry_after' => 60,

 9    ],

10 

11    // ...

12],
```

Once your round robin mailer has been defined, you should set this mailer as the default mailer used by your application by specifying its name as the value of the `default` configuration key within your application's `mail` configuration file:

```
1'default' => env('MAIL_MAILER', 'roundrobin'),
```

The round robin transport selects a random mailer from the list of configured mailers and then switches to the next available mailer for each subsequent email. In contrast to `failover` transport, which helps to achieve *[high availability](https://en.wikipedia.org/wiki/High_availability)*, the `roundrobin` transport provides *[load balancing](https://en.wikipedia.org/wiki/Load_balancing_(computing))*.

## [Generating Mailables](#generating-mailables)

When building Laravel applications, each type of email sent by your application is represented as a "mailable" class. These classes are stored in the `app/Mail` directory. Don't worry if you don't see this directory in your application, since it will be generated for you when you create your first mailable class using the `make:mail` Artisan command:

```
1php artisan make:mail OrderShipped
```

## [Writing Mailables](#writing-mailables)

Once you have generated a mailable class, open it up so we can explore its contents. Mailable class configuration is done in several methods, including the `envelope`, `content`, and `attachments` methods.

The `envelope` method returns an `Illuminate\Mail\Mailables\Envelope` object that defines the subject and, sometimes, the recipients of the message. The `content` method returns an `Illuminate\Mail\Mailables\Content` object that defines the [Blade template](/docs/13.x/blade) that will be used to generate the message content.

### [Configuring the Sender](#configuring-the-sender)

#### [Using the Envelope](#using-the-envelope)

First, let's explore configuring the sender of the email. Or, in other words, who the email is going to be "from". There are two ways to configure the sender. First, you may specify the "from" address on your message's envelope:

```
 1use Illuminate\Mail\Mailables\Address;

 2use Illuminate\Mail\Mailables\Envelope;

 3 

 4/**

 5 * Get the message envelope.

 6 */

 7public function envelope(): Envelope

 8{

 9    return new Envelope(

10        from: new Address('[[email protected]](/cdn-cgi/l/email-protection)', 'Jeffrey Way'),

11        subject: 'Order Shipped',

12    );

13}
```

If you would like, you may also specify a `replyTo` address:

```
1return new Envelope(

2    from: new Address('[[email protected]](/cdn-cgi/l/email-protection)', 'Jeffrey Way'),

3    replyTo: [

4        new Address('[[email protected]](/cdn-cgi/l/email-protection)', 'Taylor Otwell'),

5    ],

6    subject: 'Order Shipped',

7);
```

#### [Using a Global `from` Address](#using-a-global-from-address)

However, if your application uses the same "from" address for all of its emails, it can become cumbersome to add it to each mailable class you generate. Instead, you may specify a global "from" address in your `config/mail.php` configuration file. This address will be used if no other "from" address is specified within the mailable class:

```
1'from' => [

2    'address' => env('MAIL_FROM_ADDRESS', '[[email protected]](/cdn-cgi/l/email-protection)'),

3    'name' => env('MAIL_FROM_NAME', 'Example'),

4],
```

In addition, you may define a global "reply_to" address within your `config/mail.php` configuration file:

```
1'reply_to' => [

2    'address' => '[[email protected]](/cdn-cgi/l/email-protection)',

3    'name' => 'App Name',

4],
```

### [Configuring the View](#configuring-the-view)

Within a mailable class's `content` method, you may define the `view`, or which template should be used when rendering the email's contents. Since each email typically uses a [Blade template](/docs/13.x/blade) to render its contents, you have the full power and convenience of the Blade templating engine when building your email's HTML:

```
1/**

2 * Get the message content definition.

3 */

4public function content(): Content

5{

6    return new Content(

7        view: 'mail.orders.shipped',

8    );

9}
```

You may wish to create a `resources/views/mail` directory to house all of your email templates; however, you are free to place them wherever you wish within your `resources/views` directory.

#### [Plain Text Emails](#plain-text-emails)

If you would like to define a plain-text version of your email, you may specify the plain-text template when creating the message's `Content` definition. Like the `view` parameter, the `text` parameter should be a template name which will be used to render the contents of the email. You are free to define both an HTML and plain-text version of your message:

```
 1/**

 2 * Get the message content definition.

 3 */

 4public function content(): Content

 5{

 6    return new Content(

 7        view: 'mail.orders.shipped',

 8        text: 'mail.orders.shipped-text'

 9    );

10}
```

For clarity, the `html` parameter may be used as an alias of the `view` parameter:

```
1return new Content(

2    html: 'mail.orders.shipped',

3    text: 'mail.orders.shipped-text'

4);
```

### [View Data](#view-data)

#### [Via Public Properties](#via-public-properties)

Typically, you will want to pass some data to your view that you can utilize when rendering the email's HTML. There are two ways you may make data available to your view. First, any public property defined on your mailable class will automatically be made available to the view. So, for example, you may pass data into your mailable class's constructor and set that data to public properties defined on the class:

```
 1<?php

 2 

 3namespace App\Mail;

 4 

 5use App\Models\Order;

 6use Illuminate\Bus\Queueable;

 7use Illuminate\Mail\Mailable;

 8use Illuminate\Mail\Mailables\Content;

 9use Illuminate\Queue\SerializesModels;

10 

11class OrderShipped extends Mailable

12{

13    use Queueable, SerializesModels;

14 

15    /**

16     * Create a new message instance.

17     */

18    public function __construct(

19        public Order $order,

20    ) {}

21 

22    /**

23     * Get the message content definition.

24     */

25    public function content(): Content

26    {

27        return new Content(

28            view: 'mail.orders.shipped',

29        );

30    }

31}
```

Once the data has been set to a public property, it will automatically be available in your view, so you may access it like you would access any other data in your Blade templates:

```
1<div>

2    Price: {{ $order->price }}

3</div>
```

#### [Via the `with` Parameter:](#via-the-with-parameter)

If you would like to customize the format of your email's data before it is sent to the template, you may manually pass your data to the view via the `Content` definition's `with` parameter. Typically, you will still pass data via the mailable class's constructor; however, you should set this data to `protected` or `private` properties so the data is not automatically made available to the template:

```
 1<?php

 2 

 3namespace App\Mail;

 4 

 5use App\Models\Order;

 6use Illuminate\Bus\Queueable;

 7use Illuminate\Mail\Mailable;

 8use Illuminate\Mail\Mailables\Content;

 9use Illuminate\Queue\SerializesModels;

10 

11class OrderShipped extends Mailable

12{

13    use Queueable, SerializesModels;

14 

15    /**

16     * Create a new message instance.

17     */

18    public function __construct(

19        protected Order $order,

20    ) {}

21 

22    /**

23     * Get the message content definition.

24     */

25    public function content(): Content

26    {

27        return new Content(

28            view: 'mail.orders.shipped',

29            with: [

30                'orderName' => $this->order->name,

31                'orderPrice' => $this->order->price,

32            ],

33        );

34    }

35}
```

Once the data has been passed via the `with` parameter, it will automatically be available in your view, so you may access it like you would access any other data in your Blade templates:

```
1<div>

2    Price: {{ $orderPrice }}

3</div>
```

### [Attachments](#attachments)

To add attachments to an email, you will add attachments to the array returned by the message's `attachments` method. First, you may add an attachment by providing a file path to the `fromPath` method provided by the `Attachment` class:

```
 1use Illuminate\Mail\Mailables\Attachment;

 2 

 3/**

 4 * Get the attachments for the message.

 5 *

 6 * @return array<int, \Illuminate\Mail\Mailables\Attachment>

 7 */

 8public function attachments(): array

 9{

10    return [

11        Attachment::fromPath('/path/to/file'),

12    ];

13}
```

When attaching files to a message, you may also specify the display name and / or MIME type for the attachment using the `as` and `withMime` methods:

```
 1/**

 2 * Get the attachments for the message.

 3 *

 4 * @return array<int, \Illuminate\Mail\Mailables\Attachment>

 5 */

 6public function attachments(): array

 7{

 8    return [

 9        Attachment::fromPath('/path/to/file')

10            ->as('name.pdf')

11            ->withMime('application/pdf'),

12    ];

13}
```

#### [Attaching Files From Disk](#attaching-files-from-disk)

If you have stored a file on one of your [filesystem disks](/docs/13.x/filesystem), you may attach it to the email using the `fromStorage` attachment method:

```
 1/**

 2 * Get the attachments for the message.

 3 *

 4 * @return array<int, \Illuminate\Mail\Mailables\Attachment>

 5 */

 6public function attachments(): array

 7{

 8    return [

 9        Attachment::fromStorage('/path/to/file'),

10    ];

11}
```

Of course, you may also specify the attachment's name and MIME type:

```
 1/**

 2 * Get the attachments for the message.

 3 *

 4 * @return array<int, \Illuminate\Mail\Mailables\Attachment>

 5 */

 6public function attachments(): array

 7{

 8    return [

 9        Attachment::fromStorage('/path/to/file')

10            ->as('name.pdf')

11            ->withMime('application/pdf'),

12    ];

13}
```

The `fromStorageDisk` method may be used if you need to specify a storage disk other than your default disk:

```
 1/**

 2 * Get the attachments for the message.

 3 *

 4 * @return array<int, \Illuminate\Mail\Mailables\Attachment>

 5 */

 6public function attachments(): array

 7{

 8    return [

 9        Attachment::fromStorageDisk('s3', '/path/to/file')

10            ->as('name.pdf')

11            ->withMime('application/pdf'),

12    ];

13}
```

#### [Raw Data Attachments](#raw-data-attachments)

The `fromData` attachment method may be used to attach a raw string of bytes as an attachment. For example, you might use this method if you have generated a PDF in memory and want to attach it to the email without writing it to disk. The `fromData` method accepts a closure which resolves the raw data bytes as well as the name that the attachment should be assigned:

```
 1/**

 2 * Get the attachments for the message.

 3 *

 4 * @return array<int, \Illuminate\Mail\Mailables\Attachment>

 5 */

 6public function attachments(): array

 7{

 8    return [

 9        Attachment::fromData(fn () => $this->pdf, 'Report.pdf')

10            ->withMime('application/pdf'),

11    ];

12}
```

### [Inline Attachments](#inline-attachments)

Embedding inline images into your emails is typically cumbersome; however, Laravel provides a convenient way to attach images to your emails. To embed an inline image, use the `embed` method on the `$message` variable within your email template. Laravel automatically makes the `$message` variable available to all of your email templates, so you don't need to worry about passing it in manually:

```
1<body>

2    Here is an image:

3 

4    <img src="{{ $message->embed($pathToImage) }}">

5</body>
```

The `$message` variable is not available in plain-text message templates since plain-text messages do not utilize inline attachments.

#### [Embedding Raw Data Attachments](#embedding-raw-data-attachments)

If you already have a raw image data string you wish to embed into an email template, you may call the `embedData` method on the `$message` variable. When calling the `embedData` method, you will need to provide a filename that should be assigned to the embedded image:

```
1<body>

2    Here is an image from raw data:

3 

4    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">

5</body>
```

### [Attachable Objects](#attachable-objects)

While attaching files to messages via simple string paths is often sufficient, in many cases the attachable entities within your application are represented by classes. For example, if your application is attaching a photo to a message, your application may also have a `Photo` model that represents that photo. When that is the case, wouldn't it be convenient to simply pass the `Photo` model to the `attach` method? Attachable objects allow you to do just that.

To get started, implement the `Illuminate\Contracts\Mail\Attachable` interface on the object that will be attachable to messages. This interface dictates that your class defines a `toMailAttachment` method that returns an `Illuminate\Mail\Attachment` instance:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Contracts\Mail\Attachable;

 6use Illuminate\Database\Eloquent\Model;

 7use Illuminate\Mail\Attachment;

 8 

 9class Photo extends Model implements Attachable

10{

11    /**

12     * Get the attachable representation of the model.

13     */

14    public function toMailAttachment(): Attachment

15    {

16        return Attachment::fromPath('/path/to/file');

17    }

18}
```

Once you have defined your attachable object, you may return an instance of that object from the `attachments` method when building an email message:

```
1/**

2 * Get the attachments for the message.

3 *

4 * @return array<int, \Illuminate\Mail\Mailables\Attachment>

5 */

6public function attachments(): array

7{

8    return [$this->photo];

9}
```

Of course, attachment data may be stored on a remote file storage service such as Amazon S3. So, Laravel also allows you to generate attachment instances from data that is stored on one of your application's [filesystem disks](/docs/13.x/filesystem):

```
1// Create an attachment from a file on your default disk...

2return Attachment::fromStorage($this->path);

3 

4// Create an attachment from a file on a specific disk...

5return Attachment::fromStorageDisk('backblaze', $this->path);
```

In addition, you may create attachment instances via data that you have in memory. To accomplish this, provide a closure to the `fromData` method. The closure should return the raw data that represents the attachment:

```
1return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

Laravel also provides additional methods that you may use to customize your attachments. For example, you may use the `as` and `withMime` methods to customize the file's name and MIME type:

```
1return Attachment::fromPath('/path/to/file')

2    ->as('Photo Name')

3    ->withMime('image/jpeg');
```

### [Headers](#headers)

Sometimes you may need to attach additional headers to the outgoing message. For instance, you may need to set a custom `Message-Id` or other arbitrary text headers.

To accomplish this, define a `headers` method on your mailable. The `headers` method should return an `Illuminate\Mail\Mailables\Headers` instance. This class accepts `messageId`, `references`, and `text` parameters. Of course, you may provide only the parameters you need for your particular message:

```
 1use Illuminate\Mail\Mailables\Headers;

 2 

 3/**

 4 * Get the message headers.

 5 */

 6public function headers(): Headers

 7{

 8    return new Headers(

 9        messageId: '[[email protected]](/cdn-cgi/l/email-protection)',

10        references: ['[[email protected]](/cdn-cgi/l/email-protection)'],

11        text: [

12            'X-Custom-Header' => 'Custom Value',

13        ],

14    );

15}
```

### [Tags and Metadata](#tags-and-metadata)

Some third-party email providers such as Mailgun and Postmark support message "tags" and "metadata", which may be used to group and track emails sent by your application. You may add tags and metadata to an email message via your `Envelope` definition:

```
 1use Illuminate\Mail\Mailables\Envelope;

 2 

 3/**

 4 * Get the message envelope.

 5 *

 6 * @return \Illuminate\Mail\Mailables\Envelope

 7 */

 8public function envelope(): Envelope

 9{

10    return new Envelope(

11        subject: 'Order Shipped',

12        tags: ['shipment'],

13        metadata: [

14            'order_id' => $this->order->id,

15        ],

16    );

17}
```

If your application is using the Mailgun driver, you may consult Mailgun's documentation for more information on [tags](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) and [metadata](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages). Likewise, the Postmark documentation may also be consulted for more information on their support for [tags](https://postmarkapp.com/blog/tags-support-for-smtp) and [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq).

If your application is using Amazon SES to send emails, you should use the `metadata` method to attach [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html) to the message.

### [Customizing the Symfony Message](#customizing-the-symfony-message)

Laravel's mail capabilities are powered by Symfony Mailer. Laravel allows you to register custom callbacks that will be invoked with the Symfony Message instance before sending the message. This gives you an opportunity to deeply customize the message before it is sent. To accomplish this, define a `using` parameter on your `Envelope` definition:

```
 1use Illuminate\Mail\Mailables\Envelope;

 2use Symfony\Component\Mime\Email;

 3 

 4/**

 5 * Get the message envelope.

 6 */

 7public function envelope(): Envelope

 8{

 9    return new Envelope(

10        subject: 'Order Shipped',

11        using: [

12            function (Email $message) {

13                // ...

14            },

15        ]

16    );

17}
```

## [Markdown Mailables](#markdown-mailables)

Markdown mailable messages allow you to take advantage of the pre-built templates and components of [mail notifications](/docs/13.x/notifications#mail-notifications) in your mailables. Since the messages are written in Markdown, Laravel is able to render beautiful, responsive HTML templates for the messages while also automatically generating a plain-text counterpart.

### [Generating Markdown Mailables](#generating-markdown-mailables)

To generate a mailable with a corresponding Markdown template, you may use the `--markdown` option of the `make:mail` Artisan command:

```
1php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

Then, when configuring the mailable `Content` definition within its `content` method, use the `markdown` parameter instead of the `view` parameter:

```
 1use Illuminate\Mail\Mailables\Content;

 2 

 3/**

 4 * Get the message content definition.

 5 */

 6public function content(): Content

 7{

 8    return new Content(

 9        markdown: 'mail.orders.shipped',

10        with: [

11            'url' => $this->orderUrl,

12        ],

13    );

14}
```

### [Writing Markdown Messages](#writing-markdown-messages)

Markdown mailables use a combination of Blade components and Markdown syntax which allow you to easily construct mail messages while leveraging Laravel's pre-built email UI components:

```
 1<x-mail::message>

 2# Order Shipped

 3 

 4Your order has been shipped!

 5 

 6<x-mail::button :url="$url">

 7View Order

 8</x-mail::button>

 9 

10Thanks,<br>

11{{ config('app.name') }}

12</x-mail::message>
```

Do not use excess indentation when writing Markdown emails. Per Markdown standards, Markdown parsers will render indented content as code blocks.

#### [Button Component](#button-component)

The button component renders a centered button link. The component accepts two arguments, a `url` and an optional `color`. Supported colors are `primary`, `success`, and `error`. You may add as many button components to a message as you wish:

```
1<x-mail::button :url="$url" color="success">

2View Order

3</x-mail::button>
```

#### [Panel Component](#panel-component)

The panel component renders the given block of text in a panel that has a slightly different background color than the rest of the message. This allows you to draw attention to a given block of text:

```
1<x-mail::panel>

2This is the panel content.

3</x-mail::panel>
```

#### [Table Component](#table-component)

The table component allows you to transform a Markdown table into an HTML table. The component accepts the Markdown table as its content. Table column alignment is supported using the default Markdown table alignment syntax:

```
1<x-mail::table>

2| Laravel       | Table         | Example       |

3| ------------- | :-----------: | ------------: |

4| Col 2 is      | Centered      | $10           |

5| Col 3 is      | Right-Aligned | $20           |

6</x-mail::table>
```

### [Customizing the Components](#customizing-the-components)

You may export all of the Markdown mail components to your own application for customization. To export the components, use the `vendor:publish` Artisan command to publish the `laravel-mail` asset tag:

```
1php artisan vendor:publish --tag=laravel-mail
```

This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like.

#### [Customizing the CSS](#customizing-the-css)

After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be converted to inline CSS styles within the HTML representations of your Markdown mail messages.

If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of your application's `config/mail.php` configuration file to match the name of your new theme.

To customize the theme for an individual mailable, you may set the `$theme` property of the mailable class to the name of the theme that should be used when sending that mailable.

## [Sending Mail](#sending-mail)

To send a message, use the `to` method on the `Mail` [facade](/docs/13.x/facades). The `to` method accepts an email address, a user instance, or a collection of users. If you pass an object or collection of objects, the mailer will automatically use their `email` and `name` properties when determining the email's recipients, so make sure these attributes are available on your objects. Once you have specified your recipients, you may pass an instance of your mailable class to the `send` method:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Mail\OrderShipped;

 6use App\Models\Order;

 7use Illuminate\Http\RedirectResponse;

 8use Illuminate\Http\Request;

 9use Illuminate\Support\Facades\Mail;

10 

11class OrderShipmentController extends Controller

12{

13    /**

14     * Ship the given order.

15     */

16    public function store(Request $request): RedirectResponse

17    {

18        $order = Order::findOrFail($request->order_id);

19 

20        // Ship the order...

21 

22        Mail::to($request->user())->send(new OrderShipped($order));

23 

24        return redirect('/orders');

25    }

26}
```

You are not limited to just specifying the "to" recipients when sending a message. You are free to set "to", "cc", and "bcc" recipients by chaining their respective methods together:

```
1Mail::to($request->user())

2    ->cc($moreUsers)

3    ->bcc($evenMoreUsers)

4    ->send(new OrderShipped($order));
```

#### [Looping Over Recipients](#looping-over-recipients)

Occasionally, you may need to send a mailable to a list of recipients by iterating over an array of recipients / email addresses. However, since the `to` method appends email addresses to the mailable's list of recipients, each iteration through the loop will send another email to every previous recipient. Therefore, you should always re-create the mailable instance for each recipient:

```
1foreach (['[[email protected]](/cdn-cgi/l/email-protection)', '[[email protected]](/cdn-cgi/l/email-protection)'] as $recipient) {

2    Mail::to($recipient)->send(new OrderShipped($order));

3}
```

#### [Sending Mail via a Specific Mailer](#sending-mail-via-a-specific-mailer)

By default, Laravel will send email using the mailer configured as the `default` mailer in your application's `mail` configuration file. However, you may use the `mailer` method to send a message using a specific mailer configuration:

```
1Mail::mailer('postmark')

2    ->to($request->user())

3    ->send(new OrderShipped($order));
```

### [Queueing Mail](#queueing-mail)

#### [Queueing a Mail Message](#queueing-a-mail-message)

Since sending email messages can negatively impact the response time of your application, many developers choose to queue email messages for background sending. Laravel makes this easy using its built-in [unified queue API](/docs/13.x/queues). To queue a mail message, use the `queue` method on the `Mail` facade after specifying the message's recipients:

```
1Mail::to($request->user())

2    ->cc($moreUsers)

3    ->bcc($evenMoreUsers)

4    ->queue(new OrderShipped($order));
```

This method will automatically take care of pushing a job onto the queue so the message is sent in the background. You will need to [configure your queues](/docs/13.x/queues) before using this feature.

#### [Delayed Message Queueing](#delayed-message-queueing)

If you wish to delay the delivery of a queued email message, you may use the `later` method. As its first argument, the `later` method accepts a `DateTime` instance indicating when the message should be sent:

```
1Mail::to($request->user())

2    ->cc($moreUsers)

3    ->bcc($evenMoreUsers)

4    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```

#### [Pushing to Specific Queues](#pushing-to-specific-queues)

Since all mailable classes generated using the `make:mail` command make use of the `Illuminate\Bus\Queueable` trait, you may call the `onQueue` and `onConnection` methods on any mailable class instance, allowing you to specify the connection and queue name for the message:

```
1$message = (new OrderShipped($order))

2    ->onConnection('sqs')

3    ->onQueue('emails');

4 

5Mail::to($request->user())

6    ->cc($moreUsers)

7    ->bcc($evenMoreUsers)

8    ->queue($message);
```

Alternatively, you may specify the connection and queue using the `Connection` and `Queue` attributes on the mailable class:

```
1use Illuminate\Queue\Attributes\Connection;

2use Illuminate\Queue\Attributes\Queue;

3 

4#[Connection('sqs')]

5#[Queue('emails')]

6class OrderShipped extends Mailable

7{

8    // ...

9}
```

#### [Queueing by Default](#queueing-by-default)

If you have mailable classes that you want to always be queued, you may implement the `ShouldQueue` contract on the class. Now, even if you call the `send` method when mailing, the mailable will still be queued since it implements the contract:

```
1use Illuminate\Contracts\Queue\ShouldQueue;

2 

3class OrderShipped extends Mailable implements ShouldQueue

4{

5    // ...

6}
```

#### [Queued Mailables and Database Transactions](#queued-mailables-and-database-transactions)

When queued mailables are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your mailable depends on these models, unexpected errors can occur when the job that sends the queued mailable is processed.

If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued mailable should be dispatched after all open database transactions have been committed by calling the `afterCommit` method when sending the mail message:

```
1Mail::to($request->user())->send(

2    (new OrderShipped($order))->afterCommit()

3);
```

Alternatively, you may call the `afterCommit` method from your mailable's constructor:

```
 1<?php

 2 

 3namespace App\Mail;

 4 

 5use Illuminate\Bus\Queueable;

 6use Illuminate\Contracts\Queue\ShouldQueue;

 7use Illuminate\Mail\Mailable;

 8use Illuminate\Queue\SerializesModels;

 9 

10class OrderShipped extends Mailable implements ShouldQueue

11{

12    use Queueable, SerializesModels;

13 

14    /**

15     * Create a new message instance.

16     */

17    public function __construct()

18    {

19        $this->afterCommit();

20    }

21}
```

To learn more about working around these issues, please review the documentation regarding [queued jobs and database transactions](/docs/13.x/queues#jobs-and-database-transactions).

#### [Queued Email Failures](#queued-email-failures)

When a queued email fails, the `failed` method on the queued mailable class will be invoked if it has been defined. The `Throwable` instance that caused the queued email to fail will be passed to the `failed` method:

```
 1<?php

 2 

 3namespace App\Mail;

 4 

 5use Illuminate\Contracts\Queue\ShouldQueue;

 6use Illuminate\Mail\Mailable;

 7use Illuminate\Queue\SerializesModels;

 8use Throwable;

 9 

10class OrderDelayed extends Mailable implements ShouldQueue

11{

12    use SerializesModels;

13 

14    /**

15     * Handle a queued email's failure.

16     */

17    public function failed(Throwable $exception): void

18    {

19        // ...

20    }

21}
```

## [Rendering Mailables](#rendering-mailables)

Sometimes you may wish to capture the HTML content of a mailable without sending it. To accomplish this, you may call the `render` method of the mailable. This method will return the evaluated HTML content of the mailable as a string:

```
1use App\Mail\InvoicePaid;

2use App\Models\Invoice;

3 

4$invoice = Invoice::find(1);

5 

6return (new InvoicePaid($invoice))->render();
```

### [Previewing Mailables in the Browser](#previewing-mailables-in-the-browser)

When designing a mailable's template, it is convenient to quickly preview the rendered mailable in your browser like a typical Blade template. For this reason, Laravel allows you to return any mailable directly from a route closure or controller. When a mailable is returned, it will be rendered and displayed in the browser, allowing you to quickly preview its design without needing to send it to an actual email address:

```
1Route::get('/mailable', function () {

2    $invoice = App\Models\Invoice::find(1);

3 

4    return new App\Mail\InvoicePaid($invoice);

5});
```

## [Localizing Mailables](#localizing-mailables)

Laravel allows you to send mailables in a locale other than the request's current locale, and will even remember this locale if the mail is queued.

To accomplish this, the `Mail` facade offers a `locale` method to set the desired language. The application will change into this locale when the mailable's template is being evaluated and then revert back to the previous locale when evaluation is complete:

```
1Mail::to($request->user())->locale('es')->send(

2    new OrderShipped($order)

3);
```

#### [User Preferred Locales](#user-preferred-locales)

Sometimes, applications store each user's preferred locale. By implementing the `HasLocalePreference` contract on one or more of your models, you may instruct Laravel to use this stored locale when sending mail:

```
 1use Illuminate\Contracts\Translation\HasLocalePreference;

 2 

 3class User extends Model implements HasLocalePreference

 4{

 5    /**

 6     * Get the user's preferred locale.

 7     */

 8    public function preferredLocale(): string

 9    {

10        return $this->locale;

11    }

12}
```

Once you have implemented the interface, Laravel will automatically use the preferred locale when sending mailables and notifications to the model. Therefore, there is no need to call the `locale` method when using this interface:

```
1Mail::to($request->user())->send(new OrderShipped($order));
```

## [Testing](#testing-mailables)

### [Testing Mailable Content](#testing-mailable-content)

Laravel provides a variety of methods for inspecting your mailable's structure. In addition, Laravel provides several convenient methods for testing that your mailable contains the content that you expect:

Pest

PHPUnit

```
 1use App\Mail\InvoicePaid;

 2use App\Models\User;

 3 

 4test('mailable content', function () {

 5    $user = User::factory()->create();

 6 

 7    $mailable = new InvoicePaid($user);

 8 

 9    $mailable->assertFrom('[[email protected]](/cdn-cgi/l/email-protection)');

10    $mailable->assertTo('[[email protected]](/cdn-cgi/l/email-protection)');

11    $mailable->assertHasCc('[[email protected]](/cdn-cgi/l/email-protection)');

12    $mailable->assertHasBcc('[[email protected]](/cdn-cgi/l/email-protection)');

13    $mailable->assertHasReplyTo('[[email protected]](/cdn-cgi/l/email-protection)');

14    $mailable->assertHasSubject('Invoice Paid');

15    $mailable->assertHasTag('example-tag');

16    $mailable->assertHasMetadata('key', 'value');

17 

18    $mailable->assertSeeInHtml($user->email);

19    $mailable->assertDontSeeInHtml('Invoice Not Paid');

20    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

21 

22    $mailable->assertSeeInText($user->email);

23    $mailable->assertDontSeeInText('Invoice Not Paid');

24    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

25 

26    $mailable->assertHasAttachment('/path/to/file');

27    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));

28    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);

29    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);

30    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);

31});
```

```
 1use App\Mail\InvoicePaid;

 2use App\Models\User;

 3 

 4public function test_mailable_content(): void

 5{

 6    $user = User::factory()->create();

 7 

 8    $mailable = new InvoicePaid($user);

 9 

10    $mailable->assertFrom('[[email protected]](/cdn-cgi/l/email-protection)');

11    $mailable->assertTo('[[email protected]](/cdn-cgi/l/email-protection)');

12    $mailable->assertHasCc('[[email protected]](/cdn-cgi/l/email-protection)');

13    $mailable->assertHasBcc('[[email protected]](/cdn-cgi/l/email-protection)');

14    $mailable->assertHasReplyTo('[[email protected]](/cdn-cgi/l/email-protection)');

15    $mailable->assertHasSubject('Invoice Paid');

16    $mailable->assertHasTag('example-tag');

17    $mailable->assertHasMetadata('key', 'value');

18 

19    $mailable->assertSeeInHtml($user->email);

20    $mailable->assertDontSeeInHtml('Invoice Not Paid');

21    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

22 

23    $mailable->assertSeeInText($user->email);

24    $mailable->assertDontSeeInText('Invoice Not Paid');

25    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

26 

27    $mailable->assertHasAttachment('/path/to/file');

28    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));

29    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);

30    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);

31    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);

32}
```

As you might expect, the "HTML" assertions assert that the HTML version of your mailable contains a given string, while the "text" assertions assert that the plain-text version of your mailable contains a given string.

### [Testing Mailable Sending](#testing-mailable-sending)

We suggest testing the content of your mailables separately from your tests that assert that a given mailable was "sent" to a specific user. Typically, the content of mailables is not relevant to the code you are testing, and it is sufficient to simply assert that Laravel was instructed to send a given mailable.

You may use the `Mail` facade's `fake` method to prevent mail from being sent. After calling the `Mail` facade's `fake` method, you may then assert that mailables were instructed to be sent to users and even inspect the data the mailables received:

Pest

PHPUnit

```
 1<?php

 2 

 3use App\Mail\OrderShipped;

 4use Illuminate\Support\Facades\Mail;

 5 

 6test('orders can be shipped', function () {

 7    Mail::fake();

 8 

 9    // Perform order shipping...

10 

11    // Assert that no mailables were sent...

12    Mail::assertNothingSent();

13 

14    // Assert that a mailable was sent...

15    Mail::assertSent(OrderShipped::class);

16 

17    // Assert a mailable was sent twice...

18    Mail::assertSent(OrderShipped::class, 2);

19 

20    // Assert a mailable was sent to an email address...

21    Mail::assertSent(OrderShipped::class, '[[email protected]](/cdn-cgi/l/email-protection)');

22 

23    // Assert a mailable was sent to multiple email addresses...

24    Mail::assertSent(OrderShipped::class, ['[[email protected]](/cdn-cgi/l/email-protection)', '...']);

25 

26    // Assert a mailable was not sent...

27    Mail::assertNotSent(AnotherMailable::class);

28 

29    // Assert a mailable was sent twice...

30    Mail::assertSentTimes(OrderShipped::class, 2);

31 

32    // Assert 3 total mailables were sent...

33    Mail::assertSentCount(3);

34});
```

```
 1<?php

 2 

 3namespace Tests\Feature;

 4 

 5use App\Mail\OrderShipped;

 6use Illuminate\Support\Facades\Mail;

 7use Tests\TestCase;

 8 

 9class ExampleTest extends TestCase

10{

11    public function test_orders_can_be_shipped(): void

12    {

13        Mail::fake();

14 

15        // Perform order shipping...

16 

17        // Assert that no mailables were sent...

18        Mail::assertNothingSent();

19 

20        // Assert that a mailable was sent...

21        Mail::assertSent(OrderShipped::class);

22 

23        // Assert a mailable was sent twice...

24        Mail::assertSent(OrderShipped::class, 2);

25 

26        // Assert a mailable was sent to an email address...

27        Mail::assertSent(OrderShipped::class, '[[email protected]](/cdn-cgi/l/email-protection)');

28 

29        // Assert a mailable was sent to multiple email addresses...

30        Mail::assertSent(OrderShipped::class, ['[[email protected]](/cdn-cgi/l/email-protection)', '...']);

31 

32        // Assert a mailable was not sent...

33        Mail::assertNotSent(AnotherMailable::class);

34 

35        // Assert a mailable was sent twice...

36        Mail::assertSentTimes(OrderShipped::class, 2);

37 

38        // Assert 3 total mailables were sent...

39        Mail::assertSentCount(3);

40    }

41}
```

If you are queueing mailables for delivery in the background, you should use the `assertQueued` method instead of `assertSent`:

```
1Mail::assertQueued(OrderShipped::class);

2Mail::assertNotQueued(OrderShipped::class);

3Mail::assertNothingQueued();

4Mail::assertQueuedCount(3);
```

You can also assert the total number of mailables that have been sent or queued using the `assertOutgoingCount` method:

```
1Mail::assertOutgoingCount(3);
```

You may pass a closure to the `assertSent`, `assertNotSent`, `assertQueued`, or `assertNotQueued` methods in order to assert that a mailable was sent that passes a given "truth test". If at least one mailable was sent that passes the given truth test then the assertion will be successful:

```
1Mail::assertSent(function (OrderShipped $mail) use ($order) {

2    return $mail->order->id === $order->id;

3});
```

When calling the `Mail` facade's assertion methods, the mailable instance accepted by the provided closure exposes helpful methods for examining the mailable:

```
 1Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {

 2    return $mail->hasTo($user->email) &&

 3           $mail->hasCc('...') &&

 4           $mail->hasBcc('...') &&

 5           $mail->hasReplyTo('...') &&

 6           $mail->hasFrom('...') &&

 7           $mail->hasSubject('...') &&

 8           $mail->hasMetadata('order_id', $mail->order->id);

 9           $mail->usesMailer('ses');

10});
```

The mailable instance also includes several helpful methods for examining the attachments on a mailable:

```
 1use Illuminate\Mail\Mailables\Attachment;

 2 

 3Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {

 4    return $mail->hasAttachment(

 5        Attachment::fromPath('/path/to/file')

 6            ->as('name.pdf')

 7            ->withMime('application/pdf')

 8    );

 9});

10 

11Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {

12    return $mail->hasAttachment(

13        Attachment::fromStorageDisk('s3', '/path/to/file')

14    );

15});

16 

17Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($pdfData) {

18    return $mail->hasAttachment(

19        Attachment::fromData(fn () => $pdfData, 'name.pdf')

20    );

21});
```

You may have noticed that there are two methods for asserting that mail was not sent: `assertNotSent` and `assertNotQueued`. Sometimes you may wish to assert that no mail was sent **or** queued. To accomplish this, you may use the `assertNothingOutgoing` and `assertNotOutgoing` methods:

```
1Mail::assertNothingOutgoing();

2 

3Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {

4    return $mail->order->id === $order->id;

5});
```

## [Mail and Local Development](#mail-and-local-development)

When developing an application that sends email, you probably don't want to actually send emails to live email addresses. Laravel provides several ways to "disable" the actual sending of emails during local development.

#### [Log Driver](#log-driver)

Instead of sending your emails, the `log` mail driver will write all email messages to your log files for inspection. Typically, this driver would only be used during local development. For more information on configuring your application per environment, check out the [configuration documentation](/docs/13.x/configuration#environment-configuration).

#### [HELO / Mailtrap / Mailpit](#mailtrap)

Alternatively, you may use a service like [HELO](https://usehelo.com) or [Mailtrap](https://mailtrap.io) and the `smtp` driver to send your email messages to a "dummy" mailbox where you may view them in a true email client. This approach has the benefit of allowing you to actually inspect the final emails in Mailtrap's message viewer.

If you are using [Laravel Sail](/docs/13.x/sail), you may preview your messages using [Mailpit](https://github.com/axllent/mailpit). When Sail is running, you may access the Mailpit interface at: `http://localhost:8025`.

#### [Using a Global `to` Address](#using-a-global-to-address)

Finally, you may specify a global "to" address by invoking the `alwaysTo` method offered by the `Mail` facade. Typically, this method should be called from the `boot` method of one of your application's service providers:

```
 1use Illuminate\Support\Facades\Mail;

 2 

 3/**

 4 * Bootstrap any application services.

 5 */

 6public function boot(): void

 7{

 8    if ($this->app->environment('local')) {

 9        Mail::alwaysTo('[[email protected]](/cdn-cgi/l/email-protection)');

10    }

11}
```

When using the `alwaysTo` method, any additional "cc" or "bcc" addresses on mail messages will be removed.

## [Events](#events)

Laravel dispatches two events while sending mail messages. The `MessageSending` event is dispatched prior to a message being sent, while the `MessageSent` event is dispatched after a message has been sent. Remember, these events are dispatched when the mail is being *sent*, not when it is queued. You may create [event listeners](/docs/13.x/events) for these events within your application:

```
 1use Illuminate\Mail\Events\MessageSending;

 2// use Illuminate\Mail\Events\MessageSent;

 3 

 4class LogMessage

 5{

 6    /**

 7     * Handle the event.

 8     */

 9    public function handle(MessageSending $event): void

10    {

11        // ...

12    }

13}
```

## [Custom Transports](#custom-transports)

Laravel includes a variety of mail transports; however, you may wish to write your own transports to deliver email via other services that Laravel does not support out of the box. To get started, define a class that extends the `Symfony\Component\Mailer\Transport\AbstractTransport` class. Then, implement the `doSend` and `__toString` methods on your transport:

```
 1<?php

 2 

 3namespace App\Mail;

 4 

 5use MailchimpTransactional\ApiClient;

 6use Symfony\Component\Mailer\SentMessage;

 7use Symfony\Component\Mailer\Transport\AbstractTransport;

 8use Symfony\Component\Mime\Address;

 9use Symfony\Component\Mime\MessageConverter;

10 

11class MailchimpTransport extends AbstractTransport

12{

13    /**

14     * Create a new Mailchimp transport instance.

15     */

16    public function __construct(

17        protected ApiClient $client,

18    ) {

19        parent::__construct();

20    }

21 

22    /**

23     * {@inheritDoc}

24     */

25    protected function doSend(SentMessage $message): void

26    {

27        $email = MessageConverter::toEmail($message->getOriginalMessage());

28 

29        $this->client->messages->send(['message' => [

30            'from_email' => $email->getFrom(),

31            'to' => collect($email->getTo())->map(function (Address $email) {

32                return ['email' => $email->getAddress(), 'type' => 'to'];

33            })->all(),

34            'subject' => $email->getSubject(),

35            'text' => $email->getTextBody(),

36        ]]);

37    }

38 

39    /**

40     * Get the string representation of the transport.

41     */

42    public function __toString(): string

43    {

44        return 'mailchimp';

45    }

46}
```

Once you've defined your custom transport, you may register it via the `extend` method provided by the `Mail` facade. Typically, this should be done within the `boot` method of your application's `AppServiceProvider`. A `$config` argument will be passed to the closure provided to the `extend` method. This argument will contain the configuration array defined for the mailer in the application's `config/mail.php` configuration file:

```
 1use App\Mail\MailchimpTransport;

 2use Illuminate\Support\Facades\Mail;

 3use MailchimpTransactional\ApiClient;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Mail::extend('mailchimp', function (array $config = []) {

11        $client = new ApiClient;

12 

13        $client->setApiKey($config['key']);

14 

15        return new MailchimpTransport($client);

16    });

17}
```

Once your custom transport has been defined and registered, you may create a mailer definition within your application's `config/mail.php` configuration file that utilizes the new transport:

```
1'mailchimp' => [

2    'transport' => 'mailchimp',

3    'key' => env('MAILCHIMP_API_KEY'),

4    // ...

5],
```

### [Additional Symfony Transports](#additional-symfony-transports)

Laravel includes support for some existing Symfony maintained mail transports like Mailgun and Postmark. However, you may wish to extend Laravel with support for additional Symfony maintained transports. You can do so by requiring the necessary Symfony mailer via Composer and registering the transport with Laravel. For example, you may install and register the "Brevo" (formerly "Sendinblue") Symfony mailer:

```
1composer require symfony/brevo-mailer symfony/http-client
```

Once the Brevo mailer package has been installed, you may add an entry for your Brevo API credentials to your application's `services` configuration file:

```
1'brevo' => [

2    'key' => env('BREVO_API_KEY'),

3],
```

Next, you may use the `Mail` facade's `extend` method to register the transport with Laravel. Typically, this should be done within the `boot` method of a service provider:

```
 1use Illuminate\Support\Facades\Mail;

 2use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;

 3use Symfony\Component\Mailer\Transport\Dsn;

 4 

 5/**

 6 * Bootstrap any application services.

 7 */

 8public function boot(): void

 9{

10    Mail::extend('brevo', function () {

11        return (new BrevoTransportFactory)->create(

12            new Dsn(

13                'brevo+api',

14                'default',

15                config('services.brevo.key')

16            )

17        );

18    });

19}
```

Once your transport has been registered, you may create a mailer definition within your application's `config/mail.php` configuration file that utilizes the new transport:

```
1'brevo' => [

2    'transport' => 'brevo',

3    // ...

4],
```
