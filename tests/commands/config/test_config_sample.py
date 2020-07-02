import os
import re
import json
import pytest
import click

from pathlib import Path
from unittest import mock
from click.testing import CliRunner
from BALSAMIC.commands.base import cli


def test_dag_graph_success(tumor_normal_wgs_config, tumor_only_config,
                           tumor_normal_config, tumor_only_wgs_config):
    # WHEN creating config using standard CLI input
    # THEN DAG graph should be created successfully
    assert Path(json.load(
        open(tumor_normal_config))["analysis"]["dag"]).exists()
    assert Path(json.load(open(tumor_only_config))["analysis"]["dag"]).exists()
    assert Path(json.load(
        open(tumor_only_wgs_config))["analysis"]["dag"]).exists()
    assert Path(json.load(
        open(tumor_normal_wgs_config))["analysis"]["dag"]).exists()


def test_tumor_only_config_bad_filename(tmp_path_factory, analysis_dir,
                                        singularity_container):

    #GIVEN existing fastq file with wrong naming convention
    faulty_fastq_dir = tmp_path_factory.mktemp("error_fastq")
    Path(faulty_fastq_dir / "error.fastq.gz").touch()

    case_id = "faulty_tumor"
    tumor = Path(faulty_fastq_dir / "error.fastq.gz").as_posix()
    panel_bed_file = 'tests/test_data/references/panel/panel.bed'
    reference_json = 'tests/test_data/references/reference.json'

    # Invoke CLI command using file as argument
    runner = CliRunner()
    result = runner.invoke(cli, [
        'config',
        'case',
        '-t',
        tumor,
        "-p",
        panel_bed_file,
        '--case-id',
        case_id,
        '--analysis-dir',
        analysis_dir,
        '--singularity',
        singularity_container,
        '--reference-config',
        reference_json,
    ])

    # THEN run should abort
    assert result.exit_code == 1


def test_tumor_only_config_bad_reference(tmpdir_factory, sample_fastq,
                                         singularity_container, analysis_dir):
    # GIVEN CLI arguments including a bad reference config
    faulty_reference_json = 'tests/test_data/references/error_reference.json'
    Path(faulty_reference_json).touch()
    case_id = "sample_tumor_only"
    tumor = sample_fastq['tumor']
    panel_bed_file = 'tests/test_data/references/panel/panel.bed'
    reference_json = faulty_reference_json

    runner = CliRunner()
    result = runner.invoke(cli, [
        'config',
        'case',
        '-p',
        panel_bed_file,
        '-t',
        tumor,
        '--case-id',
        case_id,
        '--analysis-dir',
        analysis_dir,
        '--singularity',
        singularity_container,
        '--reference-config',
        reference_json,
    ])
    # THEN program exits before completion
    assert result.exit_code == 1
