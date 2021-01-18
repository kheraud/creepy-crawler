from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    SmallIntegerField,
    CharField,
    TextField,
    DateTimeField,
    ForeignKeyField,
    CompositeKey,
)

db = SqliteDatabase(None)

REPOSITORY_STATUS = [
    (0, "None"),
    (1, "To test"),
    (2, "Dropped"),
    (3, "To implement"),
    (4, "Implemented"),
    (5, "Usefull later"),
]

REPOSITORY_REVIEW_STATUS = [
    (0, "No interest"),
    (1, "Why not"),
    (2, "Cool"),
    (3, "Must have"),
]

DATETIME_FORMATS = "%Y-%m-%d %H:%M:%S.%f"


class BaseModel(Model):
    class Meta:
        database = db


class Repository(BaseModel):
    id = AutoField()
    name = CharField(index=True, unique=True)
    url = TextField()
    description = TextField(null=True)
    status = SmallIntegerField(
        index=True, default=0, choices=REPOSITORY_STATUS
    )
    review_status = SmallIntegerField(
        index=True, null=True, choices=REPOSITORY_REVIEW_STATUS
    )
    review_comment = TextField(null=True)
    review_date = DateTimeField(null=True)
    crawl_date = DateTimeField()
    crawl_stars = SmallIntegerField(index=True)
    crawl_forks = SmallIntegerField(index=True)
    crawl_issues = SmallIntegerField(index=True)


class Page(BaseModel):
    id = AutoField()
    url = TextField(index=True, unique=True)
    name = CharField()
    crawl_start_date = DateTimeField(formats=DATETIME_FORMATS)
    crawl_end_date = DateTimeField(formats=DATETIME_FORMATS, null=True)


class PageTargetRepository(BaseModel):
    page = ForeignKeyField(Page, backref="page_targets")
    repository = ForeignKeyField(Repository, backref="repository_targets")

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (("page", "repository"), True),
        )
        primary_key = CompositeKey("page", "repository")
