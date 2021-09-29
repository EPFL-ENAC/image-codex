import base64
from io import BytesIO
from typing import Any, List

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from fastapi_pagination.bases import AbstractPage
from image_codex.models.page import CursorPage, CursorParams
from PIL import Image
from PIL.ExifTags import TAGS
from pydantic import BaseModel

router = APIRouter()
root_path = '/images'
root_folder = 'image-codex'


class RequestImage(BaseModel):
    content: str


class ResponseImage(BaseModel):
    id: str
    name: str
    url: str
    tags: List[str]
    author: str
    license: str


@router.post(root_path)
async def create_image(body: RequestImage):
    with BytesIO(base64.b64decode(body.content)) as file:
        with Image.open(file) as image:
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
                image.save(new_file, 'JPEG')
                new_file.seek(0)
                return cloudinary.uploader.upload(file=new_file,
                                                  folder=root_folder,
                                                  tags=tags,
                                                  context=context)


def __get_tag_value(exif: Image.Exif, tag_id: int) -> str:
    value = exif.get(tag_id)
    if isinstance(value, bytes):
        return value.decode()
    else:
        return str(value)


@router.get(root_path, response_model=CursorPage[ResponseImage])
async def get_images(params: CursorParams = Depends(),
                     tags: List[str] = Query([]),
                     ) -> AbstractPage[ResponseImage]:
    folder_expressions = ['folder=' + root_folder]
    tag_expressions = ['tags=' + tag for tag in tags]
    expressions = folder_expressions + tag_expressions
    response = cloudinary.Search()\
        .expression(' AND '.join(expressions))\
        .max_results(params.size)\
        .next_cursor(params.next)\
        .with_field('context')\
        .with_field('tags')\
        .execute()
    total_count = response.get('total_count', 0)
    params.next = response.get('next_cursor')
    resources: List[dict[str, Any]] = response.get('resources', [])
    images = [__get_response_images(resource) for resource in resources]
    return CursorPage.create(images, total_count, params)


def __get_response_images(resource: dict[str, Any]) -> ResponseImage:
    context: dict[str, Any] = resource.get('context', {})
    return ResponseImage(id=resource.get('asset_id'),
                         name=resource.get('filename'),
                         url=resource.get('secure_url'),
                         tags=resource.get('tags'),
                         author=context.get('Artist'),
                         license=context.get('Copyright'))
