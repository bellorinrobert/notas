from pydantic import BaseModel

class Nota(BaseModel):
    id: int
    value: int
    