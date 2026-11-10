# Week 4 — Autonomous Navigation

## Assignment objective

The 2025 handout states:

> You will learn about using computer vision techniques to detect markers and build a self-correcting algorithm to follow the markers and make turns based on the markers.

## Implementation plan

Develop a camera-based marker-following behaviour for the TurtleBot.

The detailed task notes associated with this assignment specify the following marker convention:

- Use OpenCV ArUco detection with the `DICT_ARUCO_ORIGINAL` dictionary.
- Marker ID `0`: command a right turn of 90 degrees.
- Marker ID `1`: command a left turn of 90 degrees.
- Handle five marker encounters as part of the navigation exercise.

These marker IDs, dictionary, turn directions, and number of encounters are detailed task notes, rather than details present in the short 2025 overview handout.

## Implementation plan

1. Confirm that the Webots TurtleBot model exposes a camera device and a ROS 2 image topic.
2. Subscribe to the camera image stream.
3. Convert incoming ROS images to OpenCV images using `cv_bridge`.
4. Detect ArUco markers using the specified dictionary.
5. Estimate marker position relative to the image centre.
6. Apply a self-correcting alignment behaviour to keep the robot following the detected marker.
7. Trigger the specified turn when marker ID 0 or 1 is detected.
8. Add safeguards for marker loss, repeated detections, and completion of a turn before processing the next marker.

The camera device/topic and the exact control strategy must be verified in the selected Webots robot model; do not assume they are already available.

## Verification checklist

- [ ] Verify camera availability in the robot model and ROS 2 graph.
- [ ] Verify image encoding and image topic.
- [ ] Confirm detection of `DICT_ARUCO_ORIGINAL` markers.
- [ ] Confirm marker ID 0 causes a right 90-degree turn.
- [ ] Confirm marker ID 1 causes a left 90-degree turn.
- [ ] Verify self-correcting marker following.
- [ ] Test marker loss and reacquisition.
- [ ] Complete and record the five-marker sequence.
- [ ] Record limitations of the Webots camera/simulation setup.

## Status

Not implemented yet. No camera availability or marker-navigation behaviour is claimed as verified.
