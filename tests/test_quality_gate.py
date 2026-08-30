import unittest

from src.quality_gate import evaluate_reconstruction


class QualityGateTest(unittest.TestCase):
    def test_rejects_large_reprojection_error(self):
        result = evaluate_reconstruction({
            "xyz": [0, 0, 1],
            "cameras": ["CAM_1", "CAM_2"],
            "max_reprojection_error_px": 5.1,
        }, max_reprojection_error_px=5.0)
        self.assertFalse(result["accepted"])
        self.assertTrue(result["reasons"])


if __name__ == "__main__":
    unittest.main()
