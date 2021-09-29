import configparser
import os

import cloudinary
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.api import add_pagination

from image_codex.routers import images, root


class EnvInterpolation(configparser.BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


config = configparser.ConfigParser(interpolation=EnvInterpolation())
config.read('image_codex/config.ini')

# fast_api
fast_api_config = config['fast_api']

app = FastAPI(root_path=fast_api_config.get('root_path', ''))
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
app.include_router(images.router)

add_pagination(app)

# cloudinary
cloudinary_config = config['cloudinary']

cloudinary.config(
    cloud_name=cloudinary_config.get('cloud_name'),
    api_key=cloudinary_config.get('api_key'),
    api_secret=cloudinary_config.get('api_secret')
)
