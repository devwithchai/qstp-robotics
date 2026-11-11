"""Small, ROS-independent helpers for processing LaserScan ranges."""

import math


def get_front_sector_min_distance(
    ranges,
    angle_min,
    angle_increment,
    half_angle,
    range_min=0.0,
    range_max=math.inf,
):
    """Return the nearest valid range in a forward angular sector.

    Positive infinity is treated as a valid no-return reading (no obstacle
    detected at that beam). NaN, negative infinity, and values outside the
    sensor's declared range are ignored. None means that no usable beam was
    available in the requested sector.
    """
    if not 0.0 <= half_angle <= math.pi:
        raise ValueError('half_angle must be between 0 and pi')
    if range_min < 0.0 or range_max < range_min:
        raise ValueError('invalid sensor range limits')

    valid_readings = 0
    nearest_distance = math.inf

    for index, raw_distance in enumerate(ranges):
        angle = angle_min + index * angle_increment
        if not math.isfinite(angle) or abs(angle) > half_angle:
            continue

        distance = float(raw_distance)
        if math.isnan(distance) or distance == -math.inf:
            continue
        if distance == math.inf:
            valid_readings += 1
            continue
        if distance < range_min or distance > range_max:
            continue

        valid_readings += 1
        nearest_distance = min(nearest_distance, distance)

    if valid_readings == 0:
        return None
    return nearest_distance
