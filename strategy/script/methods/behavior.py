#!/usr/bin/env python
from __future__ import print_function
import rospy
import math
import numpy as np
from robot.robot import Robot

ORBIT_KP_V = -0.5
ORBIT_KP_W = 4.2

REMAINING_RANGE_V = 5
REMAINING_RANGE_YAW = 2

class Behavior(Robot):
  def __init__(self):
    pass

  def Orbit(self, goal_ang):
    orbit_radius = 33.5 # 22.5 + 11 cm
    velocity = goal_ang
    # velocity = velocity if abs(velocity) < 45 else 45 # maximum speed
    w = (velocity / orbit_radius)

    v_x   = 0
    v_y   = velocity * ORBIT_KP_V
    v_yaw = w * ORBIT_KP_W
    o_yaw = v_yaw if abs(v_yaw) > 0.2 else 0.2 * np.sign(v_yaw) # 0.2 is minimum speed

    remaining_yaw = o_yaw
    if abs(remaining_yaw) < REMAINING_RANGE_YAW:
      arrived = True
    else:
      arrived = False
    return v_x, v_y, o_yaw, arrived

  def Go2Point(self, tx, ty, tyaw):
    robot_info = self.GetRobotInfo()

    v_x   = tx - robot_info['location']['x']
    v_y   = ty - robot_info['location']['y']
    o_x, o_y = self.Rotate(v_x, v_y, robot_info['location']['yaw'] * -1)

    v_yaw = tyaw - robot_info['location']['yaw']
    if abs(v_yaw - 360) < abs(v_yaw):
      o_yaw = v_yaw - 360
    elif abs(v_yaw + 360) < abs(v_yaw):
      o_yaw = v_yaw + 360
    else:
      o_yaw = v_yaw

    remaining_v   = math.sqrt(o_x**2 + o_y**2)
    remaining_yaw = o_yaw
    if abs(remaining_v) < REMAINING_RANGE_V and abs(remaining_yaw) < REMAINING_RANGE_YAW:
      arrived = True
    else:
      arrived = False

    return o_x, o_y, o_yaw, arrived
