from typing import Optional

from pydantic import BaseModel


class Chore(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    name: str
    category: str
    type: str
    alert_days: int

    # provide configurations to Pydantic
    class Config:
        # will tell the Pydantic model to read the data even if it is not a dict
        orm_mode = True
