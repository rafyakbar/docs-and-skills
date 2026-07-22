[Components](/docs/5.x/components/overview)

# Rendering a widget in a Blade view

Before proceeding, make sure `filament/widgets` is installed in your project. You can check by running:

```
composer show filament/widgets
```

If it’s not installed, consult the [installation guide](../introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

## [​](#creating-a-widget)Creating a widget

Use the `make:filament-widget` command to generate a new widget. For details on customization and usage, see the [widgets section](../widgets).

## [​](#adding-the-widget)Adding the widget

Since widgets are Livewire components, you can easily render a widget in any Blade view using the `@livewire` directive:

```
<div>
    @livewire(\App\Livewire\Dashboard\PostsChart::class)
</div>
```

If you’re using a [table widget](../widgets/overview#table-widgets), make sure to install `filament/tables` as well.  
Refer to the [installation guide](../introduction/installation#installing-the-individual-components) and follow the steps to configure the **individual components** properly.

[Rendering a table in a Blade view](/docs/5.x/components/table)[Avatar Blade component](/docs/5.x/components/avatar)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
