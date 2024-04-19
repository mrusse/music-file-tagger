import music_tag
import argparse
import os

parser = argparse.ArgumentParser(description='music-tagger')
parser.add_argument('-d',type=str, required=True)
args = parser.parse_args()

songs = []

for path, subdirs, files in os.walk(args.d):
    for name in files:
        try:
            file = music_tag.load_file(os.path.join(path, name))
            songs.append(file)
        except:
            print("An exception occurred with file: " + os.path.join(path, name)) 

for song in songs:
    title_item = song['title']
    print(str(title_item))