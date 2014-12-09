from .util import *

import click

@click.command("cron_hook")
@click.argument("state")
def zzz_cron_hook(state):

	conf = load_config()

	crons = load_cron_rc(conf)

	match = None

	for entry in crons:
		if state == entry['time']:
			match = entry

	if match:
		for command in entry['commands']:
			print(command)
	else:
		# so that eval-ing our output will exit with non-zero status
		print("false")
