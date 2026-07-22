[Schemas](/docs/5.x/schemas/overview)

# Callouts

## [​](#introduction)Introduction

Callouts are used to draw attention to important information or messages. They are often used for alerts, notices, or tips. You can create a callout using the `Callout` component:

```
use Filament\Schemas\Components\Callout;

Callout::make('New version available')
    ->description('Filament v4 has been released with exciting new features and improvements.')
    ->info()
```

## [​](#using-status-variants)Using status variants

Callouts have built-in status variants that automatically set the appropriate icon, icon color, and background color. You can use the `danger()`, `info()`, `success()`, or `warning()` methods:

```
use Filament\Schemas\Components\Callout;

Callout::make('Payment successful')
    ->description('Your order has been confirmed and is being processed.')
    ->success()

Callout::make('Session expiring soon')
    ->description('Your session will expire in 5 minutes. Save your work to avoid losing changes.')
    ->warning()

Callout::make('Connection failed')
    ->description('Unable to connect to the server. Please check your internet connection.')
    ->danger()
```

### [​](#accessibility-of-status-variants)Accessibility of status variants

Since a callout’s status is conveyed visually through its icon and background color, Filament also announces it to screen readers. When you use a status variant, a visually-hidden severity prefix (`Error:`, `Note:`, `Success:`, or `Warning:`) is rendered inside the callout’s heading, so assistive technology users hear the severity before the message. The leading icon is marked as decorative (`aria-hidden`) so it is not announced separately. Callouts render as a plain `<div>`, which is correct for content that is present when the page loads. If you reveal a callout dynamically (for example, after an action completes) and want screen readers to announce it, opt into a live region using `extraAttributes()`:

```
use Filament\Schemas\Components\Callout;

Callout::make('Changes saved')
    ->success()
    ->extraAttributes(['role' => 'status']) // Use `alert` instead of `status` for urgent messages
```

## [​](#removing-the-background-color)Removing the background color

By default, status callouts have a colored background. You can remove the background color while keeping the status icon and icon color by using `color(null)`:

```
use Filament\Schemas\Components\Callout;

Callout::make('Scheduled maintenance')
    ->description('The system will be unavailable on Sunday from 2:00 AM to 4:00 AM.')
    ->warning()
    ->color(null)
```

## [​](#adding-a-custom-icon)Adding a custom icon

You can add a custom [icon](/docs/5.x/styling/icons) to the callout using the `icon()` method:

```
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('Pro tip')
    ->description('You can use keyboard shortcuts to navigate faster. Press ? to see all available shortcuts.')
    ->icon(Heroicon::OutlinedLightBulb)
```

### [​](#changing-the-icon-color)Changing the icon color

You can change the icon color using the `iconColor()` method:

```
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('Pro tip')
    ->description('You can use keyboard shortcuts to navigate faster. Press ? to see all available shortcuts.')
    ->icon(Heroicon::OutlinedLightBulb)
    ->iconColor('primary')
```

### [​](#changing-the-icon-size)Changing the icon size

By default, the icon size is “large”. You can change it to “small” or “medium” using the `iconSize()` method:

```
use Filament\Schemas\Components\Callout;
use Filament\Support\Enums\IconSize;

Callout::make('Quick note')
    ->description('This callout has a smaller icon.')
    ->info()
    ->iconSize(IconSize::Small)
```

## [​](#using-a-custom-background-color)Using a custom background color

You can set a custom background color using the `color()` method:

```
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('Pro tip')
    ->description('You can use keyboard shortcuts to navigate faster. Press ? to see all available shortcuts.')
    ->color('primary')
    ->icon(Heroicon::OutlinedLightBulb)
    ->iconColor('primary')
```

## [​](#adding-actions-to-the-callout-footer)Adding actions to the callout footer

You can add [actions](/docs/5.x/actions) to the callout footer using the `actions()` method:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;

Callout::make('Your trial ends in 3 days')
    ->description('Upgrade now to keep access to all premium features.')
    ->warning()
    ->actions([
        Action::make('upgrade')
            ->label('Upgrade to Pro')
            ->button(),
        Action::make('compare')
            ->label('Compare plans'),
    ])
```

### [​](#changing-the-footer-actions-alignment)Changing the footer actions alignment

By default, actions are aligned to the start. You can change the alignment using the `footerActionsAlignment()` method:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;
use Filament\Support\Enums\Alignment;

Callout::make('Updates available')
    ->description('New features and improvements are ready to install.')
    ->info()
    ->actions([
        Action::make('install')->label('Install Now'),
        Action::make('later')->label('Remind Me Later'),
    ])
    ->footerActionsAlignment(Alignment::End)
```

The available alignment options are `Alignment::Start`, `Alignment::Center`, `Alignment::End`, and `Alignment::Between`.

## [​](#adding-custom-footer-content)Adding custom footer content

You can add custom content to the footer using the `footer()` method. This accepts an array of schema components:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;
use Filament\Schemas\Components\Text;

Callout::make('Backup complete')
    ->description('Your data has been successfully backed up to the cloud.')
    ->success()
    ->footer([
        Text::make('Last backup: 5 minutes ago')
            ->color('gray'),
        Action::make('viewBackups')
            ->label('View All Backups')
            ->button(),
    ])
```

## [​](#adding-custom-control-content)Adding custom control content

You can add custom content to the controls (top-right corner) using the `controls()` method. This accepts an array of schema components:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;

Callout::make('Backup complete')
    ->description('Your data has been successfully backed up to the cloud.')
    ->success()
    ->controls([
        Action::make('dismiss')
            ->icon('heroicon-m-x-mark')
            ->iconButton()
            ->color('gray'),
    ])
```

## [​](#adding-control-actions-to-the-callout)Adding control actions to the callout

You can add control [actions](/docs/5.x/actions) to the top-right corner of the callout using the `controlActions()` method. For example, you could add a dismiss button that hides the callout for the duration of the user’s session:

```
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('New version available')
    ->description('Filament v4 has been released with exciting new features and improvements.')
    ->info()
    ->controlActions([
        Action::make('dismiss')
            ->icon(Heroicon::XMark)
            ->iconButton()
            ->color('gray')
            ->action(fn () => session()->put('new-version-callout-dismissed', true)),
    ])
    ->visible(fn (): bool => ! session()->get('new-version-callout-dismissed'))
```

[Wizards](/docs/5.x/schemas/wizards)[Empty states](/docs/5.x/schemas/empty-states)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
