#
#

all: run

## Build local images | Dev
django_shell:
	docker-compose -f local.yml build

## Runs django shell | Dev
django_shell:
	docker-compose -f local.yml run --rm django /bin/bash

## Runs application | Common
run:
	docker-compose -f local.yml up

## Test | Dev
test:
	docker-compose -f local.yml run --rm django pytest
