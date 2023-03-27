import os
import yaml
import mutagen

def read_tag(file_path, tag):
    # Read the metadata for the music file
    audio = mutagen.File(file_path)
    
    # Return the tag if it exists, otherwise return an empty string
    return " ".join(audio.tags[tag]) if tag in audio.tags else ""

def generate_yaml(files, save_dir, track_identifier, read_tags, matching_tags, modification_tags):
    metadata = {}

    for file in files:
        current_file_type = os.path.splitext(file)[1]
        # Create a dictionary of tags
        tags = {}
        for file_type in read_tags:
            if current_file_type == file_type:
                for tag in read_tags[file_type]:
                    tags[tag] = read_tag(file, tag)
        
        # Grab the tag value using the key from matching_tags
        album_artist = tags[matching_tags[current_file_type]["album_artist"]]
        album_title = tags[matching_tags[current_file_type]["album_title"]]
        track_title = tags[matching_tags[current_file_type]["track_title"]]
        track_number = tags[matching_tags[current_file_type]["track_number"]]
        
        # Grab the modified values using the key from modification_tags
        title = tags[modification_tags[current_file_type]["title"]]
        original_artist = tags[modification_tags[current_file_type]["original_artist"]]
        
        # Add explicit indicator to track
        # mod_track_title = ""
        # if itunes_advisory == "1":
        #     mod_track_title = track_title + " " + u"\U0001F174"

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
            metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])]["original_artist"] = original_artist
            metadata[album_artist]["albums"][album_title]["tracks"][int(track_number.split("/")[0])]["title"] = title
        
        elif track_identifier == "track_title":
            if track_number not in metadata[album_artist]["albums"][album_title]["tracks"]:
                metadata[album_artist]["albums"][album_title]["tracks"][track_title] = {}
            metadata[album_artist]["albums"][album_title]["tracks"][track_title]["original_artist"] = original_artist
            metadata[album_artist]["albums"][album_title]["tracks"][track_title]["title"] = title
        
        print(tags)

    # Wrap the metadata dictionary in another dictionary
    metadata_dict = {"metadata": metadata}

    # Save the metadata to a YAML file\
    yaml.dump(metadata_dict, open(save_dir + "\Music.yml", "w", encoding="utf8"), default_flow_style=False, allow_unicode=True)