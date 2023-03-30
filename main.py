import modules.generator as generator
import modules.scanner as scanner
import yaml

def main():
  # Load Config
  config = yaml.safe_load(open("config.yml", "rb"))
  settings = config.get("settings")
  matching_tags = config.get("matching_tags")
  modification_tags = config.get("modification_tags")
  read_tags = config.get("read_tags")
  
  # Generate list of files to edit
  music_files = scanner.scan_files(settings.get("root_directory"), settings.get("scan_mode"), settings.get("modified_time_days"), matching_tags)
  
  # Generate YAML
  generator.generate_yaml(music_files, settings.get("save_directory"), settings.get("track_identifier"), settings.get("explicit_character"), read_tags, matching_tags, modification_tags)

if __name__ == "__main__":
  main()