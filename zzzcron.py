#!/usr/bin/env python3


import util

def load_stats(conf):
	table = util.SleepPredictionTable()

	with open(conf['stats']['location']) as statFile:
		for line in statFile:
			time, probability = line.rstrip("\n").split(" ")
			table[time] = float(probability)
	return table


def load_cron(conf):
	
	entries = []

	last_entry = None

	with open( conf['zzzcron']['location'] ) as cronFile:
		for line in cronFile:
			line = line.rstrip('\n')
			line = line.lstrip(' ').rstrip(' ')

			if len(line) <= 0:
				continue

			if line.find(">") is not 0:
				if last_entry:
					entries.append( last_entry )
				state = util.SleepState[line]
				last_entry = {'time' : state,
						'commands' : [] }
			else:
				line = line.lstrip(">")
				line = line.lstrip(' ').rstrip(' ')
				last_entry['commands'].append( line )

	if last_entry is not None:
		entries.append( last_entry )

	return entries


def now():
	now = datetime.datetime.now()
	return ( now.hour, now.minute )
	

def state_lookup(conf, table, time ):

	time = ( time[0], util.floor_minutes(time[1]) )

	sleep_threshold = int(conf['zzzcron']['sleep_threshold'])
	awake_threshold = int(conf['zzzcron']['awake_threshold'])

	probability = table[ util.time_str_from_tuple( time ) ]

	if probability >= awake_threshold / 100.0 :
		return util.SleepState.awake
	elif probability <= sleep_threshold / 100.0:
		return util.SleepState.asleep
	else:
		# FIXME iterate to figure it out
		return util.SleepState.waking_up
		

def run_commands( commands ):
	for c in commands:
		# FIXME this should run the command
		print(c)


import datetime
import time

def run(conf, table, crons):

	state = state_lookup( conf, table, now() )

	while True:
		time_now = now()

		new_state = state_lookup( conf, table, time_now )

		if new_state != state:
			# do the thing
			for c in crons:
				if c['time'] == new_state:
					run_commands( c['commands'] )

		state = new_state
		print("state: " + state.name )

		time.sleep(5)


if __name__ == "__main__":
	# do stuff

	conf = util.load_config()

	table = load_stats(conf)

	crons = load_cron(conf)

	print("Cron RC:")
	for c in crons:
		print( c['time'] )
		print( c['commands'] )

	print()
	print()

	run(conf, table, crons)

# signal stuff:
# https://docs.python.org/2/library/signal.html
