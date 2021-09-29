from fastapi import Depends
from fastapi import Security
import fastapi
import graphene
from starlette.graphql import GraphQLApp
from starlette.requests import Request
from api.graphql.queries import Query
from api.graphql.mutations import Mutation
from api.models.user import User
from infrastructure.api_auth import get_api_key
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


@router.post('/graphql',
             dependencies=[Security(get_api_key)],
             name="GraphQL Interface"
             )
async def graphql_endpoint(request: Request, user: User = Depends(get_api_key)):
    """
    Interface for GraphQL queries and mutations.

    Example Query:

    \n
    {\n
      \tuser_chores {\n
        \tuser_name\n
        \toccupation\n
        \temail\n
        \tchore_id\n
        \tchore_name\n
        \ttype\n
        \talert_days\n
      \t}\n
    }\n

    Example Mutation:

    \n
    mutation {\n
        \tcreate_chore(\n
            \t\tchore_name: "TEST GraphQL"\n
            \t\tcategory: "Dev"\n
            \t\ttype: "one-time"\n
            \t\talert_days: 1\n
        \t) {\n
            \tchore {\n
            \t\tuser_id\n
            \t\tchore_name\n
            \t\tcategory\n
            \t\ttype\n
            \t}\n
            \tok\n
        }\n
    }\n
    """

    # extract the user_id from header's api key and pass to request state
    request.state.user_id = user.user_id

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
