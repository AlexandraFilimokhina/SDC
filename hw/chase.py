#! /usr/bin/env python

import rospy
from math import sqrt, atan2, pi, log
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from rospy import Publisher, Subscriber

class Chase:
	def __init__(self):

		self.position = Pose()
		self.publisher = Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
		self.sub_t1 = Subscriber('/turtle1/pose', Pose, self.chasing)
		self.sub_t2 = Subscriber('/turtle2/pose', Pose, self.pose_upd)

	@staticmethod
	def calc_distance(p_0, p_1):
		return sqrt((p_1.y - p_0.y) ** 2 + (p_1.x - p_0.x) ** 2)

	@staticmethod
	def calc_angle(p_0, p_1):
		return atan2(p_1.y - p_0.y, p_1.x - p_0.x) - p_0.theta

	def pose_upd(self, position):
		self.position = position

	def chasing(self, position):
		twist = Twist()
		distance = self.calc_distance(self.position, position)

 		if distance > 1e-1:
			angle = self.calc_angle(self.position, position)
			while angle > pi:
				angle -= 2 * pi
			while angle < - pi:
				angle += 2 * pi
			twist.linear.x = distance
			twist.angular.z = angle
			self.publisher.publish(twist)
		
				
			

if __name__ == '__main__':
	rospy.init_node('chase')
	Chase()
	rospy.spin()
