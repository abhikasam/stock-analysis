from pydantic import BaseModel


class StockCreate(BaseModel):
    symbol:str
    description:str


class StockResponse(StockCreate):
    id:int

    class Config:
        from_attributes = True