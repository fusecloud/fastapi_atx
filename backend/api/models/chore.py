from typing import Optional
from pydantic import BaseModel


# for more examples of documentation with sample calls
# https://fastapi.tiangolo.com/tutorial/schema-extra-example/

class Chore(BaseModel):
    chore_id: Optional[int]
    user_id: Optional[int]
    chore_name: str
    category: str
    type: str
    alert_days: int

    # provide configurations to Pydantic
    class Config:
        # will tell the Pydantic model to read the data even if it is not a dict
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Clean kitchen",
                "category": "cleaning",
                "type": "recurring",
                "alert_days": 14
            }
        }
