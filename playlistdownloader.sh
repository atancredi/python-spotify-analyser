python -m zotify https://open.spotify.com/playlist/$1 --download-real-time=true --root-path $2 --song-archive=$2/archive.txt --print-downloads=True --skip-previously-downloaded=True --download-quality=high --download-format=mp3 --output='{playlist}/{artist} - {song_name}.{ext}'