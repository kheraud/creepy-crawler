ifndef VERBOSE
	MAKEFLAGS += --no-print-directory
endif

default:

####################### Migrate #######################
migrate_db: .out_docker
	@cd build/dev && docker-compose run --rm py-back make .migrate_db

.migrate_db: .refresh_pipenv
	@echo -e "\e[1;33mLaunching database migration scripts\e[0m"
	@python manager.py db upgrade 

.refresh_pipenv:
	@pipenv install --system --deploy

####################### Docker init #######################
ifndef enable_app
override enable_app = 1
endif

.out_docker:
# @todo check docker version
# @todo check docker-compose version
ifeq (, $(shell which docker))
	$(error "You must run this command outside the docker container")
endif

.configure: .out_docker
	$(shell build/dev/configure.sh)

reset_configuration: .out_docker
	rm -f build/dev/.env

create: .out_docker .configure
	@cd build/dev && docker-compose build --pull --parallel --quiet
	@make .up enable_app=0
	@cd build/dev && docker-compose run --rm py-back make .waiting_for_dependency
	@make migrate_db
	@make .up
	@echo "Environment is up, start coding and follow runs with 'make log_app'"

remove: .out_docker
	@cd build/dev && docker-compose down --remove-orphans --volumes

.up: .out_docker
	@cd build/dev && docker-compose up \
	    --detach \
	    --remove-orphans \
	    --quiet-pull \
	    --scale py-back=$(enable_app)

.waiting_for_dependency:
	@make .waiting_for service=postgres port=5432 timeout=30

.waiting_for:
	@echo -e "\e[1;33mWaiting for $(service) is Ready\e[0m"
	@/bin/sh -c 'for i in `seq 1 $(timeout)`;do nc $(service) $(port) -w 1 -z && exit 0;sleep 1;done;exit 1'
	@echo -e "\e[1;32m$(service) is ready\e[0m"

start: .out_docker .up

stop: .out_docker
	@cd build/dev && docker-compose stop

restart: stop start

####################### Docker mgt #######################
ps: .out_docker
	@cd build/dev && docker-compose ps

shell: .out_docker
	@cd build/dev && docker-compose exec py-back /bin/bash

####################### Docker logs #######################
log: .out_docker
	@cd build/dev && docker-compose logs --follow --tail=50 $([ "$timestamp" == true ] && echo "--timestamps" || echo "") $(service)

log_app:
	@make log service="py-back" timestamp=false
