#!/bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
find ${SCRIPTPATH}/.. -name '*.egg-info' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '*.egg' -exec rm -f {} +
find ${SCRIPTPATH}/.. -name '*.pyc' -exec rm -f {} +
find ${SCRIPTPATH}/.. -name '*.pyo' -exec rm -f {} +
find ${SCRIPTPATH}/.. -name '*~' -exec rm -f {} +
find ${SCRIPTPATH}/.. -name '__pycache__' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '__pypackages__' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '.pdm.toml' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '.pdm-python' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '.pdm-build' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '.venv' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '.pytest_cache' -exec rm -fr {} +
find ${SCRIPTPATH}/.. -name '.ruff_cache' -exec rm -fr {} +
