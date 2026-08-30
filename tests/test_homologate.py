import unittest

from src.homologate import homologate


class HomologationTest(unittest.TestCase):
    def test_right_side_aliases(self):
        record = {
            "trial_id": "trial-demo-001",
            "side": "right",
            "keypoints": {
                "RHip": [1, 2],
                "RKnee": [3, 4],
                "RAnkle": [5, 6],
                "RBigToe": [7, 8],
            },
        }
        result = homologate(record)
        self.assertEqual([point["landmark"] for point in result["landmarks"]], ["hip", "knee", "ankle", "foot"])
        self.assertEqual(result["landmarks"][2]["x_px"], 5.0)

    def test_missing_point_is_not_zero(self):
        result = homologate({"side": "left", "keypoints": {"LHip": [1, 2]}})
        self.assertFalse(result["landmarks"][1]["valid"])
        self.assertIsNone(result["landmarks"][1]["x_px"])


if __name__ == "__main__":
    unittest.main()

