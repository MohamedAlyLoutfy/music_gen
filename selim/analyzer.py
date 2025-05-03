import os
import librosa
import pandas as pd

# Folder where separated instrumentals are
input_folder = r"/home/selim/Documents/Uni Stuttgart/DeepLearningLab/MusicGen/selim/separated/htdemucs"

# Prepare data list
data = []

folders = sorted(os.listdir(input_folder))
# Go through each song folder
for folder in folders:
    folder_path = os.path.join(input_folder, folder)
    instrumental_path = os.path.join(folder_path, "no_vocals.wav")

    if os.path.exists(instrumental_path):
        print(f"Analyzing: {folder}")

        # Load audio
        y, sr = librosa.load(instrumental_path)

        # Estimate BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Estimate key
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key_index = chroma.mean(axis=1).argmax()
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key = keys[key_index]

        # Save to data
        data.append({
            "Song": folder,
            "BPM": round(float(tempo)),
            "Key": key,
            "Instruments": "",  # Fill manually later
            "Mood": "",  # Fill manually later
            "Loop files": ""  # Fill manually later
        })

# Save results
df = pd.DataFrame(data)
output_csv = os.path.join(input_folder, "musical_analysis.csv")
df.to_csv(output_csv, index=False)

print("✅ Musical analysis completed and saved to CSV!")