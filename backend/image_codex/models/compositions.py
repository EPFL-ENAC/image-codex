from typing import List, Tuple
from pydantic import BaseModel


class ComposedImage(BaseModel):
    id: str
    url: str
    x: int
    y: int
    width: int
    height: int


class Composition(BaseModel):
    name: str
    width: int
    height: int
    background_color: Tuple[int, ...] = (255, 255, 255)
    images: List[ComposedImage]
