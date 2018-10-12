The ROS Node Challenge
======================

In robotics research and, more recently, also in Autonomous Driving, the
**Robot Operating System** ([ROS](http://wiki.ros.org/)) framework is a
de-facto standard for application development.

ROS can be described as an advanced publish-subscribe message transport system.
Applications can, for example, subscribe to measurement update messages that are published
by _nodes_ managing individual sensors.
Since each sensor can have its own _frame of reference_ for measurements, ROS sets up a
mechanism for publishing _[transforms](http://wiki.ros.org/tf)_ which convert measurements
(e.g. coordinates, distances, from one frame to another).

Your challenge is to master the basic use of the ROS publish/subscribe mechanism and of
transform writing.

### Problem Description

You are given two sensors that can measure _distances_ in 2D. The sensors report their findings in
polar coordinates, i.e. a _distance_ value (expressed in meters) and an _angle_ (expressed in radians,
measuring counterclockwise rotation from the X-axis of the sensor).

However, the sensors are not perfectly accurate and can have measurement errors.

You are given two CSV files (`data/sensor1.csv` and `data/sensor2.csv`), which contain 100 range measurements **of the same target**
(i.e. a single point in 2D), one for each sensor.

Your tasks are the following:

  1. Analyse the measurement distributions for distance and angle for each sensor
  2. Since they are distances and headings towards the same point, establish the 2D transformation
    operations (rotation and translation) required to convert measurements _from_ the reference
    frame of sensor 1 _to_ the reference frame of sensor 2.
  3. Write the code for a [ROS Node](http://wiki.ros.org/ROS/Tutorials/UnderstandingNodes),
  corresponding to sensor 1, which publishes the transform from the reference frame of sensor 1, to that of sensor 2.
  The frame IDs should be named _sensor1_ and _sensor2_, respectively. Study
  [this tutorial](http://wiki.ros.org/tf/Tutorials/Writing%20a%20tf%20broadcaster%20%28Python%29) to get started.

  4. Have the the above ROS Node _publish_ a set of random range measurements in the polar coordinate
  form mentioned previously (distance, angle in radians).
  The measurements are published _in the reference frame_ of sensor 1. For this you have to:

    - define a ROS message format for your measurements (see [this tutorial](http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv) for examples)
    - _publish_ the measurements on the /range/sensor1 topic (see [this ROS Publsih/Subscribe tutorial](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29)
     to get started)

  5. Write another ROS Node, for sensor 2, whose job it is to:

    - subscribe to the ROS Node for sensor 1 to receive range measurements of that node
    - use to the transform broadcast by the ROS Node of sensor 1 to convert the measurements from the
    reference frame of sensor 1 to that of sensor 2
    - publish the transformed measurements under the topic /range/sensor2

To test tasks 4 and 5, you may use the data in `data/test_sensor1.csv`,
which provides 10 measurements (of **different** targets this time). Have the ROS Node for sensor 1 publish
these points.

The ROS Node for sensor 2 should output values that can be compared against those of `data/test_sensor2.csv`.
Distances should be exact within a +/- 0.75 m, while angle measurements
should be exact to within +/- 2 degrees (i.e. +/- pi/90 radians).
