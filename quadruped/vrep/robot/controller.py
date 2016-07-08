from __future__ import division
from __future__ import print_function
import time
# import math
# from math import radians as d2r
# from robot.tranforms import rotate
from robot.gaits import TrotGait, CrawlGait
import sys
import os
sys.path.insert(0, os.path.abspath('../..'))
import lib.zmqclass as Zmq


class RobotController(object):
	"""
	"""
	def __init__(self, robot):
		"""
		in: robot - either a real or virtual robot
		"""
		self.robot = robot

		# desired position
		self.dx = 100
		self.dy = 0.0
		self.dz = 0.0
		self.drot = [0.0, 0.0, 0.0]  # roll pitch yaw deltas?

		self.startTime = time.time()
		# self.trotgait = TrotGait(self.robot)
		self.trotgait = CrawlGait(self.robot)
		self.trotgait.reset()

	def start(self):
		"""
		setup everything before main loop.
		"""
		self.robot.start()
		self.sub = Zmq.Sub('ctlr')

	def trot(self):
		"""
		executes a step of the "trot" gait.
		"""
		return self.trotgait.iterate([self.dx, self.dy, self.dz], self.drot)
		self.robot.commandServos()

	def iterate(self):
		"""
		runs one iteration of the code, usually called in a loop
		"""
		self.dx = 0.0
		self.dy = 0.0
		self.dz = 0.0
		self.drot[2] = -0.50  # i think these are rates not positions

		ret = 1

		msg = self.sub.recv()
		# if msg:
		# 	self.dx = msg['linear']['x']
		# 	self.dy = msg['linear']['y']
		# 	self.dz = msg['linear']['z']

		while ret != 0:  # complete one full gait and be stable
			# if not msg: break  # don't move if no command
			ret = self.trot()
			self.robot.finish_iteration()
			time.sleep(0.05)




if __name__ == "__main__":
	pass