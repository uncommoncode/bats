class TimeSpan:
    def __init__(self, start_frame, n_frames, total_n_frames):
        if start_frame is None:
            start_frame = 0
        if n_frames is None:
            n_frames = total_n_frames - start_frame
        self._start_frame = start_frame
        self._n_frames = n_frames
        self._total_n_frames = total_n_frames

    @property
    def absolute_start_frame(self):
        return self._start_frame

    @property
    def absolute_end_frame(self):
        return self._start_frame + self._n_frames
    
    @property
    def relative_start_frame(self):
        return 0

    @property
    def relative_end_frame(self):
        return self._n_frames
    
    @property
    def n_frames(self):
        return self._n_frames

    @property
    def total_n_frames(self):
        return self._total_n_frames

    def from_absolute_slice(self, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0

        if end_frame is None:
            end_frame = self.n_frames

        n_frames = end_frame - start_frame
        if n_frames <= 0:
            raise RuntimeError(f'Invalid timespan start:{start_frame} end:{end_frame}')

        return TimeSpan(
            start_frame=start_frame,
            n_frames=n_frames,
            total_n_frames=self.total_n_frames,
        )

    def from_relative_slice(self, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = self.relative_start_frame

        if end_frame is None:
            end_frame = self.relative_end_frame

        return self.from_absolute_slice(
            start_frame=self.absolute_start_frame + start_frame,
            end_frame=self.absolute_start_frame + end_frame,
        )
