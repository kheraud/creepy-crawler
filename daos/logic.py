from .model import (
    db,
    Repository,
    Page,
    PageTargetRepository,
)
from peewee import fn


def init_database(sqlite_file):
    db.init(sqlite_file, pragmas=(("foreign_keys", "on"),))


def create_schema():
    with db:
        db.create_tables([Repository, Page, PageTargetRepository], safe=True)


def match_repositories_by_names(repo_names):
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


def fetch_repositories(status, target_page, sort_key, limit, offset):
    query = Repository.select(Repository)

    if status:
        query = query.where(Repository.status.in_(status))
    if target_page:
        query = query.join(
            PageTargetRepository, on=PageTargetRepository.repository
        ).where(PageTargetRepository.page == target_page)

    if sort_key == "stars":
        query = query.order_by(-Repository.crawl_stars)
    elif sort_key == "forks":
        query = query.order_by(-Repository.crawl_forks)
    elif sort_key == "issues":
        query = query.order_by(-Repository.crawl_issues)
    elif sort_key == "status":
        query = query.order_by(-Repository.status)
    elif sort_key == "review_status":
        query = query.order_by(-Repository.review_status)
    else:
        query = query.order_by(-Repository.crawl_date)

    return query.offset(offset).limit(limit).dicts()


def fetch_repositories_count(status, target_page):
    query = Repository.select(fn.Count(Repository.name))

    if status:
        query = query.where(Repository.status.in_(status))
    if target_page:
        query = query.join(
            PageTargetRepository, on=PageTargetRepository.repository
        ).where(PageTargetRepository.page == target_page)

    for res in query.tuples():
      if res and len(res) > 0:
        return res[0]
      else:
        return None


def fetch_aggregated_pages(target_page):

    query = (
        Repository.select(
            Page, Repository.status, fn.Count(Repository.name).alias("count")
        )
        .join(PageTargetRepository)
        .group_by(PageTargetRepository.page, Repository.status)
        .join(Page)
    )

    if target_page:
        query = query.where(PageTargetRepository.page == target_page)

    pages_stats = {}

    for page_stat in query.dicts():
        page_id = page_stat["id"]
        page_status = page_stat["status"]
        repo_count = page_stat["count"]

        if page_id not in pages_stats:
            pages_stats[page_id] = page_stat
            pages_stats[page_id]["status"] = {}
            del pages_stats[page_id]["count"]

        pages_stats[page_id]["status"][page_status] = repo_count

    return sorted(pages_stats.values(), key=lambda x: x["name"])
