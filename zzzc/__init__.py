__all__ = ["sleep_stats", "sleep_state", "sleep_cron"]

from .util import *
from .algorithms import *
from .sleep_stats import update_stats
from .sleep_state import sleep_state
from .sleep_cron import sleep_cron
from .sleep_cron_hook import zzz_cron_hook

import click

@click.group()
def zzzc():
	pass

zzzc.add_command( update_stats )
zzzc.add_command( sleep_state )
zzzc.add_command( sleep_cron )
zzzc.add_command( zzz_cron_hook )

