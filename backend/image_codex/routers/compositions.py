import base64
from io import BytesIO
from typing import List, Tuple

import requests
from fastapi import APIRouter
from image_codex.models.api import ApiFile
from PIL import Image
from pydantic.main import BaseModel

router = APIRouter()
root_path = '/compositions'


class ComposedImage(BaseModel):
    id: str
    url: str
    x: int
    y: int
    width: int
    height: int


class RequestComposition(BaseModel):
    name: str
    width: int
    height: int
    background_color: Tuple[int, ...] = (255, 255, 255)
    images: List[ComposedImage]


@router.post(root_path, response_model=ApiFile)
async def create_composition(request: RequestComposition) -> ApiFile:
    composition = Image.new('RGB',
                            (request.width, request.height),
                            request.background_color)
    for image in request.images:
        with BytesIO(requests.get(image.url).content) as file:
            with Image.open(file) as img:
                img.thumbnail((image.width, image.height), Image.ANTIALIAS)
                composition.paste(img, (image.x, image.y))
    with BytesIO() as file:
        composition.save(file, format='PDF')
        data = base64.b64encode(file.getvalue())
    return ApiFile(name=request.name,
                   type='application/pdf',
                   base64=data)
