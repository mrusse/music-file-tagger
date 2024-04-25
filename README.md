# music-file-tagger
Python script to batch tag, convert, and organize music files in my preferred style.

![](https://i.imgur.com/IwVMWsp.gif)

# Setup

Install the requirments
```
python -m pip install -r requirements.txt
```

When running the script supply the directory of your files with `-d`

Example:
```
python music-tagger.py -d 'C:\music'
```

# Features

I know music tagging can be very personal and this script may not fit your needs... but you might find it interesting!

The script takes in a directory that is holding subdirectories of freshly downloaded flacs (my preferred format and currently the only supported starting format). 

It will then:
- Adjust the files tags to my preference. It pads the track number: "1" -> "01" and removes the discnumber.
- Convert a copy to mp3 (320kbps)
- Downloads and embeds the album art for each track.

Non-music files will also be deleted such as: cue files, log files, non embedded album art, etc. 

Note: for mp3s I currently do not add the track number to the filename. This is because I mostly use mp3s on an iPod which adds the track number in it's UI when listing tracks.

If the `-a` tag is provided you are able to manually supply album art when downloading art automatically fails. When this happens the progress bar description will change to say "COVER IMAGE NOT FOUND: artist - album" and the script will wait. You can then copy a any `.jpg` file to the folder you supplied with `-d`. This file will be resized and embedded to the tracks on the album that failed the automatic download.
# File Structure

Files should begin in one level deep folders of albums. Ex: `C:\music\album1 , C:\music\album2, etc.`

After the script is run files are arranged in my prefered structure. Here is a directory listing from the gif example above. It is basically just `filetype -> artist -> album -> tracks`.

```
+---Music (320)
|   +---Alvvays
|   |   \---Alvvays
|   |           Adult Diversion.mp3
|   |
|   +---Caroline Polachek
|   |   \---Pang
|   |           Pang.mp3
|   |           The Gate.mp3
|   |
|   \---The Microphones
|       \---The Glow Pt. 2
|               I Want Wind to Blow.mp3
|               the Glow pt. 2.mp3
|               the Moon.mp3
|
\---Music (FLAC)
    +---Alvvays
    |   \---Alvvays
    |           01 Adult Diversion.flac
    |
    +---Caroline Polachek
    |   \---Pang
    |           01 The Gate.flac
    |           02 Pang.flac
    |
    \---The Microphones
        \---The Glow Pt. 2
                01 I Want Wind to Blow.flac
                02 the Glow pt. 2.flac
                03 the Moon.flac
```
