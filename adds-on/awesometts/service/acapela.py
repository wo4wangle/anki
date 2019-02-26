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
Service implementation for the Acapela Group's text-to-speech demo
"""

from re import compile as re_compile

from .base import Service
from .common import Trait

__all__ = ['Acapela']


LANGS = {'Alice': 'fr-FR', 'Alyona': 'ru', 'Andreas': 'de', 'Ania': 'pl',
         'Antoine': 'fr-FR', 'AntoineFromAfar (emotive voice)': 'fr-FR',
         'AntoineHappy (emotive voice)': 'fr-FR',
         'AntoineSad (emotive voice)': 'fr-FR',
         'AntoineUpClose (emotive voice)': 'fr-FR', 'Antonio': 'es-ES',
         'Bente': 'no', 'Biera': 'se', 'Bruno': 'fr-FR', 'Celia': 'pt-PT',
         'Chiara': 'it', 'Claire': 'fr-FR', 'Claudia': 'de', 'Daan': 'nl-NL',
         'Deepa': 'en-IN', 'Dimitris': 'el',
         'DimitrisHappy (emotive voice)': 'el',
         'DimitrisSad (emotive voice)': 'el', 'Elin': 'sv', 'Eliska': 'cs',
         'Ella (genuine child voice)': 'en-US', 'Elle': 'se', 'Emil': 'sv',
         'Emilio (genuine child voice)': 'es-US',
         'EmilioEnglish (genuine child voice)': 'en-US', 'Emma': 'sv',
         'Erik': 'sv', 'Fabiana': 'it', 'Femke': 'nl-NL', 'Graham': 'en-GB',
         'Hanna': 'fo', 'Hanus': 'fo', 'Harry (genuine child voice)': 'en-GB',
         'Ines': 'es-ES', 'Ipek': 'tr', 'Jasmijn': 'nl-NL', 'Jeroen': 'nl-BE',
         'JeroenHappy (emotive voice)': 'nl-BE',
         'JeroenSad (emotive voice)': 'nl-BE',
         'Jonas (genuine child voice)': 'de',
         'Josh (genuine child voice)': 'en-US', 'Julia': 'de',
         'Julie': 'fr-FR', 'Justine': 'fr-BE', 'Kal': 'sv-Gothenburg',
         'Karen': 'en-US', 'Kari': 'no',
         'Kenny (artificial child voice)': 'en-US', 'Klaus': 'de',
         'Laia': 'ca', 'Laura': 'en-US', 'Lea (genuine child voice)': 'de',
         'Leila': 'ar', 'Liam (genuine child voice)': 'en-AU',
         'Lisa': 'en-AU', 'Louise': 'fr-CA', 'Lucy': 'en-GB', 'Lulu': 'zh',
         'Manon': 'fr-FR', 'Marcia': 'pt-BR', 'Margaux': 'fr-FR',
         'MargauxHappy (emotive voice)': 'fr-FR',
         'MargauxSad (emotive voice)': 'fr-FR', 'Maria': 'es-ES',
         'Max': 'nl-NL', 'Mehdi': 'ar', 'Mette': 'da', 'Mia': 'sv-Scanian',
         'Micah': 'en-US', 'Minji': 'ko', 'Monika': 'pl',
         'Nelly (artificial child voice)': 'en-US', 'Nizar': 'ar',
         'Nizareng': 'en-GB', 'Olav': 'no',
         'Olivia (genuine child voice)': 'en-AU', 'Peter': 'en-GB',
         'PeterHappy (emotive voice)': 'en-GB',
         'PeterSad (emotive voice)': 'en-GB',
         'QueenElizabeth (her majesty)': 'en-GB', 'Rachel': 'en-GB',
         'Rasmus': 'da', 'Rhona': 'en-Scottish', 'Rod': 'en-US',
         'Rodrigo': 'es-US', 'Rosa': 'es-US',
         'Rosie (genuine child voice)': 'en-GB', 'Ryan': 'en-US',
         'Sakura': 'ja', 'Salma': 'ar', 'Samuel': 'sv-FI', 'Sanna': 'fi',
         'Sarah': 'de', 'Saul': 'en-US',
         'Scott (genuine teenager voice)': 'en-US', 'Sharon': 'en-US',
         'Sofie': 'nl-BE', 'Tracy': 'en-US', 'Tyler': 'en-AU',
         'Valeria (genuine child voice)': 'es-US',
         'ValeriaEnglish (genuine child voice)': 'en-US', 'Vittorio': 'it',
         'Will': 'en-US', 'WillBadGuy (emotive voice)': 'en-US',
         'WillFromAfar (emotive voice)': 'en-US',
         'WillHappy (emotive voice)': 'en-US',
         'WillLittleCreature (emotive voice)': 'en-US',
         'WillOldMan (emotive voice)': 'en-US',
         'WillSad (emotive voice)': 'en-US',
         'WillUpClose (emotive voice)': 'en-US', 'Zoe': 'nl-BE'}

VOICES = {long_voice_name.partition(' ')[0]: (long_voice_name, language_code)
          for long_voice_name, language_code in LANGS.items()}

assert len(LANGS) == len(VOICES)

FORM_ENDPOINT = 'http://www.acapela-group.com/demo-tts/DemoHTML5Form_V2.php'

RE_MP3 = re_compile(r'https?://[-\w]+\.acapela-group\.com/[-\w/]+\.mp3')

REQUIRE_MP3 = dict(mime='audio/mpeg', size=256)


class Acapela(Service):
    """
    Provides a Service-compliant implementation for Acapela.
    """

    __slots__ = [
    ]

    NAME = "Acapela Group"

    TRAITS = [Trait.INTERNET]

    def desc(self):
        """Returns service name with a voice count."""

        return "Acapela Group TTS Demo (%d voices)" % len(VOICES)

    def options(self):
        """Provides access to voice only."""

        voice_lookup = {self.normalize(key): key for key in VOICES.keys()}

        def transform_voice(value):
            """Fixes whitespace and casing errors only."""
            normal = self.normalize(value)
            return voice_lookup[normal] if normal in voice_lookup else value

        return [
            dict(
                key='voice',
                label="Voice",
                values=[
                    (
                        short_voice_name,
                        "%s (%s)" % (short_voice_name, language_code),
                    )
                    for short_voice_name, (_, language_code)
                    in sorted(VOICES.items(), key=lambda voice: voice[1][1])
                ],
                transform=transform_voice,
            ),
        ]

    def run(self, text, options, path):
        """Requests MP3 URLs and then downloads them."""

        long_voice_name = VOICES[options['voice']][0]

        def fetch_piece(subtext, subpath):
            """
            Gets the MP3 URL for the given subtext and downloads it to
            the given subpath.
            """

            payload = self.net_stream(
                (
                    FORM_ENDPOINT,
                    dict(
                        MySelectedVoice=long_voice_name,
                        MyTextForTTS=subtext,
                        SendToVaaS='',
                        t=1,
                    ),
                ),
                method='POST',
            )
            match = RE_MP3.search(payload)
            match = match.group(0)
            self.net_download(subpath, match, require=REQUIRE_MP3)

        subtexts = self.util_split(text, 300)  # see `maxlength` on site
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
