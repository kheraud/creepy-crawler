ifndef VERBOSE
	MAKEFLAGS += --no-print-directory
endif

default:

####################### Refresh #######################

refresh_pipenv: .out_docker .configure
	@cd build/dev && docker-compose exec py-api pipenv install --system

refresh_npm: .out_docker .configure
	@cd build/dev && docker-compose exec js-front npm install

crawl_md_url: .out_docker .configure
	@cd build/dev && docker-compose exec py-api python creep-crawl.py $(CRAWL_URL)

####################### Docker init #######################

.out_docker:
# @todo check docker version
# @todo check docker-compose version
ifeq (, $(shell which docker))
	$(error "You must run this command outside the docker container")
endif

.configure: .out_docker
	$(shell build/dev/configure.sh)

.init_database: .out_docker
	@touch databases/app.db

reset_configuration: .out_docker
	rm -f build/dev/.env

create: .out_docker .configure .init_database
	@cd build/dev && docker-compose build --pull --parallel --quiet
	@make .up
	@echo "Environment is up, start coding and follow runs with 'make log_all'"

remove: .out_docker
	@cd build/dev && docker-compose down --remove-orphans --volumes

.up: .out_docker .init_database
	@cd build/dev && docker-compose up \
	    --detach \
	    --remove-orphans \
	    --quiet-pull;

start: .out_docker .up

stop: .out_docker
	@cd build/dev && docker-compose stop

restart: stop start

####################### Docker mgt #######################
ps: .out_docker
	@cd build/dev && docker-compose ps

shell: shell_api

shell_api: .out_docker
	@cd build/dev && docker-compose exec py-api /bin/bash

shell_front: .out_docker
	@cd build/dev && docker-compose exec js-front /bin/bash

####################### Docker logs #######################
.log: .out_docker
	@cd build/dev && docker-compose logs --follow --tail=50 $([ "$timestamp" == true ] && echo "--timestamps" || echo "") $(service)

log_api:
	@make .log service="py-api" timestamp=false

log_front:
	@make .log service="js-front" timestamp=false

log_all:
	@make .log service="" timestamp=false

