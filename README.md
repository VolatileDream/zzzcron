zzzcron
=======

Like Cron, but based around your sleep schedule

## Architecture

zzzcron is built in multiple parts:

* the "machine learning" to determine when a user is probably awake (sleep_prob.py)
* the ~cron daemon to run commands based on the sleep probability (zzzcron.py)
* a mini wake/sleep log command line program (sleep-state.py)


