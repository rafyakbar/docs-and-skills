[Components](/docs/5.x/components/overview)

# Empty State Blade component

## [​](#introduction)Introduction

An empty state can be used to communicate that there is no content to display yet, and to guide the user towards the next action. A heading is required:

```
<x-filament::empty-state>
    <x-slot name="heading">
        No users yet
    </x-slot>
</x-filament::empty-state>
```

## [​](#adding-a-description-to-the-empty-state)Adding a description to the empty state

You can add a description below the heading to the empty state by using the `description` slot:

```
<x-filament::empty-state>
    <x-slot name="heading">
        No users yet
    </x-slot>

    <x-slot name="description">
        Get started by creating a new user.
    </x-slot>
</x-filament::empty-state>
```

## [​](#adding-an-icon-to-the-empty-state)Adding an icon to the empty state

You can add an [icon](../styling/icons) to an empty state by using the `icon` attribute:

```
<x-filament::empty-state
    icon="heroicon-o-user"
>
    <x-slot name="heading">
        No users yet
    </x-slot>
</x-filament::empty-state>
```

### [​](#changing-the-color-of-the-empty-state-icon)Changing the color of the empty state icon

By default, the color of the empty state icon is `primary`. You can change it to be `gray`, `danger`, `info`, `success` or `warning` by using the `icon-color` attribute:

```
<x-filament::empty-state
    icon="heroicon-o-user"
    icon-color="info"
>
    <x-slot name="heading">
        No users yet
    </x-slot>
</x-filament::empty-state>
```

### [​](#changing-the-size-of-the-empty-state-icon)Changing the size of the empty state icon

By default, the size of the empty state icon is “large”. You can change it to be “small” or “medium” by using the `icon-size` attribute:

```
<x-filament::empty-state
    icon="heroicon-m-user"
    icon-size="sm"
>
    <x-slot name="heading">
        No users yet
    </x-slot>
</x-filament::empty-state>

<x-filament::empty-state
    icon="heroicon-m-user"
    icon-size="md"
>
    <x-slot name="heading">
        No users yet
    </x-slot>
</x-filament::empty-state>
```

## [​](#adding-footer-actions-to-the-empty-state)Adding footer actions to the empty state

You can add actions below the description by using the `footer` slot. This is useful for placing buttons, like the [`<x-filament::button>`](./button) component:

```
<x-filament::empty-state>
    <x-slot name="heading">
        No users yet
    </x-slot>

    <x-slot name="footer">
        <x-filament::button icon="heroicon-m-plus">
            Create user
        </x-filament::button>
    </x-slot>
</x-filament::empty-state>
```

## [​](#removing-the-empty-state-container)Removing the empty state container

By default, empty states have a background color, shadow and border. You can remove these styles and just render the content of the empty state without the container using the `:contained` attribute:

```
<x-filament::empty-state :contained="false">
    <x-slot name="heading">
        No users yet
    </x-slot>
</x-filament::empty-state>
```

[Dropdown Blade component](/docs/5.x/components/dropdown)[Fieldset Blade component](/docs/5.x/components/fieldset)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
