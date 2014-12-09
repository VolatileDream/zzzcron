from .util import *

def state_lookup(conf, table):

	sleep_threshold = int(conf['zzzcron']['sleep_threshold'])
	awake_threshold = int(conf['zzzcron']['awake_threshold'])

	def _state_lookup( time ):

		time = ( time[0], floor_minutes(time[1]) )

		probability = table[ time_str_from_tuple( time ) ]

		if probability >= awake_threshold / 100.0 :
			return SleepState.awake
		elif probability <= sleep_threshold / 100.0:
			return SleepState.asleep
		else:
			return SleepState.waking_up

	return _state_lookup


def transition_times(conf, stats_table):

	state_check = state_lookup(conf, stats_table)

	states = SleepPredictionTable()

	last_states = { SleepState.awake : None, SleepState.asleep : None }

	for time in time_iter_all():
		state = state_check( time )
		states[ time_str_from_tuple( time ) ] = state
		last_states[ state ] = time

	iter_restart = None

	if last_states[ SleepState.awake ] is not None:
		iter_restart = last_states[ SleepState.awake ]
	if last_states[ SleepState.asleep ] is not None:
		iter_restart = last_states[ SleepState.asleep ]

	if not iter_restart:
		raise Error("No discernable awake/sleep transition");

	next_state = { SleepState.awake : SleepState.falling_asleep, SleepState.asleep : SleepState.waking_up }

	state_transitions = []

	last_state = states[ time_str_from_tuple( iter_restart ) ]
	last_state_time = iter_restart

	for time in time_iter_all( iter_restart ):
		state = states[ time_str_from_tuple( time ) ]
		if state not in [ SleepState.awake, SleepState.asleep ]:
			states[ time_str_from_tuple( time ) ] = next_state[ last_state ]
		else:
			if last_state is not state:
				# transitioning from awake -> asleep, or asleep -> awake
				# mark the current time as being the change
				state_transitions.append( (last_state_time, last_state, time, state) )
			last_state = state
			last_state_time = time

	return state_transitions


def transform_transitions_to_states(state_transitions, modifier=None):
	
	prev_state = { SleepState.awake : SleepState.falling_asleep, SleepState.asleep : SleepState.waking_up }

	state_changes = { SleepState.awake : [], SleepState.waking_up : [], SleepState.asleep : [], SleepState.falling_asleep : [] }

	for trans in state_transitions:
		start_time, start_state, end_time, end_state = trans
		if modifier:
			start_time = modifier(start_time)
			end_time = modifier(end_time)
		# if we started as awake, this transition is a falling asleep period
		state_changes[ prev_state[ start_state ] ].append( start_time )
		state_changes[ end_state ].append( end_time )

	return state_changes

from .zparser import get_parser
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

	transitions = transition_times( conf, table )
	#print(transitions)
	#print()

	# generate times in minutes, because the parser expects them that way
	time_table = transform_transitions_to_states(transitions, lambda x: x[0]*60 + x[1])

	#for t in time_table:
	#	print(t)
	#	print(time_table[t])
	#	print()

	grammar, parser = get_parser(time_table)

	for entry in crons:
		time_expr = entry['time']
		#print( "time parse:", time_expr )
		tree = grammar.parse( time_expr )
		times_occuring = parser.transform(tree)
		#print( times_occuring )
		for time in times_occuring:
			hours = time // 60
			minutes = time % 60
			print(minutes, hours, "*", "*", "*", 'eval "`zzzcron cron_hook "%s"`"' % time_expr )

