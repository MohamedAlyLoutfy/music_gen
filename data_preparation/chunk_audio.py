import os
import librosa
import soundfile as sf

def chunk_audio(input_root, output_root, chunk_length_sec=30, stride_sec=30, target_sr=32000):
    os.makedirs(output_root, exist_ok=True)

    for song_dir in os.listdir(input_root):
        song_input_path = os.path.join(input_root, song_dir)
        song_output_path = os.path.join(output_root, song_dir)

        if not os.path.isdir(song_input_path):
            continue

        os.makedirs(song_output_path, exist_ok=True)

        for file_name in os.listdir(song_input_path):
            if not file_name.endswith(".wav"):
                continue

            file_lower = file_name.lower()
            if "vocals" in file_lower and "no_vocals" not in file_lower:
                stem_type = "conditioning"
            elif "no_vocals" in file_lower:
                stem_type = "target"
            else:
                continue  # Skip unrelated stems like "drums", "bass", etc.

            input_file_path = os.path.join(song_input_path, file_name)
            y, sr = librosa.load(input_file_path, sr=None)

            if sr != target_sr:
                y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)

            chunk_len = chunk_length_sec * target_sr
            stride = stride_sec * target_sr
            total_samples = len(y)

            chunk_count = 0
            for i in range(0, total_samples - chunk_len + 1, stride):
                chunk = y[i:i + chunk_len]
                out_filename = f"{stem_type}_{chunk_count:04d}.wav"
                out_path = os.path.join(song_output_path, out_filename)
                sf.write(out_path, chunk, samplerate=target_sr)
                chunk_count += 1

            print(f"Processed {file_name}: {chunk_count} chunks")

def main():
    # 🔧 EDIT THESE PATHS
    input_root = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/full_test_split/test"
    output_root = "/home/selim/Documents/Uni Stuttgart/DeepLearningLab/full_test_chunks"

    chunk_audio(input_root, output_root)

if __name__ == "__main__":
    main()
