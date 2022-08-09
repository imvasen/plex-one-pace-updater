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

one_pace_req = requests.get('https://api.onepace.net//list_progress_episodes.php')
one_pace_data = one_pace_req.json()

arcs_episodes = {}
for episode in one_pace_data['episodes']:
    if f'{episode["arc_id"]}' not in arcs_episodes:
        arcs_episodes[f'{episode["arc_id"]}'] = []
    arcs_episodes[f'{episode["arc_id"]}'].append(episode)

plex_show = plex.library.section('Anime').get('One Pace')
plex_show.uploadArt('https://pbs.twimg.com/media/EUolT2OWsAYzRM8?format=jpg&name=large')
plex_show.uploadPoster('https://dg31sz3gwrwan.cloudfront.net/poster/335179/1317675-4-optimized.jpg')

for season, arc in enumerate(one_pace_data['arcs']):
    try:
        plex_season = plex_show.season(season)
    except plexapi.exceptions.NotFound:
        print('S%02d: %s Not Found' % (season, arc['title']))
        continue

    poster_url = f'https://onepace.net/_next/image?url=%2Fimages%2Farcs%2Fcover-{"-".join(arc["title"].lower().split(" "))}-arc_405w.webp&w=828&q=75'
    plex_season.uploadPoster(poster_url)
    plex_season.uploadArt(poster_url)
    plex_season.edit(**{
        'title.value': arc['title'],
        'summary.value': (
            f'Chapters: {arc["chapters"]}\n'
            f'Episodes: {arc["episodes"]}'
        ),
    })

    for episode in arcs_episodes[f'{arc["id"]}']:
        try:
            plex_episode = plex_season.episode(episode['part'])
        except plexapi.exceptions.NotFound:
            print('S%02d E%02d: %s - %s Not Found' % (season, episode['part'], arc['title'], episode['title']))
            continue
        plex_episode.edit(**{
            'title.value': episode['title'],
            'summary.value': (
                f'Chapters: {episode["chapters"]}\n'
                f'Episodes: {episode["episodes"]}'
            ),
        })
