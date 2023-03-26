cd "X:\Programming\Music Tags YAML Generator"
X:\Programs\Python\Python311\python.exe yaml_generator.py
Copy-Item "F:\Music\Music.yml" -Destination "X:\Programs\Plex Meta Manager\1.18.3\Plex-Meta-Manager\config"
cd "X:\Programs\Plex Meta Manager\1.18.3\Plex-Meta-Manager"
X:\Programs\Python\Python310\python.exe plex_meta_manager.py --run-metadata-files "Music"