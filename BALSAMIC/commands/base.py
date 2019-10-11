"""
Entry cli for balsamic
"""
import logging
import click
import coloredlogs

# Subcommands
from BALSAMIC.commands.run.base import run as run_command
from BALSAMIC.commands.config.base import config as config_command
from BALSAMIC.commands.plugins.base import plugins as plugins_command

# CLI commands and decorators
from BALSAMIC.utils.cli import add_doc as doc

# Get version
from BALSAMIC import __version__

LOG = logging.getLogger(__name__)
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


@click.group()
@click.option('--loglevel',
              default='DEBUG',
              type=click.Choice(LOG_LEVELS),
              help="Set the level of log output.",
              show_default=True)
@click.version_option(version=__version__)
@click.pass_context
@doc("""BALSAMIC {version}: Bioinformatic Analysis pipeLine for
        SomAtic MutatIons in Cancer""".format(version=__version__))
def cli(context, loglevel):
    "BALSAMIC"
    coloredlogs.install(
        level=loglevel,
        fmt='[%(hostname)s] %(asctime)s %(levelname)s %(message)s')
    context.obj = {}
    context.obj['loglevel'] = loglevel
    # LOG.info(f"BALSAMIC started with log level {loglevel}.")


cli.add_command(run_command)
cli.add_command(config_command)
cli.add_command(plugins_command)
