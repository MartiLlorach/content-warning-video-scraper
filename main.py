import os
from moviepy.editor import *
from win32com.shell import shell, shellcon

desk_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, None, 0)
rec_path = os.path.join(os.path.expanduser('~'), "AppData", "Local", "Temp", "rec")

clips_folders = [
   f for f in os.listdir(rec_path) if os.path.isdir( os.path.join(rec_path, f) ) 
]

for clips_folder in clips_folders:
    files = [
        f for f in os.listdir( os.path.join(rec_path, clips_folder) ) if os.path.isfile( os.path.join(rec_path, clips_folder, f) )
    ]
    if (len(files)): 
        print("clips already merged, skiping...")
        continue
    
    print("merging clips... ")

    merged_clips = None
    sub_clips_folders = [
        f for f in os.listdir( os.path.join(rec_path, clips_folder) ) if os.path.isdir( os.path.join(rec_path, clips_folder, f) ) 
    ]
    sub_clips_folders.sort(key=lambda sub_clips_folder: os.path.getmtime( os.path.join(rec_path, clips_folder, sub_clips_folder) ))

    for sub_clips_folder in sub_clips_folders:
        clip = VideoFileClip( os.path.join(rec_path, clips_folder, sub_clips_folder, "output.webm") )
        if not merged_clips:
            merged_clips = clip
        else:
            merged_clips = concatenate_videoclips([merged_clips, clip])
    
    merged_clips.write_videofile( os.path.join(rec_path, clips_folder, "merged.webm") )
    merged_clips.write_videofile( os.path.join(desk_path, "merged.webm") )
    print(f"clips merged, written at {os.path.join(rec_path, clips_folder, 'merged.webm')}")


print("done")


