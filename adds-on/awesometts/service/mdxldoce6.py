# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
#
# Copyright (C) 2016       Anki AwesomeTTS Development Team
# Copyright (C) 2016       Dave Shifflett
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
Service implementation for the LDOCE 6 dictionary on MDX Server
"""

import re

from .base import Service
from .common import Trait

__all__ = ['Collins']


BASE_PATTERN = r'<a href="sound://([\w/]+\w*\.mp3)"><img src="img/spkr_%s.png"></a>'

MAPPINGS = [
    ('br', "British English", 'bre', [re.compile(BASE_PATTERN % r'r')]),
    ('us', "American English", 'usa', [re.compile(BASE_PATTERN % r'b')])
]

LANG_TO_REGEXPS = {lang: regexps for lang, _, _, regexps in MAPPINGS}
DEFAULT_LANG = 'br'

MDX_SERVER = 'http://localhost:8000/'
REQUIRE_MP3 = dict(mime='audio/mpeg', size=256)


class MdxLDOCE6(Service):
    """Provides a Service-compliant implementation for MDX server."""

    __slots__ = []

    NAME = "LDOCE6 on MDX Server"

    TRAITS = [Trait.INTERNET, Trait.DICTIONARY]

    def desc(self):
        """Returns a short, static description."""

        return "LDOCE 6 on MDX Server(%d languages)." % len(MAPPINGS)

    def options(self):
        """Provides access to voice only."""

        voice_lookup = dict([(self.normalize(desc), lang)
                             for lang, desc, _, _ in MAPPINGS] +
                            [(self.normalize(lang), lang)
                             for lang, _, _, _ in MAPPINGS])

        return [
            dict(
                key='voice',
                label="Voice",
                values=[(lang, desc) for lang, desc, _, _ in MAPPINGS],
                transform=lambda value: voice_lookup.get(self.normalize(value),
                                                         value),
                default=DEFAULT_LANG,
            ),
        ]



    def run(self, text, options, path):
        """Find audio filename and then download it."""

        voice = options['voice']

        payload = self.net_stream(MDX_SERVER + text, method='GET')

        for regexp in LANG_TO_REGEXPS[voice]:
            self._logger.debug("MDX Server: trying pattern %s", regexp.pattern)

            match = regexp.search(payload)
            if match:
                self.net_download(path,
                                  MDX_SERVER + match.group(1),
                                  require=REQUIRE_MP3)
                break

        else:
            raise IOError("Cannot find any recorded audio in LDOCE 6 "
                          "dictionary on MDX Server.")
