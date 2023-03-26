import os
import yaml
import mutagen

def read_tag(file_path, tag):
    # Read the metadata for the music file
    audio = mutagen.File(file_path)
    
    # Return the "DISPLAY ARTIST" vorbis comment if it exists,
    # otherwise return an empty string
    return " ".join(audio.tags[tag]) if tag in audio.tags else ""


def extract_metadata_from_file_path(file_path):
    # Extract the file name and directory name from the file path
    file_name = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)

    # Extract the album artist and album title from the directory name
    album_artist = dir_name.split("\\")[-2]
    album_title = dir_name.split("\\")[-1]

    # Extract the track number from the file name
    track_number = int(file_name.split(" ")[0].split("-")[1])

    return album_artist, album_title, track_number


# Set the root directory for the music files
root_dir = "F:\Music"

# Initialize a dictionary for storing the metadata
metadata = {}

# Loop through every music file in the root directory and its subdirectories
for root, dirs, files in os.walk(root_dir):
    for file in files:
        # Check if the file is a music file
        if file.endswith(".mp3") or file.endswith(".flac") or file.endswith(".ogg"):
            # Read Vorbis Comments
            if file.endswith(".flac") or file.endswith(".ogg"):
                display_artist = read_tag(os.path.join(root, file), "DISPLAY ARTIST")
                album_artist = read_tag(os.path.join(root, file), "ALBUMARTIST")
                album_title = read_tag(os.path.join(root, file), "ALBUM")
                track_title = read_tag(os.path.join(root, file), "TITLE")
                itunes_advisory = read_tag(os.path.join(root, file), "ITUNESADVISORY")
                track_number = read_tag(os.path.join(root, file), "TRACKNUMBER")
            # ID3v2 tags
            if file.endswith(".mp3"):
                display_artist = read_tag(os.path.join(root, file), "TXXX:DISPLAY ARTIST")
                album_artist = read_tag(os.path.join(root, file), "TPE2")
                album_title = read_tag(os.path.join(root, file), "TALB")
                track_title = read_tag(os.path.join(root, file), "TIT2")
                itunes_advisory = read_tag(os.path.join(root, file), "TXXX:ITUNESADVISORY")
                track_number = read_tag(os.path.join(root, file), "TRCK")
                
            # Extract the album artist, album title, and track number from the file path
            # album_artist, album_title, track_number = extract_metadata_from_file_path(os.path.join(root, file))
            
            # skip adding to the yaml file if the display artist doesn't exist or is the same as the album artist
            
                    
            # Add explicit indicator to track
            if itunes_advisory == "1":
                track_title = track_title + " " + u"\U0001F174"

            # Add the display artist to the metadata dictionary
            if album_artist not in metadata:
                metadata[album_artist] = {}                         # adds an empty dictionary at the album artist
                metadata[album_artist]["albums"] = {}               # adds the albums key and creates an empty dictionary there
                
            if album_title not in metadata[album_artist]["albums"]:
                metadata[album_artist]["albums"][album_title] = {}
                metadata[album_artist]["albums"][album_title]["tracks"] = {}
                
            if track_number not in metadata[album_artist]["albums"][album_title]["tracks"]:
                metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])] = {}
                
            metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])]["original_artist"] = display_artist
            metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])]["title"] = track_title
            print(track_number + " " + track_title + " - " + display_artist)


# Wrap the metadata dictionary in another dictionary
metadata_dict = {"metadata": metadata}

# Save the metadata to a YAML file
with open("F:\Music\Music.yml", "w", encoding="utf8") as outfile:
    yaml.dump(metadata_dict, outfile, default_flow_style=False, allow_unicode=True)