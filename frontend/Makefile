### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

VOLTO_VERSION=$$(cat version.txt)

# Docker Image
IMAGE_NAME=ghcr.io/collective/plone-intranet-frontend
IMAGE_TAG=latest

ifndef CI
	CONFIG_SUFFIX=""
else
	CONFIG_SUFFIX=--https
endif

ifndef NOCACHE
	NOCACHE_SUFFIX=
else
	NOCACHE_SUFFIX=--no-cache
endif

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: config
config:  ## Prepare jsconfig and checkout packages
	@npx -p mrs-developer missdev --config=jsconfig.json --output=addons $(CONFIG_SUFFIX)

.PHONY: build-image
build-image:  config ## Build Docker Image
	@docker buildx build . -t $(IMAGE_NAME):$(IMAGE_TAG) -f dockerfiles/Dockerfile ${NOCACHE_SUFFIX} --build-arg VOLTO_VERSION=$(VOLTO_VERSION)
