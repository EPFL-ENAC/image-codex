"""
Handle /hash requests
"""
import base64
from io import BytesIO

import imagehash
from fastapi import APIRouter, Query
from image_codex.models import ApiFile, HashMethod
from PIL import Image

router = APIRouter(
    prefix='/hash',
    tags=['hash']
)


@router.post('/image')
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
