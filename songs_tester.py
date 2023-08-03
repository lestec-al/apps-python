import os, sys
from pygame import mixer

def songs_tester(path: str):
    """Testing MP3 songs and moving damaged to new folder. There may be errors
    Path: folder with songs"""
    # Path fix for different OS
    if sys.platform == "win32":
        if "/" in path:
            path = path.replace("/", "\\")
    else:
        if "\\" in path:
            path = path.replace("\\", "/")
    # Check path
    try:
        all_files = os.listdir(path)
        # Scan MP3 songs
        songs = []
        for f in all_files:
            if ".mp3" in f:
                songs.append(f)
        # Testing songs
        if len(songs) > 0:
            damage_songs = []
            correct_songs = 0
            mixer.init()
            for song in songs:
                try:
                    mixer.music.load(path + song)
                    mixer.music.play()
                    mixer.music.stop()
                    mixer.music.unload()
                    correct_songs += 1
                except:
                    mixer.music.unload()
                    damage_songs.append(song)
            mixer.quit()
            # Move damage songs to folder
            if len(damage_songs) > 0:
                try:
                    os.mkdir(path + "Damaged.Songs")
                except:pass
                for d_song in damage_songs:
                    path_damage_song = os.path.join(path, d_song)
                    os.rename(path_damage_song, f"{path}Damaged.Songs/{d_song}")
            print(f"\nCorrect songs: {correct_songs}. Damaged songs: {len(damage_songs)}\n")
        else:
            print("\nFolder has no songs\n")
    except:
        print("\nIncorrect path\n")

if __name__ == "__main__":
    # songs_tester("path/to/folder/with/sounds/")
    songs_tester("c:/Music/")