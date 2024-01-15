# python_spotify_analyser

Python3 application for extracting useful data from Spotify.

Based on spotipy.

---

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