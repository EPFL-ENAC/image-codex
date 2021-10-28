"""
Handle /compositions requests
"""
import base64
from io import BytesIO

import requests
from fastapi import APIRouter, Query
from image_codex.models import ApiFile, Composition
from image_codex.utils import get_pil_format
from PIL import Image

router = APIRouter(
    prefix='/compositions',
    tags=['compositions']
)


@router.post('', response_model=ApiFile)
async def create_composition(
        composition: Composition,
        mimetype: str = Query('application/pdf')) -> ApiFile:
    """
    Create an image composition and return it in the given type
    """
    composedImage = Image.new('RGB',
                              (composition.width, composition.height),
                              composition.background_color)
    for image in composition.images:
        with BytesIO(requests.get(image.url).content) as file:
            with Image.open(file) as img:
                img.thumbnail((image.width, image.height), Image.ANTIALIAS)
                composedImage.paste(img, (image.x, image.y))
    with BytesIO() as file:
        composedImage.save(file, format=get_pil_format(mimetype))
        data = base64.b64encode(file.getvalue())
    return ApiFile(name=composition.name,
                   type=mimetype,
                   base64=data)
