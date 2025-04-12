from pydantic import BaseModel


class SymbolCreate(BaseModel):
    name:str
    description:str


class SymbolResponse(SymbolCreate):
    id:int

    class Config:
        from_attributes = True