import os
import yaml
import modules.generator

def main():
  # Load Config
  config = yaml.safe_load(open("config.yml", "rb"))
  settings = config.get("settings")
  
  # Generate YAML
  modules.generator.generate_yaml(settings.get("root_directory"), settings.get("save_directory"))

if __name__ == "__main__":
  main()