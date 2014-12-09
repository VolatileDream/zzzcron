from .util import *

def state_lookup(conf, table, time ):

	time = ( time[0], floor_minutes(time[1]) )

	sleep_threshold = int(conf['zzzcron']['sleep_threshold'])
	awake_threshold = int(conf['zzzcron']['awake_threshold'])

	probability = table[ time_str_from_tuple( time ) ]

	if probability >= awake_threshold / 100.0 :
		return SleepState.awake
	elif probability <= sleep_threshold / 100.0:
		return SleepState.asleep
	else:
		# FIXME iterate to figure it out
		return SleepState.waking_up


import click

@click.command("cron")
@click.option("--edit", is_flag=True, help="Edit the cron.rc file")
def sleep_cron(edit):
	conf = load_config()

	if edit:
		cron_rc = conf['zzzcron']['location']
		import os
		os.spawnlp(os.P_WAIT, "sensible-editor", "sensible-editor", cron_rc)

	table = load_stats(conf)

	crons = load_cron_rc(conf)

	print(table)

