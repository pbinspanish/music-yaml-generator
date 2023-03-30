import yaml

def write_yaml(metadata_dict, save_dir):
  yaml.dump(metadata_dict, open(save_dir + "\Music.yml", "w", encoding="utf8"), default_flow_style=False, allow_unicode=True)