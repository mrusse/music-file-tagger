import os
import sys
import time
import shutil
from io import StringIO

import argparse
import music_tag
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import mediainfo
from get_cover_art import CoverFinder

#Track number padder (turns "1" to "01") 
def pad_track_num(num):
  if(len(num) < 2):
      return "0" + num
  else:
      return num
  
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

dirsToRemove = []
illegalChars = ["\\","/",":","*","?",'"',"<",">","|"]
finder = CoverFinder({'art-size': 600, 'cleanup': True, 'clear': True, 'verbose': False})
s = StringIO()

print("\n♪♪♪♪♪♪♪♪♪♪ Music tagger and organizer! ♪♪♪♪♪♪♪♪♪♪\n\n")

for path, subdirs, files in os.walk(args.d):
    #Erase empty progress bar print
    if(songs == []):
        print ("\033[A                             \033[A")

    songList = tqdm(files, bar_format='{desc}{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')
    for name in songList:
        try:
            #Get song from file
            song = music_tag.load_file(os.path.join(path, name))
            title        = song['title']
            artist       = str(song['artist'])
            album        = str(song['album'])

            #Progress bar
            songList.set_description("Applying metadata for: " + artist + " - " + album + " - " + str(title))

            #Basic editing of metadata (pad tracknumber and remove discnumber)
            raw_tracknum = song.raw['tracknumber'].value.split("\\")[0].split("/")[0]
            song.raw['tracknumber'] = pad_track_num(raw_tracknum)
            song.remove_tag('discnumber')
            songs.append(song)
            song.save()

            #Edit song filenames to %tracknumber% %title% structure
            tracknumber  = song.raw['tracknumber'].value
            filename = str(tracknumber) + " " + str(title) + ".flac"
            flac_location = args.d + "\\" + "Music (FLAC)"
            mp3_location = args.d + "\\" + "Music (320)"
        
            #Check filename for illegal chars that can sneak in from track title
            for c in illegalChars:
                if c in filename:
                    filename = filename.replace(c,"")
                if c in artist:
                    artist = artist.replace(c,"")                    
                if c in album:
                    album = album.replace(c,"")

            #Make "Artist\Album" folders if they don't exist
            if not os.path.isdir(os.path.join(flac_location, artist, album)):
                os.makedirs(os.path.join(flac_location, artist, album))
                os.makedirs(os.path.join(mp3_location, artist, album))
                
            if(path not in dirsToRemove):
                dirsToRemove.append(path)

            #Progress bar
            songList.set_description("Converting flac > mp3: " + artist + " - " + album + " - " + str(title))

            #Convert flacs to mp3's then rename and move processed files
            flac_path = os.path.join(path, name)
            flac_audio = AudioSegment.from_file(flac_path, "flac")

            mp3_filename = filename.replace(".flac",".mp3").split(" ",1)[1]
            mp3_tags = mediainfo(flac_path).get('TAG', {})
            mp3_extension = ".mp3"

            if(os.path.isfile(os.path.join(mp3_location, artist, album, mp3_filename))):
                mp3_filename = mp3_filename.replace(".mp3","(1).mp3")
                mp3_extension = "(1).mp3"

            mp3_old = name.replace(".flac",mp3_extension)
            flac_audio.export(os.path.join(path, mp3_old), format="mp3", tags=mp3_tags, bitrate="320k")

            os.rename(flac_path, os.path.join(flac_location, artist, album, filename))
            os.rename(os.path.join(path, mp3_old), os.path.join(mp3_location, artist, album, mp3_filename))

            #Remove discnumber if it failed to do so before (sometimes gets added back to the mp3 somehow)
            new_mp3 = music_tag.load_file(os.path.join(mp3_location, artist, album, mp3_filename))
            if(str(new_mp3['discnumber']) != ""):
                new_mp3.remove_tag('discnumber')
                new_mp3.save()

            #Progress bar
            songList.set_description("Embedding cover image: " + artist + " - " + album + " - " + str(title))

            #Grab artwork      
            sys.stdout = s
            finder.scan_file(os.path.join(flac_location, artist, album, filename))
            finder.scan_file(os.path.join(mp3_location, artist, album, mp3_filename))
            sys.stdout = sys.__stdout__

        except NotImplementedError:
            #Progress bar
            songList.set_description("Skipped non-flac file: " + name)
            pass
        except Exception as e:
            print(e)
            sys.exit(0)

        if(name == files[-1]):
            #Progress bar    
            songList.set_description("Finished processing!!: " + artist + " - " + album)

#Remove old dirs
for path in dirsToRemove:
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(e)

#Print out files that we missed grabbing artwork for
if finder.files_skipped != []:
    print("\nSkipped grabbing artwork for these files: ")
for file in finder.files_skipped:
    split = file.split("\\")
    title = split[-1]
    album = split[-2]
    artist = split[-3]
    print(artist + " - " + album + " - " + title)

print("\n♪♪♪♪♪♪♪♪♪♪ Finished in: %s seconds! ♪♪♪♪♪♪♪♪♪♪" % '{0:.2f}'.format(time.time() - start_time))