from pathlib import Path
from typing import Optional

import fastapi
import uvicorn
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
import fastapi_chameleon

from data import db_session, load_fake_data

# web app views
from views import home, account, chores

# api routes
# from api import chores

app = fastapi.FastAPI()


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
    # links to the fastapi.APIRouter() object in views modules
    app.include_router(home.router)
    app.include_router(account.router)
    app.include_router(chores.router)

    # todo api routes
    # app.include_router(chores.api)
    # api.include_router(sse_api.router)
    # api.include_router(lab_api.router)
    # api.include_router(chartlab_api.router)


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
