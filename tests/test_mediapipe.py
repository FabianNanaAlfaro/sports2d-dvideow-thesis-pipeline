import unittest

import numpy as np

from src.run_mediapipe import crop_with_padding


class MediaPipeAdapterTest(unittest.TestCase):
    def test_roi_geometry_is_kept_in_original_pixel_space(self):
        frame = np.zeros((100, 120, 3), dtype=np.uint8)
        crop, geometry = crop_with_padding(
            frame,
            {"x": 20, "y": 10, "width": 40, "height": 30, "padding": 0.25, "scale": 1},
        )
        self.assertEqual(crop.shape[:2], (46, 60))
        self.assertEqual(geometry, {"x": 10, "y": 2, "width": 60, "height": 46, "scale": 1.0})

    def test_without_roi_uses_the_full_frame(self):
        frame = np.zeros((10, 12, 3), dtype=np.uint8)
        crop, geometry = crop_with_padding(frame, None)
        self.assertEqual(crop.shape, frame.shape)
        self.assertEqual(geometry["width"], 12)
        self.assertEqual(geometry["height"], 10)


if __name__ == "__main__":
    unittest.main()
