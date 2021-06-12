from typing import Optional, List

from data.models.chore import Chore
from data.models.user import User
from sqlalchemy import text

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


async def edit_chore(id: int, name: str, category: str, type: str, alert_days: int,
                     user_id: Optional[int] = False, api_key: Optional[str] = False):
    async with db_session.create_async_session() as session:
        sql = f'''
        update chores
        set 
        name = '{name}',
        category = '{category}',
        type = '{type}',
        alert_days = {alert_days}
        where id = {id}
        {"and user_id = " + str(user_id) if user_id
        else "and user_id IN (select id from users where api_key = '" + api_key + "')"}
        '''
        print(sql)
        await session.execute(sql)
        await session.commit()


async def remove_chore(id: int, user_id: Optional[int] = False, api_key: Optional[str] = False):
    async with db_session.create_async_session() as session:
        sql = f'''
        delete from chores 
        where id = {id}
        {"and user_id = " + str(user_id) if user_id
        else "and user_id IN (select id from users where api_key = '" + api_key + "')"}
        '''
        print(sql)
        await session.execute(sql)
        await session.commit()
        # query = select(Chore).filter(Chore.id == id).delete()
        # session.query(Chore).filter(Chore.id == id).delete()
        # await session.commit()
        # await session.execute(query)


async def get_user_chores(user_id: int, chore_id: Optional[int] = False) -> Optional[List[Chore]]:
    """

    :param api_key:
    :param user_id:
    :param chore_id:
    :return:
    """

    print("user_id")
    print(user_id)
    print(type(user_id))

    # print("api_key")
    # print(api_key)
    # print(type(api_key))

    print("chore_id")
    print(chore_id)
    print(type(chore_id))

    async with db_session.create_async_session() as session:
        query = \
            (
                select(Chore)
                    .filter(Chore.user_id == user_id)
            )

        if chore_id:
            query = query.filter(Chore.id == chore_id)

        result = await session.execute(query)
        chores = result.scalars()

        return list({r for r in chores})
