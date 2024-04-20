from get_cover_art import CoverFinder
from tqdm import tqdm
import music_tag
import argparse
import shutil
import os
import time

#Track number padder (turns "1" to "01") 
def pad_track_num(num):
  if(len(str(num)) < 2):
      return "0" + str(num)
  else:
      return str(num)
  
#Song to string. TODO: add more data to this   
def song_to_string(song):
    tracknumber  = song.raw['tracknumber'].value
    artist       = song['artist']
    album        = song['album']
    title        = song['title']
    discnumber   = song['discnumber']
    return(str(artist) + " - " + str(album) + " - " + str(tracknumber) + " " + str(title) + " - " + str(discnumber))

start_time = time.time()

parser = argparse.ArgumentParser(description='music-tagger')
parser.add_argument('-d',type=str, required=True)
args = parser.parse_args()

songs = []
artists = {}
albums = {}

dirsToRemove = []
illegalChars = ["\\","/",":","*","?",'"',"<",">","|"]

print("\n---------- Metadata organizer! ----------\n\n")

for path, subdirs, files in os.walk(args.d):
    #Erase empty progress bar print
    if(songs == []):
        print ("\033[A                             \033[A")

    songList = tqdm(files, bar_format='{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')
    for name in songList:
        try:
            #Get song from file
            song = music_tag.load_file(os.path.join(path, name))

            #Basic editing of metadata (pad tracknumber and remove discnumber)
            song.raw['tracknumber'] = pad_track_num(song['tracknumber'])
            song.remove_tag('discnumber')
            songs.append(song)
            song.save()

            #Add songs to albums
            album = song['album']
            if(str(album) not in albums):
                albums[str(album)] = [song]
            else:
                albums[str(album)].append(song)

            #Edit song filenames to %tracknumber% %title% structure
            tracknumber  = song.raw['tracknumber'].value
            title        = song['title']
            artist       = str(song['artist'])
            album        = str(song['album'])
            filename = str(tracknumber) + " " + str(title) + ".flac"
            
            songList.set_description("Processing: " + artist + " - " + album + " - " + str(title))

            #Check filename for illegal chars that can sneak in from track title
            for c in illegalChars:
                if c in filename:
                    filename = filename.replace(c,"")
                if c in artist:
                    artist = artist.replace(c,"")                    
                if c in album:
                    album = album.replace(c,"")

            #Make "Artist\Album" folders if they don't exist
            if not os.path.isdir(os.path.join(args.d, artist)):
                os.mkdir(os.path.join(args.d, artist))
                os.mkdir(os.path.join(args.d + "\\" + artist, album))
            elif not os.path.isdir(os.path.join(args.d + "\\" + artist, album)):
                os.mkdir(os.path.join(args.d + "\\" + artist, album))

            if(path not in dirsToRemove):
                dirsToRemove.append(path)

            #Rename and move processed files
            os.rename(os.path.join(path, name), os.path.join(args.d + "\\" + artist + "\\" + album, filename))
        except Exception as e:
            pass
            #print("Skipping processing of non-music file: " + os.path.join(path, name)) 

#Remove old dirs
for path in dirsToRemove:
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(e)

print("\n---------- Now time for artwork! ----------\n")

finder = CoverFinder({'art-size': 600, 'cleanup': True, 'clear': True, 'verbose': False})
finder.scan_folder(args.d)

#Print out files that we missed grabbing artwork for
if finder.files_skipped != []:
    print("\nSkipped grabbing artwork for these files: ")
for file in finder.files_skipped:
    split = file.split("\\")
    title = split[-1]
    album = split[-2]
    artist = split[-3]
    print(artist + " - " + album + " - " + title)

print("\n---------- %s seconds ----------" % (time.time() - start_time))