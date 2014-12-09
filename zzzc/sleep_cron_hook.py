from .util import *

import click

@click.command("cron_hook")
@click.argument("state")
def zzz_cron_hook(state):

	conf = load_config()

	crons = load_cron_rc(conf)

	match = None

	#print("# running through:", state, type(state))

	for entry in crons:
		#print("# checking:", entry['time'], type(entry['time']) )
		if state == entry['time']:
			#print("# match")
			match = entry

	if match:
		for command in match['commands']:
			print(command)
	else:
		# so that eval-ing our output will exit with non-zero status
		print("false")
