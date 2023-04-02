# Music YAML Generator
Scripts for generating a YAML file from music files (.FLAC, .mp3) for use with [Plex Meta Manager](https://github.com/meisnate12/Plex-Meta-Manager).

## Installation
1. Clone this repository:
`git clone https://github.com/pbinspanish/music-yaml-generator`
2. Install [mutagen](https://github.com/quodlibet/mutagen).

To run the script, use `python main.py`. Note that while this will likely work with on other platforms and versions, it has only been tested with Python 3.11 and on Windows 11.

## Config File
### Fields
#### settings
- `root_directory`: root directory for scan
- `save_directory`: location to save the final YAML file
- `track_identifier`: how to identify the track on the album. Can be `track_number` or `track_title`. Note that if tracks share a track number (e.g. track 1 on disc 1 and track 1 on disc 2), the second will overwrite the first. This also applies for tracks on the same album with the same name.
- `scan_mode`: how to scan the given root directory. `all` will scan every file in the directory. `modified` will scan only the files modified in the given number of days in `modified_time_days`.
- `modified_time_days`: when `scan_mode` is set to `modified`, it will scan the last X days of changes, X being the value in `modified_time_days`
- `explicit_character`: the string to be appended to the title when `append_explicit` is set in `matching_tags`
#### read_tags
The first level in `read_tags` is the file extensions, with the dot, that will be scanned e.g. ".flac". Each file extension takes a list of tags to be read. See the [mutagen documentation](https://mutagen.readthedocs.io/en/latest/) for more information about which tags and file types are supported.

#### matching_tags
These tags are used for matching. Like `read_tags`, the first level is the file extensions. each file extension contains a list of fields used for matching music files to tracks in plex. The values of each of these fields must match a read tag in `read_tags`.
- `album_artist`: The artist in Plex.
- `album_title`: The title of the album in Plex.
- `track_title`: The title of the track in Plex. Note that this is only used if `track_identifier` is set to `track_title`.
- `track_number`: The track number of the track in Plex. Note that this is only used if `track_identifier` is set to `track_number`. In addition, the default track number tag in id3 files store the track number along with the total track count in the form `1/13`. To pull just the track number, the script by default splits the `track_number` tag at a `/`, regardless of the set tag or file extension.
- `append_explicit`: This is the tag to read to determine whether to append the string in `explicit_character`. Note that this assumes the tag is set to 1 when explicit. Intended for use with the ITUNESADVISORY tag.

#### modification_tags
These tags are used for modifying fields in Plex, as per the [Plex Meta Manager documentation](https://metamanager.wiki/en/latest/metadata/metadata/music.html#general-attributes). Currently, only `title` and `original_artist` are supported. The values of each of these fields must match a read tag in `read_tags`.
- `title`: Changes the title of a track in Plex. If `append_explicit` is used, then the `explicit_character` string will be appended to this tag.
- `original_artist`: Changes the original_artist field in Plex. Note that this is not the album artist, used for grouping and matching, but rather a per track field.

### Example Config File
```yaml
settings:
  root_directory: F:\Music
  save_directory: X:\Programs\plex-meta-manager\config
  track_identifier: track_number
  scan_mode: modified
  modified_time_days: 1
  explicit_character: 🅴

read_tags:
  .flac:
    - ALBUMARTIST
    - ALBUM
    - TITLE
    - TRACKNUMBER
    - DISPLAY ARTIST
    - ITUNESADVISORY
  .mp3:
    - TPE2
    - TALB
    - TIT2
    - TRCK
    - TXXX:DISPLAY ARTIST
    - TXXX:ITUNESADVISORY

matching_tags:
  .flac:
    album_artist: ALBUMARTIST
    album_title: ALBUM
    track_title: TITLE
    track_number: TRACKNUMBER
    append_explicit: ITUNESADVISORY
  .mp3:
    album_artist: TPE2
    album_title: TALB
    track_title: TIT2
    track_number: TRCK
    append_explicit: TXXX:ITUNESADVISORY

modification_tags:
  .flac:
    title: TITLE
    original_artist: DISPLAY ARTIST
  .mp3:
    title: TIT2
    original_artist: TXXX:DISPLAY ARTIST
```