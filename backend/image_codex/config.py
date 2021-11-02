
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=['image_codex/settings.toml'],
    validators=[
        Validator('cors_enabled', default=False),
        Validator('root_path', default=''),
        Validator('username', must_exist=True),
        Validator('password', must_exist=True),
        Validator('cloudinary_cloud_name', must_exist=True),
        Validator('cloudinary_api_key', must_exist=True),
        Validator('cloudinary_api_secret', must_exist=True),
        Validator('cloudinary_folder', default='image-codex'),
    ],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
