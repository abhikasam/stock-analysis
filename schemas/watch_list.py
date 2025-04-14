from pydantic import BaseModel


class WatchListCreate(BaseModel):
    name:str
    user_id:int

class WatchListResponse(WatchListCreate):
    id:int

    class Config:
        from_attributes = True