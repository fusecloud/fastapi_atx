from typing import Optional, List, Dict
from fastapi import Header, Body, Depends
from api.models.chore import Chore
from api.models.user import User
from starlette import status
from starlette.responses import Response
from services import chore_service, user_service
from infrastructure.api_auth import get_api_key
from fastapi import Security, HTTPException

import fastapi
import graphene
from starlette.graphql import GraphQLApp
from api.graphql.queries import QueryTest, Query
from graphql.execution.executors.asyncio import AsyncioExecutor

router = fastapi.APIRouter()

# To disable graphql interface in production
# graphiql=False in GraphQLApp constructor
router.add_route(
    "/graphql_test",
    GraphQLApp(
        schema=graphene.Schema(query=QueryTest)
    )
)

router.add_route(
    "/graphql",
    GraphQLApp(
        schema=graphene.Schema(query=Query, auto_camelcase=False),
        executor_class=AsyncioExecutor,
    )
)
