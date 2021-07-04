# ComposerPackageInfo

A Sublime Text 3 / 4 package which provides a popup for Composer packages.

![Capture](https://raw.githubusercontent.com/gh640/SublimeComposerPackageInfo/master/assets/capture.png)


## Installation

1. Install the [Package Control](https://packagecontrol.io/installation) to your Sublime Text 3.
2. Open the command palette and select `Package Controll: Install Package`.
3. Search for and select `ComposerPackageInfo`.


## Usage

### Showing package data popup

1. Open a `composer.json` file.
2. Mouse over a package name in `require` or `require-dev`.
3. The meta data of the package is fetched from Packagist ([API](https://packagist.org/apidoc)) and shown in a popup window automatically.

![Capture](https://raw.githubusercontent.com/gh640/SublimeComposerPackageInfo/master/assets/capture.gif)

### Clearing local cache

Fetched package data are stored in the local SQLite database `cache.sqlite3` in the Sublime Text's cache directory. You can delete all the cache with the command `ComposerPackageInfo: Clear all cache`.

1. Open the command palette.
2. Search and select `ComposerPackageInfo: Clear all cache`.
3. The cache data are deleted.


## Settings

There are following setting options.

- `cache_max_count`

`cache_max_count`
:    (default: `1000`) Max number of locally cached package data. If the number of cached pacakge data gets greater than this value, old tuples are deleted from the database table for cache.


## Links

- [`PhpArrayConverter`](https://github.com/gh640/SublimePhpArrayConverter): A Sublime Text 3 package which converts PHP array syntax.
- [`PypiPackageInfo`](https://github.com/gh640/SublimePypiPackageInfo): `ComposerPackageInfo` for Python (PyPI) packages.


## License

Licensed under the MIT license.
