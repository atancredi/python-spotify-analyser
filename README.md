# ___Fuck Spotify___
While you are boasting your little 2024 Wrapped, Spotify had the brilliant idea to close a lot of their API endpoints.
- ### Which ones?
    They just stopped providing their own AI-elaborated data! Such as related artists, recommendations, audio feature, audio analysis and algorimtic/editorial playlist created by them.
- ### Why?
    While claiming the measure aimed to ['creating a more secure platform'](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api), it is SO obvious that the only reason is this: [AI Playlist Is Rolling Out in Beta in the US, Canada, Ireland, and New Zealand — September 24, 2024](https://newsroom.spotify.com/2024-09-24/ai-playlist-expanding-usa-canada-ireland-new-zealand/).

    So... they want us to pay for a service that was free, and most importantly *THEY WANT TO KILL THE COMPETITION ON AI PLAYLIST GENERATION TOOLS*.

    Is this acceptable? Considering how they get their money by exploiting artists, that's more than enough.
 
- ### I encourage you to have a look at the community's reaction... [here](https://community.spotify.com/t5/Spotify-for-Developers/Changes-to-Web-API/td-p/6540414)

# python_spotify_analyser

Python3 application for extracting useful data from Spotify.
Based on spotipy and pytubefix for audio downloading.

## How to use the Command Line Interface
<!-- TODO instructions on how to get playlist uri and how to set up a virtual environment -->
0. Make sure you are running at least python3 (tested on python 3.10.6):
    You can check with
    ```
    python --version
    ```

1. Install all the requirements
    ```
    python -m pip install -r requirements.txt
    ```

2. Use:
    ```
    python spotify_analyser -m <mode> -i <Spotify ID / URI>
    ```
    **Specify the mode with the `-m` flag:** `['playlist', 'artist']`

    **Specify the URI given by Spotify with the `-i` flag** (required).

    The `-o` flag can optionally be used to give a custom name to the output file (default: `output.txt`).

    The `-h` flag can be used to get help
    The `--reduced` flag can be used to print a more compact result

    The result will be written in a file in `results/` folder

    Example scan for playlist:
    ```
    python spotify_analyser -m playlist -i 2isAAljf09SJuE8QTUWzVl
    ```

### Note:
    The Spotify playlist URI must refer to a public playlist.