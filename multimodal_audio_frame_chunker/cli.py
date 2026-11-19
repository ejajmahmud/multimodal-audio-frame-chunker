"""CLI for Audio Chunker."""
import argparse
from .core import AudioFrameChunker

def main():
    parser = argparse.ArgumentParser(description="Multimodal Audio Frame Chunker CLI")
    parser.add_argument("--demo", action="store_true", help="Run audio chunker demo")
    args = parser.parse_args()

    chunker = AudioFrameChunker(energy_threshold=100.0)
    fake_pcm = bytes(640) # 320 samples of silence
    chunks = chunker.process_stream(fake_pcm)
    print(f"Processed {len(chunks)} frames. Is speech: {[c.is_speech for c in chunks]}")

if __name__ == "__main__":
    main()
