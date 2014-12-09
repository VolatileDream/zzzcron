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

Eats sleeps distribution data (24h in 5m increments), and spits out cron tab entries.

Invoked through zzzcron with `zzzcron cron [--update|--edit]`.

## zzzcron

Wrapper around all of the other commands and setup to be hooked into cron.

Invoked by cron with `zzzcron cron_hook <awake|asleep|waking_up|falling_asleep>`.

## extras

To get completion use `eval $(zzzcron completion <shell>)`

