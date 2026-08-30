import unittest

import numpy as np

from src.dlt import projection_matrix_from_dlt, triangulate_point, triangulate_trajectory
from src.quality_gate import evaluate_reconstruction


class DltTest(unittest.TestCase):
    def test_two_view_triangulation(self):
        matrices = {
            "CAM_1": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
            "CAM_2": [[1, 0, 0, -1], [0, 1, 0, 0], [0, 0, 1, 0]],
        }
        observations = {"CAM_1": [0.125, 0.05], "CAM_2": [-0.375, 0.05]}
        result = triangulate_point(observations, matrices)
        np.testing.assert_allclose(result["xyz"], [0.25, 0.1, 2.0], atol=1e-10)
        self.assertLess(result["max_reprojection_error_px"], 1e-10)

    def test_legacy_coefficients_are_explicit(self):
        matrix = projection_matrix_from_dlt([1] * 11)
        self.assertEqual(matrix.shape, (3, 4))
        self.assertEqual(matrix[2, 3], 1.0)

    def test_trajectory_keeps_invalid_frames_explicit(self):
        matrices = {
            "CAM_1": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
            "CAM_2": [[1, 0, 0, -1], [0, 1, 0, 0], [0, 0, 1, 0]],
        }
        frames = triangulate_trajectory([
            {"frame_index": 10, "observations": {"CAM_1": [0.125, 0.05], "CAM_2": [-0.375, 0.05]}},
            {"frame_index": 11, "observations": {"CAM_1": [0.125, 0.05]}},
        ], matrices)
        self.assertEqual(frames[0]["status"], "ok")
        self.assertEqual(frames[1]["status"], "invalid")
        self.assertTrue(evaluate_reconstruction(frames[0])["accepted"])


if __name__ == "__main__":
    unittest.main()
