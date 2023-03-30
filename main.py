import os
import yaml
import modules.generator
import datetime

def main():
  # Load Config
  config = yaml.safe_load(open("config.yml", "rb"))
  settings = config.get("settings")
  matching_tags = config.get("matching_tags")
  modification_tags = config.get("modification_tags")
  read_tags = config.get("read_tags")
  
  # Generate list of files to edit
  music_files = []
  file_types = matching_tags.keys()
  if settings.get("scan_mode") == "all":
    for root, dirs, files in os.walk(settings.get("root_directory")):
      for file in files:
        for file_type in file_types:
          if file.endswith(file_type):
            music_files.append(os.path.join(root, file))
  
  elif settings.get("scan_mode") == "modified":
    for root, dirs, files in os.walk(settings.get("root_directory")):
      for file in files:
        for file_type in file_types:
          if file.endswith(file_type):
            full_path = os.path.join(root, file)
            modified_time = os.path.getmtime(full_path)
            if modified_time:
                modified_time = datetime.datetime.fromtimestamp(modified_time)
                if (datetime.datetime.now() - modified_time).days < settings.get("modified_time_days"):
                    music_files.append(full_path)
  
  # Generate YAML
  modules.generator.generate_yaml(music_files, settings.get("save_directory"), settings.get("track_identifier"), settings.get("explicit_character"), read_tags, matching_tags, modification_tags)

if __name__ == "__main__":
  main()