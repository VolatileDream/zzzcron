
_algorithm_set = { }

def GetAlgorithm(name):
	return _algorithm_set[ name ]

def SleepAlgorithm(clz):
	_algorithm_set [ clz.__name__ ] = clz
	return clz


import util


class SleepPredictionAlgorithm:

	def __init__(self):
		self.data = util.SleepPredictionTable()

	def update(self, time_string, prev, value):
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
			prev = self.data[time_string]
			self.data[time_string] = self.update(time_string, prev, value)

	# returns a SleepPredictionTable object
	def get_result(self):
		return self.data


@SleepAlgorithm
class ExponentialDecayMovingAverage(SleepPredictionAlgorithm):

	def __init__(self, **kwargs):
		SleepPredictionAlgorithm.__init__(self)
		self.interval=int(kwargs['day_interval'])

	def update(self, _time_string, prev, value):
		return (( self.interval - 1 ) * prev + value ) / self.interval


@SleepAlgorithm
class CumulativeMovingAverage(SleepPredictionAlgorithm):

	def __init__(self, **kwargs):
		SleepPredictionAlgorithm.__init__(self)
		self.counts = util.SleepPredictionTable()

	def update(self, time, prev, value):
		self.counts[time] += 1
		return ( self.counts[time] * prev + value ) / ( self.counts[time] + 1 )

