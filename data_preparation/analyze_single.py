import os
import librosa

def analyze_song(song_path):
    if not os.path.exists(song_path):
        print(f"❌ File not found: {song_path}")
        return

    print(f"Analyzing: {song_path}")

    # Load audio
    y, sr = librosa.load(song_path)

    # Estimate BPM
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Estimate key
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_index = chroma.mean(axis=1).argmax()
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = keys[key_index]

    print(f"🎵 BPM: {round(float(tempo))}")
    print(f"🎼 Key: {key}")

# Example usage:
song_path = r"/mnt/sda3/MusicGen2/MusicGen/85 - Whitney Houston - How Will I Know (Official HD Video)/no_vocals.wav"  # Replace this with your file path
analyze_song(song_path)
