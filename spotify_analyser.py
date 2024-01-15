import spotipy
from typing import List
from os.path import exists
import argparse
from json import dump
from traceback import format_exc

from spotipy.oauth2 import SpotifyClientCredentials
from typing import Optional, Any

###################
#   DATA MODELS   #
###################
#REGION
class Serializable:
    def as_dict(self, obj = None):
        """
        Convert an object or the current instance to a dictionary representation.
        
        Args:
            obj (object, optional): The object to be converted to a dictionary. If not provided, the current instance is used.
        
        Returns:
            dict: A dictionary representation of the object or the current instance.
        """
        ret = {}
        if obj != None:
            read = obj.__dict__
        else:
            read = self.__dict__

        for key in read:
            value = read[key]
            if "data." in str(type(value)):
                ret[key] = self.as_dict(obj=value)
            else:
                ret[key] = value
        return ret

class SongFeatures(Serializable):
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

    def from_api_response(self, res: dict):
        """
        Initializes the instance variables of the class with the values from the API response.

        Args:
            res (dict): The API response as a dictionary.

        Returns:
            self: The instance of the class with the updated variables.
        """
        self.danceability = res["danceability"]
        self.energy = res["energy"]
        self.key = res["key"]
        self.loudness = res["loudness"]
        self.mode = res["mode"]
        self.speechiness = res["speechiness"]
        self.acousticness = res["acousticness"]
        self.instrumentalness = res["instrumentalness"]
        self.liveness = res["liveness"]
        self.valence = res["valence"]
        self.tempo = res["tempo"]
        self.type = res["type"]
        self.id = res["id"]
        self.uri = res["uri"]
        self.track_href = res["track_href"]
        self.analysis_url = res["analysis_url"]
        self.duration_ms = res["duration_ms"]
        self.time_signature = res["time_signature"]
        return self

    @property
    def __dict__(self):
        return {
            "danceability": self.danceability,
            "energy": self.energy,
            "key": self.key,
            "loudness": self.loudness,
            "mode": self.mode,
            "speechiness": self.speechiness,
            "acousticness": self.acousticness,
            "instrumentalness": self.instrumentalness,
            "liveness": self.liveness,
            "valence": self.valence,
            "tempo": self.tempo,
            "type": self.type,
            "id": self.id,
            "uri": self.uri,
            "track_href": self.track_href,
            "analysis_url": self.analysis_url,
            "duration_ms": self.duration_ms,
            "time_signature": self.time_signature
        }

class SongData(Serializable):

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
    features: Optional[SongFeatures]
    duration: Optional[float]
    
    def __init__(self):
        super().__init__()
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
        self.features = None
        self.duration = None

    @property
    def __dict__(self):
        return {
            "position": self.position,
            "uri": self.uri,
            "name": self.name,
            "artist_uri": self.artist_uri,
            "artist_info": self.artist_info,
            "artist_name": self.artist_name,
            "artist_pop": self.artist_pop,
            "artist_genres": self.artist_genres,
            "album": self.album,
            "track_pop": self.track_pop,
            "features": self.features,
            "duration": self.duration
        }

class ReducedSongData(Serializable):

    position: int
    name: str
    artist_name: str
    album: str
    tempo: float
    duration: int

    def __init__(self):
        super().__init__()
        self.position = None
        self.name = ""
        self.artist_name = ""
        self.album = ""
        self.tempo = None
    
    def from_song_data(self, song_data: SongData):
        """
        Initializes the object's attributes with the given song data.

        Parameters:
            song_data (SongData): The song data used to initialize the object.

        Returns:
            self: The object itself.
        """
        self.position = song_data.position
        self.name = song_data.name
        self.artist_name = song_data.artist_name
        self.album = song_data.album
        self.tempo = song_data.features["tempo"]
        minutes, seconds = divmod(song_data.features["duration_ms"] / 1000, 60)
        self.duration = f'{minutes:0>2.0f}:{seconds:.3f}'
        return self
#ENDREGION

####################
#   SCAN METHODS   #
####################
#REGION

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

            data_item.features = SongFeatures().from_api_response(sp.audio_features(track["id"])[0])

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

    ################
    song_data = []
    # READ DATA
    _cnt = 1
    for track in sp.playlist_tracks(playlist_uri)["items"]:
        data_item = SongData()

        data_item.position = _cnt
        
        #URI
        data_item.uri = track["track"]["uri"]
    
        #Track name
        data_item.name = track["track"]["name"]
    
        #Main Artist
        data_item.artist_uri = track["track"]["artists"][0]["uri"]
        data_item.artist_info = sp.artist(data_item.artist_uri)
    
        #Name, popularity, genre
        data_item.artist_name = track["track"]["artists"][0]["name"]
        data_item.artist_pop = data_item.artist_info["popularity"]
        data_item.artist_genres = data_item.artist_info["genres"]
    
        #Album
        data_item.album = track["track"]["album"]["name"]
    
        #Popularity of the track
        data_item.track_pop = track["track"]["popularity"]
                
        features = sp.audio_features(data_item.uri)[0]
        # Half tempo if over 135BPM
        if features["tempo"] > 135.0:
            features["tempo"] = features["tempo"] / 2
        
        data_item.features = SongFeatures().from_api_response(features)

        data_item.duration = divmod(data_item.features.duration_ms / 1000, 60)

        if reduced:
            song_data.append(ReducedSongData().from_song_data(data_item))
        else:
            song_data.append(data_item)

        _cnt += 1
        
    return song_data
#ENDREGION

##############################
#   COMMAND LINE INTERFACE   #
##############################
#REGION

if __name__ == "__main__":

    from dotenv import load_dotenv
    from os import environ as env, mkdir
    load_dotenv()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mode", type=str, default="playlist", help="Scan mode (playlist, artist)")
    parser.add_argument("-i","--id", type=str, required=True, help="Playlist URI from Spotify")
    parser.add_argument("-o","--output", type=str, help="Name for the output file", default="output.json")
    parser.add_argument("--reduced", help="Reduced output", action='store_true')
    
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
        dump([i.__dict__ for i in res],open(f"results/{args.mode}/{args.output}", "w"), indent=4)

        print("Done")
    except Exception as ex:
        print("Error: "+str(ex))
        print(format_exc())

#ENDREGION