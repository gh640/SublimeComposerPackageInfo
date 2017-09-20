# coding: utf-8

'''Provides function related to PHP Composer packages.
'''

import json
import os.path
import re
import webbrowser
import requests
import sublime
import sublime_plugin
import mdpopups


URL_JSON = 'https://packagist.org/packages/{package}.json'
URL_PAGE = 'https://packagist.org/packages/{package}'
TEMPLATE = '''
# {name}

{description}

- Stats: DL {downloads_total} / Fav {favers}
- Page: [Packagist]({url_packagist}) / [Repository]({url_repo})
- Command: [require]({command_require}) / [remove]({command_remove})

<div class="close-btn-wrapper">
    <a href="close">{close_btn}</a>
</div>
'''
CSS = '''
body {
    margin: 0;
    padding: 0;
}
.mdpopups {
}
.composer-package-info {
    font-size: 12px;
    line-height: 20px;
    padding: 0 18px 10px 10px;
}
.composer-package-info h1 {
    background-color: var(--mdpopups-admon-success-bg);
    color: var(--mdpopups-admon-success-title-fg);
    font-family: var(--mdpopups-font-mono);
    font-size: 12px;
    line-height: 12px;
    margin: 0 -18px 10px -10px;
    padding: 10px;
}
.composer-package-info p {
    margin: 6px 0;
}
.composer-package-info ul {
    margin: 6px 0;
}
.close-btn-wrapper {
    margin-top: 12px;
}
.close-btn-wrapper a {
    text-decoration: none;
}
'''
WRAPPER_CLASS = 'composer-package-info'
CMD_REQUIRE = 'composer require {}'
CMD_REMOVE = 'composer remove {}'
PREFIX_COPY = 'copy: '
MESSAGE_KEY = 'composer_info'
MESSAGE_TTL = 2000
LENGTH_DESC = 100


class ComposerInfoPackageInfo(sublime_plugin.ViewEventListener):
    '''A view event listener for showing composer package data.
    '''

    def on_hover(self, point, hover_zone):
        if not self._is_composer():
            return

        if not self._is_on_text(hover_zone):
            return

        if not self._is_in_scope(point):
            return

        package_name = self._get_selected_pacakge_name(point)
        if not self._is_valid_package_name(package_name):
            return

        self.view.set_status(MESSAGE_KEY, 'Fetching data...')
        try:
            data_raw = self._fetch_package_info(package_name)
            data = self._extract_pakcage_info(data_raw, package_name)
        except BaseException as e:
            sublime.set_timeout(lambda: self.view.erase_status(MESSAGE_KEY),
                                MESSAGE_TTL)
            raise e
        else:
            self._show_popup(data, point)
            self.view.set_status(MESSAGE_KEY, 'Data fetched successfully.')
            sublime.set_timeout(lambda: self.view.erase_status(MESSAGE_KEY),
                                MESSAGE_TTL)

    def _is_composer(self):
        return self._get_basename() == 'composer.json'

    def _get_basename(self):
        return os.path.basename(self.view.file_name())

    def _is_on_text(self, hover_zone):
        return hover_zone == sublime.HOVER_TEXT

    def _is_in_scope(self, point):
        scope_name = self.view.scope_name(point)
        names = [
            'meta.structure.dictionary.key.json',
            'string.quoted.double.json'
        ]
        return all(n in scope_name for n in names)

    def _get_selected_pacakge_name(self, point):
        quoted_text = self.view.substr(self.view.extract_scope(point))
        package_name = quoted_text.strip('"')
        return package_name

    def _is_valid_package_name(self, name):
        if re.match(r'[\w-]+/[\w-]+', name):
            return True
        return False

    def _fetch_package_info(self, name):
        response = requests.get(URL_JSON.format(package=name))
        if not response.status_code != '200':
            raise BaseException('Package data fetch failed.')
        return json.loads(response.text)

    def _extract_pakcage_info(self, data, name):
        try:
            package = data['package']
            name = package['name']
            url = URL_PAGE.format(package=package['name'])
            description = self._truncate(package['description'], LENGTH_DESC)
            print(data)
            return {
                'name': name,
                'description': description,
                'downloads_total': package['downloads']['total'],
                'favers': package['favers'],
                'url_packagist': url,
                'url_repo': package['repository'],
                'command_require': PREFIX_COPY + CMD_REQUIRE.format(name),
                'command_remove': PREFIX_COPY + CMD_REMOVE.format(name),
                'close_btn': '[' + chr(0x00D7) + ']',
            }
        except Exception as e:
            raise BaseException('Package data extraction failed.')

    def _show_popup(self, data, location):
        if mdpopups.is_popup_visible(self.view):
            mdpopups.hide_popup(self.view)

        mdpopups.show_popup(self.view,
                            TEMPLATE.format(**data),
                            css=CSS,
                            wrapper_class=WRAPPER_CLASS,
                            max_width=400,
                            location=location,
                            flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                            on_navigate=self.on_phantom_click)

    def on_phantom_click(self, href):
        if href.startswith('https://'):
            webbrowser.open_new_tab(href)
        elif href.startswith(PREFIX_COPY):
            sublime.set_clipboard(href[len(PREFIX_COPY):])

        mdpopups.hide_popup(self.view)

    def _truncate(self, string, count):
        return string[:count] + ('...' if string[count:] else '')


class BaseException(Exception):
    pass
