ARG PYTHON_MAJOR_VERSION=3.10

###############################################################################################
######################################   BASE IMAGE   #########################################
###############################################################################################

FROM --platform=linux/amd64 python:$PYTHON_MAJOR_VERSION AS base

# System setup
ENV TZ="UTC"
ENV TERM=xterm

# Env vars
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

#git can be removed if is not planned to use Nextail libraries
RUN set -ex \
    && apt-get update \
    && apt-get install -y curl git gcc \
    && rm -rf /var/lib/apt/lists/*

# Avoid pdm installation though pip in order to avoid conflicts when installing packages globally
# Ref: https://github.com/pdm-project/pdm/issues/1388
ARG PDM_VERSION=2.8.2
RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/${PDM_VERSION}/install-pdm.py | python3 - --version=${PDM_VERSION} --path /usr/local

###############################################################################################
######################################   STAGE IMAGE   ########################################
###############################################################################################

FROM base AS stage

ARG PYTHON_MAJOR_VERSION

# set python env
ENV PYPACKAGES=/usr/python
RUN mkdir -p $PYPACKAGES
WORKDIR $PYPACKAGES

# copy PDM files
COPY ./pyproject.toml ./pdm.lock $PYPACKAGES/

# install dependencies
RUN pdm config python.use_venv false
RUN pdm install --prod --check --no-editable

# set python env
ENV PYTHONPATH=$PYPACKAGES/__pypackages__/$PYTHON_MAJOR_VERSION/lib
ENV PATH=$PYPACKAGES/__pypackages__/$PYTHON_MAJOR_VERSION/bin/:$PATH

# set dagster env & workdir
ENV DAGSTER_HOME=/opt/dagster
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME

###############################################################################################
####################################   SERVICE IMAGE     ######################################
###############################################################################################

FROM stage AS srv

# install dev dependencies
WORKDIR $PYPACKAGES
RUN pdm install --check -G dev

# copy dagster configuration file to dagster home
WORKDIR $DAGSTER_HOME
COPY ./docker/dagster/dagster.yaml ./docker/dagster/workspace.yaml $DAGSTER_HOME/
