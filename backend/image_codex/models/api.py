from typing import Optional

from pydantic.main import BaseModel


class ApiFile(BaseModel):
    name: Optional[str]
    type: Optional[str]
    base64: str
