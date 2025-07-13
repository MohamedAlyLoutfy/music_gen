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
    parser.add_argument("--description", type=str, required=True, help="Text description prompt")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save generated audio")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the melody pretrained model
    model = MusicGen.get_pretrained("melody")
    model.set_generation_params(duration=30)  # adjust duration as needed

    # Load your checkpoint and apply weights to lm
    print("Loading fine-tuned checkpoint...")
    ckpt = torch.load(args.model_ckpt, map_location=device)
    if "model" not in ckpt:
        raise RuntimeError("Checkpoint missing 'model' key.")
    model.lm.load_state_dict(ckpt["model"])
    model.lm.eval()
    model.lm.eval().to(device)

    # Load melody waveform (mono, 32kHz)
    wav, sr = torchaudio.load(args.melody)
    if sr != 32000:
        raise ValueError("Melody must be 32kHz.")
    wav = wav.mean(dim=0, keepdim=True).to(device)

    # Run inference
    print("Generating music...")
    with torch.no_grad():
        output = model.generate_with_chroma([args.description], melody_wavs=wav, melody_sample_rate=32000)

    # Save output
    os.makedirs(args.output_dir, exist_ok=True)
    audio_write(os.path.join(args.output_dir, "generated"), output[0].cpu(), model.sample_rate, strategy="loudness")
    print("✅ Done! Audio saved.")

if __name__ == "__main__":
    main()
