import os
import argparse
import torch
import torchaudio

from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--melody", type=str, required=True, help="Path to input .wav file (32kHz)")
    parser.add_argument("--model_ckpt", type=str, required=True, help="Path to training checkpoint .th file")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save generated audio")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load training checkpoint and extract model weights
    print("📦 Loading model checkpoint...")
    checkpoint = torch.load(args.model_ckpt, map_location=device)
    if "model" not in checkpoint:
        raise RuntimeError("Checkpoint does not contain a 'model' key.")
    model_state_dict = checkpoint["model"]

    # Load melody model and apply finetuned weights
    print("🎛️  Loading melody model...")
    model = MusicGen.get_pretrained("melody")
    model.set_generation_params(duration=90)
    model.lm.load_state_dict(model_state_dict)
    model.lm.eval().to(device)

    # Load 32kHz mono melody
    print(f"🎼 Loading melody: {args.melody}")
    wav, sr = torchaudio.load(args.melody)
    if sr != 32000:
        raise ValueError(f"Expected 32kHz input, got {sr}")
    wav = wav.mean(dim=0, keepdim=True).to(device)  # Convert to mono if needed

    # Run generation (no prompt)
    print("🎶 Generating music from melody input...")
    with torch.no_grad():
        gen_audio = model.generate_with_chroma([""], melody_wavs=wav, melody_sample_rate=32000)

    # Save output
    os.makedirs(args.output_dir, exist_ok=True)
    output_path = os.path.join(args.output_dir, "generated")
    audio_write(output_path, gen_audio[0].cpu(), model.sample_rate, strategy="loudness")
    print(f"✅ Output saved to: {output_path}.wav")

if __name__ == "__main__":
    main()
