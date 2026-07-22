# Prompts

- [Introduction](#introduction)
- [Installation](#installation)
- [Available Prompts](#available-prompts)
  * [Text](#text)
  * [Textarea](#textarea)
  * [Number](#number)
  * [Password](#password)
  * [Confirm](#confirm)
  * [Select](#select)
  * [Multi-select](#multiselect)
  * [Suggest](#suggest)
  * [Search](#search)
  * [Multi-search](#multisearch)
  * [Pause](#pause)
  * [Autocomplete](#autocomplete)
- [Transforming Input Before Validation](#transforming-input-before-validation)
- [Forms](#forms)
- [Informational Messages](#informational-messages)
- [Callouts](#callouts)
- [Tables](#tables)
- [Spin](#spin)
- [Progress Bar](#progress)
- [Task](#task)
- [Stream](#stream)
- [Terminal Title](#terminal-title)
- [Clearing the Terminal](#clear)
- [Terminal Considerations](#terminal-considerations)
- [Unsupported Environments and Fallbacks](#fallbacks)
- [Testing](#testing)

## [Introduction](#introduction)

[Laravel Prompts](https://github.com/laravel/prompts) is a PHP package for adding beautiful and user-friendly forms to your command-line applications, with browser-like features including placeholder text and validation.

Laravel Prompts is perfect for accepting user input in your [Artisan console commands](/docs/13.x/artisan#writing-commands), but it may also be used in any command-line PHP project.

Laravel Prompts supports macOS, Linux, and Windows with WSL. For more information, please see our documentation on [unsupported environments & fallbacks](#fallbacks).

## [Installation](#installation)

Laravel Prompts is already included with the latest release of Laravel.

Laravel Prompts may also be installed in your other PHP projects by using the Composer package manager:

```
1composer require laravel/prompts
```

## [Available Prompts](#available-prompts)

### [Text](#text)

The `text` function will prompt the user with the given question, accept their input, and then return it:

```
1use function Laravel\Prompts\text;

2 

3$name = text('What is your name?');
```

You may also include placeholder text, a default value, and an informational hint:

```
1$name = text(

2    label: 'What is your name?',

3    placeholder: 'E.g. Taylor Otwell',

4    default: $user?->name,

5    hint: 'This will be displayed on your profile.'

6);
```

#### [Required Values](#text-required)

If you require a value to be entered, you may pass the `required` argument:

```
1$name = text(

2    label: 'What is your name?',

3    required: true

4);
```

If you would like to customize the validation message, you may also pass a string:

```
1$name = text(

2    label: 'What is your name?',

3    required: 'Your name is required.'

4);
```

#### [Additional Validation](#text-validation)

Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
1$name = text(

2    label: 'What is your name?',

3    validate: fn (string $value) => match (true) {

4        strlen($value) < 3 => 'The name must be at least 3 characters.',

5        strlen($value) > 255 => 'The name must not exceed 255 characters.',

6        default => null

7    }

8);
```

The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes.

Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument:

```
1$name = text(

2    label: 'What is your name?',

3    validate: ['name' => 'required|max:255|unique:users']

4);
```

### [Textarea](#textarea)

The `textarea` function will prompt the user with the given question, accept their input via a multi-line textarea, and then return it:

```
1use function Laravel\Prompts\textarea;

2 

3$story = textarea('Tell me a story.');
```

You may also include placeholder text, a default value, and an informational hint:

```
1$story = textarea(

2    label: 'Tell me a story.',

3    placeholder: 'This is a story about...',

4    hint: 'This will be displayed on your profile.'

5);
```

#### [Required Values](#textarea-required)

If you require a value to be entered, you may pass the `required` argument:

```
1$story = textarea(

2    label: 'Tell me a story.',

3    required: true

4);
```

If you would like to customize the validation message, you may also pass a string:

```
1$story = textarea(

2    label: 'Tell me a story.',

3    required: 'A story is required.'

4);
```

#### [Additional Validation](#textarea-validation)

Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
1$story = textarea(

2    label: 'Tell me a story.',

3    validate: fn (string $value) => match (true) {

4        strlen($value) < 250 => 'The story must be at least 250 characters.',

5        strlen($value) > 10000 => 'The story must not exceed 10,000 characters.',

6        default => null

7    }

8);
```

The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes.

Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument:

```
1$story = textarea(

2    label: 'Tell me a story.',

3    validate: ['story' => 'required|max:10000']

4);
```

### [Number](#number)

The `number` function will prompt the user with the given question, accept their numeric input, and then return it. The `number` function allows the user to use the up and down arrow keys to manipulate the number:

```
1use function Laravel\Prompts\number;

2 

3$number = number('How many copies would you like?');
```

You may also include placeholder text, a default value, and an informational hint:

```
1$name = number(

2    label: 'How many copies would you like?',

3    placeholder: '5',

4    default: 1,

5    hint: 'This will be determine how many copies to create.'

6);
```

#### [Required Values](#number-required)

If you require a value to be entered, you may pass the `required` argument:

```
1$copies = number(

2    label: 'How many copies would you like?',

3    required: true

4);
```

If you would like to customize the validation message, you may also pass a string:

```
1$copies = number(

2    label: 'How many copies would you like?',

3    required: 'A number of copies is required.'

4);
```

#### [Additional Validation](#number-validation)

Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
1$copies = number(

2    label: 'How many copies would you like?',

3    validate: fn (?int $value) => match (true) {

4        $value < 1 => 'At least one copy is required.',

5        $value > 100 => 'You may not create more than 100 copies.',

6        default => null

7    }

8);
```

The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes.

Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument:

```
1$copies = number(

2    label: 'How many copies would you like?',

3    validate: ['copies' => 'required|integer|min:1|max:100']

4);
```

### [Password](#password)

The `password` function is similar to the `text` function, but the user's input will be masked as they type in the console. This is useful when asking for sensitive information such as passwords:

```
1use function Laravel\Prompts\password;

2 

3$password = password('What is your password?');
```

You may also include placeholder text and an informational hint:

```
1$password = password(

2    label: 'What is your password?',

3    placeholder: 'password',

4    hint: 'Minimum 8 characters.'

5);
```

#### [Required Values](#password-required)

If you require a value to be entered, you may pass the `required` argument:

```
1$password = password(

2    label: 'What is your password?',

3    required: true

4);
```

If you would like to customize the validation message, you may also pass a string:

```
1$password = password(

2    label: 'What is your password?',

3    required: 'The password is required.'

4);
```

#### [Additional Validation](#password-validation)

Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
1$password = password(

2    label: 'What is your password?',

3    validate: fn (string $value) => match (true) {

4        strlen($value) < 8 => 'The password must be at least 8 characters.',

5        default => null

6    }

7);
```

The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes.

Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument:

```
1$password = password(

2    label: 'What is your password?',

3    validate: ['password' => 'min:8']

4);
```

### [Confirm](#confirm)

If you need to ask the user for a "yes or no" confirmation, you may use the `confirm` function. Users may use the arrow keys or press `y` or `n` to select their response. This function will return either `true` or `false`.

```
1use function Laravel\Prompts\confirm;

2 

3$confirmed = confirm('Do you accept the terms?');
```

You may also include a default value, customized wording for the "Yes" and "No" labels, and an informational hint:

```
1$confirmed = confirm(

2    label: 'Do you accept the terms?',

3    default: false,

4    yes: 'I accept',

5    no: 'I decline',

6    hint: 'The terms must be accepted to continue.'

7);
```

#### [Requiring "Yes"](#confirm-required)

If necessary, you may require your users to select "Yes" by passing the `required` argument:

```
1$confirmed = confirm(

2    label: 'Do you accept the terms?',

3    required: true

4);
```

If you would like to customize the validation message, you may also pass a string:

```
1$confirmed = confirm(

2    label: 'Do you accept the terms?',

3    required: 'You must accept the terms to continue.'

4);
```

### [Select](#select)

If you need the user to select from a predefined set of choices, you may use the `select` function:

```
1use function Laravel\Prompts\select;

2 

3$role = select(

4    label: 'What role should the user have?',

5    options: ['Member', 'Contributor', 'Owner']

6);
```

You may also specify the default choice and an informational hint:

```
1$role = select(

2    label: 'What role should the user have?',

3    options: ['Member', 'Contributor', 'Owner'],

4    default: 'Owner',

5    hint: 'The role may be changed at any time.'

6);
```

You may also pass an associative array to the `options` argument to have the selected key returned instead of its value:

```
1$role = select(

2    label: 'What role should the user have?',

3    options: [

4        'member' => 'Member',

5        'contributor' => 'Contributor',

6        'owner' => 'Owner',

7    ],

8    default: 'owner'

9);
```

Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument:

```
1$role = select(

2    label: 'Which category would you like to assign?',

3    options: Category::pluck('name', 'id'),

4    scroll: 10

5);
```

#### [Secondary Information](#select-info)

The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`:

```
 1$role = select(

 2    label: 'What role should the user have?',

 3    options: [

 4        'member' => 'Member',

 5        'contributor' => 'Contributor',

 6        'owner' => 'Owner',

 7    ],

 8    info: fn (string $value) => match ($value) {

 9        'member' => 'Can view and comment.',

10        'contributor' => 'Can view, comment, and edit.',

11        'owner' => 'Full access to all resources.',

12        default => null,

13    }

14);
```

You may also pass a static string to the `info` argument if the information does not depend on the highlighted option:

```
1$role = select(

2    label: 'What role should the user have?',

3    options: ['Member', 'Contributor', 'Owner'],

4    info: 'The role may be changed at any time.'

5);
```

#### [Additional Validation](#select-validation)

Unlike other prompt functions, the `select` function doesn't accept the `required` argument because it is not possible to select nothing. However, you may pass a closure to the `validate` argument if you need to present an option but prevent it from being selected:

```
 1$role = select(

 2    label: 'What role should the user have?',

 3    options: [

 4        'member' => 'Member',

 5        'contributor' => 'Contributor',

 6        'owner' => 'Owner',

 7    ],

 8    validate: fn (string $value) =>

 9        $value === 'owner' && User::where('role', 'owner')->exists()

10            ? 'An owner already exists.'

11            : null

12);
```

If the `options` argument is an associative array, then the closure will receive the selected key, otherwise it will receive the selected value. The closure may return an error message, or `null` if the validation passes.

### [Multi-select](#multiselect)

If you need the user to be able to select multiple options, you may use the `multiselect` function:

```
1use function Laravel\Prompts\multiselect;

2 

3$permissions = multiselect(

4    label: 'What permissions should be assigned?',

5    options: ['Read', 'Create', 'Update', 'Delete']

6);
```

You may also specify default choices and an informational hint:

```
1use function Laravel\Prompts\multiselect;

2 

3$permissions = multiselect(

4    label: 'What permissions should be assigned?',

5    options: ['Read', 'Create', 'Update', 'Delete'],

6    default: ['Read', 'Create'],

7    hint: 'Permissions may be updated at any time.'

8);
```

You may also pass an associative array to the `options` argument to return the selected options' keys instead of their values:

```
 1$permissions = multiselect(

 2    label: 'What permissions should be assigned?',

 3    options: [

 4        'read' => 'Read',

 5        'create' => 'Create',

 6        'update' => 'Update',

 7        'delete' => 'Delete',

 8    ],

 9    default: ['read', 'create']

10);
```

Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument:

```
1$categories = multiselect(

2    label: 'What categories should be assigned?',

3    options: Category::pluck('name', 'id'),

4    scroll: 10

5);
```

#### [Secondary Information](#multiselect-info)

The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`:

```
 1$permissions = multiselect(

 2    label: 'What permissions should be assigned?',

 3    options: [

 4        'read' => 'Read',

 5        'create' => 'Create',

 6        'update' => 'Update',

 7        'delete' => 'Delete',

 8    ],

 9    info: fn (string $value) => match ($value) {

10        'read' => 'View resources and their properties.',

11        'create' => 'Create new resources.',

12        'update' => 'Modify existing resources.',

13        'delete' => 'Permanently remove resources.',

14        default => null,

15    }

16);
```

#### [Requiring a Value](#multiselect-required)

By default, the user may select zero or more options. You may pass the `required` argument to enforce one or more options instead:

```
1$categories = multiselect(

2    label: 'What categories should be assigned?',

3    options: Category::pluck('name', 'id'),

4    required: true

5);
```

If you would like to customize the validation message, you may provide a string to the `required` argument:

```
1$categories = multiselect(

2    label: 'What categories should be assigned?',

3    options: Category::pluck('name', 'id'),

4    required: 'You must select at least one category'

5);
```

#### [Additional Validation](#multiselect-validation)

You may pass a closure to the `validate` argument if you need to present an option but prevent it from being selected:

```
 1$permissions = multiselect(

 2    label: 'What permissions should the user have?',

 3    options: [

 4        'read' => 'Read',

 5        'create' => 'Create',

 6        'update' => 'Update',

 7        'delete' => 'Delete',

 8    ],

 9    validate: fn (array $values) => ! in_array('read', $values)

10        ? 'All users require the read permission.'

11        : null

12);
```

If the `options` argument is an associative array then the closure will receive the selected keys, otherwise it will receive the selected values. The closure may return an error message, or `null` if the validation passes.

### [Suggest](#suggest)

The `suggest` function can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints:

```
1use function Laravel\Prompts\suggest;

2 

3$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

Alternatively, you may pass a closure as the second argument to the `suggest` function. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far and return an array of options for auto-completion:

```
1$name = suggest(

2    label: 'What is your name?',

3    options: fn ($value) => collect(['Taylor', 'Dayle'])

4        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))

5)
```

You may also include placeholder text, a default value, and an informational hint:

```
1$name = suggest(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle'],

4    placeholder: 'E.g. Taylor',

5    default: $user?->name,

6    hint: 'This will be displayed on your profile.'

7);
```

#### [Secondary Information](#suggest-info)

The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`:

```
1$name = suggest(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle'],

4    info: fn (string $value) => match ($value) {

5        'Taylor' => 'Administrator',

6        'Dayle' => 'Contributor',

7        default => null,

8    }

9);
```

#### [Required Values](#suggest-required)

If you require a value to be entered, you may pass the `required` argument:

```
1$name = suggest(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle'],

4    required: true

5);
```

If you would like to customize the validation message, you may also pass a string:

```
1$name = suggest(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle'],

4    required: 'Your name is required.'

5);
```

#### [Additional Validation](#suggest-validation)

Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
1$name = suggest(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle'],

4    validate: fn (string $value) => match (true) {

5        strlen($value) < 3 => 'The name must be at least 3 characters.',

6        strlen($value) > 255 => 'The name must not exceed 255 characters.',

7        default => null

8    }

9);
```

The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes.

Alternatively, you may leverage the power of Laravel's [validator](/docs/13.x/validation). To do so, provide an array containing the name of the attribute and the desired validation rules to the `validate` argument:

```
1$name = suggest(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle'],

4    validate: ['name' => 'required|min:3|max:255']

5);
```

### [Search](#search)

If you have a lot of options for the user to select from, the `search` function allows the user to type a search query to filter the results before using the arrow keys to select an option:

```
1use function Laravel\Prompts\search;

2 

3$id = search(

4    label: 'Search for the user that should receive the mail',

5    options: fn (string $value) => strlen($value) > 0

6        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

7        : []

8);
```

The closure will receive the text that has been typed by the user so far and must return an array of options. If you return an associative array then the selected option's key will be returned, otherwise its value will be returned instead.

When filtering an array where you intend to return the value, you should use the `array_values` function or the `values` Collection method to ensure the array doesn't become associative:

```
1$names = collect(['Taylor', 'Abigail']);

2 

3$selected = search(

4    label: 'Search for the user that should receive the mail',

5    options: fn (string $value) => $names

6        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))

7        ->values()

8        ->all(),

9);
```

You may also include placeholder text and an informational hint:

```
1$id = search(

2    label: 'Search for the user that should receive the mail',

3    placeholder: 'E.g. Taylor Otwell',

4    options: fn (string $value) => strlen($value) > 0

5        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

6        : [],

7    hint: 'The user will receive an email immediately.'

8);
```

Up to five options will be displayed before the list begins to scroll. You may customize this by passing the `scroll` argument:

```
1$id = search(

2    label: 'Search for the user that should receive the mail',

3    options: fn (string $value) => strlen($value) > 0

4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

5        : [],

6    scroll: 10

7);
```

#### [Secondary Information](#search-info)

The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`:

```
1$id = search(

2    label: 'Search for the user that should receive the mail',

3    options: fn (string $value) => strlen($value) > 0

4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

5        : [],

6    info: fn (int $userId) => User::find($userId)?->email

7);
```

#### [Additional Validation](#search-validation)

If you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
 1$id = search(

 2    label: 'Search for the user that should receive the mail',

 3    options: fn (string $value) => strlen($value) > 0

 4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

 5        : [],

 6    validate: function (int|string $value) {

 7        $user = User::findOrFail($value);

 8 

 9        if ($user->opted_out) {

10            return 'This user has opted-out of receiving mail.';

11        }

12    }

13);
```

If the `options` closure returns an associative array, then the closure will receive the selected key, otherwise, it will receive the selected value. The closure may return an error message, or `null` if the validation passes.

### [Multi-search](#multisearch)

If you have a lot of searchable options and need the user to be able to select multiple items, the `multisearch` function allows the user to type a search query to filter the results before using the arrow keys and space-bar to select options:

```
1use function Laravel\Prompts\multisearch;

2 

3$ids = multisearch(

4    'Search for users who should receive the mail',

5    fn (string $value) => strlen($value) > 0

6        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

7        : []

8);
```

The closure will receive the text that has been typed by the user so far and must return an array of options. If you return an associative array then the selected options' keys will be returned; otherwise, their values will be returned instead.

When filtering an array where you intend to return the value, you should use the `array_values` function or the `values` Collection method to ensure the array doesn't become associative:

```
1$names = collect(['Taylor', 'Abigail']);

2 

3$selected = multisearch(

4    label: 'Search for users who should receive the mail',

5    options: fn (string $value) => $names

6        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))

7        ->values()

8        ->all(),

9);
```

You may also include placeholder text and an informational hint:

```
1$ids = multisearch(

2    label: 'Search for users who should receive the mail',

3    placeholder: 'E.g. Taylor Otwell',

4    options: fn (string $value) => strlen($value) > 0

5        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

6        : [],

7    hint: 'The user will receive an email immediately.'

8);
```

Up to five options will be displayed before the list begins to scroll. You may customize this by providing the `scroll` argument:

```
1$ids = multisearch(

2    label: 'Search for the users that should receive the mail',

3    options: fn (string $value) => strlen($value) > 0

4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

5        : [],

6    scroll: 10

7);
```

#### [Secondary Information](#multisearch-info)

The `info` argument may be used to display additional information about the currently highlighted option. When a closure is provided, it will receive the value of the currently highlighted option and should return a string or `null`:

```
1$ids = multisearch(

2    label: 'Search for the users that should receive the mail',

3    options: fn (string $value) => strlen($value) > 0

4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

5        : [],

6    info: fn (int $userId) => User::find($userId)?->email

7);
```

#### [Requiring a Value](#multisearch-required)

By default, the user may select zero or more options. You may pass the `required` argument to enforce one or more options instead:

```
1$ids = multisearch(

2    label: 'Search for the users that should receive the mail',

3    options: fn (string $value) => strlen($value) > 0

4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

5        : [],

6    required: true

7);
```

If you would like to customize the validation message, you may also provide a string to the `required` argument:

```
1$ids = multisearch(

2    label: 'Search for the users that should receive the mail',

3    options: fn (string $value) => strlen($value) > 0

4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

5        : [],

6    required: 'You must select at least one user.'

7);
```

#### [Additional Validation](#multisearch-validation)

If you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
 1$ids = multisearch(

 2    label: 'Search for the users that should receive the mail',

 3    options: fn (string $value) => strlen($value) > 0

 4        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()

 5        : [],

 6    validate: function (array $values) {

 7        $optedOut = User::whereLike('name', '%a%')->findMany($values);

 8 

 9        if ($optedOut->isNotEmpty()) {

10            return $optedOut->pluck('name')->join(', ', ', and ').' have opted out.';

11        }

12    }

13);
```

If the `options` closure returns an associative array, then the closure will receive the selected keys; otherwise, it will receive the selected values. The closure may return an error message, or `null` if the validation passes.

### [Pause](#pause)

The `pause` function may be used to display informational text to the user and wait for them to confirm their desire to proceed by pressing the Enter / Return key:

```
1use function Laravel\Prompts\pause;

2 

3pause('Press ENTER to continue.');
```

### [Autocomplete](#autocomplete)

The `autocomplete` function can be used to provide inline auto-completion for possible choices. As the user types, suggestions that match their input will appear as ghost text that can be accepted by pressing `Tab` or the right arrow key:

```
1use function Laravel\Prompts\autocomplete;

2 

3$name = autocomplete(

4    label: 'What is your name?',

5    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim']

6);
```

You may also include placeholder text, a default value, and an informational hint:

```
1$name = autocomplete(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],

4    placeholder: 'E.g. Taylor',

5    default: $user?->name,

6    hint: 'Use tab to accept, up/down to cycle.'

7);
```

#### [Dynamic Options](#autocomplete-closure)

You may also pass a closure to dynamically generate options based on the user's input. The closure will be called each time the user types a character and should return an array of options for auto-completion:

```
1$file = autocomplete(

2    label: 'Which file?',

3    options: fn (string $value) => collect($files)

4        ->filter(fn ($file) => str_starts_with(strtolower($file), strtolower($value)))

5        ->values()

6        ->all(),

7);
```

#### [Required Values](#autocomplete-required)

If you require a value to be entered, you may pass the `required` argument:

```
1$name = autocomplete(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],

4    required: true

5);
```

If you would like to customize the validation message, you may also pass a string:

```
1$name = autocomplete(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],

4    required: 'Your name is required.'

5);
```

#### [Additional Validation](#autocomplete-validation)

Finally, if you would like to perform additional validation logic, you may pass a closure to the `validate` argument:

```
1$name = autocomplete(

2    label: 'What is your name?',

3    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],

4    validate: fn (string $value) => match (true) {

5        strlen($value) < 3 => 'The name must be at least 3 characters.',

6        strlen($value) > 255 => 'The name must not exceed 255 characters.',

7        default => null

8    }

9);
```

The closure will receive the value that has been entered and may return an error message, or `null` if the validation passes.

## [Transforming Input Before Validation](#transforming-input-before-validation)

Sometimes you may want to transform the prompt input before validation takes place. For example, you may wish to remove white space from any provided strings. To accomplish this, many of the prompt functions provide a `transform` argument, which accepts a closure:

```
1$name = text(

2    label: 'What is your name?',

3    transform: fn (string $value) => trim($value),

4    validate: fn (string $value) => match (true) {

5        strlen($value) < 3 => 'The name must be at least 3 characters.',

6        strlen($value) > 255 => 'The name must not exceed 255 characters.',

7        default => null

8    }

9);
```

## [Forms](#forms)

Often, you will have multiple prompts that will be displayed in sequence to collect information before performing additional actions. You may use the `form` function to create a grouped set of prompts for the user to complete:

```
1use function Laravel\Prompts\form;

2 

3$responses = form()

4    ->text('What is your name?', required: true)

5    ->password('What is your password?', validate: ['password' => 'min:8'])

6    ->confirm('Do you accept the terms?')

7    ->submit();
```

The `submit` method will return a numerically indexed array containing all of the responses from the form's prompts. However, you may provide a name for each prompt via the `name` argument. When a name is provided, the named prompt's response may be accessed via that name:

```
 1use App\Models\User;

 2use function Laravel\Prompts\form;

 3 

 4$responses = form()

 5    ->text('What is your name?', required: true, name: 'name')

 6    ->password(

 7        label: 'What is your password?',

 8        validate: ['password' => 'min:8'],

 9        name: 'password'

10    )

11    ->confirm('Do you accept the terms?')

12    ->submit();

13 

14User::create([

15    'name' => $responses['name'],

16    'password' => $responses['password'],

17]);
```

The primary benefit of using the `form` function is the ability for the user to return to previous prompts in the form using `CTRL + U`. This allows the user to fix mistakes or alter selections without needing to cancel and restart the entire form.

If you need more granular control over a prompt in a form, you may invoke the `add` method instead of calling one of the prompt functions directly. The `add` method is passed all previous responses provided by the user:

```
 1use function Laravel\Prompts\form;

 2use function Laravel\Prompts\outro;

 3use function Laravel\Prompts\text;

 4 

 5$responses = form()

 6    ->text('What is your name?', required: true, name: 'name')

 7    ->add(function ($responses) {

 8        return text("How old are you, {$responses['name']}?");

 9    }, name: 'age')

10    ->submit();

11 

12outro("Your name is {$responses['name']} and you are {$responses['age']} years old.");
```

## [Informational Messages](#informational-messages)

The `note`, `info`, `warning`, `error`, and `alert` functions may be used to display informational messages:

```
1use function Laravel\Prompts\info;

2 

3info('Package installed successfully.');
```

## [Callouts](#callouts)

The `callout` function displays a boxed message with a label and content. Callouts are useful for displaying important information that should stand out, such as deployment summaries, error details, or status updates:

```
1use function Laravel\Prompts\callout;

2 

3callout(

4    label: 'Environment Configured',

5    content: 'Your application is running in production mode with 4 workers.',

6);
```

You may pass `warning` or `error` as the `type` argument to change the callout's visual style:

```
 1callout(

 2    label: 'Deprecation Notice',

 3    content: 'The `--prefer-stable` flag will be removed in v4.0. Use `--stability=stable` instead.',

 4    type: 'warning',

 5);

 6 

 7callout(

 8    label: 'Database Connection Failed',

 9    content: 'Could not connect to MySQL on 127.0.0.1:3306.',

10    type: 'error',

11);
```

The `info` argument adds a footer line to the callout, which is useful for displaying metadata like IDs or timestamps:

```
1callout(

2    label: 'Deployment Summary',

3    content: 'Your application was deployed to production.',

4    info: 'deploy-id: d4f8a2c',

5);
```

#### [Rich Content](#callout-rich-content)

Instead of passing a string, you may pass an array of strings and elements to build rich, structured callouts. The `Element` class provides factory methods for creating headings, bulleted lists, numbered lists, key-value lists, and links:

```
 1use Laravel\Prompts\Elements\Element;

 2 

 3use function Laravel\Prompts\callout;

 4 

 5callout('Deployment Summary', [

 6    'Your application was deployed to production at 2024-03-15 14:32 UTC.',

 7    Element::heading('What Changed'),

 8    Element::bulletedList([

 9        'Migrated 3 pending database migrations',

10        'Cleared and rebuilt route cache',

11        'Restarted 4 queue workers',

12    ]),

13    Element::heading('Next Steps'),

14    Element::numberedList([

15        'Verify the health check endpoint at /up',

16        'Monitor error rates for the next 15 minutes',

17        'Confirm background jobs are processing',

18    ]),

19]);
```

You may also use `Element::keyValueList` to display labeled data:

```
1callout('Database Connection Failed', [

2    'Could not connect to the database server.',

3    Element::keyValueList([

4        'Host' => '127.0.0.1',

5        'Port' => '3306',

6        'Database' => 'forge',

7        'Status' => 'Connection refused',

8    ]),

9], type: 'error');
```

The `Element::link` method creates a clickable hyperlink in terminals that support [OSC 8](https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda). You may provide a URL alone, or a URL with a custom label:

```
1callout('Server Health Check', [

2    'Multiple services are reporting degraded performance.',

3    Element::heading('Affected Services'),

4    'Look here: '.Element::link('https://example.com/health', 'Health Dashboard'),

5    Element::link('https://example.com/health'),

6]);
```

If no label is provided, the URL itself will be displayed as the link text.

## [Tables](#tables)

The `table` function makes it easy to display multiple rows and columns of data. All you need to do is provide the column names and the data for the table:

```
1use function Laravel\Prompts\table;

2 

3table(

4    headers: ['Name', 'Email'],

5    rows: User::all(['name', 'email'])->toArray()

6);
```

## [Spin](#spin)

The `spin` function displays a spinner along with an optional message while executing a specified callback. It serves to indicate ongoing processes and returns the callback's results upon completion:

```
1use function Laravel\Prompts\spin;

2 

3$response = spin(

4    callback: fn () => Http::get('http://example.com'),

5    message: 'Fetching response...'

6);
```

The `spin` function requires the [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP extension to animate the spinner. When this extension is not available, a static version of the spinner will appear instead.

## [Progress Bars](#progress)

For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `progress` function, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value:

```
1use function Laravel\Prompts\progress;

2 

3$users = progress(

4    label: 'Updating users',

5    steps: User::all(),

6    callback: fn ($user) => $this->performTask($user)

7);
```

The `progress` function acts like a map function and will return an array containing the return value of each iteration of your callback.

The callback may also accept the `Laravel\Prompts\Progress` instance, allowing you to modify the label and hint on each iteration:

```
 1$users = progress(

 2    label: 'Updating users',

 3    steps: User::all(),

 4    callback: function ($user, $progress) {

 5        $progress

 6            ->label("Updating {$user->name}")

 7            ->hint("Created on {$user->created_at}");

 8 

 9        return $this->performTask($user);

10    },

11    hint: 'This may take some time.'

12);
```

Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar via the `advance` method after processing each item:

```
 1$progress = progress(label: 'Updating users', steps: 10);

 2 

 3$users = User::all();

 4 

 5$progress->start();

 6 

 7foreach ($users as $user) {

 8    $this->performTask($user);

 9 

10    $progress->advance();

11}

12 

13$progress->finish();
```

## [Task](#task)

The `task` function displays a labeled task with a spinner and a scrolling live output area while a given callback is executing. It is ideal for wrapping long-running processes such as dependency installation or deployment scripts, providing real-time visibility into what is happening:

```
1use function Laravel\Prompts\task;

2 

3task(

4    label: 'Installing dependencies',

5    callback: function ($logger) {

6        // Long-running process...

7    }

8);
```

The callback receives a `Logger` instance that you may use to display log lines, status messages, and streamed text in the task's output area.

The `task` function requires the [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP extension to animate the spinner. When this extension is not available, a static version of the task will appear instead.

#### [Logging Lines](#task-logging)

The `line` method writes a single log line to the task's scrolling output area:

```
1task(

2    label: 'Installing dependencies',

3    callback: function ($logger) {

4        $logger->line('Resolving packages...');

5        // ...

6        $logger->line('Downloading laravel/framework');

7        // ...

8    }

9);
```

#### [Status Messages](#task-status-messages)

You may use the `success`, `warning`, and `error` methods to display status messages. These appear as stable, highlighted messages above the scrolling log area:

```
 1task(

 2    label: 'Deploying application',

 3    callback: function ($logger) {

 4        $logger->line('Pulling latest changes...');

 5        // ...

 6        $logger->success('Changes pulled!');

 7 

 8        $logger->line('Running migrations...');

 9        // ...

10        $logger->warning('No new migrations to run.');

11 

12        $logger->line('Clearing cache...');

13        // ...

14        $logger->success('Cache cleared!');

15    }

16);
```

#### [Updating the Label](#task-label)

The `label` method allows you to update the task's label while it is running:

```
 1task(

 2    label: 'Starting deployment...',

 3    callback: function ($logger) {

 4        $logger->label('Pulling latest changes...');

 5        // ...

 6        $logger->label('Running migrations...');

 7        // ...

 8        $logger->label('Clearing cache...');

 9        // ...

10    }

11);
```

#### [Displaying a Sub-Label](#task-sub-label)

The `subLabel` method displays a dim line beneath the task's main label, which is useful for communicating ephemeral status such as the step currently in progress. Pass an empty string to clear the sub-label:

```
 1task(

 2    label: 'Deploying',

 3    callback: function ($logger) {

 4        $logger->subLabel('Building assets...');

 5        // ...

 6        $logger->subLabel('Running migrations...');

 7        // ...

 8        $logger->subLabel('');

 9    }

10);
```

You may also provide an initial sub-label via the `subLabel` argument:

```
1task(

2    label: 'Deploying',

3    callback: function ($logger) {

4        // ...

5    },

6    subLabel: 'Preparing...'

7);
```

#### [Streaming Text](#task-streaming)

For processes that produce output incrementally, such as AI-generated responses, the `partial` method allows you to stream text word-by-word or chunk-by-chunk. Once the stream is complete, call `commitPartial` to finalize the output:

```
 1task(

 2    label: 'Generating response...',

 3    callback: function ($logger) {

 4        foreach ($words as $word) {

 5            $logger->partial($word . ' ');

 6        }

 7 

 8        $logger->commitPartial();

 9    }

10);
```

#### [Customizing the Output Limit](#task-limit)

By default, the task displays up to 10 lines of scrolling output. You may customize this via the `limit` argument:

```
1task(

2    label: 'Installing dependencies',

3    callback: function ($logger) {

4        // ...

5    },

6    limit: 20

7);
```

#### [Keeping the Summary](#task-keep-summary)

By default, the task's output is erased once the callback finishes. If you would like to keep the status messages on screen after the task has completed, you may pass the `keepSummary` argument:

```
1task(

2    label: 'Deploying',

3    callback: function ($logger) {

4        $logger->success('Assets built');

5        // ...

6        $logger->success('Migrations complete');

7    },

8    keepSummary: true,

9);
```

## [Stream](#stream)

The `stream` function displays text that streams into the terminal, ideal for displaying AI-generated content or any text that arrives incrementally:

```
 1use function Laravel\Prompts\stream;

 2 

 3$stream = stream();

 4 

 5foreach ($words as $word) {

 6    $stream->append($word . ' ');

 7    usleep(25_000); // Simulate delay between chunks...

 8}

 9 

10$stream->close();
```

The `append` method adds text to the stream, rendering it with a gradual fade-in effect. When all content has been streamed, call the `close` method to finalize the output and restore the cursor.

## [Terminal Title](#terminal-title)

The `title` function updates the title of the user's terminal window or tab:

```
1use function Laravel\Prompts\title;

2 

3title('Installing Dependencies');
```

To reset the terminal title back to its default, pass an empty string:

```
1title('');
```

## [Clearing the Terminal](#clear)

The `clear` function may be used to clear the user's terminal:

```
1use function Laravel\Prompts\clear;

2 

3clear();
```

## [Terminal Considerations](#terminal-considerations)

#### [Terminal Width](#terminal-width)

If the length of any label, option, or validation message exceeds the number of "columns" in the user's terminal, it will be automatically truncated to fit. Consider minimizing the length of these strings if your users may be using narrower terminals. A typically safe maximum length is 74 characters to support an 80-character terminal.

#### [Terminal Height](#terminal-height)

For any prompts that accept the `scroll` argument, the configured value will automatically be reduced to fit the height of the user's terminal, including space for a validation message.

## [Unsupported Environments and Fallbacks](#fallbacks)

Laravel Prompts supports macOS, Linux, and Windows with WSL. Due to limitations in the Windows version of PHP, it is not currently possible to use Laravel Prompts on Windows outside of WSL.

For this reason, Laravel Prompts supports falling back to an alternative implementation such as the [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html).

When using Laravel Prompts with the Laravel framework, fallbacks for each prompt have been configured for you and will be automatically enabled in unsupported environments.

#### [Fallback Conditions](#fallback-conditions)

If you are not using Laravel or need to customize when the fallback behavior is used, you may pass a boolean to the `fallbackWhen` static method on the `Prompt` class:

```
1use Laravel\Prompts\Prompt;

2 

3Prompt::fallbackWhen(

4    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()

5);
```

#### [Fallback Behavior](#fallback-behavior)

If you are not using Laravel or need to customize the fallback behavior, you may pass a closure to the `fallbackUsing` static method on each prompt class:

```
 1use Laravel\Prompts\TextPrompt;

 2use Symfony\Component\Console\Question\Question;

 3use Symfony\Component\Console\Style\SymfonyStyle;

 4 

 5TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {

 6    $question = (new Question($prompt->label, $prompt->default ?: null))

 7        ->setValidator(function ($answer) use ($prompt) {

 8            if ($prompt->required && $answer === null) {

 9                throw new \RuntimeException(

10                    is_string($prompt->required) ? $prompt->required : 'Required.'

11                );

12            }

13 

14            if ($prompt->validate) {

15                $error = ($prompt->validate)($answer ?? '');

16 

17                if ($error) {

18                    throw new \RuntimeException($error);

19                }

20            }

21 

22            return $answer;

23        });

24 

25    return (new SymfonyStyle($input, $output))

26        ->askQuestion($question);

27});
```

Fallbacks must be configured individually for each prompt class. The closure will receive an instance of the prompt class and must return an appropriate type for the prompt.

## [Testing](#testing)

Laravel provides a variety of methods for testing that your command displays the expected Prompt messages:

Pest

PHPUnit

```
 1test('report generation', function () {

 2    $this->artisan('report:generate')

 3        ->expectsPromptsInfo('Welcome to the application!')

 4        ->expectsPromptsWarning('This action cannot be undone')

 5        ->expectsPromptsError('Something went wrong')

 6        ->expectsPromptsAlert('Important notice!')

 7        ->expectsPromptsIntro('Starting process...')

 8        ->expectsPromptsOutro('Process completed!')

 9        ->expectsPromptsTable(

10            headers: ['Name', 'Email'],

11            rows: [

12                ['Taylor Otwell', '[[email protected]](/cdn-cgi/l/email-protection)'],

13                ['Jason Beggs', '[[email protected]](/cdn-cgi/l/email-protection)'],

14            ]

15        )

16        ->assertExitCode(0);

17});
```

```
 1public function test_report_generation(): void

 2{

 3    $this->artisan('report:generate')

 4        ->expectsPromptsInfo('Welcome to the application!')

 5        ->expectsPromptsWarning('This action cannot be undone')

 6        ->expectsPromptsError('Something went wrong')

 7        ->expectsPromptsAlert('Important notice!')

 8        ->expectsPromptsIntro('Starting process...')

 9        ->expectsPromptsOutro('Process completed!')

10        ->expectsPromptsTable(

11            headers: ['Name', 'Email'],

12            rows: [

13                ['Taylor Otwell', '[[email protected]](/cdn-cgi/l/email-protection)'],

14                ['Jason Beggs', '[[email protected]](/cdn-cgi/l/email-protection)'],

15            ]

16        )

17        ->assertExitCode(0);

18}
```
