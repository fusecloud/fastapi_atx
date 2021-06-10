from typing import Optional, List

from data.models.chore import Chore
from data.models.user import User

from sqlalchemy.future import select

from data import db_session


async def add_chore(name: str, category: str,
                    type: str, alert_days: int,
                    user_id: int
                    ) -> Chore:
    chore = Chore()
    chore.name = name
    chore.user_id = user_id
    chore.category = category
    chore.type = type
    chore.alert_days = alert_days

    async with db_session.create_async_session() as session:
        session.add(chore)
        await session.commit()

    return chore


async def edit_chore(id: int, name: str, category: str, type: str, alert_days: int):
    async with db_session.create_async_session() as session:
        sql = f'''
        update chores
        set name = '{name}',
        category = '{category}',
        type = '{type}',
        alert_days = {alert_days}
        where id = {id}
        '''
        print(sql)
        await session.execute(sql)
        await session.commit()


async def remove_chore(id: int):
    async with db_session.create_async_session() as session:
        sql = f"delete from chores where id = {id}"
        print(sql)
        await session.execute(sql)
        await session.commit()
        # query = select(Chore).filter(Chore.id == id).delete()
        # session.query(Chore).filter(Chore.id == id).delete()
        # await session.commit()
        # await session.execute(query)


async def get_user_chores(user_id: int, chore_id: Optional[int] = False) -> Optional[List[Chore]]:
    """

    :param user_id:
    :param chore_id:
    :return:
    """
    async with db_session.create_async_session() as session:
        query = select(Chore).filter(Chore.user_id == user_id)
        if chore_id:
            query = query.filter(Chore.id == chore_id)
            # query = query.filter(Chore.type == 'recurring')

        result = await session.execute(query)
        chores = result.scalars()
        return list({r for r in chores})

# async def get_chores_by_user_email(email: str) -> Optional[List[Chore]]:
#     async with db_session.create_async_session() as session:
#         query = select(Chore).filter(Chore.email == email)
#         result = await session.execute(query)
#         return result.fetchall()
