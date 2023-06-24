import os
import datetime

def scan_files(root_dir, scan_mode, modified_time_days, matching_tags):
    music_files = []
    file_types = matching_tags.keys()
    if scan_mode == "all":
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                for file_type in file_types:
                    if file.endswith(file_type):
                        music_files.append(os.path.join(root, file))

    elif scan_mode == "modified":
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                for file_type in file_types:
                    if file.endswith(file_type):
                        full_path = os.path.join(root, file)
                        modified_time = os.path.getmtime(full_path)
                        if modified_time:
                            modified_time = datetime.datetime.fromtimestamp(modified_time)
                            if (datetime.datetime.now() - modified_time).days < modified_time_days:
                                music_files.append(full_path)
                    
    return music_files