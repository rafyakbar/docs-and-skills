[Components](/docs/5.x/components/overview)

# Loading indicator Blade component

## [​](#introduction)Introduction

The loading indicator is an animated SVG that can be used to indicate that something is in progress:

```
<x-filament::loading-indicator class="h-5 w-5" />
```

## [​](#replacing-the-default-loading-indicator)Replacing the default loading indicator

Filament renders the loading indicator through the `Filament\Support\Contracts\LoadingIndicator` contract, which is bound to `Filament\Support\View\DefaultLoadingIndicator` by default. You may replace it with your own implementation by binding a different class in a service provider:

```
use App\Support\CustomLoadingIndicator;
use Filament\Support\Contracts\LoadingIndicator;

public function register(): void
{
    $this->app->bind(LoadingIndicator::class, CustomLoadingIndicator::class);
}
```

Your class must implement the `LoadingIndicator` contract, whose `toHtml()` method receives a `ComponentAttributeBag` and returns the indicator’s HTML:

```
namespace App\Support;

use Filament\Support\Contracts\LoadingIndicator;
use Illuminate\View\ComponentAttributeBag;

class CustomLoadingIndicator implements LoadingIndicator
{
    public function toHtml(ComponentAttributeBag $attributes): string
    {
        return <<<HTML
            <svg {$attributes->toHtml()}>
                <!-- ... -->
            </svg>
        HTML;
    }
}
```

The attributes already contain the `fi-icon fi-loading-indicator` and size hook classes, so you can forward them directly to your root element.

The resolved `LoadingIndicator` instance is cached for the lifetime of the PHP process. Under Laravel Octane, this means the binding is only resolved once when the worker boots and will not be re-resolved between requests. Register your binding in a service provider rather than rebinding it at runtime.

[Link Blade component](/docs/5.x/components/link)[Modal Blade component](/docs/5.x/components/modal)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
