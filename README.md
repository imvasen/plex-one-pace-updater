# One Pace Updater (for Plex)

![sh1](./assets/one-pace-sh.png)
![sh2](./assets/ennies-lobby-sh.png)

If you have Plex and want to store your [One Pace](one-pace-home) episode's
collection, this script might help you.

One Pace is not an official anime, so Plex Series Scanner won't find it
anywhere, thus it won't be able to update One Pace's metadata.

This script allows you to automate the process of renaming One Pace episodes and
seasons manually.

## Requirements

### Python 3.9

Once you have Python installed, you also need to install requirements.

```bash
pip install -r requirements.txt
```

### `.env` file

Create a `.env` file at `plex_one_pace_updater/` in this repository and add the
following values:

- `PLEX_TOKEN`: To find this you need to inspect the requests Plex does to your
  server when authenticated. [Check this](plex-token-how-to) to find it faster.
- `PLEX_URL`: This is the location of your Plex server. It probably is
  `http://localhost:32400` or `http://<server-ip>:32400`.

Your `.env` should look like this:

```bash
PLEX_TOKEN='the_value_you_copied_and_pasted_from_the_request'
PLEX_URL='localhost:32400'
```

### Folder structure

In order for the script to work, Plex should already know where the seasons and
episodes are in your library. If it doesn't, you probably need to
modify your folder structure as explained [here](plex-folder-structure).

## Run the script

Once the requirements are met, do:

```bash
python one_pace_updater.py
```

### What does the script do?

The script is written in Python for easier understanding of the code. A more
detailed explanation:

1. Connect to Plex via `plexapi` library.
2. Connect to One Pace's official site and download JSON with information about
   the episodes.
3. Iterate over seasons in the JSON, search for them in your Plex library and,
   if exists, add the season title.
   - Iterate over episodes in the season, search for them in your Plex library,
     and, if exists, add information (title, manga chapters the episode what
     based in, description) from the JSON to the episode in your library.

[one-pace-home]: https://onepace.net
[plex-token-how-to]: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
[plex-folder-structure]: https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/
