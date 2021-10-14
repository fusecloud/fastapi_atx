import datetime
import graphene
from pydantic import BaseModel


class User(graphene.ObjectType):
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


class Chore(graphene.ObjectType):
    # chore fields
    chore_id = graphene.Int()
    user_id = graphene.Int()
    chore_name = graphene.String()
    category = graphene.String()
    type = graphene.String()
    alert_days = graphene.Int()


class UserChore(graphene.ObjectType):
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
    chore_name = graphene.String()
    category = graphene.String()
    type = graphene.String()
    alert_days = graphene.Int()
