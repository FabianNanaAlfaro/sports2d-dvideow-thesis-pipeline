import unittest

from src.biomechanics import angle_at_vertex, symmetry_index, velocity_from_positions


class BiomechanicsTest(unittest.TestCase):
    def test_velocity_uses_sampling_rate(self):
        result = velocity_from_positions([[0, 0, 0], [1, 0, 0], [2, 0, 0]], sampling_hz=10)
        self.assertAlmostEqual(result[1][0], 10.0)

    def test_angle_is_geometric_and_missing_safe(self):
        self.assertAlmostEqual(angle_at_vertex([1, 0, 0], [0, 0, 0], [0, 1, 0]), 90.0)
        self.assertIsNone(angle_at_vertex(None, [0, 0, 0], [0, 1, 0]))

    def test_symmetry_is_explicit(self):
        self.assertAlmostEqual(symmetry_index(2, 3), 40.0)
        self.assertIsNone(symmetry_index(0, 0))


if __name__ == "__main__":
    unittest.main()
