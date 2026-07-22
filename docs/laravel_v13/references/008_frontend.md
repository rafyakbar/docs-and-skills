# Frontend

- [Introduction](#introduction)
- [Using PHP](#using-php)
  * [PHP and Blade](#php-and-blade)
  * [Livewire](#livewire)
  * [Starter Kits](#php-starter-kits)
- [Using React, Svelte, or Vue](#using-react-svelte-or-vue)
  * [Inertia](#inertia)
  * [Starter Kits](#inertia-starter-kits)
- [Bundling Assets](#bundling-assets)

## [Introduction](#introduction)

Laravel is a backend framework that provides all of the features you need to build modern web applications, such as [routing](/docs/13.x/routing), [validation](/docs/13.x/validation), [caching](/docs/13.x/cache), [queues](/docs/13.x/queues), [file storage](/docs/13.x/filesystem), and more. However, we believe it's important to offer developers a beautiful full-stack experience, including powerful approaches for building your application's frontend.

There are two primary ways to tackle frontend development when building an application with Laravel, and which approach you choose is determined by whether you would like to build your frontend by leveraging PHP or by using JavaScript frameworks such as React, Svelte, and Vue. We'll discuss both of these options below so that you can make an informed decision regarding the best approach to frontend development for your application.

## [Using PHP](#using-php)

### [PHP and Blade](#php-and-blade)

In the past, most PHP applications rendered HTML to the browser using simple HTML templates interspersed with PHP `echo` statements which render data that was retrieved from a database during the request:

```
1<div>

2    <?php foreach ($users as $user): ?>

3        Hello, <?php echo $user->name; ?> <br />

4    <?php endforeach; ?>

5</div>
```

In Laravel, this approach to rendering HTML can still be achieved using [views](/docs/13.x/views) and [Blade](/docs/13.x/blade). Blade is an extremely light-weight templating language that provides convenient, short syntax for displaying data, iterating over data, and more:

```
1<div>

2    @foreach ($users as $user)

3        Hello, {{ $user->name }} <br />

4    @endforeach

5</div>
```

When building applications in this fashion, form submissions and other page interactions typically receive an entirely new HTML document from the server and the entire page is re-rendered by the browser. Even today, many applications may be perfectly suited to having their frontends constructed in this way using simple Blade templates.

#### [Growing Expectations](#growing-expectations)

However, as user expectations regarding web applications have matured, many developers have found the need to build more dynamic frontends with interactions that feel more polished. In light of this, some developers choose to begin building their application's frontend using JavaScript frameworks such as React, Svelte, and Vue.

Others, preferring to stick with the backend language they are comfortable with, have developed solutions that allow the construction of modern web application UIs while still primarily utilizing their backend language of choice. For example, in the [Rails](https://rubyonrails.org/) ecosystem, this has spurred the creation of libraries such as [Turbo](https://turbo.hotwired.dev/) [Hotwire](https://hotwired.dev/), and [Stimulus](https://stimulus.hotwired.dev/).

Within the Laravel ecosystem, the need to create modern, dynamic frontends by primarily using PHP has led to the creation of [Laravel Livewire](https://livewire.laravel.com) and [Alpine.js](https://alpinejs.dev/).

### [Livewire](#livewire)

[Laravel Livewire](https://livewire.laravel.com) is a framework for building Laravel powered frontends that feel dynamic, modern, and alive just like frontends built with modern JavaScript frameworks like React, Svelte, and Vue.

When using Livewire, you will create Livewire "components" that render a discrete portion of your UI and expose methods and data that can be invoked and interacted with from your application's frontend. For example, a simple "Counter" component might look like the following:

```
 1<?php

 2 

 3use Livewire\Component;

 4 

 5new class extends Component

 6{

 7    public $count = 0;

 8 

 9    public function increment()

10    {

11        $this->count++;

12    }

13};

14?>

15 

16<div>

17    <button wire:click="increment">+</button>

18    <h1>{{ $count }}</h1>

19</div>
```

As you can see, Livewire enables you to write new HTML attributes such as `wire:click` that connect your Laravel application's frontend and backend. In addition, you can render your component's current state using simple Blade expressions.

For many, Livewire has revolutionized frontend development with Laravel, allowing them to stay within the comfort of Laravel while constructing modern, dynamic web applications. Typically, developers using Livewire will also utilize [Alpine.js](https://alpinejs.dev/) to "sprinkle" JavaScript onto their frontend only where it is needed, such as in order to render a dialog window.

If you're new to Laravel, we recommend getting familiar with the basic usage of [views](/docs/13.x/views) and [Blade](/docs/13.x/blade). Then, consult the official [Laravel Livewire documentation](https://livewire.laravel.com/docs) to learn how to take your application to the next level with interactive Livewire components.

### [Starter Kits](#php-starter-kits)

If you would like to build your frontend using PHP and Livewire, you can leverage our [Livewire starter kit](/docs/13.x/starter-kits) to jump-start your application's development.

## [Using React, Svelte, or Vue](#using-react-svelte-or-vue)

Although it's possible to build modern frontends using Laravel and Livewire, many developers still prefer to leverage the power of a JavaScript framework like React, Svelte, or Vue. This allows developers to take advantage of the rich ecosystem of JavaScript packages and tools available via NPM.

However, without additional tooling, pairing Laravel with React, Svelte, or Vue would leave us needing to solve a variety of complicated problems such as client-side routing, data hydration, and authentication. Client-side routing is often simplified by using opinionated React / Svelte / Vue frameworks such as [Next](https://nextjs.org/) and [Nuxt](https://nuxt.com/); however, data hydration and authentication remain complicated and cumbersome problems to solve when pairing a backend framework like Laravel with these frontend frameworks.

In addition, developers are left maintaining two separate code repositories, often needing to coordinate maintenance, releases, and deployments across both repositories. While these problems are not insurmountable, we don't believe it's a productive or enjoyable way to develop applications.

### [Inertia](#inertia)

Thankfully, Laravel offers the best of both worlds. [Inertia](https://inertiajs.com) bridges the gap between your Laravel application and your modern React, Svelte, or Vue frontend, allowing you to build full-fledged, modern frontends using React, Svelte, or Vue while leveraging Laravel routes and controllers for routing, data hydration, and authentication — all within a single code repository. With this approach, you can enjoy the full power of both Laravel and React / Svelte / Vue without crippling the capabilities of either tool.

After installing Inertia into your Laravel application, you will write routes and controllers like normal. However, instead of returning a Blade template from your controller, you will return an Inertia page:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use App\Models\User;

 6use Inertia\Inertia;

 7use Inertia\Response;

 8 

 9class UserController extends Controller

10{

11    /**

12     * Show the profile for a given user.

13     */

14    public function show(string $id): Response

15    {

16        return Inertia::render('users/show', [

17            'user' => User::findOrFail($id)

18        ]);

19    }

20}
```

An Inertia page corresponds to a React, Svelte, or Vue component, typically stored within the `resources/js/pages` directory of your application. The data given to the page via the `Inertia::render` method will be used to hydrate the "props" of the page component:

```
 1import Layout from '@/layouts/authenticated';

 2import { Head } from '@inertiajs/react';

 3 

 4export default function Show({ user }) {

 5    return (

 6        <Layout>

 7            <Head title="Welcome" />

 8            <h1>Welcome</h1>

 9            <p>Hello {user.name}, welcome to Inertia.</p>

10        </Layout>

11    )

12}
```

As you can see, Inertia allows you to leverage the full power of React, Svelte, or Vue when building your frontend, while providing a light-weight bridge between your Laravel powered backend and your JavaScript powered frontend.

#### Server-Side Rendering

If you're concerned about diving into Inertia because your application requires server-side rendering, don't worry. Inertia offers [server-side rendering support](https://inertiajs.com/server-side-rendering). And, when deploying your application via [Laravel Cloud](https://cloud.laravel.com) or [Laravel Forge](https://forge.laravel.com), it's a breeze to ensure that Inertia's server-side rendering process is always running.

### [Starter Kits](#inertia-starter-kits)

If you would like to build your frontend using Inertia and React / Svelte / Vue, you can leverage our [React, Svelte, or Vue application starter kits](/docs/13.x/starter-kits) to jump-start your application's development. All of these starter kits scaffold your application's backend and frontend authentication flow using Inertia, React / Svelte / Vue, [Tailwind](https://tailwindcss.com), and [Vite](https://vitejs.dev) so that you can start building your next big idea.

## [Bundling Assets](#bundling-assets)

Regardless of whether you choose to develop your frontend using Blade and Livewire or React / Svelte / Vue and Inertia, you will likely need to bundle your application's CSS into production-ready assets. Of course, if you choose to build your application's frontend with React, Svelte, or Vue, you will also need to bundle your components into browser ready JavaScript assets.

By default, Laravel utilizes [Vite](https://vitejs.dev) to bundle your assets. Vite provides lightning-fast build times and near instantaneous Hot Module Replacement (HMR) during local development. In all new Laravel applications, including those using our [starter kits](/docs/13.x/starter-kits), you will find a `vite.config.js` file that loads our light-weight Laravel Vite plugin that makes Vite a joy to use with Laravel applications.

The fastest way to get started with Laravel and Vite is by beginning your application's development using [our application starter kits](/docs/13.x/starter-kits), which jump-starts your application by providing frontend and backend authentication scaffolding.

For more detailed documentation on utilizing Vite with Laravel, please see our [dedicated documentation on bundling and compiling your assets](/docs/13.x/vite).
