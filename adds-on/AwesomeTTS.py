# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
#
# Copyright (C) 2010-2016  Anki AwesomeTTS Development Team
# Copyright (C) 2010-2013  Arthur Helfstein Fragoso
# Copyright (C) 2013-2016  Dave Shifflett
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Entry point for AwesomeTTS add-on from Anki

Performs any migration tasks and then loads the 'awesometts' package.
Need help or more information? Visit one of these places...

- https://ankiatts.appspot.com                    Documentation
- https://anki.tenderapp.com/discussions/add-ons  Support Forum
- https://github.com/AwesomeTTS/AwesomeTTS        Source, Issues, Pulls
- https://ankiweb.net/shared/info/301952613       User Reviews
"""

import os
from sys import stderr

__all__ = []


if __name__ == "__main__":
    stderr.write(
        "AwesomeTTS is a text-to-speech add-on for Anki.\n"
        "It is not intended to be run directly.\n"
        "To learn more or download Anki, please visit <http://ankisrs.net>.\n"
    )
    exit(1)


# Begin temporary migration code from Beta 10 and older (unless noted)

def os_call(callee, *args, **kwargs):
    """Call the function with the given arguments, ignoring OSError."""

    try:
        callee(*args, **kwargs)
    except OSError:
        pass

_PKG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'awesometts')

for _filename in ['logger.py', 'logger.pyc', 'logger.pyo',  # dropped for 1.5
                  'main.py', 'main.pyc', 'main.pyo',
                  'util.py', 'util.pyc', 'util.pyo']:
    os_call(os.unlink, os.path.join(_PKG, _filename))

for _directory, _rmdir, _filenames in [
        ('designer', True, [
            'configurator.ui', 'filegenerator.ui', 'massgenerator.ui',
        ]),
        ('forms', True, [
            'configurator.py', 'configurator.pyc', 'configurator.pyo',
            'filegenerator.py', 'filegenerator.pyc', 'filegenerator.pyo',
            'massgenerator.py', 'massgenerator.pyc', 'massgenerator.pyo',
            '__init__.py', '__init__.pyc', '__init__.pyo',
        ]),
        ('service', False, [
            'sapi5.js',   # for 1.0 thru 1.2
            'sapi5.vbs',  # for Beta 11 and older
        ]),
        ('services', True, [
            'ekho.py', 'ekho.pyc', 'ekho.pyo',
            'espeak.py', 'espeak.pyc', 'espeak.pyo',
            'Google.py', 'Google.pyc', 'Google.pyo',
            'sapi5.py', 'sapi5.pyc', 'sapi5.pyo', 'sapi5.vbs',
            'say.py', 'say.pyc', 'say.pyo',
            '__init__.py', '__init__.pyc', '__init__.pyo',
        ]),
        ('tools', True, [
            'build_ui.sh',
        ]),
]:
    for _filename in _filenames:
        os_call(os.unlink, os.path.join(_PKG, _directory, _filename))

    if _rmdir:
        os_call(os.rmdir, os.path.join(_PKG, _directory))

os_call(
    os.rename,
    os.path.join(_PKG, 'conf.db'),
    os.path.join(_PKG, 'config.db'),
)

# End temporary migration code


# n.b. Import is intentionally placed down here so that Python processes it
# after *after* any package migration steps above (e.g. module renames) occur.

import awesometts  # noqa, pylint:disable=wrong-import-position


# If a specific component of AwesomeTTS that you do not need is causing a
# problem (e.g. conflicting with another add-on), you can disable it here by
# prefixing it with a hash (#) sign and restarting Anki.

awesometts.browser_menus()     # mass generator and MP3 stripper
awesometts.cache_control()     # automatically clear the media cache regularly
awesometts.cards_button()      # on-the-fly templater helper in card view
awesometts.config_menu()       # provides access to configuration dialog
awesometts.editor_button()     # single audio clip generator button
awesometts.reviewer_hooks()    # on-the-fly playback/shortcuts, context menus
awesometts.sound_tag_delays()  # delayed playing of stored [sound]s in review
awesometts.temp_files()        # remove temporary files upon session exit
awesometts.update_checker()    # if enabled, runs the add-on update checker
awesometts.window_shortcuts()  # enable/update shortcuts for add-on windows
