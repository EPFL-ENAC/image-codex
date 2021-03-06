"""
Handle /images requests
"""
import base64
from io import BytesIO
from typing import Any, Dict, List, Optional

import cloudinary
import cloudinary.api
import cloudinary.uploader
import imagehash
from exif import Image as ExifImage
from fastapi import APIRouter, Depends, Query
from fastapi_pagination.bases import AbstractPage
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS

from image_codex.models import ApiFile, CursorPage, CursorParams, TaggedImage
from image_codex.utils import (
    CLOUDINARY_FOLDER,
    MetadataKey,
    get_pil_format,
    is_admin,
    map_dms_to_dd,
    map_id_to_public_id,
    map_public_id_to_id,
)

router = APIRouter(prefix="/images", tags=["images"])


@router.post("")
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
            exif_data = {
                TAGS.get(tag_id, tag_id): __get_tag_value(value)
                for tag_id, value in exif.items()
            }
            tags = [
                tag.strip() for tag in exif_data.get("ImageDescription", "").split(",")
            ]
            artist = exif_data.get("Artist")
            copyright = exif_data.get("Copyright")
            context: Dict[str, Any] = {
                MetadataKey.ARTIST.value: artist,
                MetadataKey.COPYRIGHT.value: copyright,
                MetadataKey.GPS_LATITUDE.value: map_dms_to_dd(
                    exif_image.get("gps_latitude"), exif_image.get("gps_latitude_ref")
                ),
                MetadataKey.GPS_LONGITUDE.value: map_dms_to_dd(
                    exif_image.get("gps_longitude"), exif_image.get("gps_longitude_ref")
                ),
            }
            with BytesIO() as new_file:
                image.save(new_file, get_pil_format(body.type))
                new_file.seek(0)
                print(f"uploading {image.format} file to {CLOUDINARY_FOLDER}")
                return cloudinary.uploader.upload(
                    public_id=f"{CLOUDINARY_FOLDER}/{hash}",
                    file=new_file,
                    image_metadata=True,
                    tags=tags,
                    context=context,
                )


@router.get("", response_model=CursorPage[TaggedImage])
async def get_all_images(
    params: CursorParams = Depends(),
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
    expression = " AND ".join(expressions)
    print(expression)
    response = (
        cloudinary.Search()
        .expression(expression)
        .max_results(params.size)
        .next_cursor(params.next)
        .with_field("context")
        .with_field("tags")
        .execute()
    )
    total_count = response.get("total_count", 0)
    params.next = response.get("next_cursor")
    resources: List[dict[str, Any]] = response.get("resources", [])
    images = [__get_search_response_image(resource) for resource in resources]
    return CursorPage.create(images, total_count, params)


@router.post(
    "/{image_id}", dependencies=[Depends(is_admin)], response_model=TaggedImage
)
async def update_image(image_id: str, body: TaggedImage) -> TaggedImage:
    """
    Update following fields of an image:
    * tags
    """
    public_id = map_id_to_public_id(image_id)
    resource = cloudinary.api.update(public_id, tags=body.tags)
    return __get_admin_response_image(resource)


@router.get("/{image_ids}", response_model=List[TaggedImage])
async def get_images(image_ids: str) -> List[TaggedImage]:
    """
    Get images with given comma-separated ids
    """
    public_ids = [map_id_to_public_id(id) for id in image_ids.split(",")]
    resources = [
        cloudinary.api.resource(public_id=public_id, context=True, tags=True)
        for public_id in public_ids
    ]
    return [__get_admin_response_image(resource) for resource in resources]


@router.delete("/{image_ids}", dependencies=[Depends(is_admin)])
async def delete_images(image_ids: str) -> List[str]:
    """
    Delete images with given comma-separated ids
    """
    public_ids = [map_id_to_public_id(id) for id in image_ids.split(",")]
    response = cloudinary.api.delete_resources(public_ids=public_ids)
    return [
        key for key, value in response.get("deleted", {}).items() if value == "deleted"
    ]


def __get_tag_value(value: Any) -> str:
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
    context: dict[str, Any] = resource.get("context", {})
    id = map_public_id_to_id(resource.get("public_id", ""))
    return TaggedImage(
        id=id,
        name=resource.get("filename"),
        url=resource.get("secure_url"),
        width=resource.get("width"),
        height=resource.get("height"),
        tags=resource.get("tags"),
        author=context.get(MetadataKey.ARTIST.value),
        license=context.get(MetadataKey.COPYRIGHT.value),
    )


def __get_admin_response_image(resource: dict[str, Any]) -> TaggedImage:
    """
    https://cloudinary.com/documentation/admin_api
    """
    context: dict[str, Any] = resource.get("context", {}).get("custom", {})
    id = map_public_id_to_id(resource.get("public_id", ""))
    return TaggedImage(
        id=id,
        name=id,
        url=resource.get("secure_url"),
        width=resource.get("width"),
        height=resource.get("height"),
        tags=resource.get("tags"),
        author=context.get(MetadataKey.ARTIST.value),
        license=context.get(MetadataKey.COPYRIGHT.value),
    )
