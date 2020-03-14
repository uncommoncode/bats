import soundfile as sf
import numpy as np
import scipy.signal


class AudioView:
    def __init__(self, sample_rate, duration, n_channels, path, start_frame=None, end_frame=None, data=None):
        self.sample_rate = sample_rate
        self.duration = duration
        self.n_channels = n_channels
        self._path = path
        self._start_frame = start_frame
        self._end_frame = end_frame
        self._data = data
        if self._path is None and self._data is None:
            raise RuntimeError('Invalid AudioView that has no file path or data!')
            
    def start_time(self):
        if self._start_frame is None:
            return 0.0
        return self.frame_to_second(self._start_frame)
    
    def end_time(self):
        if self._end_frame is None:
            return self.duration + self.start_time()
        return self.frame_to_second(self._end_frame)
        
    def _view_from_slice(self, arg):
        if arg.step:
            raise RuntimeError('Downsampling with slice steps not supported!')
        # TODO: propogate self.data if we have already loaded
        start_time = arg.start
        end_time = arg.stop
        if start_time is None:
            start_time = 0.0
        if end_time is None:
            end_time = self.duration
        duration = end_time - start_time
        duration = self.frame_to_second(self.second_to_frame(duration))
        if duration <= 0:
            raise RuntimeError(f'Invalid view start: {start_time} end: {end_time}')
        return AudioView(
            sample_rate=self.sample_rate,
            duration=duration,
            n_channels=self.n_channels,
            path=self._path,
            start_frame=self.second_to_frame(start_time),
            end_frame=self.second_to_frame(end_time),
        )
    
    def second_to_frame(self, second):
        if second is None:
            return None
        return int(self.sample_rate * second + 0.5)
    
    def frame_to_second(self, frame):
        if frame is None:
            return None
        return frame / self.sample_rate

    def __getitem__(self, arg):
        if isinstance(arg, slice):
            return self._view_from_slice(arg)
        raise
        
    def mean(self):
        return self.data().mean()
    
    def min(self):
        return self.data().min()
    
    def max(self):
        return self.data().max()
    
    def mean_power(self):
        return (self.data()**2).mean()
    
    def is_zero(self):
        return not np.any(self.data() != 0)
        
    def data(self):
        if self._data is None:
            if self._path is None:
                raise RuntimeError('Invalid AudioView that has no file path or data!')
            self._data, _ = sf.read(
                self._path, 
                start=self._start_frame, 
                stop=self._end_frame,
                always_2d=True,
                dtype='float32',
            )
        return self._data
    
    def _plot_time_series(self, data, n_points, use_downsample, y_axis_name):
        downsample_factor = data.shape[0] // n_points
        for channel in range(data.shape[1]):
            plot_data = data[:, channel]
            if use_downsample:
                plot_data = scipy.signal.decimate(plot_data, downsample_factor, ftype='fir')
            t = np.linspace(start=self.start_time(), stop=self.end_time(), num=plot_data.shape[0])
            plt.title(f'Channel {channel} {y_axis_name}')
            plt.plot(t, plot_data)
            plt.ylabel(y_axis_name)
            plt.xlabel('Time [s]')
            plt.show()
    
    def plot_amplitude(self, n_points=400, use_downsample=True):
        return self._plot_time_series(
            data=self.data(),
            n_points=n_points,
            use_downsample=use_downsample,
            y_axis_name='Amplitude',
        )
            
    def plot_power(self, n_points=400, use_downsample=True):
        return self._plot_time_series(
            data=self.data()**2,
            n_points=n_points,
            use_downsample=use_downsample,
            y_axis_name='Power',
        )
    
    def display(self, normalize=False):
        return display_audio(self.data(), self.sample_rate, normalize)
    
    def describe(self):
        column_names = [''] + [f'Channel{n}' for n in range(self.n_channels)] + ['All']
        rows = []
        row = {f'Channel{n}':self.sample_rate for n in range(self.n_channels)}
        row['All'] = self.sample_rate
        row[''] = 'Sample Rate [Hz]'
        rows.append(row)
        row = {f'Channel{n}':self.data()[:, n].mean() for n in range(self.n_channels)}
        row['All'] = self.data().mean()
        row[''] = 'Mean'
        rows.append(row)
        row = {f'Channel{n}':self.data()[:, n].min() for n in range(self.n_channels)}
        row['All'] = self.data().min()
        row[''] = 'Min'
        rows.append(row)
        row = {f'Channel{n}':self.data()[:, n].max() for n in range(self.n_channels)}
        row['All'] = self.data().max()
        row[''] = 'Max'
        rows.append(row)
        row = {f'Channel{n}':(self.data()[:, n]**2).mean() for n in range(self.n_channels)}
        row['All'] = (self.data()**2).mean()
        row[''] = 'Mean Power'
        rows.append(row)
        row = {f'Channel{n}':self.duration for n in range(self.n_channels)}
        row['All'] = self.duration
        row[''] = 'Duration [s]'
        rows.append(row)
        return display_table('Description', column_names, rows)
    
    def _from_mutated_data(self, data):
        return self.from_data(
            data=data,
            sample_rate=self.sample_rate,
            start_frame=self._start_frame,
            end_frame=self._end_frame,
        )
        
    def __add__(self, value):
        return self._from_mutated_data(self.data() + value)
    
    def __sub__(self, value):
        return self._from_mutated_data(self.data() - value)
    
    def __mul__(self, value):
        return self._from_mutated_data(self.data() * value)
    
    def __truediv__(self, value):
        return self._from_mutated_data(self.data() / value)
    
    @classmethod
    def from_file(cls, path):
        info = sf.info(path)
        return cls(
            sample_rate=info.samplerate,
            duration=info.duration,
            n_channels=info.channels,
            path=path,
        )
    
    @classmethod
    def from_data(cls, data, sample_rate, start_frame=None, end_frame=None):
        if len(data.shape) == 1:
            data = np.expand_dims(data, axis=-1)
        if len(data.shape) != 2:
            raise RuntimeError(f'Invalid audio data with shape: {data.shape}')
        n_frames = data.shape[0]
        n_channels = data.shape[1]
        duration = n_frames / sample_rate
        return cls(
            sample_rate=sample_rate,
            duration=duration,
            n_channels=n_channels,
            path=None,
            data=data,
            start_frame=start_frame,
            end_frame=end_frame,
        )
