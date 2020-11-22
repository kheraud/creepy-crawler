from .model import (
    db,
    Repository,
    Page,
    PageTargetRepository,
)


def init_database(sqlite_file):
    db.init(sqlite_file, pragmas=(("foreign_keys", "on"),))


def create_schema():
    with db:
        db.create_tables([Repository, Page, PageTargetRepository], safe=True)


def fetch_repositories_by_names(repo_names):
    return Repository.select().where(Repository.name.in_(repo_names)).dicts()


def add_page(url, name, crawl_start_date, crawl_end_date):
    user = Page.get_or_none(Page.url == url)

    upsert_id = (
        Page.insert(
            url=url,
            name=name,
            crawl_start_date=crawl_start_date,
            crawl_end_date=crawl_end_date,
        )
        .on_conflict(
            conflict_target=[Page.url],
            preserve=[
                Page.name,
                Page.crawl_start_date,
                Page.crawl_end_date,
            ],
        )
        .execute()
    )

    return user.id if user else upsert_id


def add_repository(
    target_page,
    name,
    url,
    description,
    crawl_date,
    crawl_stars,
    crawl_forks,
    crawl_issues,
):
    formated_name = name.lower()
    repo = Repository.get_or_none(Repository.name == formated_name)

    upsert_id = (
        Repository.insert(
            name=name.lower(),
            url=url,
            description=description,
            crawl_date=crawl_date,
            crawl_stars=crawl_stars,
            crawl_forks=crawl_forks,
            crawl_issues=crawl_issues,
        )
        .on_conflict(
            conflict_target=[Repository.name],
            preserve=[
                Repository.description,
                Repository.crawl_date,
                Repository.crawl_stars,
                Repository.crawl_forks,
                Repository.crawl_issues,
            ],
        )
        .execute()
    )

    target_repository = repo.id if repo else upsert_id

    PageTargetRepository.insert(
        page_id=target_page,
        repository_id=target_repository,
    ).on_conflict_ignore().execute()
