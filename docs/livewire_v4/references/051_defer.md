The `#[Defer]` attribute makes a component load immediately after the initial page load is complete, preventing slow components from blocking the page render.

## Basic usage[¶](#basic-usage "")

Apply the `#[Defer]` attribute to any component that should be deferred:

```
<?php // resources/views/components/⚡revenue.blade.php

 

use Livewire\Attributes\Defer;

use Livewire\Component;

use App\Models\Transaction;

 

new #[Defer] class extends Component {

    public $amount;

 

    public function mount()

    {

        // Slow database query...

        $this->amount = Transaction::monthToDate()->sum('amount');

    }

};

?>

 

<div>

    Revenue this month: {{ $amount }}

</div>


```
With `#[Defer]`, the component initially renders as an empty `<div></div>`, then loads immediately after the page finishes loading—without waiting for it to enter the viewport.

## Lazy vs Defer[¶](#lazy-vs-defer "")

Livewire provides two ways to delay component loading:

- **Lazy loading (`#[Lazy]`)** - Components load when they become visible in the viewport (when the user scrolls to them)
- **Deferred loading (`#[Defer]`)** - Components load immediately after the initial page load is complete


Both prevent slow components from blocking your initial page render, but differ in when the component actually loads.

## Rendering placeholders[¶](#rendering-placeholders "")

By default, Livewire renders an empty `<div></div>` before the component loads. You can provide a custom placeholder using the `placeholder()` method:

```
<?php // resources/views/components/⚡revenue.blade.php

 

use Livewire\Attributes\Defer;

use Livewire\Component;

use App\Models\Transaction;

 

new #[Defer] class extends Component {

    public $amount;

 

    public function mount()

    {

        $this->amount = Transaction::monthToDate()->sum('amount');

    }

 

    public function placeholder()

    {

        return <<<'HTML'

        <div>

            <svg><!-- Loading spinner... --></svg>

        </div>

        HTML;

    }

};

?>

 

<div>

    Revenue this month: {{ $amount }}

</div>


```
Users will see the loading spinner until the component fully loads.

Match placeholder element type

If your placeholder's root element is a `<div>`, your component must also use a `<div>` element.

## Bundling requests[¶](#bundling-requests "")

By default, deferred components load in parallel with independent network requests. To bundle multiple deferred components into a single request, use the `bundle` parameter:

```
<?php // resources/views/components/⚡revenue.blade.php

 

use Livewire\Attributes\Defer;

use Livewire\Component;

 

new #[Defer(bundle: true)] class extends Component {

    // ...

};


```
Now, if there are ten `revenue` components on the page, all ten will load via a single bundled network request instead of ten parallel requests.

## Alternative approach[¶](#alternative-approach "")

### Using the defer parameter[¶](#using-the-defer-parameter "")

Instead of the attribute, you can defer specific component instances using the `defer` parameter:

```
<livewire:revenue defer />


```
This is useful when you only want certain instances of a component to be deferred.

### Overriding the attribute[¶](#overriding-the-attribute "")

If a component has `#[Defer]` but you want to load it immediately in certain cases, you can override it:

```
<livewire:revenue :defer="false" />


```


## When to use[¶](#when-to-use "")

Use `#[Defer]` when:

- Components contain slow operations (database queries, API calls) that would delay page load
- The component is always visible on initial page load (if it's below the fold, use `#[Lazy]` instead)
- You want to improve perceived performance by showing the page faster


## Learn more[¶](#learn-more "")

For complete documentation on lazy and deferred loading, including placeholders and bundling strategies, see the [Lazy Loading documentation](/docs/4.x/lazy).

## Reference[¶](#reference "")

```
#[Defer(

    bool|null $bundle = null,

)]


```


| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `$bundle` | `bool|null` | `null` | Bundle multiple deferred components into a single network request |
