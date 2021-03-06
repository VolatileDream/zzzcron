
from enum import Enum

class SleepState(Enum):
	asleep = 1
	waking_up = 2 # going from asleep to awake
	awake =  3
	falling_asleep = 4 # going from awake to asleep

import os

def require_file(file_path):
	if not os.path.isfile( file_path ):
		with open( file_path, "w" ) as f:
			pass


ZzzCronConfigDir = os.path.expanduser("~/.config/zzzcron.d/")
ZzzCronConfig = ZzzCronConfigDir + "config.ini"

import configparser

def load_config():

	if not os.path.exists(ZzzCronConfigDir):
		os.makedirs(ZzzCronConfigDir)

	if not os.path.isfile( ZzzCronConfig ):
		# create the config, and then save it
		config = configparser.ConfigParser()
		config['zzzcron'] = { 'awake_threshold' : 80,
					'sleep_threshold': 20,
					'location' : ZzzCronConfigDir + 'cron.rc' }
		config['stats'] = { 'day_interval' : 30,
					'location' : ZzzCronConfigDir + "stats",
					'algo' : "ExponentialDecayMovingAverage" }
		config['log'] = { 'location' : ZzzCronConfigDir + "sleep.log" }
		save_config(config)

	config = configparser.ConfigParser()
	config.read( ZzzCronConfig )
	return config

def save_config(config):

	if type(config) is not configparser.ConfigParser:
		raise TypeError("save_config expects configparser.ConfigParser")

	with open(ZzzCronConfig, 'w') as confFile:
		config.write(confFile)
	

import datetime

DateTimeFormat = "%Y-%m-%dT%H:%M"

import math

def floor_minutes(m):
	# floor to 5 minute increments
	minutes = math.floor((m % 10) / 5) * 5
	minutes += (m - m % 10)
	return minutes

def time_str_from_tuple(t):
    return "{:02d}:{:02d}".format(t[0], t[1])

def str_from_datetime(o):
	return o.strftime(DateTimeFormat);

def datetime_from_str(o):
	return datetime.datetime.strptime(o, DateTimeFormat);

def time_iter_all(offset=None):
	if not offset:
		offset = (0,0)
	for hours in range(0,24):
		for minutes in range(0,12):
			yield ( (hours+offset[0])%24, ((minutes * 5) + offset[1]) % 60)

def time_iter(start, end):

	"""iterates between the hour and minute values for 2 datetime objects
	or (hour,minute) pairs. Yields a tuple of (hour,minute), does not return
	a tuple for the end value."""

	if type(start) == datetime.datetime:
		start = (start.hour, start.minute)

	if type(end) == datetime.datetime:
		end = (end.hour, end.minute)

	hours, minutes = start
	end_h, end_m = end

	while hours != end_h or minutes != end_m:
		y_val = (hours,minutes)

		# do time wrapping
		minutes += 5
		if minutes == 60:
			minutes = 0
			hours += 1
			if hours == 24:
				hours = 0

		yield y_val


class SleepPredictionTable:
	def __init__(self):
		self.times = {}
		for hours in range(0,24):
			for minutes in range(0,12):
				self.times[ time_str_from_tuple((hours, minutes * 5,)) ] = 0.0

	def __getitem__(self, key):
		return self.times[key]

	def __setitem__(self, key, value):
		# Don't allow bad key setting
		if key not in self.times:
			raise KeyError( key )
		self.times[key] = value
		return self.times[key]

	def __iter__( self ):
		return self.times.__iter__()


def load_stats(conf):
	table = SleepPredictionTable()

	if not os.path.isfile( conf['stats']['location'] ):
		return table

	with open(conf['stats']['location']) as statFile:
		for line in statFile:
			time, probability = line.rstrip("\n").split(" ")
			table[time] = float(probability)
	return table


def load_cron_rc(conf):

	entries = []

	last_entry = None

	require_file( conf['zzzcron']['location'] )

	with open( conf['zzzcron']['location'] ) as cronFile:
		for line in cronFile:
			line = line.rstrip('\n')
			stripped_line = line.lstrip()

			if len(line) <= 0:
				continue

			if line == stripped_line:
				line = stripped_line.rstrip()
				if last_entry:
					entries.append( last_entry )
				state = line
				#state = SleepState[line]
				last_entry = {'time' : state,
						'commands' : [] }
			else:
				line = stripped_line.rstrip()
				last_entry['commands'].append( line )

	if last_entry is not None:
		entries.append( last_entry )

	return entries
