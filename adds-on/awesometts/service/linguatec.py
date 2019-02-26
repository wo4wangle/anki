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
Service implementation for Linguatec's text-to-speech demo engine
"""

from re import compile as re_compile
from socket import error as SocketError  # non-caching error class

from .base import Service
from .common import Trait

__all__ = ['Linguatec']


# list of (API name, human-readable name, language code) tuples
VOICES = [('Alice-ml', "Alice", 'it'), ('Allison', "Allison", 'en-US'),
          ('alva', "Alva", 'sv'), ('Amelie', "Amelie", 'fr-CA'),
          ('angelica', "Angelica", 'es-MX'), ('Anna-ml', "Anna", 'de'),
          ('Audrey-ml', "Audrey", 'fr'), ('Aurelie', "Aurelie", 'fr'),
          ('Ava', "Ava", 'en-US'), ('Carlos', "Carlos", 'es-CO'),
          ('Carmela', "Carmela", 'gl'), ('Carmit', "Carmit", 'he'),
          ('Catarina', "Catarina", 'pt'), ('cem', "Cem", 'tr'),
          ('Chantal', "Chantal", 'fr-CA'), ('Claire', "Claire", 'nl-NL'),
          ('Damayanti', "Damayanti", 'id'), ('Daniel', "Daniel", 'en-GB'),
          ('diego', "Diego", 'es-AR'), ('Ellen', "Ellen", 'nl-BE'),
          ('Empar', "Empar", 'ca-Valencian'), ('Ewa', "Ewa", 'pl'),
          ('Federica', "Federica", 'it'), ('Felipe', "Felipe", 'pt-BR'),
          ('Fiona', "Fiona", 'en-Scottish'), ('Henrik', "Henrik", 'no'),
          ('Ioana', "Ioana", 'ro'), ('iveta', "Iveta", 'cs'),
          ('Joana', "Joana", 'pt'), ('Jordi', "Jordi", 'ca'),
          ('jorge', "Jorge", 'es'), ('juan', "Juan", 'es-MX'),
          ('Kanya', "Kanya", 'th'), ('Karen', "Karen", 'en-AU'),
          ('Kate', "Kate", 'en-GB'), ('Katya', "Katya", 'ru'),
          ('klara', "Klara", 'sv'), ('Kyoko', "Kyoko", 'ja'),
          ('Laura', "Laura", 'sk'), ('Lee', "Lee", 'en-AU'),
          ('Lekha', "Lekha", 'hi'), ('Luca', "Luca", 'it'),
          ('Luciana', "Luciana", 'pt-BR'), ('Magnus', "Magnus", 'da'),
          ('mariska', "Mariska", 'hu'), ('Markus', "Markus", 'de'),
          ('Mei-Jia', "Mei-Jia", 'zh-TW'), ('Melina', "Melina", 'el'),
          ('Milena', "Milena", 'ru'), ('Miren', "Miren", 'eu'),
          ('Moira', "Moira", 'en-IE'), ('monica', "Monica", 'es'),
          ('Montserrat', "Montserrat", 'ca'), ('Nicolas', "Nicolas", 'fr-CA'),
          ('Nikos', "Nikos", 'el'), ('Nora', "Nora", 'no'),
          ('Oliver', "Oliver", 'en-GB'), ('oskar', "Oskar", 'sv'),
          ('Otoya', "Otoya", 'ja'), ('Paola', "Paola", 'it'),
          ('paulina', "Paulina", 'es-MX'), ('Petra', "Petra", 'de'),
          ('Samantha', "Samantha", 'en-US'), ('Sara', "Sara", 'da'),
          ('Satu', "Satu", 'fi'), ('Serena', "Serena", 'en-GB'),
          ('Sin-Ji', "Sin-Ji", 'zh-HK'), ('Soledad', "Soledad", 'es-CO'),
          ('Sora', "Sora", 'ko'), ('Susan', "Susan", 'en-US'),
          ('Tarik', "Tarik", 'ar'), ('Tessa', "Tessa", 'en-ZA'),
          ('Thomas', "Thomas", 'fr'), ('Tian-Tian', "Tian-Tian", 'zh-CN'),
          ('Tom', "Tom", 'en-US'), ('Veena', "Veena", 'en-IN'),
          ('Xander', "Xander", 'nl-NL'), ('Yannick', "Yannick", 'de'),
          ('yelda', "Yelda", 'tr'), ('yuri', "Yuri", 'ru'),
          ('Zosia', "Zosia", 'pl'), ('zuzana', "Zuzana", 'cs')]

FORM_ENDPOINT = 'http://www.linguatec.net/onlineservices/vrs15_getmp3'

RE_MP3 = re_compile(r'https?://[-\w.]+\.linguatec\.org/[-\w/]+\.mp3')

REQUIRE_MP3 = dict(mime='audio/mpeg', size=256)


class Linguatec(Service):
    """
    Provides a Service-compliant implementation for Linguatec.
    """

    __slots__ = [
    ]

    NAME = "Linguatec"

    TRAITS = [Trait.INTERNET]

    def desc(self):
        """Returns name with a voice count."""

        return "Linguatec Demo (%d voices)" % len(VOICES)

    def options(self):
        """Provides access to voice only."""

        voice_lookup = dict([(self.normalize(human_name), api_name)
                             for api_name, human_name, _ in VOICES] +
                            [(self.normalize(api_name), api_name)
                             for api_name, human_name, _ in VOICES])

        def transform_voice(value):
            """Fixes whitespace, casing, and human names."""
            normal = self.normalize(value)
            return voice_lookup[normal] if normal in voice_lookup else value

        return [dict(key='voice',
                     label="Voice",
                     values=[(api_name, "%s (%s)" % (human_name, language))
                             for api_name, human_name, language
                             in sorted(VOICES,
                                       key=lambda item: (item[2], item[1]))],
                     transform=transform_voice)]

    def run(self, text, options, path):
        """Requests MP3 URLs and then downloads them."""

        voice = options['voice']

        def fetch_piece(subtext, subpath):
            """Fetch given phrase from demo to given path."""

            payload = self.net_stream(
                (
                    FORM_ENDPOINT,
                    dict(
                        text=subtext,
                        voiceName=voice,
                        speakSpeed=100,
                        speakPith=100,  # sic
                        speakVolume=100,
                    ),
                ),
            )
            match = RE_MP3.search(payload)
            if not match:
                raise SocketError("No MP3 was returned for the input.")
            url = match.group(0)
            self.net_download(subpath, url, require=REQUIRE_MP3)

        subtexts = self.util_split(text, 250)  # see `maxlength` on site
        if len(subtexts) == 1:
            fetch_piece(text, path)
        else:
            intermediate_mp3s = []
            try:
                for subtext in subtexts:
                    intermediate_mp3 = self.path_temp('mp3')
                    intermediate_mp3s.append(intermediate_mp3)
                    fetch_piece(subtext, intermediate_mp3)
                self.util_merge(intermediate_mp3s, path)
            finally:
                self.path_unlink(intermediate_mp3s)
