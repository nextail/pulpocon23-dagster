MAKEFLAGS += --warn-undefined-variables

# Shell to use for running scripts
SHELL := $(shell which bash)
# Get current path
MKFILE_PATH := $(patsubst %/, %, $(dir $(realpath $(lastword $(MAKEFILE_LIST)))))
# Export local user & group
UNAME := $(shell id -un)
UID := $(shell id -u)
GID := $(shell id -g)
GNAME:= $(shell id -gn)

# Get docker path or an empty string
DOCKER := $(shell command -v docker)
# Get docker-compose path or an empty string
DOCKER_COMPOSE := $(shell command -v docker-compose)
ifndef DOCKER_COMPOSE
	DOCKER_COMPOSE := ${DOCKER} compose
endif

# Env var to interact with Github
COMPUTED_GITHUB_TOKEN := $(GITHUB_PIP_TOKEN)
ifeq (${COMPUTED_GITHUB_TOKEN}, )
	COMPUTED_GITHUB_TOKEN := $(GITHUB_TOKEN)
endif

# Setup msg colors
NOFORMAT := \033[0m
RED := \033[0;31m
GREEN := \033[0;32m
ORANGE := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
YELLOW := \033[1;33m

## help              : show this help
help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

## deps              : test if the dependencies we need to run this Makefile are installed
deps:
ifndef DOCKER
	@echo -e "${RED}Docker is not available${NOFORMAT}. Please install docker"
	@exit 1
endif

## start-dev         : start the docker environment in background
start-dev: deps

	@cd ${MKFILE_PATH}/docker \
	&& DOCKER_BUILDKIT=1 \
	${DOCKER_COMPOSE} up --build -d

## start-dev-nocache : start the docker environment in background without cache on build
start-dev-nocache: deps
	@cd ${MKFILE_PATH}/docker \
	&& ${DOCKER_COMPOSE} build --no-cache \
	&& ${DOCKER_COMPOSE} up -d

## stop-dev          : stop the the docker environment in background
stop-dev: deps
	@cd ${MKFILE_PATH}/docker \
	&& ${DOCKER_COMPOSE} down

## clean	    	: clean all the created containers
clean: deps
	@${DOCKER_COMPOSE} --project-directory docker down --rmi local \
	&& bash scripts/clean-env.sh

## clean-full 	: clean all the created containers and their data
clean-full: deps
	@${DOCKER_COMPOSE} --project-directory docker down --rmi local -v \
	&& bash scripts/clean-env.sh
