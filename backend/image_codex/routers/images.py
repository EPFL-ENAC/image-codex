import base64
from io import BytesIO

import cloudinary.uploader
from fastapi import APIRouter
from PIL import Image
from PIL.ExifTags import TAGS
from pydantic import BaseModel

router = APIRouter()


class ImageBody(BaseModel):
    content: str


def get_tag_value(exif: Image.Exif, tag_id: int) -> str:
    value = exif.get(tag_id)
    if isinstance(value, bytes):
        return value.decode()
    else:
        return str(value)


@router.post('/images')
async def create_image(body: ImageBody):
    with BytesIO(base64.b64decode(body.content)) as file:
        with Image.open(file) as image:
            exif = image.getexif()
            exif_data = {TAGS.get(tag_id, tag_id): get_tag_value(exif, tag_id)
                         for tag_id
                         in exif}
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
                                                  folder='image-codex',
                                                  tags=tags,
                                                  context=context)
