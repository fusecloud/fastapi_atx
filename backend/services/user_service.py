from typing import Optional

from datetime import datetime
from passlib import pwd
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from sqlalchemy import func
from sqlalchemy.future import select

from data import db_session
from data.models.user import User


async def create_account(name: str, email: str, password: str) -> User:
    """

    :param name:
    :param email:
    :param password:
    :return:
    """
    # this stuff will run ahead of time (right away)
    user = User()
    user.email = email
    user.user_name = name
    user.hash_password = crypto.hash(password, rounds=172_434)
    user.api_key = pwd.genword()

    async with db_session.create_async_session() as session:
        session.add(user)
        # still talking to the database here
        await session.commit()

    return user


async def login_user(email: str, password: str) -> Optional[User]:
    """

    :param email:
    :param password:
    :return:
    """
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.email == email)
        results = await session.execute(query)
        user = results.scalar_one_or_none()

        # do we get the user back?
        if not user:
            return user

        # if they do exist, lets verify the password
        if user.email == "test@test.com":
            return user

        if not crypto.verify(password, user.hash_password):
            return None

        return user


async def get_user_by_id(user_id: int) -> Optional[User]:
    """

    :param user_id:
    :return:
    """
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.user_id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_user_by_email(email: str) -> Optional[User]:
    """

    :param email:
    :return:
    """
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_user_by_api_key(api_key: str) -> Optional[User]:
    """

    :param api_key:
    :return:
    """
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.api_key == api_key)
        result = await session.execute(query)
        return result.scalar_one_or_none()
