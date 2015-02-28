zzzcron
=======

Like Cron, but based around your sleep schedule

## Architecture

zzzcron is built in multiple parts:

* a mini wake/sleep log command line program (state)
* the "machine learning" to determine when a user is probably awake (stats)
* a tool that analyzes the awake-distribution to generate transition times and associated cron entries (cron)
* the cron hook to run commands on state transition (cron_hook)

All parts use the `~/.config/zzzcron.d/config.ini` configuration file, and possibly other files which are in `~/.config/zzzcron.d/` by default.

Each command takes the `--help` option for more information.

## state

Minimal command line sleep tracking program.

Invoked through zzzcron with `zzzcron state --awake|--asleep`.

See `zzzc/sleep_state.py` for implementation.

## Stats

Crunches configuration and sleep log data, turning it into a 24h sleep probability distribution in 5-minute windows.

Invoked through zzzcron with `zzzcron stats [--input file] [--update [--out]]`.

See `zzzc/sleep_stats.py` for implementation, `zzzc/algorithms.py` contains all algorithms that are used to calculate sleep state probability. The algorithm that is used by zzzcron can be changed by editing `[config].stats.algo`.

## cron

Eats sleeps distribution data (24h in 5m increments), and spits out cron tab entries. This workes by
invoking the parser code in zparser.py, and evaluating the expressions left in the cron.rc file.

This spits out eval nested cron entries, because it is easier to use eval over spawning a subshell to execute all of the commands.

Expressions have the usual math syntax ( expr op expr ) and the following four variables are exposed: 

| Variable         | Represents  |
|:----------------:|:------------|
| `waking_up`      | The beginning of the time in which the user transitions from most likely asleep to most likely awake. |
| `awake`          | The end of the time in which the user transitions from most likely asleep to most likely awake.       |
| `falling_asleep` | The beginning of the time in which the user transitions from most likely awake to most likely asleep. |
| `asleep`         | The end of the time in which the user transitions from most likely awake to most likely asleep.       |

Important notes:
* Variables may have more than a single value (in the case of multi-phase sleep schedules), this causes zzzcron to evaluate the expression for all values of the variable and output them.
* If two variables are in an expression and they both have multiple values, zzzcron will print out all possible evaluations of the expression.
 * ex: `(awake+asleep)/2` will produce 4 entries for a two phase sleep cycle.
* zzzcron does **not** edit your cron tab, you have to copy entries into it. This makes it easier for

Invoked through zzzcron with `zzzcron cron [--edit]`.

See `zzzc/sleep_cron.py` for implementation, `zzzc/zparser.py` for expression grammar, parser, and evaluator.

## cron_hook

Invoked by cron to signal specific transitions changes, used as `zzzcron cron_hook expr`, where expr is an entry in the cron.rc file.

This reads in the cron.rc file, and prints any expression that matches the `expr` value passed in by cron.

See `zzzc/sleep_cron_hook.py` for implementation.

## Configuration

zzzcron has a few configuration options, by default they are as follows:

|        Setting          | Significance |
|:-----------------------:|:-------------|
| zzzcron.sleep_threshold | The probability under which the user is assumed to be asleep. |
| zzzcron.awake_threshold | The probability above which the user is assumed to be awake.  |
| zzzcron.location        | Location of the cron.rc file.  |
| stats.algo              | The algorithm in `zzzc/algorithms.py` that is used to calculate the users probability of being awake.  |
| stats.location          | The location to store the calculated sleep statistics in.     |
| log.location            | The location that the sleep state log is stored ( a record of the user being awake or asleep ). |

Note that every value under `stats` is passed to the statistical algorithm chosen, this allows algorithms to require multiple settings.

# Algorithms

Two algorithms are currently implemented in zzzcron:
* Cumulative Moving Average
* Exponential Decay Moving Average
 * Takes a decay interval setting ( `day_interval` )

