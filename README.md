# ComposerPackageInfo

A Sublime Text 3 package which provides a popup for Composer packages.

![Capture](https://raw.githubusercontent.com/gh640/SublimeComposerPackageInfo/master/assets/capture.gif)


## Installation

...


## Usage

### Showing package data popup

1. Open a `composer.json` file.
2. Mouse over a package name in `require` or `require-dev`.
3. The meta data of the package is fetched from Packagist ([API](https://packagist.org/apidoc)) and shown in a popup window automatically.

### Clearing local cache

Fetched package data are stored in the local SQLite database `cache.sqlite3` in the pacakge directory. You can delete all the cache with the command `ComposerPackageInfo: Clear all cache`.

1. Open the command palette.
2. Search and select `ComposerPackageInfo: Clear all cache`.
3. The cache data are deleted.


## License

Licensed under the MIT license.
