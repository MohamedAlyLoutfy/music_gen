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
            print(f"Resampling {filename}")
            if filename.endswith(".wav") or filename.endswith(".mp3"):
                input_path = os.path.join(input_dir, filename)
                output_filename = os.path.splitext(filename)[0] + ".wav"
                output_path = os.path.join(output_dir, output_filename)

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
    # input_root = "/home/selim/Documents/test_musicgen/split"
    # output_root = "/home/selim/Documents/test_musicgen/split_32"
    # input_root = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/self_audio"
    # output_root = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/self_audio_resampled"
    input_root = "/Users/Selim/Documents/UNI_STUTTGART/Semester 4/project_test_audio/pre_sampled"
    output_root = '/Users/Selim/Documents/UNI_STUTTGART/Semester 4/project_test_audio/sampled'

    resample_audio_files(input_root, output_root)

if __name__ == "__main__":
    main()
