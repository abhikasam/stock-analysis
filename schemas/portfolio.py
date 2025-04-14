from pydantic import BaseModel


class PortfolioCreate(BaseModel):
    user_id:int
    stock_id:int

class PortfolioResponse(PortfolioCreate):
    id:int

    class Config:
        from_attributes=True