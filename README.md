# Creepy-crawler

This tool permits to manage bookmark lists of github repositories

I started this project in order to test [Awesome tools](https://github.com/topics/awesome) in a systematic way

## Requirements

- A [github personal token](https://github.com/settings/tokens) with at least `repo.public_repo` permission
- [Make](https://www.gnu.org/software/make/)
- [Docker](https://www.docker.com/)
- [Docker-compose](https://docs.docker.com/compose/)

## How to start

:warning: A packaged and released docker image is to come. For now, you can try the development version

Clone this project, launch the development toolbox :

```shell
git clone git@github.com:kheraud/creepy-crawler.git
make create
# Supply parameters as asked
# I suppose you choose 8889 as LOCAL_FRONT_PORT
make shell_api
```

Then go to <http://localhost:8889>, you should see an empty interface with no repository listed

## Fill database with repositories

A small script is embedded which permits to crawl a markdown page and gather stats about all github repositories linked in this page

If I want to crawl [Awesome Go list of tools](https://github.com/avelino/awesome-go), I would target this specific page : <https://raw.githubusercontent.com/avelino/awesome-go/master/README.md>

:warning: Be caution, we target the raw page, not the github decorated one

```shell
# Go to py development shell
make shell_api
python creep-crawl.py "https://raw.githubusercontent.com/avelino/awesome-go/master/README.md"
```

At the end of the crawl, refresh your <http://localhost:8889> page to see the new repositories

## Start discovering great tools

You can browse the local ui and tag repositories with specific labels

## Todo

- [ ] Edition of custom labels instead of static ones
- [ ] Launch crawls from the ui
- [ ] Manually add custom repositories or pages
- [ ] Package the app in a released docker image
- [ ] Improve ui
