"""
Handle / requests
"""
from fastapi import APIRouter
from image_codex import __name__, __version__

router = APIRouter()


@router.get('/')
async def root():
    return {
        'name': __name__,
        'version': __version__,
    }
