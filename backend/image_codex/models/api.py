from pydantic.main import BaseModel


class ApiFile(BaseModel):
    name: str
    type: str
    base64: str
