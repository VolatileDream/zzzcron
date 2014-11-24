
import util

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
		self.interval=int(interval)

	def update(self, prev, value):
		return (( self.interval - 1 ) * prev + value ) / self.interval

_algorithm_set = { ExponentialDecayMovingAverage.__name__ : ExponentialDecayMovingAverage }

def GetAlgorithm(name):
	return _algorithm_set[ name ]
