from pathlib import Path
from typing import Optional

import fastapi
from fastapi import File, UploadFile
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
from starlette.staticfiles import StaticFiles
import fastapi_chameleon

from data import db_session, load_fake_data

# web app views
from views import home, account, chores, jwt

# api routes
from api import chores as chores_api
from api import jwt as jwt_api
from api.graphql import routes as graphql_api

app = fastapi.FastAPI(
    title="ChoreViz API",
    description='''
        This is the API documentation.  Always include the following headers object on API requests:\n
        {Authorization: <API_KEY>}
    ''',
    version="0.0.1"
)


# app.add_middleware(GZipMiddleware, minimum_size=1000)


def main():
    configure(dev_mode=True)
    uvicorn.run(app=app, port=8000, host='127.0.0.1')


def configure(dev_mode: bool):
    """
    Configures app components before running server
    :param dev_mode:
    :return:
    """
    configure_templates(dev_mode)
    configure_routes()
    configure_db()
    load_fake_data.run()


def configure_templates(dev_mode: bool):
    """
    Configures templates
    :param dev_mode:
    :return:
    """
    fastapi_chameleon.global_init('templates', auto_reload=dev_mode)


def configure_routes():
    """
    Configures the static files folder
    Configures the web and api routes for the app
    :return:
    """
    # mount static folder
    app.mount('/static', StaticFiles(directory='static'), name='static')

    # web app page routes
    app.include_router(home.router, include_in_schema=False)
    app.include_router(account.router, include_in_schema=False)
    app.include_router(chores.router, include_in_schema=False)

    # web jwt example endpoints
    app.include_router(jwt.router)

    # api endpoints
    app.include_router(chores_api.router)
    app.include_router(jwt_api.router)

    # graphql endpoint
    app.include_router(graphql_api.router)


def configure_db(conn_str: Optional[str] = False):
    """
    Configures the database
    :return:
    """
    if not conn_str:
        file = (Path(__file__).parent / 'db' / 'db.sqlite').absolute()
        print(file)
        db_session.global_init(file.as_posix())
    else:
        db_session.global_init(conn_str)


if __name__ == '__main__':
    print("Running on port 8000")
    main()
    uvicorn.run(app=app, port=8000, host='127.0.0.1', reload=True)
else:
    configure(dev_mode=True)
