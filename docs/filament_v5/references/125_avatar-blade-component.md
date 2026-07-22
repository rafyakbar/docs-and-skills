[Components](/docs/5.x/components/overview)

# Avatar Blade component

## [​](#introduction)Introduction

The avatar component is used to render a circular or square image, often used to represent a user or entity as their “profile picture”:

```
<x-filament::avatar
    src="https://filamentphp.com/dan.jpg"
    alt="Dan Harrin"
/>
```

## [​](#setting-the-rounding-of-an-avatar)Setting the rounding of an avatar

Avatars are fully rounded by default, but you may make them square by setting the `circular` attribute to `false`:

```
<x-filament::avatar
    src="https://filamentphp.com/dan.jpg"
    alt="Dan Harrin"
    :circular="false"
/>
```

## [​](#setting-the-size-of-an-avatar)Setting the size of an avatar

By default, the avatar will be “medium” size. You can set the size to either `sm`, `md`, or `lg` using the `size` attribute:

```
<x-filament::avatar
    src="https://filamentphp.com/dan.jpg"
    alt="Dan Harrin"
    size="lg"
/>
```

You can also pass your own custom size classes into the `size` attribute:

```
<x-filament::avatar
    src="https://filamentphp.com/dan.jpg"
    alt="Dan Harrin"
    size="w-12 h-12"
/>
```

[Rendering a widget in a Blade view](/docs/5.x/components/widget)[Badge Blade component](/docs/5.x/components/badge)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
