[Forms](/docs/5.x/forms/overview)

# Markdown editor

## [​](#introduction)Introduction

The markdown editor allows you to edit and preview markdown content, as well as upload images using drag and drop.

```
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
```

## [​](#security)Security

By default, the editor outputs raw Markdown and HTML, and sends it to the backend. Attackers are able to intercept the value of the component and send a different raw HTML string to the backend. As such, it is important that when outputting the HTML from a Markdown editor, it is sanitized; otherwise your site may be exposed to Cross-Site Scripting (XSS) vulnerabilities. When Filament outputs raw HTML from the database in components such as `TextColumn` and `TextEntry`, it sanitizes it to remove any dangerous JavaScript. However, if you are outputting the HTML from a Markdown editor in your own Blade view, this is your responsibility. One option is to use Filament’s `sanitizeHtml()` helper to do this, which is the same tool we use to sanitize HTML in the components mentioned above:

```
{!! str($record->content)->markdown()->sanitizeHtml() !!}
```

Filament’s built-in HTML sanitizer permits inline `style` attributes in order to support rich text formatting features such as font colors, text highlighting, and image sizing. This means that CSS properties like `background: url(...)` or `position: fixed` will not be stripped from sanitized HTML. If your content comes from untrusted users, you should consider restricting the default configuration. See the [security documentation](../advanced/security#customizing-the-sanitizer) for details on how to customize the sanitizer.

## [​](#customizing-the-toolbar-buttons)Customizing the toolbar buttons

You may set the toolbar buttons for the editor using the `toolbarButtons()` method. The options shown here are the defaults:

```
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
    ->toolbarButtons([
        ['bold', 'italic', 'strike', 'link'],
        ['heading'],
        ['blockquote', 'codeBlock', 'bulletList', 'orderedList'],
        ['table', 'attachFiles'],
        ['undo', 'redo'],
    ])
```

Each nested array in the main array represents a group of buttons in the toolbar.

## [​](#uploading-images-to-the-editor)Uploading images to the editor

Images may be uploaded to the editor. They will always be uploaded to a publicly available URL with public storage permissions, since generating temporary file upload URLs is not supported in static content. You may customize where images are uploaded using configuration methods:

```
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
    ->fileAttachmentsDisk('s3')
    ->fileAttachmentsDirectory('attachments')
```

### [​](#validating-uploaded-images)Validating uploaded images

You may use the `fileAttachmentsAcceptedFileTypes()` method to control a list of accepted mime types for uploaded images. By default, `image/png`, `image/jpeg`, `image/gif`, and `image/webp` are accepted:

```
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
    ->fileAttachmentsAcceptedFileTypes(['image/png', 'image/jpeg'])
```

You may use the `fileAttachmentsMaxSize()` method to control the maximum file size for uploaded images. The size is specified in kilobytes. By default, the maximum size is 12288 KB (12 MB):

```
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
    ->fileAttachmentsMaxSize(5120) // 5 MB
```

[Rich editor](/docs/5.x/forms/rich-editor)[Repeater](/docs/5.x/forms/repeater)

[github](https://github.com/filamentphp/filament)[bluesky](https://bsky.app/profile/filamentphp.com)[x](https://twitter.com/filamentphp)[discord](https://filamentphp.com/discord)[linkedin](https://linkedin.com/company/filamentphp)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=filament-34a8cf01)
