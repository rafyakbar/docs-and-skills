[Infolists](/docs/5.x/infolists/overview)

# Custom entries

## [​](#introduction)Introduction

You may create your own custom entry classes and views, which you can reuse across your project, and even release as a plugin to the community. To create a custom entry class and view, you may use the following command:

```
php artisan make:filament-infolist-entry AudioPlayerEntry
```

This will create the following component class:

```
use Filament\Infolists\Components\Entry;

class AudioPlayerEntry extends Entry
{
    protected string $view = 'filament.infolists.components.audio-player-entry';
}
```

It will also create a view file at `resources/views/filament/infolists/components/audio-player-entry.blade.php`.

Filament infolist entries are **not** Livewire components. Defining public properties and methods on a infolist entry class will not make them accessible in the Blade view.

## [​](#accessing-the-state-of-the-entry-in-the-blade-view)Accessing the state of the entry in the Blade view

Inside the Blade view, you may access the [state](./overview#entry-content-state) of the entry using the `$getState()` function:

```
<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    {{ $getState() }}
</x-dynamic-component>
```

## [​](#accessing-the-state-of-another-component-in-the-blade-view)Accessing the state of another component in the Blade view

Inside the Blade view, you may access the state of another component in the schema using the `$get()` function:

```
<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    {{ $get('email') }}
</x-dynamic-component>
```

Unless a form field is [reactive](../infolists/overview#the-basics-of-reactivity), the Blade view will not refresh when the value of the field changes, only when the next user interaction occurs that makes a request to the server. If you need to react to changes in a field’s value, it should be `live()`.

## [​](#accessing-the-eloquent-record-in-the-blade-view)Accessing the Eloquent record in the Blade view

Inside the Blade view, you may access the current Eloquent record using the `$record` variable:

```
<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    {{ $record->name }}
</x-dynamic-component>
```

## [​](#accessing-the-current-operation-in-the-blade-view)Accessing the current operation in the Blade view

Inside the Blade view, you may access the current operation, usually `create`, `edit` or `view`, using the `$operation` variable:

```
<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    @if ($operation === 'create')
        This is a new conference.
    @else
        This is an existing conference.
    @endif
</x-dynamic-component>
```

## [​](#accessing-the-current-livewire-component-instance-in-the-blade-view)Accessing the current Livewire component instance in the Blade view

Inside the Blade view, you may access the current Livewire component instance using `$this`:

```
@php
    use Filament\Resources\Users\RelationManagers\ConferencesRelationManager;
@endphp

<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    @if ($this instanceof ConferencesRelationManager)
        You are editing conferences the of a user.
    @endif
</x-dynamic-component>
```

## [​](#accessing-the-current-entry-instance-in-the-blade-view)Accessing the current entry instance in the Blade view

Inside the Blade view, you may access the current entry instance using `$entry`. You can call public methods on this object to access other information that may not be available in variables:

```
<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    @if ($entry->isLabelHidden())
        This is a new conference.
    @endif
</x-dynamic-component>
```

## [​](#adding-a-configuration-method-to-a-custom-entry-class)Adding a configuration method to a custom entry class

You may add a public method to the custom entry class that accepts a configuration value, stores it in a protected property, and returns it again from another public method:

```
use Filament\Infolists\Components\Entry;

class AudioPlayerEntry extends Entry
{
    protected string $view = 'filament.infolists.components.audio-player-entry';
  
    protected ?float $speed = null;

    public function speed(?float $speed): static
    {
        $this->speed = $speed;

        return $this;
    }

    public function getSpeed(): ?float
    {
        return $this->speed;
    }
}
```

Now, in the Blade view for the custom entry, you may access the speed using the `$getSpeed()` function:

```
<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    {{ $getSpeed() }}
</x-dynamic-component>
```

Any public method that you define on the custom entry class can be accessed in the Blade view as a variable function in this way. To pass the configuration value to the custom entry class, you may use the public method:

```
use App\Filament\Infolists\Components\AudioPlayerEntry;

AudioPlayerEntry::make('recording')
    ->speed(0.5)
```

## [​](#allowing-utility-injection-in-a-custom-entry-configuration-method)Allowing utility injection in a custom entry configuration method

[Utility injection](./overview#entry-utility-injection) is a powerful feature of Filament that allows users to configure a component using functions that can access various utilities. You can allow utility injection by ensuring that the parameter type and property type of the configuration allows the user to pass a `Closure`. In the getter method, you should pass the configuration value to the `$this->evaluate()` method, which will inject utilities into the user’s function if they pass one, or return the value if it is static:

```
use Closure;
use Filament\Infolists\Components\Entry;

class AudioPlayerEntry extends Entry
{
    protected string $view = 'filament.infolists.components.audio-player-entry';
  
    protected float | Closure | null $speed = null;

    public function speed(float | Closure | null $speed): static
    {
        $this->speed = $speed;

        return $this;
    }

    public function getSpeed(): ?float
    {
        return $this->evaluate($this->speed);
    }
}
```

Now, you can pass a static value or a function to the `speed()` method, and [inject any utility](./overview#component-utility-injection) as a parameter:

```
use App\Filament\Infolists\Components\AudioPlayerEntry;

AudioPlayerEntry::make('recording')
    ->speed(fn (Conference $record): float => $record->isGlobal() ? 1 : 0.5)
```

## [​](#calling-entry-methods-from-javascript)Calling entry methods from JavaScript

Sometimes you need to call a method on the entry class from JavaScript in the Blade view. For example, you might want to fetch data asynchronously or perform some server-side computation. Filament provides a way to expose methods on your entry class to JavaScript using the `#[ExposedLivewireMethod]` attribute.

### [​](#exposing-a-method)Exposing a method

To expose a method to JavaScript, add the `#[ExposedLivewireMethod]` attribute to a public method on your custom entry class:

```
use Filament\Infolists\Components\Entry;
use Filament\Support\Components\Attributes\ExposedLivewireMethod;

class AudioPlayerEntry extends Entry
{
    protected string $view = 'filament.infolists.components.audio-player-entry';

    #[ExposedLivewireMethod]
    public function getWaveformData(): array
    {
        // Generate waveform data from the audio file...

        return $waveformData;
    }
}
```

Only methods marked with `#[ExposedLivewireMethod]` can be called from JavaScript. This is a security measure to prevent arbitrary method execution.

### [​](#calling-the-method-from-javascript)Calling the method from JavaScript

In your Blade view, you may call the exposed method using `$wire.callSchemaComponentMethod()`. The first argument is the component’s key (available via `$getKey()`), and the second argument is the method name. You may pass arguments as a third argument:

```
@php
    $key = $getKey();
@endphp

<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    <div
        x-data="{
            waveform: null,
            async loadWaveform() {
                this.waveform = await $wire.callSchemaComponentMethod(
                    @js($key),
                    'getWaveformData',
                )
            },
        }"
        x-init="loadWaveform"
    >
        <template x-if="waveform">
            {{-- Render the waveform visualization --}}
        </template>
    </div>
</x-dynamic-component>
```

### [​](#preventing-re-renders)Preventing re-renders

By default, calling an exposed method will trigger a re-render of the Livewire component. If your method doesn’t need to update the UI, you may add Livewire’s `#[Renderless]` attribute alongside `#[ExposedLivewireMethod]` to skip the re-render:

```
use Filament\Infolists\Components\Entry;
use Filament\Support\Components\Attributes\ExposedLivewireMethod;
use Livewire\Attributes\Renderless;

class AudioPlayerEntry extends Entry
{
    protected string $view = 'filament.infolists.components.audio-player-entry';

    #[ExposedLivewireMethod]
    #[Renderless]
    public function getWaveformData(): array
    {
        // ...
    }
}
```

[Repeatable entry](/docs/5.x/infolists/repeatable-entry)[Overview](/docs/5.x/actions/overview)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
