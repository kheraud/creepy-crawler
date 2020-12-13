from .model import (
    REPOSITORY_STATUS,
)
from marshmallow import (
    Schema,
    fields,
    validate,
)

REPOSITORY_STATUS_CHOICES = [st[0] for st in REPOSITORY_STATUS]


class ReviewSchema(Schema):
    status = fields.Integer(
        validate=validate.OneOf(REPOSITORY_STATUS_CHOICES), required=True
    )
    review_comment = fields.String(
        validate=validate.Length(3, 300),
        data_key="reviewComment",
        required=False,
    )
