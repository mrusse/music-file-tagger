import music_tag
import argparse
import os

def pad_track_num(num):
  if(len(str(num)) < 2):
      return "0" + str(num)
  else:
      return str(num)
  
def song_to_string(song):
    tracknumber  = song.raw['tracknumber'].value
    artist       = song['artist']
    album        = song['album']
    title        = song['title']
    discnumber   = song['discnumber']
    return(str(artist) + " - " + str(album) + " - " + str(tracknumber) + " " + str(title) + " - " + str(discnumber))
      
parser = argparse.ArgumentParser(description='music-tagger')
parser.add_argument('-d',type=str, required=True)
args = parser.parse_args()

songs = []
artists = {}
albums = {}

illegalChars = ["\\","/",":","*","?",'"',"<",">","|"]

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
            song.raw['tracknumber'] = pad_track_num(song['tracknumber'])
            song.remove_tag('discnumber')
            print(song_to_string(song))
            song.save()

for path, subdirs, files in os.walk(args.d):
    for name in files:
        try:
            file = music_tag.load_file(os.path.join(path, name))
            tracknumber  = file.raw['tracknumber'].value
            title        = file['title']
            filename = str(tracknumber) + " " + str(title) + ".flac"

            for c in illegalChars:
                if c in filename:
                    filename = filename.replace(c,"")

            os.rename(os.path.join(path, name), os.path.join(path, filename))
        except Exception as e:
            print(e)
            #print("Skipping processing of non-music file: " + os.path.join(path, name)) 