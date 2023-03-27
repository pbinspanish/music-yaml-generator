import os
import yaml
import mutagen

def read_tag(file_path, tag):
    # Read the metadata for the music file
    audio = mutagen.File(file_path)
    
    # Return the tag if it exists, otherwise return an empty string
    return " ".join(audio.tags[tag]) if tag in audio.tags else ""

def generate_yaml(files, root_dir, save_dir, track_identifier, matching_tags, modification_tags):
    # Config
    file_types = matching_tags.keys() # assuming all file types show up in both tag configs.
    
    # Initialize a dictionary for storing the metadata
    metadata = {}

    # Loop through every music file in the root directory and its subdirectories
    for file in files:
        # Check if the file is a music file
        if file.endswith(".mp3") or file.endswith(".flac") or file.endswith(".ogg"):
            # Read Vorbis Comments
            if file.endswith(".flac") or file.endswith(".ogg"):
                display_artist = read_tag(file, "DISPLAY ARTIST")
                album_artist = read_tag(file, "ALBUMARTIST")
                album_title = read_tag(file, "ALBUM")
                track_title = read_tag(file, "TITLE")
                itunes_advisory = read_tag(file, "ITUNESADVISORY")
                track_number = read_tag(file, "TRACKNUMBER")
            # ID3v2 tags
            if file.endswith(".mp3"):
                display_artist = read_tag(file, "TXXX:DISPLAY ARTIST")
                album_artist = read_tag(file, "TPE2")
                album_title = read_tag(file, "TALB")
                track_title = read_tag(file, "TIT2")
                itunes_advisory = read_tag(file, "TXXX:ITUNESADVISORY")
                track_number = read_tag(file, "TRCK")

            # Add explicit indicator to track
            mod_track_title = ""
            if itunes_advisory == "1":
                mod_track_title = track_title + " " + u"\U0001F174"

            # Add the display artist to the metadata dictionary
            if album_artist not in metadata:
                metadata[album_artist] = {}                         # adds an empty dictionary at the album artist
                metadata[album_artist]["albums"] = {}               # adds the albums key and creates an empty dictionary there
                
            if album_title not in metadata[album_artist]["albums"]:
                metadata[album_artist]["albums"][album_title] = {}
                metadata[album_artist]["albums"][album_title]["tracks"] = {}
            
            if track_identifier == "track_number":
                if track_number not in metadata[album_artist]["albums"][album_title]["tracks"]:
                    metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])] = {}
                metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])]["original_artist"] = display_artist
                metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])]["title"] = mod_track_title
            
            elif track_identifier == "track_title":
                if track_number not in metadata[album_artist]["albums"][album_title]["tracks"]:
                    metadata[album_artist]["albums"][album_title]["tracks"][track_title] = {}
                metadata[album_artist]["albums"][album_title]["tracks"][track_title]["original_artist"] = display_artist
                metadata[album_artist]["albums"][album_title]["tracks"][track_title]["title"] = mod_track_title

            
            print(track_number + " " + track_title + " - " + display_artist)


    # Wrap the metadata dictionary in another dictionary
    metadata_dict = {"metadata": metadata}

    # Save the metadata to a YAML file\
    yaml.dump(metadata_dict, open(save_dir + "\Music.yml", "w", encoding="utf8"), default_flow_style=False, allow_unicode=True)