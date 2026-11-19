"""Tests for Audio Chunker."""
import unittest
import struct
from multimodal_audio_frame_chunker.core import AudioFrameChunker

class TestAudioFrameChunker(unittest.TestCase):
    def test_chunking_and_vad(self):
        c = AudioFrameChunker(energy_threshold=50.0)
        # 320 samples = 640 bytes for 20ms at 16kHz
        silence = bytes(640)
        chunks = c.process_stream(silence)
        self.assertEqual(len(chunks), 1)
        self.assertFalse(chunks[0].is_speech)

        # Loud tone
        loud_samples = [1000] * 320
        loud_pcm = struct.pack("<320h", *loud_samples)
        loud_chunks = c.process_stream(loud_pcm)
        self.assertEqual(len(loud_chunks), 1)
        self.assertTrue(loud_chunks[0].is_speech)
