import argparse
import mutagen

def main():
  parser = argparse.ArgumentParser(description="Read music file tags")
  parser.add_argument("file_path", type=str, help="Path to music file")
  args = parser.parse_args()
  audio = mutagen.File(args.file_path)
  for key in audio.tags:
      print(key)

if __name__ == "__main__":
  main()