# coding: utf-8
from __future__ import unicode_literals

import re

try:
    from urllib.parse import urljoin  # Python3
except ImportError:
    from urlparse import urljoin  # Python2


from .common import InfoExtractor


class NambaIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?namba\.tv/video/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'https://namba.tv/video/248837/psihologini-2-sezon-720p/',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'description': 'Что такое «когнитивная беспомощность», «синдром самозванца» и «демон ревности» выпускницы психфака Вика, Таня и Алина знают не понаслышке. Правда, встретившись ',
            'id': '248837',
            'thumbnail': 'https://namba.tv/tv/media/thumbs/b5cf4450dc4352d226beefb5e470fe2d-342.jpg',
            'title': 'Психологини - 2 сезон. | 720p',
        },
        'playlist_mincount': 13,
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        player_link = urljoin(url,
                              self._html_search_regex(r'<iframe[^>]+ src="([^"]+)"', webpage, 'player_link'))
        player = self._download_webpage(player_link, video_id, note='Downloading player')
        player_js = self._search_regex(r'new\s+Playerjs\((.+)\);', player, flags=re.DOTALL, name='player_json')

        titles = re.findall(r'"title"\s*:\s*"([^"]+)"', player_js)[1:]
        videos = re.findall(r'"file"\s*:\s*"([^"]+)"', player_js)

        playlist_title = self._og_search_title(webpage)

        entries = [
            {
                'title': '{}: {}'.format(playlist_title, title),
                'url': urljoin(player_link, video),
                'id': self._search_regex(r'videos/([0-9]+)/', video, 'video_id'),
            }
            for title, video in zip(titles, videos)
        ]

        for entry in entries:
            entry['formats'] = self._extract_m3u8_formats(entry['url'], entry['id'])

        data = {
            'id': video_id,
            'title': playlist_title,
            'description': self._og_search_description(webpage),
            'thumbnail': self._og_search_thumbnail(webpage),
            '_type': 'playlist',
            'entries': entries
        }

        print(data)

        return data
