import os, shutil


def scan(path):
    global all_files

    for i in os.scandir(path):
        if not i.is_dir():
            all_files += 1

            name = i.name.split(".", 1)[1].strip().lower()
            if name == "mp3" or name == "com).mp3" or name == "biz).mp3" or name == "fm).mp3":
                name = i.name.replace("_", " ")

            if name in files_list:
                files_copy.append(str(i.stat().st_size)+" "+name)
                # shutil.move(i.path, "c:/Users/alex-win/Music/Copies")

            else:
                files_list.append(name)

all_files = 0
files_copy = []
files_list = []
scan("c:/Users/alex-win/Music")


print("All: ", all_files)
print("Normal: ", len(files_list))
print("Copy: ", len(files_copy))
print()


print("Copies:")
files_copy.sort()
for i in files_copy:
    print(i)