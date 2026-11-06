"""Planar pose comparisons, not independent accuracy measurements.

SPDX-License-Identifier: Apache-2.0
"""

import math


def pose_error(goal, actual):
    """Compare (x meters, y meters, yaw radians) in the same frame.

    Signed errors are actual minus goal. The yaw range is [-180, 180).
    """
    if len(goal) != 3 or len(actual) != 3:
        raise ValueError('Each pose must contain x, y and yaw.')
    if not all(math.isfinite(value) for value in (*goal, *actual)):
        raise ValueError('Pose values must be finite.')
    dx_mm = (actual[0] - goal[0]) * 1000.0
    dy_mm = (actual[1] - goal[1]) * 1000.0
    yaw = (actual[2] - goal[2] + math.pi) % (2.0 * math.pi) - math.pi
    result = dict(dx_mm=dx_mm, dy_mm=dy_mm,
                  xy_mm=math.hypot(dx_mm, dy_mm), yaw_deg=math.degrees(yaw))
    if not all(math.isfinite(value) for value in result.values()):
        raise ValueError('Pose difference exceeds the finite numeric range.')
    return result


def quaternion_yaw(x, y, z, w):
    """Return yaw in radians after normalizing a finite nonzero quaternion."""
    if not all(math.isfinite(value) for value in (x, y, z, w)):
        raise ValueError('Quaternion values must be finite.')
    norm = math.hypot(x, y, z, w)
    if norm == 0.0 or not math.isfinite(norm):
        raise ValueError('Quaternion must have a finite, nonzero norm.')
    x, y, z, w = (value / norm for value in (x, y, z, w))
    return math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
