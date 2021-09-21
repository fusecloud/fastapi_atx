import sqlalchemy
from colorama import Fore
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from datetime import datetime
from typing import Optional
from passlib import pwd
import pandas as pd
import numpy as np

skip_fake_load = False


def run(conn_str: Optional[str] = "sqlite+pysqlite:////app/backend/db/db.sqlite"):
    if skip_fake_load:
        return

    user_email = "test@test.com"
    user_name = "Johnny Test"
    occupation = "Developer"
    user_id = 1051
    password = "testtesttest"  # pwd.genword()
    api_key = "testtesttest"  # pwd.genword()

    # load fake users
    df_users = \
        pd.DataFrame({
            "user_id": [user_id],
            "user_name": [user_name],
            "email": [user_email],
            "occupation": [occupation],
            "hash_password": [password],
            "api_key": [api_key],
            "created_date": [datetime.now()],
            "last_login": [datetime.now()],
            "profile_image_url": [""]
        })

    df_users.to_sql(name="users", con=conn_str, index=False, if_exists="append")
    df_users_loaded = pd.read_sql_query(sql="select * from users", con=conn_str)

    print(Fore.BLUE + "Users loaded: ")
    print(Fore.BLUE + str(df_users_loaded))

    # load fake chores
    df_chores = \
        pd.DataFrame({
            "chore_id": [259821, 259822, 259823],
            "user_id": [user_id, user_id, user_id],
            "chore_name": ["vacuum", "water plants", "clean kitchen"],
            "category": ["cleaning", "gardening", "cleaning"],
            "type": ["recurring", "recurring", "recurring"],
            "alert_days": [14, 3, 17]

        })

    try:
        df_chores.to_sql(name="chores", con=conn_str, index=False, if_exists="append")
    except sqlalchemy.ext.IntegrityError:
        df_chores['chore_id'] = df_chores['chore_id'] + np.random.randint(1, 1_000_000)
        df_chores['user_id'] = df_chores['user_id'] + np.random.randint(1, 1_000_000)
        df_chores.to_sql(name="chores", con=conn_str, index=False, if_exists="append")

    df_chores_loaded = pd.read_sql_query(sql="select * from chores", con=conn_str)

    print(Fore.CYAN + "Chores loaded: ")
    print(Fore.CYAN + str(df_chores_loaded))
    print(Fore.GREEN + f"Test Email: {user_email}")
    print(Fore.LIGHTRED_EX + f"Test Password: {password}")
    print(Fore.LIGHTRED_EX + f"Test API Key: {api_key}")
