from unittest import TestCase

from bats.audio_view import AudioView
from bats.util import generate_sine


class TestAudioViewSlicing(TestCase):
    def setUp(self):
        sample_rate = 48000
        self.duration = 1.0
        data = generate_sine(1000, self.duration, sample_rate)
        self.av = AudioView.from_data(
            data=data,
            sample_rate=sample_rate,
        )

    def test_slice_end(self):
        av = self.av[:0.1]
        # Dont modify original array
        self.assertEqual(self.av.duration, 1.0)
        # New value should be updated
        self.assertEqual(av.duration, 0.1)
        self.assertEqual(av.start_time(), 0.0)
        self.assertEqual(av.end_time(), 0.1)

    def test_slice_start(self):
        av = self.av[0.1:]
        # Dont modify original array
        self.assertEqual(self.av.duration, 1.0)
        # New value should be updated
        self.assertEqual(av.duration, 0.9)
        self.assertEqual(av.start_time(), 0.1)
        self.assertEqual(av.end_time(), 1.0)

    def test_slice_start_and_end(self):
        av = self.av[0.1:0.3]
        # Dont modify original array
        self.assertEqual(self.av.duration, 1.0)
        # New value should be updated
        self.assertEqual(av.duration, 0.2)
        self.assertEqual(av.start_time(), 0.1)
        self.assertEqual(av.end_time(), 0.3)

    def test_slice_of_slice(self):
        av = self.av[0.1:0.3][0.1:]
        # Dont modify original array
        self.assertEqual(self.av.duration, 1.0)
        # New value should be updated
        self.assertEqual(av.duration, 0.1)
        self.assertEqual(av.start_time(), 0.2)
        self.assertEqual(av.end_time(), 0.3)


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
