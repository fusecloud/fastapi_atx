import datetime
import graphene
from pydantic import BaseModel


class QueryResultGQL(graphene.ObjectType):
    # user fields
    user_id = graphene.Int()
    user_name = graphene.String()
    email = graphene.String()
    occupation = graphene.String()
    hash_password = graphene.String()
    api_key = graphene.String()
    # make sure to leave paren off so as not to have set to class create time
    created_date = graphene.String()
    last_login = graphene.String()
    profile_image_url = graphene.String()
    # chore fields
    chore_id = graphene.Int()
    chore_name = graphene.Int()
    category = graphene.String()
    type = graphene.Int()
    alert_days = graphene.Int()

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_name": "Johnny",
                "occupation": "Developer",
                "chore_name": "Walk Dog",
                "category": "Pets"
            }
        }


class QueryResultPydantic(BaseModel):
    # user fields
    user_id: int
    user_name: str
    email: str
    occupation: str
    hash_password: str
    api_key: str
    # make sure to leave paren off so as not to have set to class create time
    created_date: datetime.datetime
    last_login: datetime.datetime
    profile_image_url: str
    # chore fields
    chore_id: int
    chore_name: int
    category: str
    type: int
    alert_days: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_name": "Johnny",
                "occupation": "Developer",
                "chore_name": "Walk Dog",
                "category": "Pets"
            }
        }


class QueryResult(BaseModel):
    # user fields
    user_id: int
    user_name: str
    email: str
    occupation: str
    hash_password: str
    api_key: str
    # make sure to leave paren off so as not to have set to class create time
    created_date: datetime.datetime
    last_login: datetime.datetime
    profile_image_url: str
    # chore fields
    chore_id: int
    chore_name: int
    category: str
    type: int
    alert_days: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_name": "Johnny",
                "occupation": "Developer",
                "chore_name": "Walk Dog",
                "category": "Pets"
            }
        }
