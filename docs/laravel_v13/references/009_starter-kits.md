# Starter Kits

- [Introduction](#introduction)
- [Creating an Application Using a Starter Kit](#creating-an-application)
- [Available Starter Kits](#available-starter-kits)
  * [React](#react)
  * [Svelte](#svelte)
  * [Vue](#vue)
  * [Livewire](#livewire)
- [Starter Kit Customization](#starter-kit-customization)
  * [React](#react-customization)
  * [Svelte](#svelte-customization)
  * [Vue](#vue-customization)
  * [Livewire](#livewire-customization)
- [Authentication](#authentication)
  * [Enabling and Disabling Features](#enabling-and-disabling-features)
  * [Customizing User Creation and Password Reset](#customizing-actions)
  * [Two-Factor Authentication](#two-factor-authentication)
  * [Rate Limiting](#rate-limiting)
- [Teams](#teams)
- [WorkOS AuthKit Authentication](#workos)
- [Inertia SSR](#inertia-ssr)
- [Community Maintained Starter Kits](#community-maintained-starter-kits)
- [Frequently Asked Questions](#faqs)

## [Introduction](#introduction)

To give you a head start building your new Laravel application, we are happy to offer [application starter kits](https://laravel.com/starter-kits). These starter kits give you a head start on building your next Laravel application, and include the routes, controllers, and views you need to register and authenticate your application's users. The starter kits use [Laravel Fortify](/docs/13.x/fortify) to provide authentication.

While you are welcome to use these starter kits, they are not required. You are free to build your own application from the ground up by simply installing a fresh copy of Laravel. Either way, we know you will build something great!

## [Creating an Application Using a Starter Kit](#creating-an-application)

To create a new Laravel application using one of our starter kits, you should first [install PHP and the Laravel CLI tool](/docs/13.x/installation#installing-php). If you already have PHP and Composer installed, you may install the Laravel installer CLI tool via Composer:

```
1composer global require laravel/installer
```

Then, create a new Laravel application using the Laravel installer CLI. The Laravel installer will prompt you to select your preferred starter kit:

```
1laravel new my-app
```

After creating your Laravel application, you only need to install its frontend dependencies via NPM and start the Laravel development server:

```
1cd my-app

2npm install && npm run build

3composer run dev
```

Once you have started the Laravel development server, your application will be accessible in your web browser at <http://localhost:8000>.

## [Available Starter Kits](#available-starter-kits)

### [React](#react)

Our React starter kit provides a robust, modern starting point for building Laravel applications with a React frontend using [Inertia](https://inertiajs.com).

Inertia allows you to build modern, single-page React applications using classic server-side routing and controllers. This lets you enjoy the frontend power of React combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation.

The React starter kit utilizes React 19, TypeScript, Tailwind, and the [shadcn/ui](https://ui.shadcn.com) component library.

### [Svelte](#svelte)

Our Svelte starter kit provides a robust, modern starting point for building Laravel applications with a Svelte frontend using [Inertia](https://inertiajs.com).

Inertia allows you to build modern, single-page Svelte applications using classic server-side routing and controllers. This lets you enjoy the frontend power of Svelte combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation.

The Svelte starter kit utilizes Svelte 5, TypeScript, Tailwind, and the [shadcn-svelte](https://www.shadcn-svelte.com/) component library.

### [Vue](#vue)

Our Vue starter kit provides a great starting point for building Laravel applications with a Vue frontend using [Inertia](https://inertiajs.com).

Inertia allows you to build modern, single-page Vue applications using classic server-side routing and controllers. This lets you enjoy the frontend power of Vue combined with the incredible backend productivity of Laravel and lightning-fast Vite compilation.

The Vue starter kit utilizes the Vue Composition API, TypeScript, Tailwind, and the [shadcn-vue](https://www.shadcn-vue.com/) component library.

### [Livewire](#livewire)

Our Livewire starter kit provides the perfect starting point for building Laravel applications with a [Laravel Livewire](https://livewire.laravel.com) frontend.

Livewire is a powerful way of building dynamic, reactive, frontend UIs using just PHP. It's a great fit for teams that primarily use Blade templates and are looking for a simpler alternative to JavaScript-driven SPA frameworks like React, Svelte, and Vue.

The Livewire starter kit utilizes Livewire, Tailwind, and the [Flux UI](https://fluxui.dev) component library.

## [Starter Kit Customization](#starter-kit-customization)

### [React](#react-customization)

Our React starter kit is built with Inertia 3, React 19, Tailwind 4, and [shadcn/ui](https://ui.shadcn.com). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization.

The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application:

```
1resources/js/

2├── components/    # Reusable React components

3├── hooks/         # React hooks

4├── layouts/       # Application layouts

5├── lib/           # Utility functions and configuration

6├── pages/         # Page components

7└── types/         # TypeScript definitions
```

To publish additional shadcn components, first [find the component you want to publish](https://ui.shadcn.com). Then, publish the component using `npx`:

```
1npx shadcn@latest add switch
```

In this example, the command will publish the Switch component to `resources/js/components/ui/switch.tsx`. Once the component has been published, you can use it in any of your pages:

```
 1import { Switch } from "@/components/ui/switch"

 2 

 3const MyPage = () => {

 4  return (

 5    <div>

 6      <Switch />

 7    </div>

 8  );

 9};

10 

11export default MyPage;
```

#### [Available Layouts](#react-available-layouts)

The React starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/app-layout.tsx` file:

```
1import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout';

2import AppLayoutTemplate from '@/layouts/app/app-header-layout';
```

#### [Sidebar Variants](#react-sidebar-variants)

The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/app-sidebar.tsx` component:

```
1<Sidebar collapsible="icon" variant="sidebar">

2<Sidebar collapsible="icon" variant="inset">
```

#### [Authentication Page Layout Variants](#react-authentication-page-layout-variants)

The authentication pages included with the React starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split".

To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/auth-layout.tsx` file:

```
1import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout';

2import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout';
```

### [Svelte](#svelte-customization)

Our Svelte starter kit is built with Inertia 3, Svelte 5, Tailwind, and [shadcn-svelte](https://www.shadcn-svelte.com/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization.

The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application:

```
1resources/js/

2├── components/    # Reusable Svelte components

3├── layouts/       # Application layouts

4├── lib/           # Utility functions and configuration and Svelte rune modules

5├── pages/         # Page components

6└── types/         # TypeScript definitions
```

To publish additional shadcn-svelte components, first [find the component you want to publish](https://www.shadcn-svelte.com). Then, publish the component using `npx`:

```
1npx shadcn-svelte@latest add switch
```

In this example, the command will publish the Switch component to `resources/js/components/ui/switch/switch.svelte`. Once the component has been published, you can use it in any of your pages:

```
1<script lang="ts">

2    import { Switch } from '@/components/ui/switch'

3</script>

4 

5<div>

6    <Switch />

7</div>
```

#### [Available Layouts](#svelte-available-layouts)

The Svelte starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/AppLayout.svelte` file:

```
1import AppLayout from '@/layouts/app/AppSidebarLayout.svelte';

2import AppLayout from '@/layouts/app/AppHeaderLayout.svelte';
```

#### [Sidebar Variants](#svelte-sidebar-variants)

The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/AppSidebar.svelte` component:

```
1<Sidebar collapsible="icon" variant="sidebar">

2<Sidebar collapsible="icon" variant="inset">
```

#### [Authentication Page Layout Variants](#svelte-authentication-page-layout-variants)

The authentication pages included with the Svelte starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split".

To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/AuthLayout.svelte` file:

```
1import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte';

2import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte';
```

### [Vue](#vue-customization)

Our Vue starter kit is built with Inertia 3, Vue 3 Composition API, Tailwind, and [shadcn-vue](https://www.shadcn-vue.com/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization.

The majority of the frontend code is located in the `resources/js` directory. You are free to modify any of the code to customize the appearance and behavior of your application:

```
1resources/js/

2├── components/    # Reusable Vue components

3├── composables/   # Vue composables / hooks

4├── layouts/       # Application layouts

5├── lib/           # Utility functions and configuration

6├── pages/         # Page components

7└── types/         # TypeScript definitions
```

To publish additional shadcn-vue components, first [find the component you want to publish](https://www.shadcn-vue.com). Then, publish the component using `npx`:

```
1npx shadcn-vue@latest add switch
```

In this example, the command will publish the Switch component to `resources/js/components/ui/Switch.vue`. Once the component has been published, you can use it in any of your pages:

```
1<script setup lang="ts">

2import { Switch } from '@/components/ui/switch'

3</script>

4 

5<template>

6    <div>

7        <Switch />

8    </div>

9</template>
```

#### [Available Layouts](#vue-available-layouts)

The Vue starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is imported at the top of your application's `resources/js/layouts/AppLayout.vue` file:

```
1import AppLayout from '@/layouts/app/AppSidebarLayout.vue';

2import AppLayout from '@/layouts/app/AppHeaderLayout.vue';
```

#### [Sidebar Variants](#vue-sidebar-variants)

The sidebar layout includes three different variants: the default sidebar variant, the "inset" variant, and the "floating" variant. You may choose the variant you like best by modifying the `resources/js/components/AppSidebar.vue` component:

```
1<Sidebar collapsible="icon" variant="sidebar">

2<Sidebar collapsible="icon" variant="inset">
```

#### [Authentication Page Layout Variants](#vue-authentication-page-layout-variants)

The authentication pages included with the Vue starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split".

To change your authentication layout, modify the layout that is imported at the top of your application's `resources/js/layouts/AuthLayout.vue` file:

```
1import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue';

2import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue';
```

### [Livewire](#livewire-customization)

Our Livewire starter kit is built with Livewire 4, Tailwind, and [Flux UI](https://fluxui.dev/). As with all of our starter kits, all of the backend and frontend code exists within your application to allow for full customization.

The majority of the frontend code is located in the `resources/views` directory. You are free to modify any of the code to customize the appearance and behavior of your application:

```
1resources/views

2├── components            # Reusable components

3├── flux                  # Customized Flux components

4├── layouts               # Application layouts

5├── pages                 # Livewire pages

6├── partials              # Reusable Blade partials

7├── dashboard.blade.php   # Authenticated user dashboard

8├── welcome.blade.php     # Guest user welcome page
```

#### [Available Layouts](#livewire-available-layouts)

The Livewire starter kit includes two different primary layouts for you to choose from: a "sidebar" layout and a "header" layout. The sidebar layout is the default, but you can switch to the header layout by modifying the layout that is used by your application's `resources/views/layouts/app.blade.php` file. In addition, you should add the `container` attribute to the main Flux component:

```
1<x-layouts::app.header>

2    <flux:main container>

3        {{ $slot }}

4    </flux:main>

5</x-layouts::app.header>
```

#### [Authentication Page Layout Variants](#livewire-authentication-page-layout-variants)

The authentication pages included with the Livewire starter kit, such as the login page and registration page, also offer three different layout variants: "simple", "card", and "split".

To change your authentication layout, modify the layout that is used by your application's `resources/views/layouts/auth.blade.php` file:

```
1<x-layouts::auth.split>

2    {{ $slot }}

3</x-layouts::auth.split>
```

## [Authentication](#authentication)

All starter kits use [Laravel Fortify](/docs/13.x/fortify) to handle authentication. Fortify provides routes, controllers, and logic for login, registration, password reset, email verification, and more.

Fortify automatically registers the following authentication routes based on the features that are enabled in your application's `config/fortify.php` configuration file:

| Route                              | Method | Description                         |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`  | Display login form                  |
| `/login`                           | `POST` | Authenticate user                   |
| `/logout`                          | `POST` | Log user out                        |
| `/register`                        | `GET`  | Display registration form           |
| `/register`                        | `POST` | Create new user                     |
| `/forgot-password`                 | `GET`  | Display password reset request form |
| `/forgot-password`                 | `POST` | Send password reset link            |
| `/reset-password/{token}`          | `GET`  | Display password reset form         |
| `/reset-password`                  | `POST` | Update password                     |
| `/email/verify`                    | `GET`  | Display email verification notice   |
| `/email/verify/{id}/{hash}`        | `GET`  | Verify email address                |
| `/email/verification-notification` | `POST` | Resend verification email           |
| `/user/confirm-password`           | `GET`  | Display password confirmation form  |
| `/user/confirm-password`           | `POST` | Confirm password                    |
| `/two-factor-challenge`            | `GET`  | Display 2FA challenge form          |
| `/two-factor-challenge`            | `POST` | Verify 2FA code                     |

The `php artisan route:list` Artisan command can be used to display all of the routes in your application.

### [Enabling and Disabling Features](#enabling-and-disabling-features)

You can control which Fortify features are enabled in your application's `config/fortify.php` configuration file:

```
 1use Laravel\Fortify\Features;

 2 

 3'features' => [

 4    Features::registration(),

 5    Features::resetPasswords(),

 6    Features::emailVerification(),

 7    Features::twoFactorAuthentication([

 8        'confirm' => true,

 9        'confirmPassword' => true,

10    ]),

11],
```

To disable a feature, comment out or remove that feature entry from the `features` array. For example, remove `Features::registration()` to disable public registration.

When using the [React](#react), [Svelte](#svelte) or [Vue](#vue) starter kits, you will also need to remove any references to the disabled feature's routes in your frontend code. For example, if you disable email verification, you should remove the imports and references to the `verification` routes in your React, Svelte, or Vue components. This is necessary because these starter kits use Wayfinder for type-safe routing, which generates route definitions at build time. If you reference routes that no longer exist, your application will fail to build.

### [Customizing User Creation and Password Reset](#customizing-actions)

When a user registers or resets their password, Fortify invokes action classes located in your application's `app/Actions/Fortify` directory:

| File                          | Description                          |
| ----------------------------- | ------------------------------------ |
| `CreateNewUser.php`           | Validates and creates new users      |
| `ResetUserPassword.php`       | Validates and updates user passwords |
| `PasswordValidationRules.php` | Defines password validation rules    |

For example, to customize your application's registration logic, you should edit the `CreateNewUser` action:

```
 1public function create(array $input): User

 2{

 3    Validator::make($input, [

 4        'name' => ['required', 'string', 'max:255'],

 5        'email' => ['required', 'email', 'max:255', 'unique:users'],

 6        'phone' => ['required', 'string', 'max:20'],

 7        'password' => $this->passwordRules(),

 8    ])->validate();

 9 

10    return User::create([

11        'name' => $input['name'],

12        'email' => $input['email'],

13        'phone' => $input['phone'],

14        'password' => Hash::make($input['password']),

15    ]);

16}
```

### [Two-Factor Authentication](#two-factor-authentication)

Starter kits include built-in two-factor authentication (2FA), allowing users to secure their accounts using any TOTP-compatible authenticator app. 2FA is enabled by default via `Features::twoFactorAuthentication()` in your application's `config/fortify.php` configuration file.

The `confirm` option requires users to verify a code before 2FA is fully enabled, while `confirmPassword` requires password confirmation before enabling or disabling 2FA. For more details, see [Fortify's two-factor authentication documentation](/docs/13.x/fortify#two-factor-authentication).

### [Rate Limiting](#rate-limiting)

Rate limiting prevents brute-forcing and repeated login attempts from overwhelming your authentication endpoints. You can customize Fortify's rate limiting behavior in your application's `FortifyServiceProvider`:

```
1use Illuminate\Support\Facades\RateLimiter;

2use Illuminate\Cache\RateLimiting\Limit;

3 

4RateLimiter::for('login', function ($request) {

5    return Limit::perMinute(5)->by($request->email.$request->ip());

6});
```

## [Teams](#teams)

The React, Svelte, Vue, and Livewire starter kits may also be generated with team support. When the teams feature is enabled, each user belongs to one or more teams and has a current team. During registration, new users are automatically given a personal team. The starter kits also include team management screens for creating teams, switching between teams, inviting members, and updating team details.

When a route is scoped to the current team, the current team's slug is included in the URL. For example, the dashboard route becomes `/{current_team}/dashboard`, while team management pages use routes such as `settings/teams/{team}`. When using the `{current_team}` and `{team}` route parameters, the starter kits automatically ensure that the authenticated user belongs to the requested team before allowing access to the route.

To make generating team-aware URLs more convenient, the starter kits register URL defaults for the authenticated user's current team. This allows calls to helpers such as `route('dashboard')` to automatically include the current team's slug. When a user signs in, registers, or switches teams, the starter kits update the current team and refresh these URL defaults so generated links continue to use the correct team context.

When creating or renaming a team, the starter kits also prevent users from choosing reserved names that could produce unsafe or conflicting route segments. For example, names that would collide with route prefixes such as `settings`, `login`, or `dashboard` may not be used.

## [WorkOS AuthKit Authentication](#workos)

By default, the React, Svelte, Vue, and Livewire starter kits all utilize Laravel's built-in authentication system to offer login, registration, password reset, email verification, and more. In addition, we also offer a [WorkOS AuthKit](https://authkit.com) powered variant of each starter kit that offers:

- Social authentication (Google, Microsoft, GitHub, and Apple)
- Passkey authentication
- Email based "Magic Auth"
- SSO

Using WorkOS as your authentication provider [requires a WorkOS account](https://workos.com). WorkOS offers free authentication for applications up to 1 million monthly active users.

To use WorkOS AuthKit as your application's authentication provider, select the WorkOS option when creating your new starter kit powered application via `laravel new`.

### Configuring Your WorkOS Starter Kit

After creating a new application using a WorkOS powered starter kit, you should set the `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, and `WORKOS_REDIRECT_URL` environment variables in your application's `.env` file. These variables should match the values provided to you in the WorkOS dashboard for your application:

```
1WORKOS_CLIENT_ID=your-client-id

2WORKOS_API_KEY=your-api-key

3WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

Additionally, you should configure the application homepage URL in your WorkOS dashboard. This URL is where users will be redirected after they log out of your application.

#### [Configuring AuthKit Authentication Methods](#configuring-authkit-authentication-methods)

When using a WorkOS powered starter kit, we recommend that you disable "Email + Password" authentication within your application's WorkOS AuthKit configuration settings, allowing users to only authenticate via social authentication providers, passkeys, "Magic Auth", and SSO. This allows your application to totally avoid handling user passwords.

#### [Configuring AuthKit Session Timeouts](#configuring-authkit-session-timeouts)

In addition, we recommend that you configure your WorkOS AuthKit session inactivity timeout to match your Laravel application's configured session timeout threshold, which is typically two hours.

### [Inertia SSR](#inertia-ssr)

The React, Svelte, and Vue starter kits are compatible with Inertia's [server-side rendering](https://inertiajs.com/server-side-rendering) capabilities. To build an Inertia SSR compatible bundle for your application, run the `build:ssr` command:

```
1npm run build:ssr
```

For convenience, a `composer dev:ssr` command is also available. This command will start the Laravel development server and Inertia SSR server after building an SSR compatible bundle for your application, allowing you to test your application locally using Inertia's server-side rendering engine:

```
1composer dev:ssr
```

### [Community Maintained Starter Kits](#community-maintained-starter-kits)

When creating a new Laravel application using the Laravel installer, you may provide any community maintained starter kit available on Packagist to the `--using` flag:

```
1laravel new my-app --using=example/starter-kit
```

#### [Creating Starter Kits](#creating-starter-kits)

To ensure your starter kit is available to others, you will need to publish it to [Packagist](https://packagist.org). Your starter kit should define its required environment variables in its `.env.example` file, and any necessary post-installation commands should be listed in the `post-create-project-cmd` array of the starter kit's `composer.json` file.

### [Frequently Asked Questions](#faqs)

#### [How do I upgrade?](#faq-upgrade)

Every starter kit gives you a solid starting point for your next application. With full ownership of the code, you can tweak, customize, and build your application exactly as you envision. However, there is no need to update the starter kit itself.

#### [How do I enable email verification?](#faq-enable-email-verification)

Email verification can be added by uncommenting the `MustVerifyEmail` import in your `App/Models/User.php` model and ensuring the model implements the `MustVerifyEmail` interface:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Contracts\Auth\MustVerifyEmail;

 6// ...

 7 

 8class User extends Authenticatable implements MustVerifyEmail

 9{

10    // ...

11}
```

After registration, users will receive a verification email. To restrict access to certain routes until the user's email address is verified, add the `verified` middleware to the routes:

```
1Route::middleware(['auth', 'verified'])->group(function () {

2    Route::get('dashboard', function () {

3        return Inertia::render('dashboard');

4    })->name('dashboard');

5});
```

Email verification is not required when using the [WorkOS](#workos) variant of the starter kits.

#### [How do I modify the default email template?](#faq-modify-email-template)

You may want to customize the default email template to better align with your application's branding. To modify this template, you should publish the email views to your application with the following command:

```
1php artisan vendor:publish --tag=laravel-mail
```

This will generate several files in `resources/views/vendor/mail`. You can modify any of these files as well as the `resources/views/vendor/mail/themes/default.css` file to change the look and appearance of the default email template.
