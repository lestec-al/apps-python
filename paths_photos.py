import os, shutil


def scan(path):
    global all_files

    for i in os.scandir(path):
        if i.is_dir():
            scan(i.path.replace("\\", "/"))

        else:
            all_files += 1

            if i.name in files_list:
                if i.name not in files_copy:
                    files_copy.append(i.name)
                    # shutil.move(i.path, "c:/Users/alex-win/Downloads/pix_copy")
                else:
                    files_copy_copy.append(i.name)

            else:
                files_list.append(i.name)

all_files = 0
files_copy_copy = []
files_copy = []
files_list = []
scan("c:/Users/alex-win/Pictures/Photos")

print(all_files, len(files_list), len(files_copy), len(files_copy_copy))