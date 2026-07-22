[Components](/docs/5.x/components/overview)

# Select Blade component

## [​](#introduction)Introduction

The select component is a wrapper around the native `<select>` element. It provides a simple interface for selecting a single value from a list of options:

```
<x-filament::input.wrapper>
    <x-filament::input.select wire:model="status">
        <option value="draft">Draft</option>
        <option value="reviewing">Reviewing</option>
        <option value="published">Published</option>
    </x-filament::input.select>
</x-filament::input.wrapper>
```

To use the select component, you must wrap it in an “input wrapper” component, which provides a border and other elements such as a prefix or suffix. You can learn more about customizing the input wrapper component [here](./input-wrapper).

[Section Blade component](/docs/5.x/components/section)[Tabs Blade component](/docs/5.x/components/tabs)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
