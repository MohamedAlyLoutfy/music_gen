import os
import subprocess

# List of your playlist URLs
playlists = [
    "https://www.youtube.com/watch?v=xFrGuyw1V8s&list=PLlb3q7unEBfOvlOdp3d1Q2uP8gsyE-0qw", #ABBA
    "https://www.youtube.com/watch?v=MI9ZpIKgyf0&list=PLjp0AEEJ0-fGKG_3skl0e1FQlJfnx-TJz", #ED SHEERAN
    ["https://www.youtube.com/watch?v=yKNxeF4KMsY&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=FM7MFYoylVs&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=dvgZkm1xWPE&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=RB-RcX5DS5A&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=VPRjCeoBqrI&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=YykjpeuMNEk&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=1G4isv_Fylg&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=VlSEIa1zubs&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=QtXby3twMmI&pp=ygUIY29sZHBsYXk%3D",
     "https://www.youtube.com/watch?v=HBZs11QKCrE"],#Coldplay
    "https://www.youtube.com/watch?v=1xsDmAYVlrs&list=RDEMg3Zp9rpDqGT6x-HHMnu6cQ&start_radio=1",#Cairokee
    "https://www.youtube.com/watch?v=WKZO-CWeOVA&list=RDEMcce0hP5SVByOVCd8UWUHEA&start_radio=1",#BillieEilish
    "https://www.youtube.com/watch?v=cHHLHGNpCSA&list=RDEM4eZDs_u8lV1UARX7tj9AEw&start_radio=1",#Avicii
    "https://www.youtube.com/watch?v=hLQl3WQQoQ0&list=RDEMTPfPURSbYpb0YHCKyIG37Q&start_radio=1",#Adele
    ["https://www.youtube.com/watch?v=kPa7bsKwL-c&pp=ygUJTGFkeSBHYWdh",
     "https://www.youtube.com/watch?v=vBynw9Isr28&pp=ygUJTGFkeSBHYWdh",
     "https://www.youtube.com/watch?v=bESGLojNYSo&pp=ygUJTGFkeSBHYWdh0gcJCSMF6IfKp2fp",
     "https://www.youtube.com/watch?v=wagn8Wrmzuc&pp=ygUJTGFkeSBHYWdh",
     "https://www.youtube.com/watch?v=qrO4YZeyl0I&pp=ygUJTGFkeSBHYWdh",
     "https://www.youtube.com/watch?v=5vheNbQlsyU&pp=ygUJTGFkeSBHYWdh",
     "https://www.youtube.com/watch?v=Gz-FO0M6CI4&pp=ygUJTGFkeSBHYWdh",
     "https://www.youtube.com/watch?v=niqrrmev4mA&pp=ygUJTGFkeSBHYWdh0gcJCSMF6IfKp2fp",
     "https://www.youtube.com/watch?v=VFwmKL5OL-Q&pp=ygUJTGFkeSBHYWdh",
     "https://www.youtube.com/watch?v=fmC6b6_ovZY&pp=ygUJTGFkeSBHYWdh"],#Lady Gaga
    "https://www.youtube.com/watch?v=fJ9rUzIMcZQ&list=PL2tMgWgIvcWmjs4i6DcXm7YmjPlTXUl9E",#Queen
    "https://www.youtube.com/watch?v=NCtzkaL2t_Y&list=RDEMDwfWqCd9jXCuVO7pjkJHTw&start_radio=1",#Beatles
    "https://www.youtube.com/watch?v=_RHIECWv728&list=RDEMujKTrOS-OKcricH1S64ZTA&start_radio=1"#Wegz

]

# Output folder
output_folder = "/Users/Selim/Documents/UNI_STUTTGART/Semester 4/Deep Learning Lab/Project/data"

# Download first 10 songs from each playlist
os.makedirs(output_folder, exist_ok=True)

# yt-dlp command templates
yt_dlp_playlist_command = (
    "yt-dlp -f bestaudio --extract-audio --audio-format mp3 "
    "--output \"{output}/%(title)s.%(ext)s\" --playlist-items 1-10 {url}"
)

yt_dlp_song_command = (
    "yt-dlp -f bestaudio --extract-audio --audio-format mp3 "
    "--output \"{output}/%(title)s.%(ext)s\" {url}"
)

# Function to run a yt-dlp command
def run_command(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)

# Process each entry
for entry in playlists:
    if isinstance(entry, list):
        for song_url in entry:
            command = yt_dlp_song_command.format(output=output_folder, url=f'"{song_url}"')
            run_command(command)
    else:
        command = yt_dlp_playlist_command.format(output=output_folder, url=f'"{entry}"')
        run_command(command)

print("Download completed!")