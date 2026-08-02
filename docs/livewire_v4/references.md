# Livewire v4 Documentation References

Total pages: 80

## Getting Started

- **[Quickstart](references/001_version-4-x.md)** — Livewire allows you to build dynamic, reactive interfaces using only PHP—no JavaScript required. Instead of writing frontend code in JavaScript frameworks, you write simple PHP classes and Blade templates, and Livewire handles all the complex JavaScript behind the scenes.

- **[Installation](references/002_installation.md)** — Livewire is a Laravel package, so you will need to have a Laravel application up and running before you can install and use Livewire. If you need help setting up a new Laravel application, please see the [official Laravel documentation](https://laravel.com/docs/installation).

- **[Upgrade Guide](references/003_upgrade-guide.md)** — Livewire v4 introduces several improvements and optimizations while maintaining backward compatibility wherever possible. This guide will help you upgrade from Livewire v3 to v4.

## Essentials

- **[Components](references/004_components.md)** — Livewire components are essentially PHP classes with properties and methods that can be called directly from a Blade template. This powerful combination allows you to create full-stack interactive interfaces with a fraction of the effort and complexity of modern JavaScript alternatives.

- **[Pages](references/005_pages.md)** — Livewire components can be used as entire pages by assigning them directly to routes. This allows you to build complete application pages using Livewire components, with additional capabilities like custom layouts, page titles, and route parameters.

- **[Properties](references/006_properties.md)** — Properties store and manage state inside your Livewire components. They are defined as public properties on component classes and can be accessed and modified on both the server and client-side.

- **[Actions](references/007_actions.md)** — Livewire actions are methods on your component that can be triggered by frontend interactions like clicking a button or submitting a form. They provide the developer experience of being able to call a PHP method directly from the browser, allowing you to focus on the logic of your application without getting bogged down writing boilerplate code connecting your application's frontend and backend.

- **[Forms](references/008_forms.md)** — Because forms are the backbone of most web applications, Livewire provides loads of helpful utilities for building them. From handling simple input elements to complex things like real-time validation or file uploading, Livewire has simple, well-documented tools to make your life easier and delight your users.

- **[Events](references/009_events.md)** — Livewire offers a robust event system that you can use to communicate between different components on the page. Because it uses browser events under the hood, you can also use Livewire's event system to communicate with Alpine components or even plain, vanilla JavaScript.

- **[Lifecycle Hooks](references/010_lifecycle-hooks.md)** — Livewire provides a variety of lifecycle hooks that allow you to execute code at specific points during a component's lifecycle. These hooks enable you to perform actions before or after particular events, such as initializing the component, updating properties, or rendering the template.

- **[Nesting Components](references/011_nesting-components.md)** — Livewire allows you to nest additional Livewire components inside of a parent component. This feature is immensely powerful, as it allows you to re-use and encapsulate behavior within Livewire components that are shared across your application.

- **[Testing](references/012_testing.md)** — Livewire components are simple to test. Because they are just Laravel classes under the hood, they can be tested using Laravel's existing testing tools. However, Livewire provides many additional utilities to make testing your components a breeze.

## Features

- **[Alpine](references/013_alpine.md)** — [AlpineJS](https://alpinejs.dev/) is a lightweight JavaScript library that makes it easy to add client-side interactivity to your web pages. It was originally built to complement tools like Livewire where a more JavaScript-centric utility is helpful for sprinkling interactivity around your app.

- **[Styles](references/014_styles.md)** — Livewire allows you to include component-specific styles directly in your single-file and multi-file components. These styles are automatically scoped to your component, preventing them from leaking into other parts of your application.

- **[Navigate](references/015_navigate.md)** — Many modern web applications are built as "single page applications" (SPAs). In these applications, each page rendered by the application no longer requires a full browser page reload, avoiding the overhead of re-downloading JavaScript and CSS assets on every request.

- **[Islands](references/016_islands.md)** — Islands allow you to create isolated regions within a Livewire component that update independently. When an action occurs inside an island, only that island re-renders — not the entire component.

- **[Lazy Loading](references/017_lazy-loading.md)** — Livewire allows you to lazy load components that would otherwise slow down the initial page load.

- **[Loading States](references/018_loading-states.md)** — When a user interacts with your Livewire components, providing visual feedback during network requests is essential for a good user experience. Livewire automatically adds a `data-loading` attribute to any element that triggers a network request, making it easy to style loading states.

- **[Validation](references/019_validation.md)** — Livewire aims to make validating a user's input and giving them feedback as pleasant as possible. By building on top of Laravel's validation features, Livewire leverages your existing knowledge while also providing you with robust, additional features like real-time validation.

- **[File Uploads](references/020_file-uploads.md)** — Livewire offers powerful support for uploading files within your components.

- **[Pagination](references/021_pagination.md)** — Laravel's pagination feature allows you to query a subset of data and provides your users with the ability to navigate between *pages* of those results.

- **[URL Query Parameters](references/022_url-query-parameters.md)** — Livewire allows you to store component properties in the URL's query string. For example, you may want a `$search` property in your component to be included in the URL: `https://example.com/users?search=bob`. This is particularly useful for things like filtering, sorting, and pagination, as it allows users to share and bookmark specific states of a page.

- **[Computed Properties](references/023_computed-properties.md)** — Computed properties are a way to create "derived" properties in Livewire. Like accessors on an Eloquent model, computed properties allow you to access values and memoize them for future access during the request.

- **[Redirecting](references/024_redirecting.md)** — After a user performs some action — like submitting a form — you may want to redirect them to another page in your application.

- **[File Downloads](references/025_file-downloads.md)** — File downloads in Livewire work much the same as in Laravel itself. Typically, you can use any Laravel download utility inside a Livewire component, and it should work as expected.

- **[Teleport](references/026_teleport.md)** — Livewire allows you to *teleport* part of your template to another part of the DOM on the page entirely.

## HTML Directives

- **[wire:bind](references/027_wire-bind.md)** — `wire:bind` is a directive that dynamically binds HTML attributes to component properties or expressions. Unlike using Blade's attribute syntax, `wire:bind` updates the attribute reactively on the client without requiring a full re-render.

- **[wire:click](references/028_wire-click.md)** — Livewire provides a simple `wire:click` directive for calling component methods (aka actions) when a user clicks a specific element on the page.

- **[wire:submit](references/029_wire-submit.md)** — Livewire makes it easy to handle form submissions via the `wire:submit` directive. By adding `wire:submit` to a `<form>` element, Livewire will intercept the form submission, prevent the default browser handling, and call any Livewire component method.

- **[wire:model](references/030_wire-model.md)** — Livewire makes it easy to bind a component property's value with form inputs using `wire:model`.

- **[wire:loading](references/031_wire-loading.md)** — Loading indicators are an important part of crafting good user interfaces. They give users visual feedback when a request is being made to the server, so they know they are waiting for a process to complete.

- **[wire:navigate](references/032_wire-navigate.md)** — Livewire's `wire:navigate` feature makes page navigation much faster, providing an SPA-like experience for your users.

- **[wire:current](references/033_wire-current.md)** — The `wire:current` directive allows you to easily detect and style currently active links on a page.

- **[wire:cloak](references/034_wire-cloak.md)** — `wire:cloak` is a directive that hides elements on page load until Livewire is fully initialized. This is useful for preventing the "flash of unstyled content" that can occur when the page loads before Livewire has a chance to initialize.

- **[wire:dirty](references/035_wire-dirty.md)** — In a traditional HTML page containing a form, the form is only ever submitted when the user presses the "Submit" button.

- **[wire:confirm](references/036_wire-confirm.md)** — Before performing dangerous actions in Livewire, you may want to provide your users with some sort of visual confirmation.

- **[wire:transition](references/037_wire-transition.md)** — `wire:transition` enables smooth animations when elements appear, disappear, or change using the browser's native [View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API).

- **[wire:init](references/038_wire-init.md)** — Livewire offers a `wire:init` directive to run an action as soon as the component is rendered. This can be helpful in cases where you don't want to hold up the entire page load, but want to load some data immediately after the page load.

- **[wire:intersect](references/039_wire-intersect.md)** — Livewire's `wire:intersect` directive allows you to execute an action when an element enters or leaves the viewport. This is useful for lazy loading content, triggering analytics, or creating scroll-based interactions.

- **[wire:poll](references/040_wire-poll.md)** — Polling is a technique used in web applications to "poll" the server (send requests on a regular interval) for updates. It's a simple way to keep a page up-to-date without the need for a more sophisticated technology like [WebSockets](/docs/4.x/events#real-time-events-using-laravel-echo).

- **[wire:offline](references/041_wire-offline.md)** — In real-time applications, it can be helpful to provide a visual indication that the user's device is no longer connected to the internet.

- **[wire:ignore](references/042_wire-ignore.md)** — Livewire's ability to make updates to the page is what makes it "live", however, there are times when you might want to prevent Livewire from updating a portion of the page.

- **[wire:ref](references/043_wire-ref.md)** — Refs in Livewire provide a way to name, then target an individual element or component inside Livewire.

- **[wire:replace](references/044_wire-replace.md)** — Livewire's DOM diffing is useful for updating existing elements on your page, but occasionally you may need to force some elements to render from scratch to reset internal state.

- **[wire:show](references/045_wire-show.md)** — Livewire's `wire:show` directive makes it easy to show and hide elements based on the result of an expression.

- **[wire:sort](references/046_wire-sort.md)** — Livewire provides drag-and-drop sorting through the `wire:sort` directive. Add it to a parent element and use `wire:sort:item` on each child to make lists sortable with smooth animations out of the box.

- **[wire:stream](references/047_wire-stream.md)** — Livewire allows you to stream content to a web page before a request is complete via the `wire:stream` API. This is an extremely useful feature for things like AI chat-bots which stream responses as they are generated.

- **[wire:text](references/048_wire-text.md)** — `wire:text` is a directive that dynamically updates an element's text content based on a component property or expression. Unlike using Blade's `{{ }}` syntax, `wire:text` updates the content without requiring a network roundtrip to re-render the component.

## PHP Attributes

- **[Async](references/049_async.md)** — The `#[Async]` attribute allows actions to run in parallel without being queued, making them execute immediately even if other requests are in-flight.

- **[Computed](references/050_computed.md)** — The `#[Computed]` attribute allows you to create derived properties that are cached during a request, providing a performance advantage when accessing expensive operations multiple times.

- **[Defer](references/051_defer.md)** — The `#[Defer]` attribute makes a component load immediately after the initial page load is complete, preventing slow components from blocking the page render.

- **[Isolate](references/052_isolate.md)** — The `#[Isolate]` attribute prevents a component's requests from being bundled with other component updates, allowing it to execute in parallel.

- **[Js](references/053_js.md)** — The `#[Js]` attribute designates methods that return JavaScript code to be executed on the client-side. Methods marked with `#[Js]` can be called directly from your templates without making a server request.

- **[Json](references/054_json.md)** — The `#[Json]` attribute marks an action as a JSON endpoint, returning data directly to JavaScript. Validation errors trigger a promise rejection with structured error data. This is ideal for actions consumed by JavaScript rather than rendered in Blade.

- **[Layout](references/055_layout.md)** — The `#[Layout]` attribute specifies which Blade layout a full-page component should use, allowing you to customize layouts on a per-component basis.

- **[Lazy](references/056_lazy.md)** — The `#[Lazy]` attribute makes a component load only when it becomes visible in the viewport, preventing slow components from blocking the initial page render.

- **[Locked](references/057_locked.md)** — The `#[Locked]` attribute prevents properties from being modified on the client-side, protecting sensitive data like model IDs from tampering by users.

- **[Modelable](references/058_modelable.md)** — The `#[Modelable]` attribute designates a property in a child component that can be bound to from a parent component using `wire:model`.

- **[On](references/059_on.md)** — The `#[On]` attribute allows a component to listen for events and execute a method when those events are dispatched.

- **[Reactive](references/060_reactive.md)** — The `#[Reactive]` attribute makes a child component's property automatically update when the parent changes the value being passed in.

- **[Renderless](references/061_renderless.md)** — The `#[Renderless]` attribute skips the rendering phase of Livewire's lifecycle when an action is called, improving performance for actions that don't modify the component's view.

- **[Session](references/062_session.md)** — The `#[Session]` attribute persists a property's value in the user's session, maintaining it across page refreshes and navigation.

- **[Title](references/063_title.md)** — The `#[Title]` attribute sets the page title for full-page Livewire components.

- **[Transition](references/064_transition.md)** — The `#[Transition]` attribute configures view transition behavior for action methods, allowing you to set transition types or skip transitions entirely.

- **[Url](references/065_url.md)** — The `#[Url]` attribute stores a property's value in the URL's query string, allowing users to share and bookmark specific states of a page.

- **[Validate](references/066_validate.md)** — The `#[Validate]` attribute associates validation rules with component properties, enabling automatic real-time validation and clean rule declaration.

## Blade Directives

- **[@island](references/067_island.md)** — The `@island` directive creates isolated regions within a component that update independently, without re-rendering the entire component.

- **[@placeholder](references/068_placeholder.md)** — The `@placeholder` directive displays custom content while lazy or deferred components and islands are loading.

- **[@persist](references/069_persist.md)** — The `@persist` directive preserves elements across page navigations when using `wire:navigate`, maintaining their state and avoiding re-initialization.

- **[@teleport](references/070_teleport.md)** — The `@teleport` directive renders a portion of your template in a different location in the DOM, outside the component's normal placement.

## Advanced

- **[Morphing](references/071_morphing.md)** — When a Livewire component updates the browser's DOM, it does so in an intelligent way we call "morphing". The term *morph* is in contrast with a word like *replace*.

- **[Hydration](references/072_hydration.md)** — Using Livewire feels like attaching a server-side PHP class directly to a web browser. Things like calling server-side functions directly from button presses support this illusion. But in reality, it is just that: an illusion.

- **[Nesting](references/073_nesting.md)** — Like many other component-based frameworks, Livewire components are nestable — meaning one component can render multiple components within itself.

- **[Troubleshooting](references/074_troubleshooting.md)** — Here at Livewire HQ, we try to remove problems from your pathway before you hit them. However, sometimes, there are some problems that we can't solve without introducing new ones, and other times, there are problems we can't anticipate.

- **[Security](references/075_security.md)** — It's important to make sure your Livewire apps are secure and don't expose any application vulnerabilities. Livewire has internal security features to handle many cases, however, there are times when it's up to your application code to keep your components secure.

- **[CSP](references/076_csp.md)** — Livewire offers a CSP-safe build that allows you to use Livewire applications in environments with strict Content Security Policy (CSP) headers that prohibit `'unsafe-eval'`.

- **[JavaScript](references/077_javascript.md)** — Livewire and Alpine provide plenty of utilities for building dynamic components directly in your HTML, however, there are times when it's helpful to break out of the HTML and execute plain JavaScript for your component.

- **[Synthesizers](references/078_synthesizers.md)** — Because Livewire components are dehydrated (serialized) into JSON, then hydrated (unserialized) back into PHP components between requests, their properties need to be JSON-serializable.

- **[Package Development](references/079_package-development.md)** — To include Livewire components in a Laravel package, you'll need to register them in your package's service provider.

- **[Contribution Guide](references/080_contribution-guide.md)** — Hi there and welcome to the Livewire contribution guide. In this guide, we are going to take a look at how you can contribute to Livewire by submitting new features, fixing failing tests, or resolving bugs.
