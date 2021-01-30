ifndef VERBOSE
	MAKEFLAGS += --no-print-directory
endif

.PHONY: default .configure reset_configuration destroy start stop  \
	restart shell_api shell_front crawl_md_url build_for_prod ps log

default:

################################
### Configuration management ###
################################
.configure:
	$(shell build/configure.sh)

reset_configuration:
	rm -f build/.env

##############################
### Environment management ###
##############################
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

destroy:
	@cd build && docker-compose down --remove-orphans --volumes
	@echo "\e[1;33mEnvironment destroyed\e[0m"

start: .configure
# Launch all services but no coding env, this service
# have to be explicity started with make shell_xxx
	@cd build && docker-compose up \
		--build \
	    --detach \
	    --remove-orphans \
	    --quiet-pull \
	    --scale py-api=0 --scale js-front=0
	@echo "\e[1;33mEnvironment is up, start coding with 'make shell_api or make shell_front'\e[0m"

stop:
	@cd build && docker-compose stop

restart: stop start

shell_api:
	@cd build && docker-compose run --service-ports --rm \
		py-api bash -c "pipenv install --dev && pipenv shell"

shell_front:
# In order to have a script run at start of bash we create
# a temporary file and relocate it in front directory
# https://stackoverflow.com/a/18756584/595223
	@TMPFILE=$(mktemp)
	@echo "npm install" > $TMPFILE
	@echo ". ~/.bashrc" >> $TMPFILE
	@echo "rm -f /var/www/html/$TMPFILE" >> $TMPFILE
	@mv $TMPFILE front/
	@cd build && docker-compose run --service-ports --rm \
		js-front bash --rcfile /var/www/html/$TMPFILE

#######################
### Util management ###
#######################
crawl_md_url: .configure
	@cd build && docker-compose exec py-api python creep-crawl.py $(CRAWL_URL)

build_for_prod:
	@docker build -f build/Dockerfile --target py-production --tag $(DOCKER_IMG_TAG) .

######################
### Log management ###
######################
ps:
	@cd build && docker-compose ps

log:
	@cd build && docker-compose logs --follow --tail=50 \
		$([ "$timestamp" == true ] && echo "--timestamps" || echo "") $(service)
