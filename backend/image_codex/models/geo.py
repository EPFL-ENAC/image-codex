from pydantic import BaseModel


class GeoImage(BaseModel):
    id: str
    url: str
    latitude: float
    longitude: float