#!/usr/bin/env python3

import util
import argparse
def usage():
	print("Usage: [zzz|awake]")
	print("    creates an entry in the sleep log for a user")
	print("    can only be invoked using symbolic links")


import datetime

def sleep_entry(state, date=None):

	if state is not util.SleepState.asleep and state is not util.SleepState.awake:
		raise "Bad SleepState: " + state

	if date is None:
		date = datetime.datetime.now()

	config = util.load_config()

	with open(config['log']['location'], "a") as logFile:
		logFile.write( state.name + " " + util.str_from_datetime(date) + "\n" );


import sys

if __name__ == "__main__":

	path = sys.argv[0].split("/")

	if path[-1] == "zzz":
		sleep_entry( util.SleepState.asleep );
	elif path[-1] == "awake":
		sleep_entry( util.SleepState.awake );
	else:
		usage()


