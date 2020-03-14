import numpy as np


def generate_sine(frequency, duration, sample_rate):
    t = np.arange(duration * sample_rate) / sample_rate
    return np.sin(2.0 * np.pi * frequency * t)
