from typing import List

from pydantic import BaseModel


class TaggedImage(BaseModel):
    id: str
    name: str
    url: str
    width: int
    height: int
    tags: List[str]
    author: str
    license: str
