[Components](/docs/5.x/components/overview)

# Rendering notifications outside of a panel

Before proceeding, make sure `filament/notifications` is installed in your project. You can check by running:

```
composer show filament/notifications
```

If it’s not installed, consult the [installation guide](../introduction/installation#installing-the-individual-components) and configure the **individual components** according to the instructions.

## [​](#introduction)Introduction

To render notifications in your app, make sure the `notifications` Livewire component is rendered in your layout:

```
<div>
    @livewire('notifications')
</div>
```

Now, when [sending a notification](../notifications) from a Livewire request, it will appear for the user.

[Rendering an infolist in a Blade view](/docs/5.x/components/infolist)[Rendering a schema in a Blade view](/docs/5.x/components/schema)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
