#!/usr/bin/env python3

import util
import datetime

import math
def sleep_changes(input_stream):
	for line in input_stream:
		if len(line) <= 0:
			continue

		line = line.rstrip("\n")
		portions = line.split(" ")
		state = util.SleepState[ portions[0] ]
		time = util.datetime_from_str( portions[1] )

		minutes = util.floor_minutes( time.minute )

		time = datetime.datetime(time.year, time.month, time.day, time.hour, minutes)

		yield (state, time)

import sys
import algorithms

def update_sleep_probability(input_stream, output_stream=None):

	config = util.load_config()['stats']

	if not output_stream:
		output_stream = open(config['location'], "w")

	algo_class = algorithms.GetAlgorithm(config['algo'])
	algo = algo_class( **config )

	last = None
	for state_change in sleep_changes( input_stream ):

		if last:
			algo.add_data( last, state_change )

		last = state_change

	data = algo.get_result()

	for data_point in util.time_iter_all():
		time = util.time_str_from_tuple( data_point )
		output_stream.write( time + " " + str(data[time]) + "\n" )

	output_stream.close()

if __name__ == "__main__":
	if len(sys.argv) > 1:
		log = sys.argv[1]
	else:
		conf = util.load_config()
		log = conf['log']['location']

	with open( log ) as logFile:
		update_sleep_probability( logFile, sys.stdout )

