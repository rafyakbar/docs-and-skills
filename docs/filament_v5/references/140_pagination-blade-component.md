[Components](/docs/5.x/components/overview)

# Pagination Blade component

## [​](#introduction)Introduction

The pagination component can be used in a Livewire Blade view only. It can render a list of paginated links:

```
use App\Models\User;
use Illuminate\Contracts\View\View;
use Livewire\Component;

class ListUsers extends Component
{
    // ...

    public function render(): View
    {
        return view('livewire.list-users', [
            'users' => User::query()->paginate(10),
        ]);
    }
}
```

```
<x-filament::pagination :paginator="$users" />
```

Alternatively, you can use simple pagination or cursor pagination, which will just render a “previous” and “next” button:

```
use App\Models\User;

User::query()->simplePaginate(10)
User::query()->cursorPaginate(10)
```

## [​](#allowing-the-user-to-customize-the-number-of-items-per-page)Allowing the user to customize the number of items per page

You can allow the user to customize the number of items per page by passing an array of options to the `page-options` attribute. You must also define a Livewire property where the user’s selection will be stored:

```
use App\Models\User;
use Illuminate\Contracts\View\View;
use Livewire\Component;

class ListUsers extends Component
{
    public int | string $perPage = 10;
  
    // ...
  
    public function render(): View
    {
        return view('livewire.list-users', [
            'users' => User::query()->paginate($this->perPage),
        ]);
    }
}
```

```
<x-filament::pagination
    :paginator="$users"
    :page-options="[5, 10, 20, 50, 100, 'all']"
    current-page-option-property="perPage"
/>
```

## [​](#displaying-links-to-the-first-and-the-last-page)Displaying links to the first and the last page

Extreme links are the first and last page links. You can add them by passing the `extreme-links` attribute to the component:

```
<x-filament::pagination
    :paginator="$users"
    extreme-links
/>
```

[Modal Blade component](/docs/5.x/components/modal)[Section Blade component](/docs/5.x/components/section)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
