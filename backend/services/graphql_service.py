from data import db_session
from typing import Optional


async def query(user_fields: Optional[list] = None, chore_fields: Optional[list] = None):
    async with db_session.create_async_session() as session:
        sql = f'''
        select
        {", ".join(["c." + x for x in chore_fields]) if chore_fields else ""}
        {"," if user_fields and chore_fields else ""}
        {", ".join(["u." + x for x in user_fields]) if user_fields else ""}
        from 
        {"chores c " if chore_fields else ""}
        {"join " if user_fields and chore_fields else ""}
        {"users u " if user_fields else ""}
        {"on c.id = u.user_id " if user_fields and chore_fields else ""}
        /*connector comma between fields sets*/
        /*table selections*/
        /*join_condition*/
        '''

        # sql = "select * from chores"

        sql = sql.replace("\n", "").replace("  ", " ").strip()
        print("sql query:")
        print(sql)

        result = await session.execute(sql)
        q_chores = result.scalars()

        print("q_chores")
        print(q_chores)

        print("list({r for r in q_chores})")
        print(list({r for r in q_chores}))

        return q_chores  # list({r for r in chores})
