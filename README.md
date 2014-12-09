zzzcron
=======

Like Cron, but based around your sleep schedule

## Architecture

zzzcron is built in multiple parts:

* a mini wake/sleep log command line program (sleep_state.py)
* the "machine learning" to determine when a user is probably awake (sleep_prob.py)
* a tool that analyzes the awake-distribution to generate transition times and associated cron entries (sleep_cron.py)
* the cron hook to run commands on state transition (zzzcron <awake|asleep|waking_up|falling_asleep>)

All parts use the `~/.zzzcron.d/config.ini` configuration file, and possibly other files which are in `~/.zzzcron.d/` by default.

## sleep_state.py

Minimal command line sleep tracking program.

Invoked through zzzcron with `zzzcron state --awake|--asleep`.

## sleep_prob.py 

Crunches configuration and sleep log data, turning it into a 24h sleep probability distribution in 5-minute windows.

Invoked through zzzcron with `zzzcron stats [--input file] [--update]`.

## sleep_cron.py

Eats sleeps distribution data (24h in 5m increments), and spits out cron tab entries. This workes by
invoking the parser code in zparser.py, and evaluating the expressions left in the cron.rc file.

This spits out eval nested cron entries, because it is easier to use eval over spawning a subshell to execute all of the commands.

Invoked through zzzcron with `zzzcron cron [--edit]`.

## sleep_cron_hook.py

Invoked by cron to signal specific transitions changes, used as `zzzcron cron_hook expr`, where expr is
an entry in the cron.rc file.

This reads in the cron.rc file, and prints any expression that matches the `expr` value passed in by cron.


