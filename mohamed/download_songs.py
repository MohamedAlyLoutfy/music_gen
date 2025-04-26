import os
import subprocess

# List of your playlist URLs
playlists = [
    "https://www.youtube.com/watch?v=kXYiU_JCYtU&list=PL9LkJszkF_Z6bJ82689htd2wch-HVbzCO",
    "https://www.youtube.com/watch?v=jKIEUdAMtrQ&list=PLNiDl4mPNqeU0vZFE_psJBq9y1ODra43G",
    "https://www.youtube.com/watch?v=ujahwfbXWuY&list=PLk2Mt72bUGzj6f1JaIhLX8OxiD7NV1Rpn",
    "https://www.youtube.com/watch?v=fS7Hv43EkZw&list=PL0F2B0F4C71A94980",
    "https://www.youtube.com/watch?v=7wtfhZwyrcc&list=PLMp5rDgAZPCi51aybeg5YZwvTPbBDT3a8",
    "https://www.youtube.com/watch?v=y32ejtuxSjM&list=PLAKPPAHY4SIKwNBbAcVa48KVUBbh6PHOA",
    "https://www.youtube.com/watch?v=b4SRE-_h8D0&list=PLcVUVL6GIPXyuOzQnGfcdepw93Fr2Vbcs",
    "https://www.youtube.com/watch?v=3JWTaaS7LdU&list=PL201BB89398FE5675",
    "https://www.youtube.com/watch?v=h3h035Eyz5A&list=PLQy4dlAQLNtwyN6rgck65mzFnk2xEqZSs",
    "https://www.youtube.com/watch?v=qeWNo7n34hY&list=PLoxM5QakbB9IiqQ6WLDhEGHFMLOTKM_Gh"
    # Add more links here
]

# Output folder
output_folder = "D:/music_gen/data_preparation"

# Download first 10 songs from each playlist
for playlist_url in playlists:
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", os.path.join(output_folder, "%(title)s.%(ext)s"),
        "--playlist-items", "1-10",
        playlist_url
    ]
    
    print(f"🚀 Downloading from playlist: {playlist_url}")
    subprocess.run(command)

print("✅ Download completed for all playlists!")
