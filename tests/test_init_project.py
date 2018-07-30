#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from click.testing import CliRunner
import pytest
import pkgutil
import shutil
from kryptoflow.managers.constants import TEMPLATE_PROJECT_FILES
from kryptoflow.managers.project import ProjectManager
from kryptoflow.main import cli
from kryptoflow.cli.init import safe_init


__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "GNU GPL v2"


@pytest.fixture
def project_manager():
    p_manager = ProjectManager()
    return p_manager


def test_template_exists():
    for file in TEMPLATE_PROJECT_FILES:
        data = pkgutil.get_data('kryptoflow', file)
        assert data


def test_template_creation(project_manager):
    runner = CliRunner()
    result = runner.invoke(cli, ['init', '--path', 'tests', '--name', 'make-money'])
    for file in TEMPLATE_PROJECT_FILES:
        assert os.path.isfile(os.path.join('tests', file.replace('template', 'make-money')))
    shutil.rmtree('tests/make-money')


def test_template_overriding(monkeypatch):
    runner = CliRunner()
    result = runner.invoke(cli, ['init', '--path', 'tests', '--name', 'make-money'])
    result = runner.invoke(cli, ['init', '--path', 'tests', '--name', 'make-money'])
    monkeypatch.setattr('builtins.input', lambda x: 'Y')
    for file in TEMPLATE_PROJECT_FILES:
        assert os.path.isfile(os.path.join('tests', file.replace('template', 'make-money')))
    shutil.rmtree('tests/make-money')


def test_safe_init(monkeypatch):
    runner = CliRunner()
    runner.invoke(cli, ['init', '--path', 'tests', '--name', 'make-money'])
    monkeypatch.setattr('builtins.input', lambda x: 'n')
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        safe_init('tests/make-money')

    assert pytest_wrapped_e.type == SystemExit

    for file in TEMPLATE_PROJECT_FILES:
        assert os.path.isfile(os.path.join('tests', file.replace('template', 'make-money')))
    shutil.rmtree('tests/make-money')
