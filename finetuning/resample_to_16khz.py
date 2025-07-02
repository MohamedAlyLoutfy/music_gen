import os
import librosa
import soundfile as sf

def resample_audio_files(input_root, output_root, target_sr=32000):
    os.makedirs(output_root, exist_ok=True)

    for song_folder in os.listdir(input_root):
        input_dir = os.path.join(input_root, song_folder)
        output_dir = os.path.join(output_root, song_folder)

        if not os.path.isdir(input_dir):
            continue

        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(input_dir):
            if filename.endswith(".wav"):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)

                try:
                    y, sr = librosa.load(input_path, sr=None)
                    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
                    sf.write(output_path, y_resampled, target_sr)
                    print(f"✔ Resampled: {input_path} → {output_path}")
                except Exception as e:
                    print(f"❌ Failed to process {input_path}: {e}")

def main():
    # 🔧 EDIT THESE PATHS
    # input_root = "/mnt/sda3/MusicGen2/MusicGen"
    # output_root = "/mnt/sda3/MusicGen2/MusicGen2_32khz"
    input_root = "/home/selim/Documents/test_musicgen/split"
    output_root = "/home/selim/Documents/test_musicgen/split_32"

    resample_audio_files(input_root, output_root)

if __name__ == "__main__":
    main()
