# Asset Bundling (Vite)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
  * [Installing Node](#installing-node)
  * [Installing Vite and the Laravel Plugin](#installing-vite-and-laravel-plugin)
  * [Configuring Vite](#configuring-vite)
  * [Loading Your Scripts and Styles](#loading-your-scripts-and-styles)
- [Running Vite](#running-vite)
- [Working With JavaScript](#working-with-scripts)
  * [Aliases](#aliases)
  * [Vue](#vue)
  * [React](#react)
  * [Svelte](#svelte)
  * [Inertia](#inertia)
  * [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Working With Fonts](#working-with-fonts)
  * [Font Providers](#font-providers)
  * [Local Fonts](#local-fonts)
  * [Font Options](#font-options)
- [Working With Blade and Routes](#working-with-blade-and-routes)
  * [Processing Static Assets With Vite](#blade-processing-static-assets)
  * [Refreshing on Save](#blade-refreshing-on-save)
  * [Aliases](#blade-aliases)
- [Asset Prefetching](#asset-prefetching)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Disabling Vite in Tests](#disabling-vite-in-tests)
- [Server-Side Rendering (SSR)](#ssr)
- [Script and Style Tag Attributes](#script-and-style-attributes)
  * [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  * [Subresource Integrity (SRI)](#subresource-integrity-sri)
  * [Arbitrary Attributes](#arbitrary-attributes)
- [Advanced Customization](#advanced-customization)
  * [Dev Server Cross-Origin Resource Sharing (CORS)](#cors)
  * [Correcting Dev Server URLs](#correcting-dev-server-urls)

## [Introduction](#introduction)

[Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production. When building applications with Laravel, you will typically use Vite to bundle your application's CSS and JavaScript files into production-ready assets.

Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production.

## [Installation & Setup](#installation)

The following documentation discusses how to manually install and configure the Laravel Vite plugin. However, Laravel's [starter kits](/docs/13.x/starter-kits) already include all of this scaffolding and are the fastest way to get started with Laravel and Vite.

### [Installing Node](#installing-node)

You must ensure that Node.js (16+) and NPM are installed before running Vite and the Laravel plugin:

```
1node -v

2npm -v
```

You can easily install the latest version of Node and NPM using simple graphical installers from [the official Node website](https://nodejs.org/en/download/). Or, if you are using [Laravel Sail](https://laravel.com/docs/13.x/sail), you may invoke Node and NPM through Sail:

```
1./vendor/bin/sail node -v

2./vendor/bin/sail npm -v
```

### [Installing Vite and the Laravel Plugin](#installing-vite-and-laravel-plugin)

Within a fresh installation of Laravel, you will find a `package.json` file in the root of your application's directory structure. The default `package.json` file already includes everything you need to get started using Vite and the Laravel plugin. You may install your application's frontend dependencies via NPM:

```
1npm install
```

### [Configuring Vite](#configuring-vite)

Vite is configured via a `vite.config.js` file in the root of your project. You are free to customize this file based on your needs, and you may also install any other plugins your application requires, such as `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte` or `@vitejs/plugin-vue`.

The Laravel Vite plugin requires you to specify the entry points for your application. These may be JavaScript or CSS files, and include preprocessed languages such as TypeScript, JSX, TSX, and Sass.

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel([

 7            'resources/css/app.css',

 8            'resources/js/app.js',

 9        ]),

10    ],

11});
```

If you are building an SPA, including applications built using Inertia, Vite works best without CSS entry points:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel([

 7            'resources/css/app.css',

 8            'resources/js/app.js',

 9        ]),

10    ],

11});
```

Instead, you should import your CSS via JavaScript. Typically, this would be done in your application's `resources/js/app.js` file:

```
1import './bootstrap';

2import '../css/app.css';
```

The Laravel plugin also supports multiple entry points and advanced configuration options such as [SSR entry points](#ssr).

#### [Working With a Secure Development Server](#working-with-a-secure-development-server)

If your local development web server is serving your application via HTTPS, you may run into issues connecting to the Vite development server.

If you are using [Laravel Herd](https://herd.laravel.com) and have secured the site or you are using [Laravel Valet](/docs/13.x/valet) and have run the [secure command](/docs/13.x/valet#securing-sites) against your application, the Laravel Vite plugin will automatically detect and use the generated TLS certificate for you.

If you secured the site using a host that does not match the application's directory name, you may manually specify the host in your application's `vite.config.js` file:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            // ...

 8            detectTls: 'my-app.test',

 9        }),

10    ],

11});
```

When using another web server, you should generate a trusted certificate and manually configure Vite to use the generated certificates:

```
 1// ...

 2import fs from 'fs';

 3 

 4const host = 'my-app.test';

 5 

 6export default defineConfig({

 7    // ...

 8    server: {

 9        host,

10        hmr: { host },

11        https: {

12            key: fs.readFileSync(`/path/to/${host}.key`),

13            cert: fs.readFileSync(`/path/to/${host}.crt`),

14        },

15    },

16});
```

If you are unable to generate a trusted certificate for your system, you may install and configure the [@vitejs/plugin-basic-ssl plugin](https://github.com/vitejs/vite-plugin-basic-ssl). When using untrusted certificates, you will need to accept the certificate warning for Vite's development server in your browser by following the "Local" link in your console when running the `npm run dev` command.

#### [Running the Development Server in Sail on WSL2](#configuring-hmr-in-sail-on-wsl2)

When running the Vite development server within [Laravel Sail](/docs/13.x/sail) on Windows Subsystem for Linux 2 (WSL2), you should add the following configuration to your `vite.config.js` file to ensure the browser can communicate with the development server:

```
 1// ...

 2 

 3export default defineConfig({

 4    // ...

 5    server: {

 6        hmr: {

 7            host: 'localhost',

 8        },

 9    },

10});
```

If your file changes are not being reflected in the browser while the development server is running, you may also need to configure Vite's [server.watch.usePolling option](https://vitejs.dev/config/server-options.html#server-watch).

### [Loading Your Scripts and Styles](#loading-your-scripts-and-styles)

With your Vite entry points configured, you may now reference them in a `@vite()` Blade directive that you add to the `<head>` of your application's root template:

```
1<!DOCTYPE html>

2<head>

3    {{-- ... --}}

4 

5    @vite(['resources/css/app.css', 'resources/js/app.js'])

6</head>
```

If you're importing your CSS via JavaScript, you only need to include the JavaScript entry point:

```
1<!DOCTYPE html>

2<head>

3    {{-- ... --}}

4 

5    @vite('resources/js/app.js')

6</head>
```

The `@vite` directive will automatically detect the Vite development server and inject the Vite client to enable Hot Module Replacement. In build mode, the directive will load your compiled and versioned assets, including any imported CSS.

If needed, you may also specify the build path of your compiled assets when invoking the `@vite` directive:

```
1<!doctype html>

2<head>

3    {{-- Given build path is relative to public path. --}}

4 

5    @vite('resources/js/app.js', 'vendor/courier/build')

6</head>
```

#### [Inline Assets](#inline-assets)

Sometimes it may be necessary to include the raw content of assets rather than linking to the versioned URL of the asset. For example, you may need to include asset content directly into your page when passing HTML content to a PDF generator. You may output the content of Vite assets using the `content` method provided by the `Vite` facade:

```
 1@use('Illuminate\Support\Facades\Vite')

 2 

 3<!doctype html>

 4<head>

 5    {{-- ... --}}

 6 

 7    <style>

 8        {!! Vite::content('resources/css/app.css') !!}

 9    </style>

10    <script>

11        {!! Vite::content('resources/js/app.js') !!}

12    </script>

13</head>
```

## [Running Vite](#running-vite)

There are two ways you can run Vite. You may run the development server via the `dev` command, which is useful while developing locally. The development server will automatically detect changes to your files and instantly reflect them in any open browser windows.

Or, running the `build` command will version and bundle your application's assets and get them ready for you to deploy to production:

```
1# Run the Vite development server...

2npm run dev

3 

4# Build and version the assets for production...

5npm run build
```

If you are running the development server in [Sail](/docs/13.x/sail) on WSL2, you may need some [additional configuration](#configuring-hmr-in-sail-on-wsl2) options.

## [Working With JavaScript](#working-with-scripts)

### [Aliases](#aliases)

By default, The Laravel plugin provides a common alias to help you hit the ground running and conveniently import your application's assets:

```
1{

2    '@' => '/resources/js'

3}
```

You may overwrite the `'@'` alias by adding your own to the `vite.config.js` configuration file:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel(['resources/ts/app.tsx']),

 7    ],

 8    resolve: {

 9        alias: {

10            '@': '/resources/ts',

11        },

12    },

13});
```

### [Vue](#vue)

If you would like to build your frontend using the [Vue](https://vuejs.org/) framework, then you will also need to install the `@vitejs/plugin-vue` plugin:

```
1npm install --save-dev @vitejs/plugin-vue
```

You may then include the plugin in your `vite.config.js` configuration file. There are a few additional options you will need when using the Vue plugin with Laravel:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3import vue from '@vitejs/plugin-vue';

 4 

 5export default defineConfig({

 6    plugins: [

 7        laravel(['resources/js/app.js']),

 8        vue({

 9            template: {

10                transformAssetUrls: {

11                    // The Vue plugin will re-write asset URLs, when referenced

12                    // in Single File Components, to point to the Laravel web

13                    // server. Setting this to `null` allows the Laravel plugin

14                    // to instead re-write asset URLs to point to the Vite

15                    // server instead.

16                    base: null,

17 

18                    // The Vue plugin will parse absolute URLs and treat them

19                    // as absolute paths to files on disk. Setting this to

20                    // `false` will leave absolute URLs un-touched so they can

21                    // reference assets in the public directory as expected.

22                    includeAbsolute: false,

23                },

24            },

25        }),

26    ],

27});
```

Laravel's [starter kits](/docs/13.x/starter-kits) already include the proper Laravel, Vue, and Vite configuration. These starter kits offer the fastest way to get started with Laravel, Vue, and Vite.

### [React](#react)

If you would like to build your frontend using the [React](https://reactjs.org/) framework, then you will also need to install the `@vitejs/plugin-react` plugin:

```
1npm install --save-dev @vitejs/plugin-react
```

You may then include the plugin in your `vite.config.js` configuration file:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3import react from '@vitejs/plugin-react';

 4 

 5export default defineConfig({

 6    plugins: [

 7        laravel(['resources/js/app.jsx']),

 8        react(),

 9    ],

10});
```

You will need to ensure that any files containing JSX have a `.jsx` or `.tsx` extension, remembering to update your entry point, if required, as [shown above](#configuring-vite).

You will also need to include the additional `@viteReactRefresh` Blade directive alongside your existing `@vite` directive.

```
1@viteReactRefresh

2@vite('resources/js/app.jsx')
```

The `@viteReactRefresh` directive must be called before the `@vite` directive.

Laravel's [starter kits](/docs/13.x/starter-kits) already include the proper Laravel, React, and Vite configuration. These starter kits offer the fastest way to get started with Laravel, React, and Vite.

### [Svelte](#svelte)

If you would like to build your frontend using the [Svelte](https://svelte.dev/) framework, then you will also need to install the `@sveltejs/vite-plugin-svelte` plugin:

```
1npm install --save-dev @sveltejs/vite-plugin-svelte
```

You may then include the plugin in your `vite.config.js` configuration file.

```
 1import { svelte } from '@sveltejs/vite-plugin-svelte';

 2import laravel from 'laravel-vite-plugin';

 3import { defineConfig } from 'vite';

 4 

 5export default defineConfig({

 6  plugins: [

 7    laravel({

 8      input: ['resources/js/app.ts'],

 9      ssr: 'resources/js/ssr.ts',

10      refresh: true,

11    }),

12    svelte(),

13  ],

14});
```

Laravel's [starter kits](/docs/13.x/starter-kits) already include the proper Laravel, Svelte, and Vite configuration. These starter kits offer the fastest way to get started with Laravel, Svelte, and Vite.

### [Inertia](#inertia)

The Laravel Vite plugin provides a convenient `resolvePageComponent` function to help you resolve your Inertia page components. Below is an example of the helper in use with Vue 3; however, you may also utilize the function in other frameworks such as React or Svelte:

```
 1import { createApp, h } from 'vue';

 2import { createInertiaApp } from '@inertiajs/vue3';

 3import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

 4 

 5createInertiaApp({

 6  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),

 7  setup({ el, App, props, plugin }) {

 8    createApp({ render: () => h(App, props) })

 9      .use(plugin)

10      .mount(el)

11  },

12});
```

If you are using Vite's code splitting feature with Inertia, we recommend configuring [asset prefetching](#asset-prefetching).

Laravel's [starter kits](/docs/13.x/starter-kits) already include the proper Laravel, Inertia, and Vite configuration. These starter kits offer the fastest way to get started with Laravel, Inertia, and Vite.

### [URL Processing](#url-processing)

When using Vite and referencing assets in your application's HTML, CSS, or JS, there are a couple of caveats to consider. First, if you reference assets with an absolute path, Vite will not include the asset in the build; therefore, you should ensure that the asset is available in your public directory. You should avoid using absolute paths when using a [dedicated CSS entrypoint](#configuring-vite) because, during development, browsers will try to load these paths from the Vite development server, where the CSS is hosted, rather than from your public directory.

When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite.

Consider the following project structure:

```
1public/

2  taylor.png

3resources/

4  js/

5    Pages/

6      Welcome.vue

7  images/

8    abigail.png
```

The following example demonstrates how Vite will treat relative and absolute URLs:

```
1<!-- This asset is not handled by Vite and will not be included in the build -->

2<img src="/taylor.png">

3 

4<!-- This asset will be re-written, versioned, and bundled by Vite -->

5<img src="../../images/abigail.png">
```

## [Working With Stylesheets](#working-with-stylesheets)

Laravel's [starter kits](/docs/13.x/starter-kits) already include the proper Tailwind and Vite configuration. Or, if you would like to use Tailwind and Laravel without using one of our starter kits, check out [Tailwind's installation guide for Laravel](https://tailwindcss.com/docs/guides/laravel).

All Laravel applications already include Tailwind and a properly configured `vite.config.js` file. So, you only need to start the Vite development server or run the `dev` Composer command, which will start both the Laravel and Vite development servers:

```
1composer run dev
```

Your application's CSS may be placed within the `resources/css/app.css` file.

## [Working With Fonts](#working-with-fonts)

The Laravel Vite plugin can serve optimized, self-hosted fonts for your application. When fonts are configured, the plugin resolves the requested font files, emits them as Vite assets, generates font CSS, and writes a font manifest that may be consumed by Blade's [`@fonts` directive](/docs/13.x/blade#fonts).

To configure fonts, import one or more provider helpers from `laravel-vite-plugin/fonts` and add them to the Laravel plugin's `fonts` option:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3import { google } from 'laravel-vite-plugin/fonts';

 4 

 5export default defineConfig({

 6    plugins: [

 7        laravel({

 8            input: 'resources/js/app.js',

 9            fonts: [

10                google('Inter', {

11                    alias: 'sans',

12                    weights: [400, 500, 600, 700],

13                    styles: ['normal', 'italic'],

14                    subsets: ['latin'],

15                    display: 'swap',

16                    preload: [

17                        { weight: 400 },

18                        { weight: 700 },

19                    ],

20                    fallbacks: ['system-ui', 'sans-serif'],

21                }),

22            ],

23        }),

24    ],

25});
```

In this example, the `Inter` font will be available through the `sans` alias. The plugin will generate a `--font-sans` CSS variable and a `.font-sans` utility class that applies the generated font stack.

### [Font Providers](#font-providers)

The Laravel Vite plugin includes provider helpers for Google Fonts, Bunny Fonts, Fontsource, and local fonts:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3import { bunny, fontsource, google, local } from 'laravel-vite-plugin/fonts';

 4 

 5export default defineConfig({

 6    plugins: [

 7        laravel({

 8            input: 'resources/js/app.js',

 9            fonts: [

10                google('Inter', { alias: 'sans' }),

11                bunny('Figtree', { alias: 'body' }),

12                fontsource('JetBrains Mono', { alias: 'mono' }),

13                local('Brand Sans', {

14                    alias: 'brand',

15                    src: 'resources/fonts/brand-sans',

16                }),

17            ],

18        }),

19    ],

20});
```

The `fontsource` provider reads fonts from an installed Fontsource package. By default, the package name is derived from the font family, such as `@fontsource/jetbrains-mono`. If your application uses a different package name, you may specify it using the `package` option.

### [Local Fonts](#local-fonts)

When using local fonts, the `src` option may point to a single font file, a directory, or a glob pattern. The plugin will discover supported font files and infer their weight and style from their filenames:

```
1local('Brand Sans', {

2    alias: 'brand',

3    src: 'resources/fonts/brand-sans/*.woff2',

4})
```

If you need full control over the available variants, you may define them explicitly using the `variants` option:

```
1local('Brand Sans', {

2    alias: 'brand',

3    variants: [

4        { src: 'resources/fonts/BrandSans-Regular.woff2', weight: 400 },

5        { src: 'resources/fonts/BrandSans-Italic.woff2', weight: 400, style: 'italic' },

6        { src: ['resources/fonts/BrandSans-Bold.woff2', 'resources/fonts/BrandSans-Bold.ttf'], weight: 700 },

7    ],

8})
```

### [Font Options](#font-options)

Depending on the provider, font definitions may accept several options that allow you to customize the generated font CSS:

- `alias` defines the name used by Blade's `@fonts` directive and defaults to a slug of the font family.
- `variable` defines the generated CSS variable and defaults to `--font-{alias}`.
- `weights` defines the remote or Fontsource font weights that should be resolved and defaults to `[400]`.
- `styles` defines the remote or Fontsource font styles that should be resolved and defaults to `['normal']`.
- `subsets` defines the remote or Fontsource font subsets that should be resolved and defaults to `['latin']`.
- `display` defines the `font-display` value and defaults to `swap`.
- `preload` controls which WOFF2 font variants should be preloaded. This option may be `true`, `false`, or an array of `{ weight, style }` selectors.
- `fallbacks` defines additional fallback fonts that should be appended to the generated font stack.
- `optimizedFallbacks` attempts to generate metric-adjusted fallback font faces using the optional `fontaine` package and defaults to `true`.

Optimized fallbacks require the `fontaine` package, which is not installed by default. If you want Laravel to generate metric-adjusted fallback font faces, you should install `fontaine` as a development dependency:

```
1npm install --save-dev fontaine
```

If `fontaine` is not installed or cannot read a font file, Laravel will skip the optimized fallback for that font and continue using any fonts configured via the `fallbacks` option.

Local fonts are resolved from the `src` or `variants` options described above instead of using `weights`, `styles`, and `subsets`.

## [Working With Blade and Routes](#working-with-blade-and-routes)

### [Processing Static Assets With Vite](#blade-processing-static-assets)

When referencing assets in your JavaScript or CSS, Vite automatically processes and versions them. In addition, when building Blade-based applications, Vite can also process and version static assets that you reference solely in Blade templates.

However, to accomplish this, you need to make Vite aware of your assets by specifying them in the plugin's `assets` option. This option is intended for static files that you want to reference directly with `Vite::asset`. If you want Laravel to generate font CSS and preload links, use the [`fonts` option](#working-with-fonts) instead.

For example, if you want to process and version all images stored in `resources/images` and all fonts stored in `resources/fonts`, you should add the following to your Vite configuration:

```
1laravel({

2    input: 'resources/js/app.js',

3    assets: ['resources/images/**', 'resources/fonts/**'],

4})
```

These assets will now be processed by Vite when running `npm run build`. You can then reference these assets in Blade templates using the `Vite::asset` method, which will return the versioned URL for a given asset:

```
1<img src="{{ Vite::asset('resources/images/logo.png') }}">
```

Prior to version 3 of the Laravel Vite plugin, static assets had to be imported in your application's entry point using `import.meta.glob`. The `assets` option was introduced due to changes in Vite 8.

### [Refreshing on Save](#blade-refreshing-on-save)

When your application is built using traditional server-side rendering with Blade, Vite can improve your development workflow by automatically refreshing the browser when you make changes to view files in your application. To get started, you can simply specify the `refresh` option as `true`.

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            // ...

 8            refresh: true,

 9        }),

10    ],

11});
```

When the `refresh` option is `true`, saving files in the following directories will trigger the browser to perform a full page refresh while you are running `npm run dev`:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

Watching the `routes/**` directory is useful if you are utilizing [Ziggy](https://github.com/tighten/ziggy) to generate route links within your application's frontend.

If these default paths do not suit your needs, you can specify your own list of paths to watch:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            // ...

 8            refresh: ['resources/views/**'],

 9        }),

10    ],

11});
```

Under the hood, the Laravel Vite plugin uses the [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) package, which offers some advanced configuration options to fine-tune this feature's behavior. If you need this level of customization, you may provide a `config` definition:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            // ...

 8            refresh: [{

 9                paths: ['path/to/watch/**'],

10                config: { delay: 300 }

11            }],

12        }),

13    ],

14});
```

### [Aliases](#blade-aliases)

It is common in JavaScript applications to [create aliases](#aliases) to regularly referenced directories. But, you may also create aliases to use in Blade by using the `macro` method on the `Illuminate\Support\Facades\Vite` class. Typically, "macros" should be defined within the `boot` method of a [service provider](/docs/13.x/providers):

```
1/**

2 * Bootstrap any application services.

3 */

4public function boot(): void

5{

6    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));

7}
```

Once a macro has been defined, it can be invoked within your templates. For example, we can use the `image` macro defined above to reference an asset located at `resources/images/logo.png`:

```
1<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```

## [Asset Prefetching](#asset-prefetching)

When building an SPA using Vite's code splitting feature, required assets are fetched on each page navigation. This behavior can lead to delayed UI rendering. If this is a problem for your frontend framework of choice, Laravel offers the ability to eagerly prefetch your application's JavaScript and CSS assets on initial page load.

You can instruct Laravel to eagerly prefetch your assets by invoking the `Vite::prefetch` method in the `boot` method of a [service provider](/docs/13.x/providers):

```
 1<?php

 2 

 3namespace App\Providers;

 4 

 5use Illuminate\Support\Facades\Vite;

 6use Illuminate\Support\ServiceProvider;

 7 

 8class AppServiceProvider extends ServiceProvider

 9{

10    /**

11     * Register any application services.

12     */

13    public function register(): void

14    {

15        // ...

16    }

17 

18    /**

19     * Bootstrap any application services.

20     */

21    public function boot(): void

22    {

23        Vite::prefetch(concurrency: 3);

24    }

25}
```

In the example above, assets will be prefetched with a maximum of `3` concurrent downloads on each page load. You can modify the concurrency to suit your application's needs or specify no concurrency limit if the application should download all assets at once:

```
1/**

2 * Bootstrap any application services.

3 */

4public function boot(): void

5{

6    Vite::prefetch();

7}
```

By default, prefetching will begin when the [page *load* event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) fires. If you would like to customize when prefetching begins, you may specify an event that Vite will listen for:

```
1/**

2 * Bootstrap any application services.

3 */

4public function boot(): void

5{

6    Vite::prefetch(event: 'vite:prefetch');

7}
```

Given the code above, prefetching will now begin when you manually dispatch the `vite:prefetch` event on the `window` object. For example, you could have prefetching begin three seconds after the page loads:

```
1<script>

2    addEventListener('load', () => setTimeout(() => {

3        dispatchEvent(new Event('vite:prefetch'))

4    }, 3000))

5</script>
```

## [Custom Base URLs](#custom-base-urls)

If your Vite compiled assets are deployed to a domain separate from your application, such as via a CDN, you must specify the `ASSET_URL` environment variable within your application's `.env` file:

```
1ASSET_URL=https://cdn.example.com
```

After configuring the asset URL, all re-written URLs to your assets will be prefixed with the configured value:

```
1https://cdn.example.com/build/assets/app.9dce8d17.js
```

Remember that [absolute URLs are not re-written by Vite](#url-processing), so they will not be prefixed.

## [Environment Variables](#environment-variables)

You may inject environment variables into your JavaScript by prefixing them with `VITE_` in your application's `.env` file:

```
1VITE_SENTRY_DSN_PUBLIC=http://example.com
```

You may access injected environment variables via the `import.meta.env` object:

```
1import.meta.env.VITE_SENTRY_DSN_PUBLIC
```

## [Disabling Vite in Tests](#disabling-vite-in-tests)

Laravel's Vite integration will attempt to resolve your assets while running your tests, which requires you to either run the Vite development server or build your assets.

If you would prefer to mock Vite during testing, you may call the `withoutVite` method, which is available for any tests that extend Laravel's `TestCase` class:

Pest

PHPUnit

```
1test('without vite example', function () {

2    $this->withoutVite();

3 

4    // ...

5});
```

```
 1use Tests\TestCase;

 2 

 3class ExampleTest extends TestCase

 4{

 5    public function test_without_vite_example(): void

 6    {

 7        $this->withoutVite();

 8 

 9        // ...

10    }

11}
```

If you would like to disable Vite for all tests, you may call the `withoutVite` method from the `setUp` method on your base `TestCase` class:

```
 1<?php

 2 

 3namespace Tests;

 4 

 5use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

 6 

 7abstract class TestCase extends BaseTestCase

 8{

 9    protected function setUp(): void

10    {

11        parent::setUp();

12 

13        $this->withoutVite();

14    }

15}
```

## [Server-Side Rendering (SSR)](#ssr)

The Laravel Vite plugin makes it painless to set up server-side rendering with Vite. To get started, create an SSR entry point at `resources/js/ssr.js` and specify the entry point by passing a configuration option to the Laravel plugin:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            input: 'resources/js/app.js',

 8            ssr: 'resources/js/ssr.js',

 9        }),

10    ],

11});
```

To ensure you don't forget to rebuild the SSR entry point, we recommend augmenting the "build" script in your application's `package.json` to create your SSR build:

```
1"scripts": {

2     "dev": "vite",

3     "build": "vite build"

4     "build": "vite build && vite build --ssr"

5}
```

Then, to build and start the SSR server, you may run the following commands:

```
1npm run build

2node bootstrap/ssr/ssr.js
```

If you are using [SSR with Inertia](https://inertiajs.com/server-side-rendering), you may instead use the `inertia:start-ssr` Artisan command to start the SSR server:

```
1php artisan inertia:start-ssr
```

Laravel's [starter kits](/docs/13.x/starter-kits) already include the proper Laravel, Inertia SSR, and Vite configuration. These starter kits offer the fastest way to get started with Laravel, Inertia SSR, and Vite.

## [Script and Style Tag Attributes](#script-and-style-attributes)

### [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)

If you wish to include a [nonce attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) on your script and style tags as part of your [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), you may generate or specify a nonce using the `useCspNonce` method within a custom [middleware](/docs/13.x/middleware):

```
 1<?php

 2 

 3namespace App\Http\Middleware;

 4 

 5use Closure;

 6use Illuminate\Http\Request;

 7use Illuminate\Support\Facades\Vite;

 8use Symfony\Component\HttpFoundation\Response;

 9 

10class AddContentSecurityPolicyHeaders

11{

12    /**

13     * Handle an incoming request.

14     *

15     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next

16     */

17    public function handle(Request $request, Closure $next): Response

18    {

19        Vite::useCspNonce();

20 

21        return $next($request)->withHeaders([

22            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",

23        ]);

24    }

25}
```

After invoking the `useCspNonce` method, Laravel will automatically include the `nonce` attributes on all generated script and style tags.

If you need to specify the nonce elsewhere, including the [Ziggy `@route` directive](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy) included with Laravel's [starter kits](/docs/13.x/starter-kits), you may retrieve it using the `cspNonce` method:

```
1@routes(nonce: Vite::cspNonce())
```

If you already have a nonce that you would like to instruct Laravel to use, you may pass the nonce to the `useCspNonce` method:

```
1Vite::useCspNonce($nonce);
```

### [Subresource Integrity (SRI)](#subresource-integrity-sri)

If your Vite manifest includes `integrity` hashes for your assets, Laravel will automatically add the `integrity` attribute on any script and style tags it generates in order to enforce [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). By default, Vite does not include the `integrity` hash in its manifest, but you may enable it by installing the [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM plugin:

```
1npm install --save-dev vite-plugin-manifest-sri
```

You may then enable this plugin in your `vite.config.js` file:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3import manifestSRI from 'vite-plugin-manifest-sri';

 4 

 5export default defineConfig({

 6    plugins: [

 7        laravel({

 8            // ...

 9        }),

10        manifestSRI(),

11    ],

12});
```

If required, you may also customize the manifest key where the integrity hash can be found:

```
1use Illuminate\Support\Facades\Vite;

2 

3Vite::useIntegrityKey('custom-integrity-key');
```

If you would like to disable this auto-detection completely, you may pass `false` to the `useIntegrityKey` method:

```
1Vite::useIntegrityKey(false);
```

### [Arbitrary Attributes](#arbitrary-attributes)

If you need to include additional attributes on your script and style tags, such as the [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) attribute, you may specify them via the `useScriptTagAttributes` and `useStyleTagAttributes` methods. Typically, this methods should be invoked from a [service provider](/docs/13.x/providers):

```
 1use Illuminate\Support\Facades\Vite;

 2 

 3Vite::useScriptTagAttributes([

 4    'data-turbo-track' => 'reload', // Specify a value for the attribute...

 5    'async' => true, // Specify an attribute without a value...

 6    'integrity' => false, // Exclude an attribute that would otherwise be included...

 7]);

 8 

 9Vite::useStyleTagAttributes([

10    'data-turbo-track' => 'reload',

11]);
```

If you need to conditionally add attributes, you may pass a callback that will receive the asset source path, its URL, its manifest chunk, and the entire manifest:

```
1use Illuminate\Support\Facades\Vite;

2 

3Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [

4    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,

5]);

6 

7Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [

8    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,

9]);
```

The `$chunk` and `$manifest` arguments will be `null` while the Vite development server is running.

## [Advanced Customization](#advanced-customization)

Out of the box, Laravel's Vite plugin uses sensible conventions that should work for the majority of applications; however, sometimes you may need to customize Vite's behavior. To enable additional customization options, we offer the following methods and options which can be used in place of the `@vite` Blade directive:

```
 1<!doctype html>

 2<head>

 3    {{-- ... --}}

 4 

 5    {{

 6        Vite::useHotFile(storage_path('vite.hot')) // Customize the "hot" file...

 7            ->useBuildDirectory('bundle') // Customize the build directory...

 8            ->useManifestFilename('assets.json') // Customize the manifest filename...

 9            ->withEntryPoints(['resources/js/app.js']) // Specify the entry points...

10            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // Customize the backend path generation for built assets...

11                return "https://cdn.example.com/{$path}";

12            })

13    }}

14</head>
```

Within the `vite.config.js` file, you should then specify the same configuration:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            hotFile: 'storage/vite.hot', // Customize the "hot" file...

 8            buildDirectory: 'bundle', // Customize the build directory...

 9            input: ['resources/js/app.js'], // Specify the entry points...

10        }),

11    ],

12    build: {

13      manifest: 'assets.json', // Customize the manifest filename...

14    },

15});
```

### [Dev Server Cross-Origin Resource Sharing (CORS)](#cors)

If you are experiencing Cross-Origin Resource Sharing (CORS) issues in the browser while fetching assets from the Vite dev server, you may need to grant your custom origin access to the dev server. Vite combined with the Laravel plugin allows the following origins without any additional configuration:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- `APP_URL` in the project's `.env`

The easiest way to allow a custom origin for your project is to ensure that your application's `APP_URL` environment variable matches the origin you are visiting in your browser. For example, if you visiting `https://my-app.laravel`, you should update your `.env` to match:

```
1APP_URL=https://my-app.laravel
```

If you need more fine-grained control over the origins, such as supporting multiple origins, you should utilize [Vite's comprehensive and flexible built-in CORS server configuration](https://vite.dev/config/server-options.html#server-cors). For example, you may specify multiple origins in the `server.cors.origin` configuration option in the project's `vite.config.js` file:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            input: 'resources/js/app.js',

 8            refresh: true,

 9        }),

10    ],

11    server: {

12        cors: {

13            origin: [

14                'https://backend.laravel',

15                'http://admin.laravel:8566',

16            ],

17        },

18    },

19});
```

You may also include regex patterns, which can be helpful if you would like to allow all origins for a given top-level domain, such as `*.laravel`:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3 

 4export default defineConfig({

 5    plugins: [

 6        laravel({

 7            input: 'resources/js/app.js',

 8            refresh: true,

 9        }),

10    ],

11    server: {

12        cors: {

13            origin: [

14                // Supports: SCHEME://DOMAIN.laravel[:PORT]

15                /^https?:\/\/.*\.laravel(:\d+)?$/,

16            ],

17        },

18    },

19});
```

### [Correcting Dev Server URLs](#correcting-dev-server-urls)

Some plugins within the Vite ecosystem assume that URLs which begin with a forward-slash will always point to the Vite dev server. However, due to the nature of the Laravel integration, this is not the case.

For example, the `vite-imagetools` plugin outputs URLs like the following while Vite is serving your assets:

```
1<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```

The `vite-imagetools` plugin is expecting that the output URL will be intercepted by Vite and the plugin may then handle all URLs that start with `/@imagetools`. If you are using plugins that are expecting this behavior, you will need to manually correct the URLs. You can do this in your `vite.config.js` file by using the `transformOnServe` option.

In this particular example, we will prepend the dev server URL to all occurrences of `/@imagetools` within the generated code:

```
 1import { defineConfig } from 'vite';

 2import laravel from 'laravel-vite-plugin';

 3import { imagetools } from 'vite-imagetools';

 4 

 5export default defineConfig({

 6    plugins: [

 7        laravel({

 8            // ...

 9            transformOnServe: (code, devServerUrl) => code.replaceAll('/@imagetools', devServerUrl+'/@imagetools'),

10        }),

11        imagetools(),

12    ],

13});
```

Now, while Vite is serving Assets, it will output URLs that point to the Vite dev server:

```
1- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">

2+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```
