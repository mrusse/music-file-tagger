# music-file-tagger
Python script to batch tag, convert, and organize music files in my preferred style.

![](https://i.imgur.com/JfPdtGg.gif)

I know music tagging can be very personal and this script may not fit your needs... but you might find it interesting!

The script takes in a directory that is holding subdirectories of freshly downloaded flacs (my preferred format and currently the only supported starting format). It will then tag, convert a copy to mp3 (320kbps), and download album art.

The files are then arranged in my prefered structure. Here is a directory listing from the gif example above. It is basically just filetype -> artist -> album.

```
+---Music (320)
|   +---Alvvays
|   |   \---Alvvays
|   +---Caroline Polachek
|   |   \---Pang
|   \---The Microphones
|       \---The Glow Pt. 2
\---Music (FLAC)
    +---Alvvays
    |   \---Alvvays
    +---Caroline Polachek
    |   \---Pang
    \---The Microphones
        \---The Glow Pt. 2
```
