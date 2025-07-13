import os
import shutil
import subprocess

# Path to the main folder containing song folders
main_folder = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/data_preparation/separated/htdemucs"

# Optional: output folder for separated stems
output_folder = "/home/selim/Documents/test_musicgen/split"
# Temporary base output where Demucs writes
temp_folder = os.path.join(output_folder, "temp_demucs_outputs")

# Name of the model folder (usually 'htdemucs')
model_name = "htdemucs"

# Make sure output folders exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(temp_folder, exist_ok=True)

# Loop through each song folder
for song_folder in sorted(os.listdir(main_folder)):
    song_path = os.path.join(main_folder, song_folder)
    if os.path.isdir(song_path):
        no_vocals_path = os.path.join(song_path, "no_vocals.wav")
        if os.path.isfile(no_vocals_path):
            print(f"Processing {no_vocals_path}...")

            # Run demucs
            subprocess.run([
                "demucs",
                "--out", temp_folder,
                no_vocals_path
            ])

            # Locate the demucs output for this song
            base_name = os.path.splitext(os.path.basename(no_vocals_path))[0]
            demucs_output = os.path.join(temp_folder, model_name, base_name)

            # Move only drums.wav, bass.wav, and other.wav back into the original song folder
            for stem in ["drums.wav", "bass.wav", "other.wav"]:
                source_file = os.path.join(demucs_output, stem)
                target_file = os.path.join(song_path, stem)
                if os.path.exists(source_file):
                    shutil.move(source_file, target_file)
                    print(f"Moved {stem} to {song_path}")
                else:
                    print(f"Warning: {stem} not found for {song_folder}")

            # Optionally: Clean up the separated output for this song
            shutil.rmtree(os.path.join(temp_folder, model_name))

    # Final cleanup: remove the temporary folder
shutil.rmtree(temp_folder)