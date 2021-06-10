from pydantic import BaseModel, Field, EmailStr
from data.models.modelbase import SqlAlchemyBase
import sqlalchemy as sa


class Chore(SqlAlchemyBase):
    __tablename__ = 'chores'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # id: int = sa.Column(sa.Integer, primary_key=True)
    user_id: int = sa.Column(sa.Integer)
    name: str = sa.Column(sa.String)
    category: str = sa.Column(sa.String)
    type: str = sa.Column(sa.String)
    alert_days: int = sa.Column(sa.Integer)
    # alert_date: str = sa.Column(sa.Integer)

    # id: int = Field(default=None)
    # name: str = Field(...)
    # category: str = Field(...)
    # type: str = Field(...)
    # alert_days: int = Field(...)
    # alert_date: str = Field(...)
    #
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Vacuum",
    #             "category": "cleaning",
    #             "type": "recurring",
    #             "alert_days": "14",
    #             "alert_date": "2021-05-01"
    #         }
    #     }
