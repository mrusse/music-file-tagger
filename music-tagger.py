import music_tag
import argparse
import os

def pad_track_num(num):
  if(len(str(num)) < 2):
      return "0" + str(num)
  else:
      return str(num)
      
parser = argparse.ArgumentParser(description='music-tagger')
parser.add_argument('-d',type=str, required=True)
args = parser.parse_args()

songs = []
artists = {}
albums = {}

for path, subdirs, files in os.walk(args.d):
    for name in files:
        try:
            file = music_tag.load_file(os.path.join(path, name))
            songs.append(file)
        except:
            print("Skipping processing of non-music file: " + os.path.join(path, name)) 

for song in songs:
    album = song['album']
    if(str(album) not in albums):
        albums[str(album)] = [song]
    else:
        albums[str(album)].append(song)

for key in albums:
    artist = albums[key][0]['artist']
    if(str(artist) not in artists):
        artists[str(artist)] = [albums[key]]
    else:
        artists[str(artist)].append(albums[key])

for artist in artists:
    for album in artists[artist]:
        for song in album:
            song_tracknumber  = song['tracknumber']
            song.raw['tracknumber'] = pad_track_num(song_tracknumber)
            song.save()

            song_tracknumber  = song.raw['tracknumber'].value
            song_artist = song['artist']
            song_album  = song['album']
            song_title  = song['title']
            print(str(song_artist) + " - " + str(song_album) + " - " + str(song_tracknumber) + " "+ str(song_title))

