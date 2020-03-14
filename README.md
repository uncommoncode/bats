# Welcome to bats 🦇!

Beautiful Audio ToolS for interactive data exploration.

It's like pandas for audio.

[![Build Status](https://travis-ci.org/uncommoncode/bats.svg?branch=master)](https://travis-ci.org/uncommoncode/bats)

# Example Usage

```python
from bats import AudioView

av = AudioView.from_file('test_wav.wav')

# Describe the per-channel statistics.
av.describe()

# Plot the power of the waveform.
av.plot_power()

# Display an audio player for the span of 3.5 to 7 seconds.
av[3.5:7.0].display()

# Scale the signal and display the audio player.
(av * 0.5).display()
```
