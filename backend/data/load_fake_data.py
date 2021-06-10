from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from datetime import datetime
from typing import Optional
from passlib import pwd

import pandas as pd


def run(conn_str: Optional[str] = "sqlite+pysqlite:////app/backend/db/db.sqlite"):
    user_email = "test@test.com"
    user_name = "Johnny Test"
    user_id = 1051
    password = pwd.genword()

    # load fake users
    df_users = \
        pd.DataFrame({
            "id": [user_id],
            "name": [user_name],
            "email": [user_email],
            "hash_password": [password],
            "api_key": [pwd.genword()],
            "created_date": [datetime.now()],
            "last_login": [datetime.now()],
            "profile_image_url": [""]
        })

    df_users.to_sql(name="users", con=conn_str, index=False, if_exists="append")
    df_users_loaded = pd.read_sql_query(sql="select * from users", con=conn_str)

    print("Users loaded: ")
    print(df_users_loaded)

    # load fake chores
    df_chores = \
        pd.DataFrame({
            "id": [259821, 259822, 259823],
            "user_id": [user_id, user_id, user_id],
            "name": ["vacuum", "water plants", "clean kitchen"],
            "category": ["cleaning", "gardening", "cleaning"],
            "type": ["recurring", "recurring", "recurring"],
            "alert_days": [14, 3, 17]

        })

    df_chores.to_sql(name="chores", con=conn_str, index=False, if_exists="append")
    df_chores_loaded = pd.read_sql_query(sql="select * from chores", con=conn_str)

    print("Chores loaded: ")
    print(df_chores_loaded)
    print(f"Test Email: {user_email}")
    print(f"Test Password: {password}")
