import uvicorn
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
import fastapi

api = fastapi.FastAPI()


class Chore(BaseModel):
    name: str
    days_until_alert: int
    date_added: Optional[str]


class Regimen(BaseModel):
    chore_list: List[Chore]


# "Database" of Todos
__todos: List[Chore] = [
    {
        "name": "walk dog",
        "days_until_alert": 1,
        "date_added": "2021-05-10"
    },
    {
        "name": "water plants",
        "days_until_alert": 2,
        "date_added": "2021-05-11"
    }
]


# SERVICES
# get list of todos
async def get_todos() -> List[Chore]:
    return __todos


# # add new todoitem
async def add_todo(chore: Chore) -> str:
    __todos.append({
        "name": chore.name,
        "days_until_alert": chore.days_until_alert,
        "date_added": datetime.now().strftime("%Y-%m-%d")
    })

    return 'todo added'


# API ROUTES
@api.get('/', name='home')
async def index():
    return {"message": "Hello FastAPI!"}


@api.get('/todos', name='Get All Todos', response_model=List[Chore])
async def todos_get() -> List[Chore]:
    return await get_todos()


@api.post('/todos', name='Create a Todo', response_model=Chore)
async def todos_post(chore: Chore) -> Chore:
    await add_todo(chore=chore)
    return chore


if __name__ == '__main__':
    print("Running on port 8000")
    uvicorn.run(app=api, port=8000, host='127.0.0.1')
