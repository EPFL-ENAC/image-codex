"""
Define all model classes
"""
from typing import Optional

from pydantic import BaseModel

from .compositions import *  # noqa: F401,F403
from .images import *  # noqa: F401,F403
from .pages import *  # noqa: F401,F403


class ApiFile(BaseModel):
    name: Optional[str]
    type: Optional[str]
    base64: str
