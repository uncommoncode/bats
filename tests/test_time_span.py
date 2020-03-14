from unittest import TestCase

from bats.time_span import TimeSpan


class TestTimeSpan(TestCase):
    def test_slice_end(self):
        n_frames = 10
        total_n_frames = 100
        time_span = TimeSpan(None, n_frames, total_n_frames)
        self.assertEqual(time_span.n_frames, n_frames)
        self.assertEqual(time_span.total_n_frames, total_n_frames)
        self.assertEqual(time_span.absolute_start_frame, 0)
        self.assertEqual(time_span.absolute_end_frame, n_frames)
        self.assertEqual(time_span.relative_start_frame, 0)
        self.assertEqual(time_span.relative_end_frame, n_frames)

        time_span = time_span.from_relative_slice(start_frame=3, end_frame=5)
        self.assertEqual(time_span.absolute_start_frame, 3)
        self.assertEqual(time_span.absolute_end_frame, 5)
        self.assertEqual(time_span.n_frames, 2)
        self.assertEqual(time_span.total_n_frames, total_n_frames)
        self.assertEqual(time_span.relative_start_frame, 0)
        self.assertEqual(time_span.relative_end_frame, 2)
        
    def test_slice_start(self):
        start = 10
        total_n_frames = 100
        n_frames = total_n_frames - start
        time_span = TimeSpan(start, None, total_n_frames)
        self.assertEqual(time_span.n_frames, n_frames)
        self.assertEqual(time_span.total_n_frames, total_n_frames)
        self.assertEqual(time_span.absolute_start_frame, start)
        self.assertEqual(time_span.absolute_end_frame, total_n_frames)
        self.assertEqual(time_span.relative_start_frame, 0)
        self.assertEqual(time_span.relative_end_frame, n_frames)

        time_span = time_span.from_relative_slice(start_frame=3, end_frame=5)
        self.assertEqual(time_span.absolute_start_frame, start + 3)
        self.assertEqual(time_span.absolute_end_frame, start + 5)
        self.assertEqual(time_span.n_frames, 2)
        self.assertEqual(time_span.total_n_frames, total_n_frames)
        self.assertEqual(time_span.relative_start_frame, 0)
        self.assertEqual(time_span.relative_end_frame, 2)

    def test_slice_start_end(self):
        start = 17
        end = 50
        total_n_frames = 100
        n_frames = end - start
        time_span = TimeSpan(start, n_frames, total_n_frames)
        self.assertEqual(time_span.n_frames, n_frames)
        self.assertEqual(time_span.total_n_frames, total_n_frames)
        self.assertEqual(time_span.absolute_start_frame, start)
        self.assertEqual(time_span.absolute_end_frame, end)
        self.assertEqual(time_span.relative_start_frame, 0)
        self.assertEqual(time_span.relative_end_frame, n_frames)

        time_span = time_span.from_relative_slice(start_frame=3, end_frame=5)
        self.assertEqual(time_span.absolute_start_frame, start + 3)
        self.assertEqual(time_span.absolute_end_frame, start + 5)
        self.assertEqual(time_span.n_frames, 2)
        self.assertEqual(time_span.total_n_frames, total_n_frames)
        self.assertEqual(time_span.relative_start_frame, 0)
        self.assertEqual(time_span.relative_end_frame, 2)
