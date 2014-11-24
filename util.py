
from enum import Enum

class SleepState(Enum):
	asleep = 1
	waking_up = 2 # going from asleep to awake
	awake =  3
	falling_asleep = 4 # going from awake to asleep

import os

ZzzCronConfigDir = os.path.expanduser("~/.zzzcron.d/")
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
	return str(t[0]) + ":" + str(t[1])

def str_from_datetime(o):
	return o.strftime(DateTimeFormat);

def datetime_from_str(o):
	return datetime.datetime.strptime(o, DateTimeFormat);

def time_iter_all():
	for hours in range(0,24):
		for minutes in range(0,12):
			yield (hours, minutes * 5)

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
				self.times[ str(hours) + ":" + str(minutes * 5) ] = 0.0

	def __getitem__(self, key):
		return self.times[key]

	def __setitem__(self, key, value):
		if key in self.times:
			self.times[key] = value
		return self.times[key]

	def __iter__( self ):
		return self.times.__iter__()

