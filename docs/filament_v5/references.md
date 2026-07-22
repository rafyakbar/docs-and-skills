# Filament v5 Documentation

Crawled from [https://filamentphp.com/docs/5.x/introduction/overview](https://filamentphp.com/docs/5.x/introduction/overview) — 145 pages covering the core Filament framework.

## Introduction

- **001** - [What is Filament?](references/001_what-is-filament.md)

  **Filament is a Server-Driven UI (SDUI) framework for Laravel.** It allows you to define user interfaces entirely in PHP using structured configuration objects, rather than traditional templating. Built on top of Livewire, Alpine.js, and Tailwind CSS, Filament empowers you to build full-featured interfaces like admin panels, dashboards, and form-based apps, all without writing custom JavaScript or frontend code. Thousands of developers use Filament to add admin panels to their Laravel applications, but it goes far beyond that. You can use Filament to build custom dashboards, user portals, CRMs, or even full applications with multiple panels. It integrates seamlessly with any frontend stack a

- **002** - [Installation](references/002_installation.md)

  PHP 8.2+ - Laravel v11.28+ - Tailwind CSS v4.1+Installation comes in two flavors, depending on whether you want to build an app using our panel builder or use the components within your app’s Blade views.

- **003** - [AI-assisted development](references/003_ai-assisted-development.md)

  This page is inspired by Laravel’s [AI Assisted Development documentation](https://laravel.com/docs/ai). Laravel Boost is developed by the Laravel team, and you can find out more about it in their official docs, alongside other information about building Laravel projects with AI assistance.

- **004** - [Optimizing local development](references/004_optimizing-local-development.md)

  This section includes optional tips to optimize performance when running your Filament app locally. If you’re looking for production-specific optimizations, check out [Deploying to production](../deployment).

- **005** - [Help](references/005_help.md)

  We offer a variety of support options, mostly free of charge. If you need help, the community is here for you! We are fortunate to have a growing community of Filament users that help each other out on our [Discord server](https://filamentphp.com/discord). Join now, it’s free! We also have many dedicated channels in different languages. Currently, we have channels for the following languages:

- **006** - [Version support policy](references/006_version-support-policy.md)

  Pull requests for new features are only accepted for the latest major version, except in special circumstances. Once a new major version is released, the Filament team will no longer accept pull requests for new features in previous versions. Any open pull requests will either be redirected to target the latest major version or closed, depending on conflicts with the new target branch.

- **007** - [Contributing](references/007_contributing.md)

  Parts of this guide are adapted from [Laravel’s contribution guide](https://laravel.com/docs/contributions), which served as valuable inspiration. If you discover a bug in Filament, please report it by opening an issue on our [GitHub repository](https://github.com/filamentphp/filament/issues/new/choose). Before opening an issue, search through the [existing issues](https://github.com/filamentphp/filament/issues?q=is%3Aissue) to check if the bug has already been reported. Please include as much information as possible, particularly the version numbers of packages in your application. You can use this Artisan command in your application to open a new issue with all the correct versions automat


## Getting Started

- **008** - [Getting started](references/008_getting-started.md)

  Once you have [installed Filament](./introduction/installation#installing-the-panel-builder), you can start building your application. This guide is for the Filament panel builder. If you are looking to use the Filament UI components outside of a panel, visit the [Components](./components) documentation.


## Resources

- **009** - [Overview](references/009_overview.md)

  Resources are static classes that are used to build CRUD interfaces for your Eloquent models. They describe how administrators should be able to interact with data from your app using tables and forms.

- **010** - [Listing records](references/010_listing-records.md)

  You can add tabs above the table, which can be used to filter the records based on some predefined conditions. Each tab can scope the Eloquent query of the table in a different way. To register tabs, add a `getTabs()` method to the List page class, and return an array of `Tab` objects:

- **011** - [Creating records](references/011_creating-records.md)

  Sometimes, you may wish to modify form data before it is finally saved to the database. To do this, you may define a `mutateFormDataBeforeCreate()` method on the Create page class, which accepts the `$data` as an array, and returns the modified version:

- **012** - [Editing records](references/012_editing-records.md)

  You may wish to modify the data from a record before it is filled into the form. To do this, you may define a `mutateFormDataBeforeFill()` method on the Edit page class to modify the `$data` array, and return the modified version before it is filled into the form:

- **013** - [Viewing records](references/013_viewing-records.md)

  To create a new resource with a View page, you can use the `--view` flag: By default, the View page will display a disabled form with the record’s data. If you preferred to display the record’s data in an “infolist”, you can define an `infolist()` method on the resource class:

- **014** - [Deleting records](references/014_deleting-records.md)

  By default, you will not be able to interact with deleted records in the app. If you’d like to add functionality to restore, force-delete and filter trashed records in your resource, use the `--soft-deletes` flag when generating the resource:

- **015** - [Managing relationships](references/015_managing-relationships.md)

  Filament provides many ways to manage relationships in the app. Which feature you should use depends on the type of relationship you are managing, and which UI you are looking for. These are compatible with `HasMany`, `HasManyThrough`, `BelongsToMany`, `MorphMany` and `MorphToMany` relationships.

- **016** - [Nested resources](references/016_nested-resources.md)

  [Relation managers](./managing-relationships#creating-a-relation-manager) and [relation pages](./managing-relationships#relation-pages) provide you with an easy way to render a table of related records inside a resource. For example, in a `CourseResource`, you may have a relation manager or page for `lessons` that belong to that course. You can create and edit lessons from the table, which opens modal dialogs. However, lessons may be too complex to be created and edited in a modal. You may wish that lessons had their own resource, so that creating and editing them would be a full page experience. This is a nested resource.

- **017** - [Singular resources](references/017_singular-resources.md)

  Resources aren’t the only way to interact with Eloquent records in a Filament panel. Even though resources may solve many of your requirements, the “index” (root) page of a resource contains a table with a list of records in that resource. Sometimes there is no need for a table that lists records in a resource. There is only a single record that the user interacts with. If it doesn’t yet exist when the user visits the page, it gets created when the form is first submitted by the user to save it. If the record already exists, it is loaded into the form when the page is first loaded, and updated when the form is submitted. For example, a CMS might have a `Page` Eloquent model and a `PageResour

- **018** - [Global search](references/018_global-search.md)

  Global search allows you to search across all of your resource records, from anywhere in the app. To enable global search on your model, you must [set a title attribute](./overview#record-titles) for your resource:

- **019** - [Using widgets on resource pages](references/019_using-widgets-on-resource-pages.md)

  Filament allows you to display widgets inside pages, below the header and above the footer. You can use an existing [dashboard widget](../widgets), or create one specifically for the resource.

- **020** - [Custom resource pages](references/020_custom-resource-pages.md)

  Filament allows you to create completely custom pages for resources. To create a new page, you can use: This command will create two files - a page class in the `/Pages` directory of your resource directory, and a view in the `/pages` directory of the resource views directory. You must register custom pages to a route in the static `getPages()` method of your resource:

- **021** - [Code quality tips](references/021_code-quality-tips.md)

  Since many Filament methods define both the UI and the functionality of the app in just one method, it can be easy to end up with giant methods and files. These can be difficult to read, even if your code has a clean and consistent style. Filament tries to mitigate some of this by providing dedicated schema and table classes when you generate a resource. These classes have a `configure()` method that accepts a `$schema` or `$table`. You can then call the `configure()` method from anywhere you want to define a schema or table. For example, if you have the following `app/Filament/Resources/Customers/Schemas/CustomerForm.php` file:


## Tables

- **022** - [Overview](references/022_overview.md)

  Tables are a common UI pattern for displaying lists of records in web applications. Filament provides a PHP-based API for defining tables with many features, while also being incredibly customizable.

- **023** - [Actions](references/023_actions.md)

  Filament’s tables can use [Actions](../actions). They are buttons that can be added to the [end of any table row](#record-actions), or even in the [header](#header-actions) or [toolbar](#toolbar-actions) of a table. For instance, you may want an action to “create” a new record in the header, and then “edit” and “delete” actions on each row. [Bulk actions](#bulk-actions) can be used to execute code when records in the table are selected. Additionally, actions can be added to any [table column](#column-actions), such that each cell in that column is a trigger for your action. It’s highly advised that you read the documentation about [customizing action trigger buttons](../actions/overview) and

- **024** - [Layout](references/024_layout.md)

  Traditional tables are notorious for having bad responsiveness. On mobile, there is only so much flexibility you have when rendering content that is horizontally long: - Allow the user to scroll horizontally to see more table content - Hide non-important columns on smaller devicesBoth of these are possible with Filament. Tables automatically scroll horizontally when they overflow anyway, and you may choose to show and hide columns based on the responsive [breakpoint](https://tailwindcss.com/docs/responsive-design#overview) of the browser. To do this, you may use a `visibleFrom()` or `hiddenFrom()` method:

- **025** - [Summaries](references/025_summaries.md)

  You may render a “summary” section below your table content. This is great for displaying the results of calculations such as averages, sums, counts, and ranges of the data in your table. By default, there will be a single summary line for the current page of data, and an additional summary line for the totals for all data if multiple pages are available. You may also add summaries for [groups](/docs/5.x/tables/grouping) of records, see [“Summarising groups of rows”](#summarising-groups-of-rows). “Summarizer” objects can be added to any [table column](/docs/5.x/tables/columns) using the `summarize()` method:

- **026** - [Grouping rows](references/026_grouping-rows.md)

  You may allow users to group table rows together using a common attribute. This is useful for displaying lots of data in a more organized way. Groups can be set up using the name of the attribute to group by (e.g. `'status'`), or a `Group` object which allows you to customize the behavior of that grouping (e.g. `Group::make('status')->collapsible()`).

- **027** - [Empty state](references/027_empty-state.md)

  The table’s “empty state” is rendered when there are no rows in the table. To customize the heading of the empty state, use the `emptyStateHeading()` method: To customize the description of the empty state, use the `emptyStateDescription()` method:

- **028** - [Custom data](references/028_custom-data.md)

  [Filament’s table builder](./overview/#introduction) was originally designed to render data directly from a SQL database using [Eloquent models](https://laravel.com/docs/eloquent) in a Laravel application. Each row in a Filament table corresponds to a row in the database, represented by an Eloquent model instance. However, this setup isn’t always possible or practical. You might need to display data that isn’t stored in a database—or data that is stored, but not accessible via Eloquent. In such cases, you can use custom data instead. Pass a function to the `records()` method of the table builder that returns an array of data. This function is called when the table renders, and the value it r


## Schemas

- **029** - [Overview](references/029_overview.md)

  Schemas form the foundation of Filament’s Server-Driven UI approach. They allow you to build user interfaces declaratively using PHP configuration objects. These configuration objects represent components that define the structure and behavior of your UI, such as forms, tables, or lists. Rather than manually writing HTML or JavaScript, you create these schemas to control what gets rendered on the server, streamlining development and ensuring consistency across your app. Schemas are used extensively across Filament to render UI elements dynamically. Whether you’re defining a form field, the layout of your page, or an action button, the schema object defines both the component’s configuration 

- **030** - [Layouts](references/030_layouts.md)

  Filament’s grid system allows you to create responsive, multi-column layouts using any layout component. Filament provides a set of built-in layout components to help you build these:

- **031** - [Sections](references/031_sections.md)

  You may want to separate your fields into sections, each with a heading and description. To do this, you can use a section component: Section::make('Rate limiting') ->description('Prevent abuse by limiting the number of requests per period') ->schema([ // ... ]) ```

- **032** - [Tabs](references/032_tabs.md)

  Some schemas can be long and complex. You may want to use tabs to reduce the number of components that are visible at once: Tabs::make('Tabs') ->tabs([ Tab::make('Tab 1') ->schema([ // ... ]), Tab::make('Tab 2') ->schema([ // ... ]), Tab::make('Tab 3') ->schema([ // ... ]), ]) ```

- **033** - [Wizards](references/033_wizards.md)

  Similar to [tabs](./tabs), you may want to use a multistep wizard to reduce the number of components that are visible at once. These are especially useful if your form has a definite chronological order, in which you want each step to be validated as the user progresses.

- **034** - [Callouts](references/034_callouts.md)

  Callouts are used to draw attention to important information or messages. They are often used for alerts, notices, or tips. You can create a callout using the `Callout` component: Callout::make('New version available') ->description('Filament v4 has been released with exciting new features and improvements.') ->info() ```

- **035** - [Empty states](references/035_empty-states.md)

  You can display an empty state in your schema to communicate that there is no content to show yet, and to guide the user towards the next action. An empty state requires a heading, but can also have a `description()`, [`icon()`](#adding-an-icon-to-the-empty-state) and [`footer()`](#inserting-actions-and-other-components-in-the-footer-of-an-empty-state):

- **036** - [Prime components](references/036_prime-components.md)

  Within Filament schemas, prime components are the most basic building blocks that can be used to insert arbitrary content into a schema, such as text and images. As the name suggests, prime components are not divisible and cannot be made simpler. Filament provides a set of built-in prime components:

- **037** - [Custom components](references/037_custom-components.md)

  You may use a “view” component to insert a Blade view into a schema arbitrarily: View::make('filament.schemas.components.chart') ``` This assumes that you have a `resources/views/filament/schemas/components/chart.blade.php` file. You may pass data to this view through the `viewData()` method:


## Forms

- **038** - [Overview](references/038_overview.md)

  Filament’s forms package allows you to easily build dynamic forms in your app. It’s used within other Filament packages to render forms within [panel resources](/docs/5.x/resources), [action modals](/docs/5.x/actions/modals), [table filters](/docs/5.x/tables/filters), and more. Learning how to build forms is essential to learning how to use these Filament packages. This guide will walk you through the basics of building forms with Filament’s form package. If you’re planning to add a new form to your own Livewire component, you should [do that first](/docs/5.x/components/form) and then come back. If you’re adding a form to a [panel resource](/docs/5.x/resources), or another Filament package, 

- **039** - [Text input](references/039_text-input.md)

  The text input allows you to interact with a string: You may set the type of string using a set of methods. Some, such as `email()`, also provide validation: TextInput::make('text') ->email() // or ->numeric() // or ->integer() // or ->password() // or ->tel() // or ->url() ```

- **040** - [Select](references/040_select.md)

  The select component allows you to select from a list of predefined options: Select::make('status') ->options([ 'draft' => 'Draft', 'reviewing' => 'Reviewing', 'published' => 'Published', ]) ```

- **041** - [Checkbox](references/041_checkbox.md)

  The checkbox component, similar to a [toggle](./toggle), allows you to interact a boolean value. If you’re saving the boolean value using Eloquent, you should be sure to add a `boolean` [cast](https://laravel.com/docs/eloquent-mutators#attribute-casting) to the model property:

- **042** - [Toggle](references/042_toggle.md)

  The toggle component, similar to a [checkbox](./checkbox), allows you to interact a boolean value. If you’re saving the boolean value using Eloquent, you should be sure to add a `boolean` [cast](https://laravel.com/docs/eloquent-mutators#attribute-casting) to the model property:

- **043** - [Checkbox list](references/043_checkbox-list.md)

  The checkbox list component allows you to select multiple values from a list of predefined options: CheckboxList::make('technologies') ->options([ 'tailwind' => 'Tailwind CSS', 'alpine' => 'Alpine.js', 'laravel' => 'Laravel', 'livewire' => 'Laravel Livewire', ]) ```

- **044** - [Radio](references/044_radio.md)

  The radio input provides a radio button group for selecting a single value from a list of predefined options: Radio::make('status') ->options([ 'draft' => 'Draft', 'scheduled' => 'Scheduled', 'published' => 'Published' ]) ```

- **045** - [Date-time picker](references/045_date-time-picker.md)

  The date-time picker provides an interactive interface for selecting a date and/or a time. DateTimePicker::make('published_at') DatePicker::make('date_of_birth') TimePicker::make('alarm_at') ```

- **046** - [File upload](references/046_file-upload.md)

  The file upload field is based on [Filepond](https://pqina.nl/filepond). Filament also supports [`spatie/laravel-medialibrary`](https://github.com/spatie/laravel-medialibrary). See our [plugin documentation](https://filamentphp.com/plugins/filament-spatie-media-library) for more information.

- **047** - [Rich editor](references/047_rich-editor.md)

  The rich editor allows you to edit and preview HTML content, as well as upload images. It uses [TipTap](https://tiptap.dev) as the underlying editor. By default, the rich editor stores content as HTML. If you would like to store the content as JSON instead, you can use the `json()` method:

- **048** - [Markdown editor](references/048_markdown-editor.md)

  The markdown editor allows you to edit and preview markdown content, as well as upload images using drag and drop. By default, the editor outputs raw Markdown and HTML, and sends it to the backend. Attackers are able to intercept the value of the component and send a different raw HTML string to the backend. As such, it is important that when outputting the HTML from a Markdown editor, it is sanitized; otherwise your site may be exposed to Cross-Site Scripting (XSS) vulnerabilities. When Filament outputs raw HTML from the database in components such as `TextColumn` and `TextEntry`, it sanitizes it to remove any dangerous JavaScript. However, if you are outputting the HTML from a Markdown edi

- **049** - [Repeater](references/049_repeater.md)

  The repeater component allows you to output a JSON array of repeated form components. Repeater::make('members') ->schema([ TextInput::make('name')->required(), Select::make('role') ->options([ 'member' => 'Member', 'administrator' => 'Administrator', 'owner' => 'Owner', ]) ->required(), ]) ->columns(2) ```

- **050** - [Builder](references/050_builder.md)

  Similar to a [repeater](/docs/5.x/forms/repeater), the builder component allows you to output a JSON array of repeated form components. Unlike the repeater, which only defines one form schema to repeat, the builder allows you to define different schema “blocks”, which you can repeat in any order. This makes it useful for building more advanced array structures. The primary use of the builder component is to build web page content using predefined blocks. This could be content for a marketing website, or maybe even fields in an online form. The example below defines multiple blocks for different elements in the page content. On the frontend of your website, you could loop through each block i

- **051** - [Tags input](references/051_tags-input.md)

  The tags input component allows you to interact with a list of tags. By default, tags are stored in JSON: If you’re saving the JSON tags using Eloquent, you should be sure to add an `array` [cast](https://laravel.com/docs/eloquent-mutators#array-and-json-casting) to the model property:

- **052** - [Textarea](references/052_textarea.md)

  The textarea allows you to interact with a multi-line string: You may change the size of the textarea by defining the `rows()` and `cols()` methods: Textarea::make('description') ->rows(10) ->cols(20) ```

- **053** - [Key-value](references/053_key-value.md)

  The key-value field allows you to interact with one-dimensional JSON object: If you’re saving the data in Eloquent, you should be sure to add an `array` [cast](https://laravel.com/docs/eloquent-mutators#array-and-json-casting) to the model property:

- **054** - [Color picker](references/054_color-picker.md)

  The color picker component allows you to pick a color in a range of formats. By default, the component uses HEX format: Clicking the color swatch opens a color picker panel where users can visually select a color:

- **055** - [Toggle buttons](references/055_toggle-buttons.md)

  The toggle buttons input provides a group of buttons for selecting a single value, or multiple values, from a list of predefined options: ToggleButtons::make('status') ->options([ 'draft' => 'Draft', 'scheduled' => 'Scheduled', 'published' => 'Published' ]) ```

- **056** - [Slider](references/056_slider.md)

  The slider component allows you to drag a handle across a track to select one or more numeric values: The [noUiSlider](https://refreshless.com/nouislider) package is used for this component, and much of its API is based upon that library.

- **057** - [Code editor](references/057_code-editor.md)

  The code editor component allows you to write code in a textarea with line numbers. By default, no syntax highlighting is applied. You may change the language syntax highlighting of the code editor using the `language()` method. The editor supports the following languages:

- **058** - [Hidden](references/058_hidden.md)

  The hidden component allows you to create a hidden field in your form that holds a value. Please be aware that the value of this field is still editable by the user if they decide to use the browser’s developer tools. You should not use this component to store sensitive or read-only information.

- **059** - [Custom fields](references/059_custom-fields.md)

  Livewire components are PHP classes that have their state stored in the user’s browser. When a network request is made, the state is sent to the server, and filled into public properties on the Livewire component class, where it can be accessed in the same way as any other class property in PHP can be. Imagine you had a Livewire component with a public property called `$name`. You could bind that property to an input field in the HTML of the Livewire component in one of two ways: with the [`wire:model` attribute](https://livewire.laravel.com/docs/properties#data-binding), or by [entangling](https://livewire.laravel.com/docs/javascript#the-wire-object) it with an Alpine.js property:

- **060** - [Validation](references/060_validation.md)

  Validation rules may be added to any [field](/docs/5.x/forms/overview#available-fields). In Laravel, validation rules are usually defined in arrays like `['required', 'max:255']` or a combined string like `required|max:255`. This is fine if you’re exclusively working in the backend with simple form requests. But Filament is also able to give your users frontend validation, so they can fix their mistakes before any backend requests are made. Filament includes many [dedicated validation methods](#available-rules), but you can also use any [other Laravel validation rules](#other-rules), including [custom validation rules](#custom-rules).


## Infolists

- **061** - [Overview](references/061_overview.md)

  Filament’s infolists package lets you display a read-only list of data for a specific entity. It’s integrated into other Filament packages, such as inside [panel resources](/docs/5.x/resources), [relation managers](/docs/5.x/resources/managing-relationships), and [action modals](/docs/5.x/actions). Understanding how to use the infolist builder will save you time when building custom Livewire applications or working with other Filament features. This guide covers the fundamentals of building infolists with Filament. If you want to add an infolist to your own Livewire component, [start here](/docs/5.x/components/infolist) before continuing. If you’re adding an infolist to a [panel resource](/d

- **062** - [Text entry](references/062_text-entry.md)

  You may set a [color](../styling/colors) for the text: TextEntry::make('status') ->color('primary') ``` Text entries may also have an [icon](../styling/icons): TextEntry::make('email') ->icon(Heroicon::Envelope) ```

- **063** - [Icon entry](references/063_icon-entry.md)

  Icon entries render an [icon](../styling/icons) representing the state of the entry: IconEntry::make('status') ->icon(fn (string $state): Heroicon => match ($state) { 'draft' => Heroicon::OutlinedPencil, 'reviewing' => Heroicon::OutlinedClock, 'published' => Heroicon::OutlinedCheckCircle, }) ```

- **064** - [Image entry](references/064_image-entry.md)

  Infolists can render images, based on the path in the state of the entry: In this case, the `header_image` state could contain `posts/header-images/4281246003439.jpg`, which is relative to the root directory of the storage disk. The storage disk is defined in the [configuration file](/docs/5.x/introduction/installation#publishing-configuration), `local` by default. You can also set the `FILESYSTEM_DISK` environment variable to change this. Alternatively, the state could contain an absolute URL to an image, such as `https://example.com/images/header.jpg`.

- **065** - [Color entry](references/065_color-entry.md)

  The color entry allows you to show the color preview from a CSS color definition, typically entered using the [color picker field](../forms/color-picker), in one of the supported formats (HEX, HSL, RGB, RGBA).

- **066** - [Code entry](references/066_code-entry.md)

  The code entry allows you to present a highlighted code snippet in your infolist. It uses [Phiki](https://github.com/phikiphp/phiki) for code highlighting on the server: CodeEntry::make('code') ->grammar(Grammar::Php) ```

- **067** - [Key-value entry](references/067_key-value-entry.md)

  The key-value entry allows you to render key-value pairs of data, from a one-dimensional JSON object / PHP array. For example, the state of this entry might be represented as: If you’re saving the data in Eloquent, you should be sure to add an `array` [cast](https://laravel.com/docs/eloquent-mutators#array-and-json-casting) to the model property:

- **068** - [Repeatable entry](references/068_repeatable-entry.md)

  The repeatable entry allows you to repeat a set of entries and layout components for items in an array or relationship. RepeatableEntry::make('comments') ->schema([ TextEntry::make('author.name'), TextEntry::make('title'), TextEntry::make('content') ->columnSpan(2), ]) ->columns(2) ```

- **069** - [Custom entries](references/069_custom-entries.md)

  You may create your own custom entry classes and views, which you can reuse across your project, and even release as a plugin to the community. To create a custom entry class and view, you may use the following command:


## Actions

- **070** - [Overview](references/070_overview.md)

  “Action” is a word that is used quite a bit within the Laravel community. Traditionally, action PHP classes handle “doing” something in your application’s business logic. For instance, logging a user in, sending an email, or creating a new user record in the database. In Filament, actions also handle “doing” something in your app. However, they are a bit different from traditional actions. They are designed to be used in the context of a user interface. For instance, you might have a button to delete a client record, which opens a modal to confirm your decision. When the user clicks the “Delete” button in the modal, the client is deleted. This whole workflow is an “action”.

- **071** - [Modals](references/071_modals.md)

  Actions may require additional confirmation or input from the user before they run. You may open a modal before an action is executed to do this. You may require confirmation before an action is run using the `requiresConfirmation()` method. This is useful for particularly destructive actions, such as those that delete records.

- **072** - [Grouping actions](references/072_grouping-actions.md)

  You may group actions together into a dropdown menu by using an `ActionGroup` object. Groups may contain many actions, or other groups: ActionGroup::make([ Action::make('view'), Action::make('edit'), Action::make('delete'), ]) ```

- **073** - [Create action](references/073_create-action.md)

  Filament includes an action that is able to create Eloquent records. When the trigger button is clicked, a modal will open with a form inside. The user fills the form, and that data is validated and saved into the database. You may use it like so:

- **074** - [Edit action](references/074_edit-action.md)

  Filament includes an action that is able to edit Eloquent records. When the trigger button is clicked, a modal will open with a form inside. The user fills the form, and that data is validated and saved into the database. You may use it like so:

- **075** - [View action](references/075_view-action.md)

  Filament includes an action that is able to view Eloquent records. When the trigger button is clicked, a modal will open with information inside. Filament uses form fields to structure this information. All form fields are disabled, so they are not editable by the user. You may use it like so:

- **076** - [Delete action](references/076_delete-action.md)

  Filament includes an action that is able to delete Eloquent records. When the trigger button is clicked, a modal asks the user for confirmation. You may use it like so: Or if you want to add it as a table bulk action, so that the user can choose which rows to delete, use `Filament\Actions\DeleteBulkAction`:

- **077** - [Replicate action](references/077_replicate-action.md)

  Filament includes an action that is able to [replicate](https://laravel.com/docs/eloquent#replicating-models) Eloquent records. You may use it like so: The `excludeAttributes()` method is used to instruct the action which columns should be excluded from replication:

- **078** - [Force-delete action](references/078_force-delete-action.md)

  Filament includes an action that is able to force-delete [soft-deleted](https://laravel.com/docs/eloquent#soft-deleting) Eloquent records. When the trigger button is clicked, a modal asks the user for confirmation. You may use it like so:

- **079** - [Restore action](references/079_restore-action.md)

  Filament includes an action that is able to restore [soft-deleted](https://laravel.com/docs/eloquent#soft-deleting) Eloquent records. When the trigger button is clicked, a modal asks the user for confirmation. You may use it like so:

- **080** - [Import action](references/080_import-action.md)

  Filament includes an action that is able to import rows from a CSV. When the trigger button is clicked, a modal asks the user for a file. Once they upload one, they are able to map each column in the CSV to a real column in the database. If any rows fail validation, they will be compiled into a downloadable CSV for the user to review after the rest of the rows have been imported. Users can also download an example CSV file containing all the columns that can be imported. This feature uses [job batches](https://laravel.com/docs/queues#job-batching) and [database notifications](/docs/5.x/notifications/database-notifications), so you need to publish those migrations from Laravel. Also, you need

- **081** - [Export action](references/081_export-action.md)

  Filament includes an action that is able to export rows to a CSV or XLSX file. When the trigger button is clicked, a modal asks for the columns that they want to export, and what they should be labeled. This feature uses [job batches](https://laravel.com/docs/queues#job-batching) and [database notifications](/docs/5.x/notifications/database-notifications), so you need to publish those migrations from Laravel. Also, you need to publish the migrations for tables that Filament uses to store information about exports:


## Notifications

- **082** - [Overview](references/082_overview.md)

  Notifications are sent using a `Notification` object that’s constructed through a fluent API. Calling the `send()` method on the `Notification` object will dispatch the notification and display it in your application. As the session is used to flash notifications, they can be sent from anywhere in your code, including JavaScript, not just Livewire components.

- **083** - [Database notifications](references/083_database-notifications.md)

  Before we start, make sure that the [Laravel notifications table](https://laravel.com/docs/notifications#database-prerequisites) is added to your database: If you’d like to receive database notifications in a panel, you can enable them in the [configuration](/docs/5.x/panel-configuration):

- **084** - [Broadcast notifications](references/084_broadcast-notifications.md)

  By default, Filament will send flash notifications via the Laravel session. However, you may wish that your notifications are “broadcast” to a user in real-time, instead. This could be used to send a temporary success notification from a queued job after it has finished processing. We have a native integration with [Laravel Echo](https://laravel.com/docs/broadcasting#client-side-installation). Make sure Echo is installed, as well as a [server-side websockets integration](https://laravel.com/docs/broadcasting#server-side-installation) like Pusher.


## Widgets

- **085** - [Overview](references/085_overview.md)

  Filament allows you to build dynamic dashboards, comprised of “widgets”. Each widget is an element on the dashboard that displays data in a specific way. For example, you can display [stats](./stats-overview), [chart](./charts), or a [table](#table-widgets).

- **086** - [Stats overview widgets](references/086_stats-overview-widgets.md)

  Filament comes with a “stats overview” widget template, which you can use to display a number of different stats in a single widget, without needing to write a custom view. Start by creating a widget with the command:

- **087** - [Chart widgets](references/087_chart-widgets.md)

  Filament comes with many “chart” widget templates, which you can use to display real-time, interactive charts. Start by creating a widget with the command: There is a single `ChartWidget` class that is used for all charts. The type of chart is set by the `getType()` method. In this example, that method returns the string `'line'`. The `protected ?string $heading` variable is used to set the heading that describes the chart. If you need to set the heading dynamically, you can override the `getHeading()` method. The `getData()` method is used to return an array of datasets and labels. Each dataset is a labeled array of points to plot on the chart, and each label is a string. This structure is 


## Panel Configuration

- **088** - [Panel configuration](references/088_panel-configuration.md)

  By default, the configuration file is located at `app/Providers/Filament/AdminPanelProvider.php`. Keep reading to learn more about [panels](#introducing-panels) and how each has [its own configuration file](#creating-a-new-panel).


## Navigation

- **089** - [Overview](references/089_overview.md)

  By default, Filament will register navigation items for each of your [resources](/docs/5.x/resources/overview), [custom pages](/docs/5.x/navigation/custom-pages), and [clusters](/docs/5.x/navigation/clusters). These classes contain static properties and methods that you can override, to configure that navigation item. If you’re looking to add a second layer of navigation to your app, you can use [clusters](/docs/5.x/navigation/clusters). These are useful for grouping resources and pages together.

- **090** - [Custom pages](references/090_custom-pages.md)

  Filament allows you to create completely custom pages for the app. This command will create two files - a page class in the `/Pages` directory of the Filament directory, and a view in the `/pages` directory of the Filament views directory. Page classes are all full-page [Livewire](https://livewire.laravel.com) components with a few extra utilities you can use with the panel.

- **091** - [User menu](references/091_user-menu.md)

  The user menu is featured in the top right corner of the admin layout. It’s fully customizable. Each menu item is represented by an [action](/docs/5.x/actions), and can be customized in the same way. To register new items, you can pass the actions to the `userMenuItems()` method of the [configuration](/docs/5.x/panel-configuration):

- **092** - [Clusters](references/092_clusters.md)

  Clusters are a hierarchical structure in panels that allow you to group [resources](../resources) and [custom pages](./custom-pages) together. They are useful for organizing your panel into logical sections, and can help reduce the size of your panel’s sidebar. When using a cluster, a few things happen:


## Users

- **093** - [Overview](references/093_overview.md)

  By default, all `App\Models\User`s can access Filament locally. To allow them to access Filament in production, you must take a few extra steps to ensure that only the correct users have access to the app.

- **094** - [Multi-factor authentication](references/094_multi-factor-authentication.md)

  Users in Filament can sign in with their email address and password by default. However, you can enable multi-factor authentication (MFA) to add an extra layer of security to your users’ accounts. When MFA is enabled, users must perform an extra step before they are authenticated and have access to the application. Filament includes two methods of MFA which you can enable out of the box:

- **095** - [Multi-tenancy](references/095_multi-tenancy.md)

  Multi-tenancy is a concept where a single instance of an application serves multiple customers. Each customer has their own data and access rules that prevent them from viewing or modifying each other’s data. This is a common pattern in SaaS applications. Users often belong to groups of users (often called teams or organizations). Records are owned by the group, and users can be members of multiple groups. This is suitable for applications where users need to collaborate on data. Multi-tenancy is a very sensitive topic. It’s important to understand the security implications of multi-tenancy and how to properly implement it. If implemented partially or incorrectly, data belonging to one tenan


## Appearance & Customization

- **096** - [Overview](references/096_overview.md)

  In the [configuration](/docs/5.x/panel-configuration), you can easily change the colors that are used. Filament ships with 6 predefined colors that are used everywhere within the framework. They are customizable as follows:

- **097** - [CSS hooks](references/097_css-hooks.md)

  Filament uses CSS “hook” classes to allow various HTML elements to be customized using CSS. We could document all the hook classes across the entire Filament UI, but that would be a lot of work, and probably not very useful to you. Instead, we recommend using your browser’s developer tools to inspect the elements you want to customize, and then use the hook classes to target those elements. All hook classes are prefixed with `fi-`, which is a great way to identify them. They are usually right at the start of the class list, so they are easy to find, but sometimes they may fall further down the list if we have to apply them conditionally with JavaScript or Blade. If you don’t find a hook clas

- **098** - [Colors](references/098_colors.md)

  Filament uses CSS variables to define its color palette. These CSS variables are mapped to Tailwind classes in the preset file that you load when installing Filament. The reason why Filament uses CSS variables is that it allows the framework to pass a color palette from PHP via a `<style>` element that gets rendered as part of the `@filamentStyles` Blade directive. By default, Filament’s Tailwind preset file ships with 6 colors:

- **099** - [Icons](references/099_icons.md)

  Icons are used throughout the entire Filament UI to visually communicate core parts of the user experience. To render icons, we use the [Blade Icons](https://github.com/blade-ui-kit/blade-icons) package from Blade UI Kit. They have a website where you can [search all the available icons](https://blade-ui-kit.com/blade-icons?set=1#search) from various Blade Icons packages. Each package contains a different icon set that you can choose from. Filament installs the “Heroicons” icon set by default, so if you are using icons from this set you do not need to install any additional packages.

- **100** - [Render hooks](references/100_render-hooks.md)

  Filament allows you to render Blade content at various points in the frameworks views. It’s useful for plugins to be able to inject HTML into the framework. Also, since Filament does not recommend publishing the views due to an increased risk of breaking changes, it’s also useful for users.

- **101** - [Registering assets](references/101_registering-assets.md)

  All packages in the Filament ecosystem share an asset management system. This allows both official plugins and third-party plugins to register CSS and JavaScript files that can then be consumed by Blade views.

- **102** - [Enum tricks](references/102_enum-tricks.md)

  Enums are special PHP classes that represent a fixed set of constants. They are useful for modeling concepts that have a limited number of possible values, like days of the week, months in a year, or the suits in a deck of cards. Since enum “cases” are instances of the enum class, adding interfaces to enums proves to be very useful. Filament provides a collection of interfaces that you can add to enums, which enhance your experience when working with them.

- **103** - [File generation](references/103_file-generation.md)

  Filament includes many CLI commands which generate files. This guide is to explain how you can customize the generated files. The vast majority of files that Filament generates are PHP classes. Filament uses [`nette/php-generator`](https://github.com/nette/php-generator) to generate classes programmatically, instead of using template files. The advantage of this is that there is much more flexibility in the generated files, which is important when you need to support as many different configuration options as Filament has. Each type of class is generated by a `ClassGenerator` class. Here are a list of `ClassGenerator` classes that Filament uses:

- **104** - [Modular architecture (DDD)](references/104_modular-architecture-(ddd).md)

  When building large-scale applications with Filament, you may want to organize your code using Domain-Driven Design (DDD) principles, splitting your application into self-contained modules. This guide explains how to integrate Filament with modular architecture packages like [InterNACHI/Modular](https://github.com/InterNACHI/modular).

- **105** - [Security](references/105_security.md)

  This page provides a general overview of security considerations when using Filament. Many individual features have their own specific security recommendations documented alongside them — for example, file uploads, rich editors, inline editable columns, and more. When using any Filament feature, make sure to read the full documentation for that feature, including any security warnings it contains.


## Testing

- **106** - [Overview](references/106_overview.md)

  All examples in this guide will be written using [Pest](https://pestphp.com). To use Pest’s Livewire plugin for testing, you can follow the installation instructions in the Pest documentation on plugins: [Livewire plugin for Pest](https://pestphp.com/docs/plugins#livewire). However, you can easily adapt this to PHPUnit, mostly by switching out the `livewire()` function from Pest with the `Livewire::test()` method. Since all Filament components are mounted to a Livewire component, we’re just using Livewire testing helpers everywhere. If you’ve never tested Livewire components before, please read [this guide](https://livewire.laravel.com/docs/testing) from the Livewire docs.

- **107** - [Testing resources](references/107_testing-resources.md)

  Ensure that you are authenticated to access the app in your `TestCase`: protected function setUp(): void { parent::setUp(); $this->actingAs(User::factory()->create()); } ``` Alternatively, if you are using Pest you can use a `beforeEach()` function at the top of your test file to authenticate:

- **108** - [Testing tables](references/108_testing-tables.md)

  To ensure a table component renders, use the `assertSuccessful()` Livewire helper: it('can render page', function () { livewire(ListPosts::class) ->assertSuccessful(); }); ``` To test which records are shown, you can use `assertCanSeeTableRecords()`, `assertCanNotSeeTableRecords()` and `assertCountTableRecords()`:

- **109** - [Testing schemas](references/109_testing-schemas.md)

  To fill a form with data, pass the data to `fillForm()`: livewire(CreatePost::class) ->fillForm([ 'title' => fake()->sentence(), // ... ]); ``` > If you have multiple schemas on a Livewire component, you can specify which form you want to fill using `fillForm([...], 'createPostForm')`.

- **110** - [Testing actions](references/110_testing-actions.md)

  You can call an action by passing its name or class to `callAction()`: it('can send invoices', function () { $invoice = Invoice::factory()->create(); livewire(EditInvoice::class, [ 'invoice' => $invoice, ]) ->callAction('send');

- **111** - [Testing notifications](references/111_testing-notifications.md)

  To check if a notification was sent using the session, use the `assertNotified()` helper: it('sends a notification', function () { livewire(CreatePost::class) ->assertNotified(); }); ```


## Plugins

- **112** - [Getting started](references/112_getting-started.md)

  While Filament comes with virtually any tool you’ll need to build great apps, sometimes you’ll need to add your own functionality either for just your app or as redistributable packages that other developers can include in their own apps. This is why Filament offers a plugin system that allows you to extend its functionality. Before we dive in, it’s important to understand the different contexts in which plugins can be used. There are two main contexts:

- **113** - [Plugin development](references/113_plugin-development.md)

  The basis of Filament plugins are Laravel packages. They are installed into your Filament project via Composer, and follow all the standard techniques, like using service providers to register routes, views, and translations. If you’re new to Laravel package development, here are some resources that can help you grasp the core concepts:

- **114** - [Build a panel plugin](references/114_build-a-panel-plugin.md)

  Please read the docs on [panel plugin development](../plugins/panel-plugins) and the [getting started guide](./getting-started) before continuing. In this walkthrough, we’ll build a simple plugin that adds a new form field that can be used in forms. This also means it will be available to users in their panels. You can find the final code for this plugin at <https://github.com/awcodes/clock-widget>.

- **115** - [Build a standalone plugin](references/115_build-a-standalone-plugin.md)

  Please read the docs on [panel plugin development](../plugins/panel-plugins) and the [getting started guide](./getting-started) before continuing. In this walkthrough, we’ll build a simple plugin that adds a new form component that can be used in forms. This also means it will be available to users in their panels. You can find the final code for this plugin at <https://github.com/awcodes/headings>.

- **116** - [Configurable resources and pages](references/116_configurable-resources-and-pages.md)

  Sometimes you need to register the same resource or page multiple times with different configurations. For example, an “Orders” resource might appear as both “Active Orders” and “Archived Orders” in the sidebar, each with different query scopes, navigation labels, and URL slugs - but sharing the same underlying resource class. Configurable resources and pages allow you to register a single class multiple times in a panel, each with a unique configuration key and its own set of options. Each configuration gets its own routes, navigation items, and URL slugs, while the resource or page class can use the active configuration to adjust its behavior at runtime.


## Blade Components

- **117** - [Overview](references/117_overview.md)

  Filament packages consume a set of core components that aim to provide a consistent and maintainable foundation for all interfaces. Some of these components are also available for use in your own applications and Filament plugins.

- **118** - [Rendering an action in a Livewire component](references/118_rendering-an-action-in-a-livewire-component.md)

  Before proceeding, make sure `filament/actions` is installed in your project. You can check by running: If it’s not installed, consult the [installation guide](/docs/5.x/introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

- **119** - [Rendering a form in a Blade view](references/119_rendering-a-form-in-a-blade-view.md)

  Before proceeding, make sure `filament/forms` is installed in your project. You can check by running: If it’s not installed, consult the [installation guide](/docs/5.x/introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

- **120** - [Rendering an infolist in a Blade view](references/120_rendering-an-infolist-in-a-blade-view.md)

  Before proceeding, make sure `filament/infolists` is installed in your project. You can check by running: If it’s not installed, consult the [installation guide](/docs/5.x/introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

- **121** - [Rendering notifications outside of a panel](references/121_rendering-notifications-outside-of-a-panel.md)

  Before proceeding, make sure `filament/notifications` is installed in your project. You can check by running: If it’s not installed, consult the [installation guide](../introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

- **122** - [Rendering a schema in a Blade view](references/122_rendering-a-schema-in-a-blade-view.md)

  Before proceeding, make sure `filament/schemas` is installed in your project. You can check by running: If it’s not installed, consult the [installation guide](/docs/5.x/introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

- **123** - [Rendering a table in a Blade view](references/123_rendering-a-table-in-a-blade-view.md)

  Before proceeding, make sure `filament/tables` is installed in your project. You can check by running: If it’s not installed, consult the [installation guide](/docs/5.x/introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

- **124** - [Rendering a widget in a Blade view](references/124_rendering-a-widget-in-a-blade-view.md)

  Before proceeding, make sure `filament/widgets` is installed in your project. You can check by running: If it’s not installed, consult the [installation guide](../introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

- **125** - [Avatar Blade component](references/125_avatar-blade-component.md)

  The avatar component is used to render a circular or square image, often used to represent a user or entity as their “profile picture”: Avatars are fully rounded by default, but you may make them square by setting the `circular` attribute to `false`:

- **126** - [Badge Blade component](references/126_badge-blade-component.md)

  The badge component is used to render a small box with some text inside: By default, the size of a badge is “medium”. You can make it “extra small” or “small” by using the `size` attribute:

- **127** - [Breadcrumbs Blade component](references/127_breadcrumbs-blade-component.md)

  The breadcrumbs component is used to render a simple, linear navigation that informs the user of their current location within the application: The keys of the array are URLs that the user is able to click on to navigate, and the values are the text that will be displayed for each link.

- **128** - [Button Blade component](references/128_button-blade-component.md)

  The button component is used to render a clickable button that can perform an action: By default, a button’s underlying HTML tag is `<button>`. You can change it to be an `<a>` tag by using the `tag` attribute:

- **129** - [Callout Blade component](references/129_callout-blade-component.md)

  A callout can be used to draw attention to important information or messages: <x-slot name="description"> Please read this information carefully before proceeding. </x-slot> </x-filament::callout> ```

- **130** - [Checkbox Blade component](references/130_checkbox-blade-component.md)

  You can use the checkbox component to render a checkbox input that can be used to toggle a boolean value: <span> Is Admin </span> </label> ``` The checkbox has special styling that you can use if it is invalid. To trigger this styling, you can use either Blade or Alpine.js. To trigger the error state using Blade, you can pass the `valid` attribute to the component, which contains either true or false based on if the checkbox is valid or not:

- **131** - [Dropdown Blade component](references/131_dropdown-blade-component.md)

  The dropdown component allows you to render a dropdown menu with a button that triggers it: <x-filament::dropdown.list> <x-filament::dropdown.list.item wire:click="openViewModal"> View </x-filament::dropdown.list.item>

- **132** - [Empty State Blade component](references/132_empty-state-blade-component.md)

  An empty state can be used to communicate that there is no content to display yet, and to guide the user towards the next action. A heading is required: You can add a description below the heading to the empty state by using the `description` slot:

- **133** - [Fieldset Blade component](references/133_fieldset-blade-component.md)

  You can use a fieldset to group multiple form fields together, optionally with a label: {{-- Form fields --}} </x-filament::fieldset> ``` [Empty State Blade component](/docs/5.x/components/empty-state)[Icon button Blade component](/docs/5.x/components/icon-button)

- **134** - [Icon button Blade component](references/134_icon-button-blade-component.md)

  The button component is used to render a clickable button that can perform an action: By default, an icon button’s underlying HTML tag is `<button>`. You can change it to be an `<a>` tag by using the `tag` attribute:

- **135** - [Input wrapper Blade component](references/135_input-wrapper-blade-component.md)

  The input wrapper component should be used as a wrapper around the [input](./input) or [select](./select) components. It provides a border and other elements such as a prefix or suffix.

- **136** - [Input Blade component](references/136_input-blade-component.md)

  The input component is a wrapper around the native `<input>` element. It provides a simple interface for entering a single line of text. To use the input component, you must wrap it in an “input wrapper” component, which provides a border and other elements such as a prefix or suffix. You can learn more about customizing the input wrapper component [here](./input-wrapper).

- **137** - [Link Blade component](references/137_link-blade-component.md)

  The link component is used to render a clickable link that can perform an action: By default, a link’s underlying HTML tag is `<a>`. You can change it to be a `<button>` tag by using the `tag` attribute:

- **138** - [Loading indicator Blade component](references/138_loading-indicator-blade-component.md)

  The loading indicator is an animated SVG that can be used to indicate that something is in progress: Filament renders the loading indicator through the `Filament\Support\Contracts\LoadingIndicator` contract, which is bound to `Filament\Support\View\DefaultLoadingIndicator` by default. You may replace it with your own implementation by binding a different class in a service provider:

- **139** - [Modal Blade component](references/139_modal-blade-component.md)

  The modal component is able to open a dialog window or slide-over with any content: {{-- Modal content --}} </x-filament::modal> ``` You can use the `trigger` slot to render a button that opens the modal. However, this is not required. You have complete control over when the modal opens and closes through JavaScript. First, give the modal an ID so that you can reference it:

- **140** - [Pagination Blade component](references/140_pagination-blade-component.md)

  The pagination component can be used in a Livewire Blade view only. It can render a list of paginated links: class ListUsers extends Component { // ... Alternatively, you can use simple pagination or cursor pagination, which will just render a “previous” and “next” button:

- **141** - [Section Blade component](references/141_section-blade-component.md)

  A section can be used to group content together, with an optional heading: {{-- Content --}} </x-filament::section> ``` You can add a description below the heading to the section by using the `description` slot:

- **142** - [Select Blade component](references/142_select-blade-component.md)

  The select component is a wrapper around the native `<select>` element. It provides a simple interface for selecting a single value from a list of options: To use the select component, you must wrap it in an “input wrapper” component, which provides a border and other elements such as a prefix or suffix. You can learn more about customizing the input wrapper component [here](./input-wrapper).

- **143** - [Tabs Blade component](references/143_tabs-blade-component.md)

  The tabs component allows you to render a set of tabs, which can be used to toggle between multiple sections of content: <x-filament::tabs.item> Tab 2 </x-filament::tabs.item> <x-filament::tabs.item> Tab 3 </x-filament::tabs.item> </x-filament::tabs> ```


## Deployment & Upgrade

- **144** - [Deploying to production](references/144_deploying-to-production.md)

  Deploying a Laravel app using Filament to production is similar to deploying any other Laravel app. However, there are a few additional steps you should take to ensure that your Filament panel is optimized for performance and security. For tips focused on local development performance, see [Optimizing local development](./introduction/optimizing-local-development).

- **145** - [Upgrade guide](references/145_upgrade-guide.md)

  If you see anything missing from this guide, please don’t hesitate to [make a pull request](https://github.com/filamentphp/filament/edit/5.x/docs/14-upgrade-guide.md) to our repository! Any help is appreciated!

