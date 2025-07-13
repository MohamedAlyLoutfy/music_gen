import os
import librosa
import numpy as np
from tqdm import tqdm

def wav_to_mel(wav_path, sr=32000, n_fft=2048, hop_length=512, n_mels=256):
    y, _ = librosa.load(wav_path, sr=sr)
    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = (mel_db + 80) / 80  # normalize to [0, 1]
    return mel_db.astype(np.float32)

def process_dataset(root_dir, output_dir, allowed_stems=None):
    if allowed_stems is None:
        allowed_stems = ['vocals', 'no_vocals', 'bass', 'drums', 'other']

    os.makedirs(output_dir, exist_ok=True)
    song_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    for song in tqdm(song_dirs, desc="Processing songs"):
        song_path = os.path.join(root_dir, song)
        out_song_path = os.path.join(output_dir, song)
        os.makedirs(out_song_path, exist_ok=True)

        for stem in allowed_stems:
            in_file = os.path.join(song_path, f"{stem}.wav")
            out_file = os.path.join(out_song_path, f"{stem}.npy")

            if os.path.exists(in_file):
                try:
                    mel = wav_to_mel(in_file)
                    np.save(out_file, mel)
                except Exception as e:
                    print(f"Failed to process {in_file}: {e}")
            else:
                print(f"Missing file: {in_file}")

def main():
    # 🔧 EDIT THESE PATHS
    # root_dir = "/media/selim/New Volume/MusicGen"
    # output_dir = "/media/selim/New Volume/MusicGen_mels"
    root_dir = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/full_test_resampled/test"
    output_dir = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/full_test_split"

    process_dataset(root_dir, output_dir)

if __name__ == "__main__":
    main()
