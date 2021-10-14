import base64
from io import BytesIO
from typing import Any, List, Optional

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from fastapi_pagination.bases import AbstractPage
from image_codex.models.api import ApiFile
from image_codex.models.page import CursorPage, CursorParams
from image_codex.utils.cloudinary import ROOT_FOLDER
from image_codex.utils.pil import get_format
from PIL import Image
from PIL.ExifTags import TAGS
from pydantic import BaseModel

router = APIRouter()
root_path = '/images'


class ResponseImage(BaseModel):
    id: str
    name: str
    url: str
    width: int
    height: int
    tags: List[str]
    author: str
    license: str


@router.post(root_path)
async def create_image(body: ApiFile):
    with BytesIO(base64.b64decode(body.base64)) as file:
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
                image.save(new_file, get_format(body.type))
                new_file.seek(0)
                print(f'uploading {image.format} file to {ROOT_FOLDER}')
                return cloudinary.uploader.upload(file=new_file,
                                                  folder=ROOT_FOLDER,
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
                     author: Optional[str] = Query(None),
                     ) -> AbstractPage[ResponseImage]:
    folder_expressions = [f'folder="{ROOT_FOLDER}"']
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
    images = [__get_response_images(resource) for resource in resources]
    return CursorPage.create(images, total_count, params)


def __get_response_images(resource: dict[str, Any]) -> ResponseImage:
    context: dict[str, Any] = resource.get('context', {})
    return ResponseImage(id=resource.get('asset_id'),
                         name=resource.get('filename'),
                         url=resource.get('secure_url'),
                         width=resource.get('width'),
                         height=resource.get('height'),
                         tags=resource.get('tags'),
                         author=context.get('Artist'),
                         license=context.get('Copyright'))
