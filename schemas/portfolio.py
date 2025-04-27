from pydantic import BaseModel


class PortfolioCreate(BaseModel):
    user_id:int
    name:str

class PortfolioResponse(PortfolioCreate):
    id:int

    class Config:
        from_attributes=True


