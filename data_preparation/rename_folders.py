import os

# Folder where separated instrumentals are
input_folder = r"/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs"

# Get all folders and sort them alphabetically
folders = sorted(os.listdir(input_folder))

# Start song numbering from 201
song_number = 311

# Rename each folder
for folder in folders:
    folder_path = os.path.join(input_folder, folder)

    # Make sure it's a directory
    if os.path.isdir(folder_path):
        new_folder_name = f"{song_number} - {folder}"
        new_folder_path = os.path.join(input_folder, new_folder_name)

        # Rename the folder
        os.rename(folder_path, new_folder_path)
        print(f"Renamed: {folder} ➡️ {new_folder_name}")

        song_number += 1

print("✅ All folders have been renamed successfully!")
