from typing import TypedDict

from answerking_app.services.service_types.ItemTypes import ItemWithIDDict


class CategoryDict(TypedDict):
    name: str
    items: list[ItemWithIDDict]
