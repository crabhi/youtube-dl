# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class MyHitSerialIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?my-hit\.org/serial/(?P<id>[0-9]+)/?'
    _TESTS = [{
#         'url': 'https://my-hit.org/serial/4866/',
#         'info_dict': {
#             'id': '4866',
#             'title': 'Рита (1\xa0сезон)',
#         },
#         'playlist': [
#             {
#                 'info_dict': {
#                     'id': 'my-hit.org/serial/4866/01/01',
#                     'ext': 'flv',
#                     'title': r're:\d+ серия',
#                     'series': 'Рита (1\xa0сезон)',
#                 }
#             },
#             {
#                 'info_dict': {
#                     'id': 'my-hit.org/serial/4866/01/02',
#                     'ext': 'flv',
#                     'title': '2 серия',
#                     'series': 'Рита (1\xa0сезон)',
#                     'episode_number': 2,
#                 }
#             },
#         ],
#     }, {
        'url': 'https://my-hit.org/serial/939',
        'info_dict': {
            'id': '939',
            'title': 'В поиске (1-2\xa0сезон)',
        },
        'playlist': [
            {
                'info_dict': {
                    'id': 'my-hit.org/serial/939/01/05',
                    'ext': 'flv',
                    'title': '5 серия',
                    'season': '1 сезон',
                    'series': 'В поиске (1-2\xa0сезон)',
                    'episode_number': 5,
                },
            },
            {
                'info_dict': {
                    'id': 'my-hit.org/serial/939/02/01',
                    'ext': 'flv',
                    'title': '1 серия',
                    'season': '2 сезон',
                    'series': 'В поиске (1-2\xa0сезон)',
                    'episode_number': 1,
                },
            },
        ],
    }]

    def _real_extract(self, url):
        if not url.endswith("/"):
            url = url + "/"

        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')
        # description = self._html_search_regex(r'<div itemprop="description">(.+?)</div>',
        #                                       webpage, 'description', flags=re.DOTALL)

        playlist = self._download_json(url + "playlist.txt", video_id)["playlist"]

        if "pltitle" in playlist[0]:
            entries = [self._get_season(it["playlist"], video_id, season=it["pltitle"], series=title, season_number=i+1) for i, it in enumerate(playlist)]
        else:
            entries = [self._get_season(playlist, video_id, series=title)]

        return {
            'id': video_id,
            'title': title,
            '_type': 'playlist',
            'entries': [it for season in entries for it in season],
        }

    def _get_season(self, playlist, video_id, **kwargs):
        season_number = kwargs.get("season_number", 1)
        return [
            dict(
                id='my-hit.org/serial/{}/{:02d}/{:02d}'.format(video_id, season_number, i + 1),
                episode_number=i + 1,
                title=item["comment"],
                url=item["file"],
                _type='url_transparent',
                **kwargs)
            for i, item in enumerate(playlist)
        ]


