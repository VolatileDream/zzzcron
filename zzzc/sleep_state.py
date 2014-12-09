from .util import *
import datetime

def sleep_entry(state, date=None):

	if state is not SleepState.asleep and state is not SleepState.awake:
		raise "Bad SleepState: " + state

	if date is None:
		date = datetime.datetime.now()

	config = load_config()

	with open(config['log']['location'], "a") as logFile:
		logFile.write( state.name + " " + str_from_datetime(date) + "\n" );


import click

@click.command("state")
@click.option("--asleep", "-z", is_flag=True, help="currently asleep")
@click.option("--awake", "-w", is_flag=True, help="currently awake")
def sleep_state(asleep, awake):

	if asleep:
		sleep_entry( SleepState.asleep )
	elif awake:
		sleep_entry( SleepState.awake )
	else:
		raise click.UsageError("must specify one of --asleep or --awake")

	with open( load_config()['log']['location'] ) as logFile:
		from .sleep_stats import update_sleep_probability
		update_sleep_probability(logFile)

	return

