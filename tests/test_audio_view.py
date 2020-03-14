from unittest import TestCase

from bats.audio_view import AudioView
from bats.util import generate_sine

class TestAudioViewOperators(TestCase):
    def setUp(self):
        sample_rate = 48000
        data = generate_sine(1000, 1.0, sample_rate)
        self.av = AudioView.from_data(
            data=data,
            sample_rate=sample_rate,
        )

    def test_add(self):
        av = self.av + 0.5
        # Dont modify original array
        self.assertEqual(self.av.max(), 1.0)
        # New value should be updated
        self.assertEqual(av.max(), 1.5)

    def test_sub(self):
        av = self.av - 0.5
        # Dont modify original array
        self.assertEqual(self.av.max(), 1.0)
        # New value should be updated
        self.assertEqual(av.max(), 0.5)
    
    def test_mul(self):
        av = self.av * 2.0
        # Dont modify original array
        self.assertEqual(self.av.max(), 1.0)
        # New value should be updated
        self.assertEqual(av.max(), 2.0)

    def test_div(self):
        av = self.av / 2.0
        # Dont modify original array
        self.assertEqual(self.av.max(), 1.0)
        # New value should be updated
        self.assertEqual(av.max(), 0.5)
