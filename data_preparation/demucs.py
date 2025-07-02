import os
import subprocess

# Set your input folder path
input_folder = r"/home/selim/Documents/test_musicgen"  # <-- Change this to your folder path

# Set of valid audio file extensions
valid_audio_extensions = {'.mp3', '.wav', '.flac', '.ogg', '.m4a'}

# List all files in the input folder
for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)

    # Check if it's a valid audio file
    if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in valid_audio_extensions:
        print(f"Processing: {filename}")

        # Run Demucs on the file
        subprocess.run(["demucs", "--device", "cuda", "--two-stems", "vocals", filepath])

    else:
        print(f"Skipping non-audio file: {filename}")

print("✅ Separation complete for all audio files.")
