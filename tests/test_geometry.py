"""Hand-calculated cases for the learning reporter's public math interface."""

import math
import unittest

from robotless_lab.geometry import pose_error, quaternion_yaw


class PoseErrorTests(unittest.TestCase):
    def test_signed_components_and_euclidean_millimeters(self):
        result = pose_error((1.0, 2.0, 0.0), (1.003, 1.996, 0.0))
        self.assertAlmostEqual(result['dx_mm'], 3.0)
        self.assertAlmostEqual(result['dy_mm'], -4.0)
        self.assertAlmostEqual(result['xy_mm'], 5.0)
        self.assertEqual(result['yaw_deg'], 0.0)

    def test_identical_pose_has_zero_error(self):
        result = pose_error((-2.0, 4.0, 1.2), (-2.0, 4.0, 1.2))
        self.assertEqual(result, dict(dx_mm=0.0, dy_mm=0.0, xy_mm=0.0, yaw_deg=0.0))

    def test_yaw_crossing_pi_uses_shortest_signed_angle(self):
        self.assertAlmostEqual(
            pose_error((0, 0, math.radians(179)), (0, 0, math.radians(-179)))['yaw_deg'],
            2.0,
        )
        self.assertAlmostEqual(
            pose_error((0, 0, math.radians(-179)), (0, 0, math.radians(179)))['yaw_deg'],
            -2.0,
        )

    def test_invalid_and_nonfinite_poses_are_rejected(self):
        for invalid in [(0, 0), (0, 0, math.nan), (math.inf, 0, 0)]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                pose_error((0, 0, 0), invalid)
            with self.subTest(goal=invalid), self.assertRaises(ValueError):
                pose_error(invalid, (0, 0, 0))

    def test_overflow_is_rejected_instead_of_reporting_infinity(self):
        with self.assertRaises(ValueError):
            pose_error((-1e308, 0, 0), (1e308, 0, 0))


class QuaternionTests(unittest.TestCase):
    def test_identity_and_positive_right_angle(self):
        self.assertEqual(quaternion_yaw(0, 0, 0, 1), 0.0)
        self.assertAlmostEqual(quaternion_yaw(0, 0, 1, 1), math.pi / 2)

    def test_negative_yaw_and_scaled_quaternion(self):
        self.assertAlmostEqual(quaternion_yaw(0, 0, -7, 7), -math.pi / 2)

    def test_zero_and_nonfinite_quaternions_are_rejected(self):
        for quaternion in [(0, 0, 0, 0), (0, 0, math.nan, 1), (0, 0, 0, math.inf)]:
            with self.subTest(quaternion=quaternion), self.assertRaises(ValueError):
                quaternion_yaw(*quaternion)


if __name__ == '__main__':
    unittest.main()
