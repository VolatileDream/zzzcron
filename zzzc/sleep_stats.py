from .util import *
import datetime

import math
def sleep_changes(input_stream):
	for line in input_stream:
		if len(line) <= 0:
			continue

		line = line.rstrip("\n")
		portions = line.split(" ")
		state = SleepState[ portions[0] ]
		time = datetime_from_str( portions[1] )

		minutes = floor_minutes( time.minute )

		time = datetime.datetime(time.year, time.month, time.day, time.hour, minutes)

		yield (state, time)

from .algorithms import *

def update_sleep_probability(input_stream, output_stream=None):

	config = load_config()['stats']

	if not output_stream:
		output_stream = open(config['location'], "w")

	algo_class = GetAlgorithm(config['algo'])
	algo = algo_class( **config )

	last = None
	for state_change in sleep_changes( input_stream ):

		if last:
			algo.add_data( last, state_change )

		last = state_change

	data = algo.get_result()

	for data_point in time_iter_all():
		time = time_str_from_tuple( data_point )
		output_stream.write( time + " " + str(data[time]) + "\n" )

	output_stream.close()


import click

@click.command("stats")
@click.option("--input", "--i", default=None, help="input file, defaults to [config].log.location")
@click.option("--update", "--u", is_flag=True, help="manually update the zzzcron sleep statistics")
@click.option("--out", "--o", is_flag=True, help="output stats to stdout. this is only required with --update")
def update_stats(input, update, out):

	conf = load_config()

	if input:
		log = input
	else:
		log = conf['log']['location']

	with open( log ) as logFile:

		if update:
			update_sleep_probability( logFile )

	# unless the user wanted to update the stats, just print them out
	if (update and out) or not update:
		import sys
		with open(conf['stats']['location']) as stats_file:
			for line in stats_file:
				sys.stdout.write(line)

