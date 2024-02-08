from plexapi.server import PlexServer
from dotenv import load_dotenv
import plexapi
import requests
import os

# Looks in your .env for PLEX_TOKEN & PLEX_URL
load_dotenv()

plex_url = os.environ['PLEX_URL']
plex_token = os.environ['PLEX_TOKEN']
plex = PlexServer(plex_url, plex_token)

one_pace_req = requests.get('https://onepace.net/_next/data/TtwDgBpWkBKTVC0Z4pbfI/en/watch.json')
one_pace_data = one_pace_req.json()['pageProps']['arcs']

plex_show = plex.library.section('Anime').get('One Pace')
plex_show.uploadArt('https://pbs.twimg.com/media/EUolT2OWsAYzRM8?format=jpg&name=large')
plex_show.uploadPoster('https://dg31sz3gwrwan.cloudfront.net/poster/335179/1317675-4-optimized.jpg')

for season, arc in enumerate(one_pace_data, 1):
    try:
        plex_season = plex_show.season(season)
    except plexapi.exceptions.NotFound:
        print('S%02d: %s Not Found' % (season, arc['invariant_title']))
        continue

    if arc['images'][0]:
        poster_url = f"https://onepace.net/_next/image?url=%2Fimages%2Farcs%2F{arc['images'][0]['src']}&w=828&q=75"
        plex_season.uploadPoster(poster_url)
        plex_season.uploadArt(poster_url)

    translation = {}
    for t in arc['translations']:
        if t['language_code'] == 'en':
            translation = t

    plex_season.edit(**{
        'title.value': translation['title'],
        'summary.value': (
            f'Anime Episodes: {arc["anime_episodes"]} | '
            f'Manga Chapters: {arc["manga_chapters"]}\n'
            f"{translation['description']}"
        ),
    })

    for episode in arc['episodes']:
        try:
            plex_episode = plex_season.episode(episode['part'])
        except plexapi.exceptions.NotFound:
            print('S%02d E%02d: %s - %s Not Found' % (season, episode['part'], arc['invariant_title'], episode['invariant_title']))
            continue

        translation = {}
        for t in episode['translations']:
            if t['language_code'] == 'en':
                translation = t

        plex_episode.edit(**{
            'title.value': translation['title'],
            'summary.value': (
                f'Anime Episodes: {episode["anime_episodes"]} | '
                f'Manga Chapters: {episode["manga_chapters"]}\n'
                f"{translation['description']}"
            ),
        })

