from pydantic import BaseModel
import datetime


class User(BaseModel):
    user_id: int
    user_name: str
    email: str
    occupation: str
    created_date: datetime.datetime
    last_login: datetime.datetime
    profile_image_url: str

    # provide configurations to Pydantic
    class Config:
        # will tell the Pydantic model to read the data even if it is not a dict
        orm_mode = True
