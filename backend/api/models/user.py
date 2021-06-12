from pydantic import BaseModel
import datetime


class User(BaseModel):
    id: int
    name: str
    email: str
    created_date: datetime.datetime
    last_login: datetime.datetime
    profile_image_url: str

    # provide configurations to Pydantic
    class Config:
        # will tell the Pydantic model to read the data even if it is not a dict
        orm_mode = True
