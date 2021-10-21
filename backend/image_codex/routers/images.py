"""
Handle /images requests
"""
import base64
from io import BytesIO
from typing import Any, List, Optional

import cloudinary
import cloudinary.api
import cloudinary.uploader
from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from fastapi_pagination.bases import AbstractPage
from image_codex.models import ApiFile, CursorPage, CursorParams, TaggedImage
from image_codex.utils import CLOUDINARY_FOLDER, get_pil_format
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS

router = APIRouter(
    prefix='/images',
    tags=['images']
)


@router.post('/')
async def create_image(body: ApiFile):
    """
    Upload a new image to the database
    """
    with BytesIO(base64.b64decode(body.base64)) as file:
        with Image.open(file) as image:
            image = ImageOps.exif_transpose(image)
            exif = image.getexif()
            exif_data = {TAGS.get(tag_id, tag_id):
                         __get_tag_value(exif, tag_id)
                         for tag_id in exif}
            tags = [tag.strip()
                    for tag
                    in exif_data.get('ImageDescription', '').split(',')]
            artist = exif_data.get('Artist')
            copyright = exif_data.get('Copyright')
            context = {
                'Artist': artist,
                'Copyright': copyright,
            }
            with BytesIO() as new_file:
                image.save(new_file, get_pil_format(body.type))
                new_file.seek(0)
                print(f'uploading {image.format} file to {CLOUDINARY_FOLDER}')
                return cloudinary.uploader.upload(file=new_file,
                                                  folder=CLOUDINARY_FOLDER,
                                                  tags=tags,
                                                  context=context)


@router.get('/', response_model=CursorPage[TaggedImage])
async def get_images(params: CursorParams = Depends(),
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
async def get_image(image_ids: str) -> List[TaggedImage]:
    """
    Get images with given ids
    """
    public_ids = [__get_public_id(id) for id in image_ids.split(',')]
    resources = [cloudinary.api.resource(public_id=public_id,
                                         context=True,
                                         tags=True)
                 for public_id in public_ids]
    return [__get_admin_response_image(resource)
            for resource in resources]


def __get_tag_value(exif: Image.Exif, tag_id: int) -> str:
    value = exif.get(tag_id)
    if isinstance(value, bytes):
        return value.decode()
    else:
        return str(value)


def __get_search_response_image(resource: dict[str, Any]) -> TaggedImage:
    """
    https://cloudinary.com/documentation/search_api
    """
    context: dict[str, Any] = resource.get('context', {})
    id = __get_id(resource)
    return TaggedImage(id=id,
                       name=resource.get('filename'),
                       url=resource.get('secure_url'),
                       width=resource.get('width'),
                       height=resource.get('height'),
                       tags=resource.get('tags'),
                       author=context.get('Artist'),
                       license=context.get('Copyright'))


def __get_admin_response_image(resource: dict[str, Any]) -> TaggedImage:
    """
    https://cloudinary.com/documentation/admin_api
    """
    context: dict[str, Any] = resource.get('context', {}).get('custom', {})
    id = __get_id(resource)
    return TaggedImage(id=id,
                       name=id,
                       url=resource.get('secure_url'),
                       width=resource.get('width'),
                       height=resource.get('height'),
                       tags=resource.get('tags'),
                       author=context.get('Artist'),
                       license=context.get('Copyright'))


def __get_id(resource: dict[str, Any]) -> str:
    public_id: str = resource.get('public_id', '')
    return public_id.removeprefix(CLOUDINARY_FOLDER + '/')


def __get_public_id(id: str) -> str:
    return f'{CLOUDINARY_FOLDER}/{id}'
