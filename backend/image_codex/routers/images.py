"""
Handle /images requests
"""
import base64
import mimetypes
from io import BytesIO
from typing import Any, Dict, List, Optional

import cloudinary
import cloudinary.api
import cloudinary.uploader
import imagehash
from exif import Image as ExifImage
from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from fastapi_pagination.bases import AbstractPage
from image_codex.models import (ApiFile, CursorPage, CursorParams, HashMethod,
                                TaggedImage)
from image_codex.utils import (CLOUDINARY_FOLDER, MetadataKey, get_pil_format,
                               map_dms_to_dd, map_id_to_public_id,
                               map_public_id_to_id)
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS

router = APIRouter(
    prefix='/images',
    tags=['images']
)


@router.post('')
async def create_image(body: ApiFile):
    """
    Upload a new image to the database
    """
    with BytesIO(base64.b64decode(body.base64)) as file:
        exif_image = ExifImage(file)
        with Image.open(file) as image:
            hash: str = str(imagehash.phash(image))
            image = ImageOps.exif_transpose(image)
            exif = image.getexif()
            exif_data = {TAGS.get(tag_id, tag_id):
                         __get_tag_value(tag_id, value)
                         for tag_id, value in exif.items()}
            tags = [tag.strip()
                    for tag
                    in exif_data.get('ImageDescription', '').split(',')]
            artist = exif_data.get('Artist')
            copyright = exif_data.get('Copyright')
            context: Dict[str, Any] = {
                MetadataKey.ARTIST.value: artist,
                MetadataKey.COPYRIGHT.value: copyright,
                MetadataKey.GPS_LATITUDE.value:
                    map_dms_to_dd(*exif_image.get('gps_latitude')),
                MetadataKey.GPS_LONGITUDE.value:
                    map_dms_to_dd(*exif_image.get('gps_longitude')),
            }
            with BytesIO() as new_file:
                image.save(new_file, get_pil_format(body.type))
                new_file.seek(0)
                print(f'uploading {image.format} file to {CLOUDINARY_FOLDER}')
                return cloudinary.uploader.upload(
                    public_id=f'{CLOUDINARY_FOLDER}/{hash}',
                    file=new_file,
                    image_metadata=True,
                    tags=tags,
                    context=context)


@router.get('', response_model=CursorPage[TaggedImage])
async def get_all_images(params: CursorParams = Depends(),
                         tags: List[str] = Query([]),
                         author: Optional[str] = Query(None),
                         ) -> AbstractPage[TaggedImage]:
    """
    Get images with filters:
    - **tags**: contains all given tags
    - **author**: has given author
    """
    folder_expressions = [f'folder="{CLOUDINARY_FOLDER}"']
    tag_expressions = [f'tags="{tag}"' for tag in tags]
    author_expressions = [f'context.Artist="{author}"'] if author else []
    expressions = folder_expressions + tag_expressions + author_expressions
    expression = ' AND '.join(expressions)
    print(expression)
    response = cloudinary.Search()\
        .expression(expression)\
        .max_results(params.size)\
        .next_cursor(params.next)\
        .with_field('context')\
        .with_field('tags')\
        .execute()
    total_count = response.get('total_count', 0)
    params.next = response.get('next_cursor')
    resources: List[dict[str, Any]] = response.get('resources', [])
    images = [__get_search_response_image(resource) for resource in resources]
    return CursorPage.create(images, total_count, params)


@router.get('/{image_ids}', response_model=List[TaggedImage])
async def get_images(image_ids: str) -> List[TaggedImage]:
    """
    Get images with given comma-separated ids
    """
    public_ids = [map_id_to_public_id(id) for id in image_ids.split(',')]
    resources = [cloudinary.api.resource(public_id=public_id,
                                         context=True,
                                         tags=True)
                 for public_id in public_ids]
    return [__get_admin_response_image(resource)
            for resource in resources]


@router.delete('/{image_ids}')
async def delete_images(image_ids: str) -> List[str]:
    """
    Delete images with given comma-separated ids
    """
    public_ids = [map_id_to_public_id(id) for id in image_ids.split(',')]
    response = cloudinary.api.delete_resources(public_ids=public_ids)
    return [key
            for key, value
            in response.get('deleted', {}).items()
            if value == 'deleted']


@router.post('/hash')
async def get_image_hash(body: ApiFile,
                         method: HashMethod = Query(HashMethod.phash)
                         ) -> str:
    """
    Returns image hash
    """
    if method == HashMethod.phash:
        with BytesIO(base64.b64decode(body.base64)) as file:
            with Image.open(file) as image:
                return str(imagehash.phash(image))


def __get_tag_value(tag_id: int, value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode()
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def __get_search_response_image(resource: dict[str, Any]) -> TaggedImage:
    """
    https://cloudinary.com/documentation/search_api
    """
    context: dict[str, Any] = resource.get('context', {})
    id = map_public_id_to_id(resource.get('public_id', ''))
    return TaggedImage(id=id,
                       name=resource.get('filename'),
                       url=resource.get('secure_url'),
                       width=resource.get('width'),
                       height=resource.get('height'),
                       tags=resource.get('tags'),
                       author=context.get(MetadataKey.ARTIST.value),
                       license=context.get(MetadataKey.COPYRIGHT.value))


def __get_admin_response_image(resource: dict[str, Any]) -> TaggedImage:
    """
    https://cloudinary.com/documentation/admin_api
    """
    context: dict[str, Any] = resource.get('context', {}).get('custom', {})
    id = map_public_id_to_id(resource.get('public_id', ''))
    return TaggedImage(id=id,
                       name=id,
                       url=resource.get('secure_url'),
                       width=resource.get('width'),
                       height=resource.get('height'),
                       tags=resource.get('tags'),
                       author=context.get(MetadataKey.ARTIST.value),
                       license=context.get(MetadataKey.COPYRIGHT.value))
