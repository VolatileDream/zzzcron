#!/usr/bin/env python3

import util
import datetime

class SleepPredictionAlgorithm:

	def __init__(self):
		self.data = util.SleepPredictionTable()

	def update(self, prev, value):
		pass

	def add_data(self, p, n):
		"""passed the last data point,
		and the next, the algorithm
		should update it's state using these 2 points"""
		start = p[1]
		end = n[1]

		value = 0.0 # assume they're asleep
		if p[0] == util.SleepState.awake:
			value = 1.0

		for segment in util.time_iter(start, end):
			time_string = util.time_str_from_tuple(segment)
			#print( "updating(" + p[0].name + " " + str(p) +"-" + str(n) + " ): " + time_string )
			prev = self.data[time_string]
			self.data[time_string] = self.update(prev, value)

	# returns a SleepPredictionTable object
	def get_result(self):
		return self.data


class ExponentialDecayMovingAverage(SleepPredictionAlgorithm):

	def __init__(self, interval=30):
		SleepPredictionAlgorithm.__init__(self)
		self.interval=interval

	def update(self, prev, value):
		return (( self.interval - 1 ) * prev + value ) / self.interval


import math
def sleep_changes(input_stream):
	for line in input_stream:
		line = line.rstrip("\n")
		portions = line.split(" ")
		state = util.SleepState[ portions[0] ]
		time = util.datetime_from_str( portions[1] )

		# floor to 5 minute increments
		minutes = math.floor((time.minute % 10) / 5) * 5
		minutes += (time.minute - time.minute % 10) # add back the 10s place

		time = datetime.datetime(time.year, time.month, time.day, time.hour, minutes)

		yield (state, time)

import sys

if __name__ == "__main__":

	algo = ExponentialDecayMovingAverage()

	last = None
	for state_change in sleep_changes( sys.stdin ):

		if last:
			algo.add_data( last, state_change )

		last = state_change

	data = algo.get_result()

	for data_point in util.time_iter_all():
		time = util.time_str_from_tuple( data_point )
		print( time + " " + str(data[time]) )
