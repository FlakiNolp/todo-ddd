from typing import Mapping, Any

from domain.models.category import Category
from domain.values.category_title import CategoryTitle


def convert_sqlalchemy_category_to_model(category_model: Mapping[str, Any]) -> Category:
    return Category(
        oid=category_model.oid,
        user_oid=category_model.user_oid,
        title=CategoryTitle(category_model.title),
    )
