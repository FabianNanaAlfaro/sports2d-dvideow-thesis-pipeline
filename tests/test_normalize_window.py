import unittest

from src.normalize_window import normalize_series


class NormalizeWindowTest(unittest.TestCase):
    def test_declared_output_length(self):
        values = normalize_series([0, 1, 2, 3], [0, 1, None, 3], points=5)
        self.assertEqual(len(values), 5)
        self.assertAlmostEqual(values[0], 0.0)
        self.assertAlmostEqual(values[-1], 3.0)

    def test_insufficient_data_stays_missing(self):
        self.assertEqual(normalize_series([0, 1], [None, 1], points=3), [None, None, None])

    def test_rejects_non_monotonic_frames(self):
        with self.assertRaises(ValueError):
            normalize_series([0, 2, 1], [0.0, 0.2, 0.1], points=4)


if __name__ == "__main__":
    unittest.main()
