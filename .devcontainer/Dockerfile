FROM python:3.10-bullseye

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install git vim nano make curl gcc libssl-dev g++ pre-commit unzip \
    apt-transport-https ca-certificates curl gnupg2 lsb-release socat htop wget

# install PDM
# Avoid pdm installation though pip in order to avoid conflicts when installing packages globally
# Ref: https://github.com/pdm-project/pdm/issues/1388
ARG PDM_VERSION=2.9.1
RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/${PDM_VERSION}/install-pdm.py | python3 - --version=${PDM_VERSION} --path /usr/local

# set python env
ENV PYPACKAGES=/usr/python
RUN mkdir -p $PYPACKAGES
WORKDIR $PYPACKAGES

# copy PDM files
COPY ./pyproject.toml ./pdm.lock $PYPACKAGES/

# install dependencies and project into the local packages directory
RUN pdm config python.use_venv false
RUN mkdir __pypackages__ && pdm sync --no-editable

# set python  env
ENV PYTHONPATH=$PYPACKAGES/__pypackages__/3.10/lib
ENV PATH=$PYPACKAGES/__pypackages__/3.10/bin/:$PATH

# utilities
# add docker bash completion
ADD https://raw.githubusercontent.com/docker/docker-ce/master/components/cli/contrib/completion/bash/docker /usr/share/bash-completion/completions/docker
RUN chmod 644 /usr/share/bash-completion/completions/docker

# Clean up apt
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
