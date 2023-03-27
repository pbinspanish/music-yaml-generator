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
  
  # Generate YAML
  modules.generator.generate_yaml(settings.get("root_directory"), settings.get("save_directory"), settings.get("track_identifier"), matching_tags, modification_tags)
  
  # Test
  # gets only files edited in the last day
  for root, dirs, files in os.walk(settings.get("root_directory")):
    for file in files:
        full_path = os.path.join(root, file)
        modified_time = os.path.getmtime(full_path)
        if modified_time:
            modified_time = datetime.datetime.fromtimestamp(modified_time)
            if (datetime.datetime.now() - modified_time).days < 1:
                print(full_path)

if __name__ == "__main__":
  main()