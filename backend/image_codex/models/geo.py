from typing import List, Optional

from pydantic import BaseModel


class GeoImage(BaseModel):
    id: str
    url: str
    latitude: Optional[float]
    longitude: Optional[float]
    author: str
    tags: List[str]
