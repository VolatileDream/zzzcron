#!/usr/bin/env python3

# BNF of cronrc file:
# file		:= entries
# entries	:= '' | entry entries
# entry		:= time_exp '\n>' eval_exprs
# time_exp	:= time_rval | time_rval op time_val
# time_rval	:= 'start' | 'awake' | 'asleep' | 'waking_up' | 'falling_asleep'
# op		:= '+' | '-'
# time_val	:= [0-9]* 'h'
# eval_exprs	:= '' | eval_exp '\n' eval_exprs
# eval_expr	:= ...

import util

def load_stats():
	table = util.SleepPredictionTable()

	with open(conf['stats']['location']) as statFile:
		for line in statFile:
			time, probability = line.rstrip("\n").split(" ")
			table[time] = float(probability)
	return table

def load_cron():
	pass

if __name__ == "__main__":
	# do stuff

	conf = util.load_config()

	table = load_stats()

	
