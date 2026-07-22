[Resources](/docs/5.x/resources/overview)

# Custom resource pages

## [​](#introduction)Introduction

Filament allows you to create completely custom pages for resources. To create a new page, you can use:

```
php artisan make:filament-page SortUsers --resource=UserResource --type=custom
```

This command will create two files - a page class in the `/Pages` directory of your resource directory, and a view in the `/pages` directory of the resource views directory. You must register custom pages to a route in the static `getPages()` method of your resource:

```
public static function getPages(): array
{
    return [
        // ...
        'sort' => Pages\SortUsers::route('/sort'),
    ];
}
```

The order of pages registered in this method matters - any wildcard route segments that are defined before hard-coded ones will be matched by Laravel’s router first.

Any [parameters](https://laravel.com/docs/routing#route-parameters) defined in the route’s path will be available to the page class, in an identical way to [Livewire](https://livewire.laravel.com/docs/components#accessing-route-parameters).

## [​](#using-a-resource-record)Using a resource record

If you’d like to create a page that uses a record similar to the [Edit](./editing-records) or [View](./viewing-records) pages, you can use the `InteractsWithRecord` trait:

```
use Filament\Resources\Pages\Page;
use Filament\Resources\Pages\Concerns\InteractsWithRecord;

class ManageUser extends Page
{
    use InteractsWithRecord;
  
    public function mount(int | string $record): void
    {
        $this->record = $this->resolveRecord($record);
    }

    // ...
}
```

The `mount()` method should resolve the record from the URL and store it in `$this->record`. You can access the record at any time using `$this->getRecord()` in the class or view. To add the record to the route as a parameter, you must define `{record}` in `getPages()`:

```
public static function getPages(): array
{
    return [
        // ...
        'manage' => Pages\ManageUser::route('/{record}/manage'),
    ];
}
```

[Using widgets on resource pages](/docs/5.x/resources/widgets)[Code quality tips](/docs/5.x/resources/code-quality-tips)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
