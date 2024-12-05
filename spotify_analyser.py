import spotipy
from typing import List
from dataclasses import dataclass

from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from typing import Optional, Any
from pytubefix import Search, YouTube


###################
#   DATA MODELS   #
###################
# REGION

@dataclass
class SongFeatures:
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    type: str
    id: str
    uri: str
    track_href: str
    analysis_url: str
    duration_ms: int
    time_signature: int

@dataclass
class SongData:

    position: Optional[int]
    uri: str
    name: str
    artist_uri: str
    artist_info: dict
    artist_name: str
    artist_pop: Any
    artist_genres: Any
    album: str
    popularity: float
    track_pop: Any
    # features: Optional[SongFeatures]
    duration: Optional[float]
    
    def __init__(self):
        self.position = None
        self.uri = ""
        self.name = ""
        self.artist_uri = ""
        self.artist_info = ""
        self.artist_name = ""
        self.artist_pop = ""
        self.artist_genres = ""
        self.album = ""
        self.track_pop = ""
        # self.features = None
        self.duration = None

    def get_reduced(self):
        # minutes, seconds = divmod(self.features.duration_ms / 1000, 60)
        return {
            "position": self.position,
            "name": self.name,
            "artist_name": self.artist_name,
            "album": self.album,
            # "tempo": self.features.tempo,
            # "duration": f'{minutes:0>2.0f}:{seconds:.3f}'
        }
# ENDREGION

####################
#   SCAN METHODS   #
####################
# REGION

def get_client(cid,secret) -> spotipy.Spotify:
    #Authentication - without user
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    return spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def scan_artist(sp: spotipy.Spotify, artist_uri: str) -> List[SongData]:
    """
    Retrieves song data for a given artist.

    Args:
        artist_uri (str): The URI of the artist.

    Returns:
        List[SongData]: A list of SongData objects containing information about the songs.

    """

    ################
    song_data = []
    # READ DATA
    artist_data = sp.artist(artist_uri)
    # popularity = artist_data["popularity"] NOSONAR

    albums = sp.artist_albums(artist_uri, "album")["items"]
    singles = sp.artist_albums(artist_uri, "single")["items"]
    appears_on = sp.artist_albums(artist_uri, "appears_on")["items"]

    for album in albums + singles + appears_on:
        print(f"({album['album_group']}, {album['album_type']}) - {album['name']}")

        tracks = sp.album_tracks(album["id"])["items"]
        for t in tracks:
            track = sp.track(t["id"])

            print(f"    {track['name']}")
            data_item = SongData()

            data_item.track_pop = track["popularity"]
            data_item.uri = track["uri"]
            data_item.name = track["name"]
        
            #Main Artist
            data_item.artist_uri = artist_uri
            data_item.artist_genres = artist_data["genres"]
            data_item.artist_pop = artist_data["popularity"]
            data_item.album = album["name"]
            data_item.artist_name = artist_data["name"]

            data_item.features = SongFeatures(**sp.audio_features(track["id"])[0])

            song_data.append(data_item)
    return song_data

def scan_playlist(sp: spotipy.Spotify, playlist_uri: str, reduced = False) -> List[SongData]:
    """
    Retrieves song data for a given playlist.

    Args:
        playlist_uri (str): The URI of the playlist.

    Returns:
        List[SongData]: A list of SongData objects containing information about the songs.

    """

    if sp == None:
        raise ValueError("Must create a Spotify Client")
    
    ################
    song_data = []
    # READ DATA
    _cnt = 1
    for track in sp.playlist_tracks(playlist_uri)["items"]:
        data_item = SongData()

        data_item.position = _cnt

        # URI
        data_item.uri = track["track"]["uri"]

        # Track name
        data_item.name = track["track"]["name"]
        print("Track:", data_item.name)

        # Main Artist
        data_item.artist_uri = track["track"]["artists"][0]["uri"]
        data_item.artist_info = sp.artist(data_item.artist_uri)

        # Name, popularity, genre
        data_item.artist_name = track["track"]["artists"][0]["name"]
        data_item.artist_pop = data_item.artist_info["popularity"]
        data_item.artist_genres = data_item.artist_info["genres"]

        # Album
        data_item.album = track["track"]["album"]["name"]

        # Popularity of the track
        data_item.track_pop = track["track"]["popularity"]

        # try:
        #     features = sp.audio_features(data_item.uri)[0]
        #     # Half tempo if over 135BPM
        #     if features["tempo"] > 135.0:
        #         features["tempo"] = features["tempo"] / 2

        #     data_item.features = SongFeatures(**features)

        #     data_item.duration = divmod(data_item.features.duration_ms / 1000, 60)
        # except SpotifyException as ex:
        #     print("Spotify error", ex)

        if reduced:
            song_data.append(data_item.get_reduced())
        else:
            song_data.append(data_item.__dict__)

        _cnt += 1

    return song_data
# ENDREGION

##############################
#   COMMAND LINE INTERFACE   #
##############################
# REGION

if __name__ == "__main__":

    import argparse
    from dotenv import load_dotenv
    from os import environ as env, mkdir
    from os.path import exists
    from json import dump
    from traceback import format_exc

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="playlist",
        help="Scan mode (playlist, artist)",
    )
    parser.add_argument(
        "-i", "--id", type=str, required=True, help="Playlist URI from Spotify"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Name for the output file",
        default="output.json",
    )
    parser.add_argument("--reduced", help="Reduced output", action="store_true")

    try:
        args = parser.parse_args()

        cid = env.get("CLIENT_ID")
        secret = env.get("SECRET_KEY")
        sp = get_client(cid, secret)

        match args.mode:
            case "playlist":
                print(f"Scanning playlist {args.id}...")
                res = scan_playlist(sp, args.id, args.reduced)

            case "artist":
                print(f"Scanning artist {args.id}...")
                res = scan_artist(sp, args.id)

        if not exists("results"):
            mkdir("results")
        if not exists(f"results/{args.mode}"):
            mkdir(f"results/{args.mode}")
        dump(res, open(f"results/{args.mode}/{args.output}.json", "w"), indent=4)

        print("Done")
    except Exception as ex:
        print("Error: " + str(ex))
        print(format_exc())

# ENDREGION