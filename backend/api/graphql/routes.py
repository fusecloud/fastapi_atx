from typing import Optional, List, Dict
from fastapi import Header, Body, Depends
from api.models.chore import Chore
from api.models.user import User
from starlette import status
from starlette.responses import Response, HTMLResponse
from services import chore_service, user_service
from infrastructure.api_auth import get_api_key
from fastapi import Security, HTTPException

import fastapi
import graphene
from starlette.graphql import GraphQLApp
from starlette.requests import Request
from api.graphql.queries import QueryTest, Query
from api.graphql.mutations import Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor

router = fastapi.APIRouter()

graphql_app = \
    GraphQLApp(
        schema=graphene.Schema(
            query=Query,
            mutation=Mutation,
            auto_camelcase=False,

        ),
        graphiql=False,  # False for production
        executor_class=AsyncioExecutor,
    )


@router.post('/graphql', dependencies=[Security(get_api_key)])
async def graphql_endpoint(request: Request, user: User = Depends(get_api_key)):
    print("user.user_id")
    print(user.user_id)
    request.state.user_id = user.user_id
    print("request.state.user_id")
    print(request.state.user_id)

    print('request.headers')
    print(request.headers)
    return await graphql_app.handle_graphql(request=request)

# @router.add_route('/graphql', methods=['GET', 'POST'])
# async def graphql_endpoint(request: Request):
#     # print("user.user_id")
#     # print(user.user_id)
#     # request.state.user_id = user.user_id
#     # print("request.state.user_id")
#     # print(request.state.user_id)
#
#     print('request.headers')
#     print(request.headers)
#     return await graphql_app.handle_graphql(request=request)
