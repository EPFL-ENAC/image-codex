from typing import List

import cloudinary.api
from fastapi import APIRouter

router = APIRouter(
    prefix='/tags',
    tags=['tags']
)


@router.get('/', response_model=List[str])
async def get_tags() -> List[str]:
    """
    Get all tags
    """
    response = cloudinary.api.tags(max_results=500)
    return response.get('tags', [])
