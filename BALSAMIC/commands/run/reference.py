#! /usr/bin/env python

import json
import subprocess
import click

from BALSAMIC.utils.cli import get_sbatchpy
from BALSAMIC.utils.cli import get_snakefile, SnakeMake, get_config


@click.command('reference', short_help="Run the GenerateRef workflow")
@click.option('-s', "--snakefile", default=get_snakefile('generate_ref'),
              help="snakefile for reference generation")
@click.option('-c', '--configfile', required=True, help="Config file to run the workflow")
@click.option('--run-mode', default='local', type=click.Choice(["slurm", "local"]),
              help="Run mode to use.(LOCAL, SLURM for HPC)")
@click.option('--cluster-config', show_default=True, default=get_config('cluster'),
              type=click.Path(), help='SLURM config json file.')
@click.option('-l', '--log-file', type=click.Path(),
              help='Log file output for BALSAMIC. This is raw log output from snakemake.')
@click.option('-r', '--run-analysis', show_default=True, default=False, is_flag=True,
              help='By default balsamic run_analysis will run in dry run mode. \
              Raise thise flag to make the actual analysis')
@click.option('--qos', type=click.Choice(['low', 'normal', 'high']), show_default=True,
              default="low", help='QOS for sbatch jobs. Passed to ' + get_sbatchpy())
@click.option('-f', '--force-all', show_default=True, default=False, is_flag=True,
              help='Force run all analysis. This is same as snakemake --forceall')
@click.option('--snakemake-opt', multiple=True, help='Pass these options directly to snakemake')
@click.pass_context
def reference(context, snakefile, configfile, run_mode, cluster_config, log_file, run_analysis, qos,
              force_all, snakemake_opt):
    """ Run generate reference workflow """
    click.echo("Reference generation workflow started")

    with open(configfile, "r") as config_fh:
        config = json.load(config_fh)

    # Construct snakemake command to run workflow
    balsamic_run = SnakeMake()
    balsamic_run.working_dir = config['output']
    balsamic_run.snakefile = snakefile
    balsamic_run.configfile = configfile
    balsamic_run.run_mode = run_mode
    balsamic_run.forceall = force_all
    balsamic_run.run_analysis = run_analysis
    balsamic_run.sm_opt = snakemake_opt
    # balsamic_run.cluster_config = cluster_config
    # balsamic_run.sbatch_py = get_sbatchpy()
    # balsamic_run.log_path = logpath
    # balsamic_run.script_path = scriptpath
    # balsamic_run.result_path = resultpath
    # balsamic_run.qos = qos

    subprocess.run(balsamic_run.build_cmd(), shell=True)