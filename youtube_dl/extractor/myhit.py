# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class MyHitSerialIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?my-hit\.org/serial/(?P<id>[0-9]+)/?'
    _TESTS = [{
        'url': 'https://my-hit.org/serial/4866/',
        'info_dict': {
            'id': '4866',
            'title': 'Рита (1\xa0сезон)',
        },
        'playlist': [
            {
                'info_dict': {
                    'id': 'my-hit.org/serial/4866/01',
                    'ext': 'flv',
                    'title': r're:\d+ серия',
                }
            },
            {
                'info_dict': {
                    'id': 'my-hit.org/serial/4866/02',
                    'ext': 'flv',
                    'title': '2 серия',
                }
            },
        ]
    }]

    def _real_extract(self, url):
        if not url.endswith("/"):
            url = url + "/"

        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # TODO more code goes here, for example ...
        title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')
        # description = self._html_search_regex(r'<div itemprop="description">(.+?)</div>',
        #                                       webpage, 'description', flags=re.DOTALL)

        # title = 'Рита (1 сезон)'

        playlist = self._download_json(url + "playlist.txt", video_id)

        return {
            'id': video_id,
            'title': title,
            '_type': 'playlist',
            'entries': [
                {
                    'id': 'my-hit.org/serial/{}/{:02d}'.format(video_id, i + 1),
                    'title': item["comment"],
                    'url': item["file"],
                    '_type': 'url_transparent'
                } for i, item in enumerate(playlist["playlist"])
            ]
        }
