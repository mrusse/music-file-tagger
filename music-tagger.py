import music_tag

file = music_tag.load_file("02. Shimmering Stars - I'm Gonna Try.flac")
title_item = file['title']

print(str(title_item))