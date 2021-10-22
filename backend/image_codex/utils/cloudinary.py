import os
from enum import Enum
from typing import Any

CLOUDINARY_FOLDER = os.getenv('CLOUDINARY_FOLDER', 'image-codex')


class MetadataKey(Enum):
    ARTIST = 'Artist'
    COPYRIGHT = 'Copyright'
    GPS_LATITUDE = 'gps_latitude'
    GPS_LONGITUDE = 'gps_longitude'


def map_public_id_to_id(public_id: str) -> str:
    return public_id.removeprefix(CLOUDINARY_FOLDER + '/')


def map_id_to_public_id(id: str) -> str:
    return f'{CLOUDINARY_FOLDER}/{id}'
