"""Core Streaming Audio Frame Chunker with Energy VAD."""
from typing import List, Optional
import struct
import math

class AudioChunk:
    def __init__(self, raw_pcm: bytes, is_speech: bool, rms_energy: float):
        self.raw_pcm = raw_pcm
        self.is_speech = is_speech
        self.rms_energy = rms_energy

class AudioFrameChunker:
    def __init__(self, sample_rate: int = 16000, frame_duration_ms: int = 20, energy_threshold: float = 500.0):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.bytes_per_sample = 2 # 16-bit PCM
        self.samples_per_frame = int(sample_rate * (frame_duration_ms / 1000.0))
        self.frame_bytes_len = self.samples_per_frame * self.bytes_per_sample
        self.energy_threshold = energy_threshold
        self._buffer = bytearray()

    def process_stream(self, chunk: bytes) -> List[AudioChunk]:
        self._buffer.extend(chunk)
        frames = []

        while len(self._buffer) >= self.frame_bytes_len:
            frame_raw = bytes(self._buffer[:self.frame_bytes_len])
            self._buffer = self._buffer[self.frame_bytes_len:]

            # Calculate RMS energy
            count = len(frame_raw) // 2
            shorts = struct.unpack(f"!{count}h" if False else f"<{count}h", frame_raw)
            sum_squares = sum(s * s for s in shorts)
            rms = math.sqrt(sum_squares / count) if count > 0 else 0.0

            is_speech = rms > self.energy_threshold
            frames.append(AudioChunk(frame_raw, is_speech, rms))

        return frames
