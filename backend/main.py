from typing import List, Dict
from datetime import datetime
import fastapi
import uvicorn

api = fastapi.FastAPI()

# "Database" of Todos
__todos: List[Dict] = [
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
async def get_todos() -> List:
    return list(__todos)


# add new todoitem
async def add_todo(name: str, frequency: int) -> str:
    __todos.append({
        "name": name,
        "days_until_alert": frequency,
        "date_added": datetime.now().strftime("%Y-%m-%d")
    })

    return 'todo added'


# API ROUTES
@api.get('/todos', name='all_todos', response_model=List)
async def todos_get() -> List:
    return await get_todos()


@api.post('/todos')
async def todos_post(todo_submission: Dict) -> str:
    return await add_todo(
        name=todo_submission['name'],
        frequency=todo_submission['days_until_alert']
    )


uvicorn.run(app=api, port=8000, host='127.0.0.1')
