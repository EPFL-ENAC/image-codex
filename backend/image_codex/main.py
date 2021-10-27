"""
Entrypoint for FastAPI application
https://fastapi.tiangolo.com/tutorial/bigger-applications/
"""
import cloudinary
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.api import add_pagination

from image_codex import __name__, __version__
from image_codex.routers import compositions, geo, hash, images, root, tags
from image_codex.utils import cloudinary_config, fast_api_config

#########################
# FastAPI Configuration #
#########################

app = FastAPI(
    title=__name__,
    version=__version__,
    root_path=fast_api_config.get('root_path', ''),
    openapi_tags=[
        {
            "name": "compositions",
            "description": "Manage image compositions",
        },
        {
            "name": "geo",
            "description": "Geographic data",
        },
        {
            "name": "images",
            "description": "Manage images",
        },
        {
            "name": "tags",
            "description": "Manage tags",
        },
    ],
)
if not fast_api_config.getboolean('cors_enabled'):
    print('cors disabled')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
else:
    print('cors enabled')
app.include_router(root.router)
app.include_router(compositions.router)
app.include_router(geo.router)
app.include_router(hash.router)
app.include_router(images.router)
app.include_router(tags.router)

add_pagination(app)

############################
# Cloudinary Configuration #
############################


cloudinary.config(
    cloud_name=cloudinary_config.get('cloud_name'),
    api_key=cloudinary_config.get('api_key'),
    api_secret=cloudinary_config.get('api_secret')
)
