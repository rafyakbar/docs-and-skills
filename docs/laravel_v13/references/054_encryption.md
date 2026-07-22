# Encryption

- [Introduction](#introduction)
- [Configuration](#configuration)
  * [Gracefully Rotating Encryption Keys](#gracefully-rotating-encryption-keys)
- [Using the Encrypter](#using-the-encrypter)

## [Introduction](#introduction)

Laravel's encryption services provide a simple, convenient interface for encrypting and decrypting text via OpenSSL using AES-256 and AES-128 encryption. All of Laravel's encrypted values are signed using a message authentication code (MAC) so that their underlying value cannot be modified or tampered with once encrypted.

## [Configuration](#configuration)

Before using Laravel's encrypter, you must set the `key` configuration option in your `config/app.php` configuration file. This configuration value is driven by the `APP_KEY` environment variable. You should use the `php artisan key:generate` command to generate this variable's value since the `key:generate` command will use PHP's secure random bytes generator to build a cryptographically secure key for your application. Typically, the value of the `APP_KEY` environment variable will be generated for you during [Laravel's installation](/docs/13.x/installation).

### [Gracefully Rotating Encryption Keys](#gracefully-rotating-encryption-keys)

If you change your application's encryption key, all authenticated user sessions will be logged out of your application. This is because every cookie, including session cookies, are encrypted by Laravel. In addition, it will no longer be possible to decrypt any data that was encrypted with your previous encryption key.

To mitigate this issue, Laravel allows you to list your previous encryption keys in your application's `APP_PREVIOUS_KEYS` environment variable. This variable may contain a comma-delimited list of all of your previous encryption keys:

```
1APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="

2APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

When you set this environment variable, Laravel will always use the "current" encryption key when encrypting values. However, when decrypting values, Laravel will first try the current key, and if decryption fails using the current key, Laravel will try all previous keys until one of the keys is able to decrypt the value.

This approach to graceful decryption allows users to keep using your application uninterrupted even if your encryption key is rotated.

## [Using the Encrypter](#using-the-encrypter)

#### [Encrypting a Value](#encrypting-a-value)

You may encrypt a value using the `encryptString` method provided by the `Crypt` facade. All encrypted values are encrypted using OpenSSL and the AES-256-CBC cipher. Furthermore, all encrypted values are signed with a message authentication code (MAC). The integrated message authentication code will prevent the decryption of any values that have been tampered with by malicious users:

```
 1<?php

 2 

 3namespace App\Http\Controllers;

 4 

 5use Illuminate\Http\RedirectResponse;

 6use Illuminate\Http\Request;

 7use Illuminate\Support\Facades\Crypt;

 8 

 9class DigitalOceanTokenController extends Controller

10{

11    /**

12     * Store a DigitalOcean API token for the user.

13     */

14    public function store(Request $request): RedirectResponse

15    {

16        $request->user()->fill([

17            'token' => Crypt::encryptString($request->token),

18        ])->save();

19 

20        return redirect('/secrets');

21    }

22}
```

#### [Decrypting a Value](#decrypting-a-value)

You may decrypt values using the `decryptString` method provided by the `Crypt` facade. If the value cannot be properly decrypted, such as when the message authentication code is invalid, an `Illuminate\Contracts\Encryption\DecryptException` will be thrown:

```
1use Illuminate\Contracts\Encryption\DecryptException;

2use Illuminate\Support\Facades\Crypt;

3 

4try {

5    $decrypted = Crypt::decryptString($encryptedValue);

6} catch (DecryptException $e) {

7    // ...

8}
```
