from pathlib import Path
import re
import numpy as np
import soundfile as sf

def numeric_key(filename: str):
    """
    Extract numeric prefix for sorting (e.g., '10.wav' -> 10).
    Files without numeric prefix are pushed to the end.
    """
    m = re.match(r"(\d+)", filename)
    return int(m.group(1)) if m else float("inf")

def concat_wavs_with_silence(
    input_dir: str,
    output_file: str,
    silence_seconds: float = 1.0
):
    input_path = Path(input_dir)
    wav_files = sorted(input_path.glob("*.wav"), key=lambda f: numeric_key(f.stem))

    if not wav_files:
        raise FileNotFoundError("No .wav files found in the directory.")

    # Read first file to define format
    first_data, samplerate = sf.read(wav_files[0], dtype="float32")
    channels = 1 if first_data.ndim == 1 else first_data.shape[1]

    # Prepare silence chunk
    silence_samples = int(silence_seconds * samplerate)
    silence = np.zeros((silence_samples, channels), dtype=np.float32)
    if channels == 1:
        silence = silence.squeeze()  # keep 1D for mono

    chunks = [first_data]

    # Read remaining files, validate format, append with silence
    for wav in wav_files[1:]:
        data, sr = sf.read(wav, dtype="float32")
        if sr != samplerate:
            raise ValueError(f"Sample rate mismatch: {wav} has {sr}, expected {samplerate}")
        file_channels = 1 if data.ndim == 1 else data.shape[1]
        if file_channels != channels:
            raise ValueError(f"Channel mismatch: {wav} has {file_channels}, expected {channels}")

        if silence_seconds > 0:
            chunks.append(silence)
        chunks.append(data)

    # Concatenate and write
    final_audio = np.concatenate(chunks, axis=0)
    sf.write(output_file, final_audio, samplerate)
    print(f"Done! Output saved to: {output_file}")

if __name__ == "__main__":
    concat_wavs_with_silence(
        input_dir="input",
        output_file="output.wav",
        silence_seconds=0.5
    )
