"""
Handle /geo requests
"""
from typing import Any, Dict, List, Optional

import cloudinary.api
from fastapi import APIRouter
from fastapi.param_functions import Query
from image_codex.models import GeoImage
from image_codex.utils import CLOUDINARY_FOLDER
from image_codex.utils.cloudinary import MetadataKey, map_public_id_to_id

router = APIRouter(
    prefix='/geo',
    tags=['geo']
)


@router.get('/images', response_model=List[GeoImage])
async def get_images(count: int = Query(10)) -> List[GeoImage]:
    """
    Get images in GeoJSON format
    """
    resources: List[Dict[str, Any]] = cloudinary.api.resources(
        prefix=CLOUDINARY_FOLDER + '/',
        type='upload',
        max_results=count,
        context=True)\
        .get('resources', [])
    images: List[GeoImage] = []
    for resource in resources:
        context: Dict[str, str] = resource.get('context', {}).get('custom', {})
        latitude: Optional[str] = context.get(MetadataKey.GPS_LATITUDE.value)
        longitude: Optional[str] = context.get(
            MetadataKey.GPS_LONGITUDE.value)
        if latitude is not None and longitude is not None:
            images.append(GeoImage(
                id=map_public_id_to_id(resource.get('public_id', '')),
                url=resource.get('secure_url'),
                latitude=float(latitude),
                longitude=float(longitude),
            ))
    return images
