from data.models.chore import Chore
import fastapi

api = fastapi.APIRouter()

chores = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]


@api.get("/api/chores", tags=["chores"])
async def get_chores() -> dict:
    return {"data": chores}


@api.get("/api/chores/{id}", tags=["chores"])
async def get_single_chore(id: int) -> dict:
    if id > len(chores):
        return {
            "error": "No such chore with the supplied ID."
        }

    for chore in chores:
        if chore["id"] == id:
            return {
                "data": chore
            }


@api.post("/api/chores", tags=["chores"])
async def add_post(chore: Chore) -> dict:
    chore.id = len(chores) + 1
    chores.append(chore.dict())
    return {
        "data": "post added."
    }
