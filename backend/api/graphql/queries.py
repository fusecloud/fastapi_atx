import graphene
from api.models.chore import Chore as ChorePydantic
from api.models.user import User as UserPydantic
from api.graphql.types import User, Chore, UserChore
from services import chore_service

# get list of table fields
chore_fields = list(ChorePydantic.schema().get('properties').keys())
user_fields = list(UserPydantic.schema().get('properties').keys())


class Query(graphene.ObjectType):
    user_chores = graphene.List(UserChore)

    async def resolve_user_chores(self, info):
        # get the metadata of the request
        request_data = info.context['request']
        # get the user_id of the requesting user
        user_id = request_data.state.user_id

        # get the fields requested from graphql
        requested_fields = [f.name.value for f in info.field_asts[0].selection_set.selections]

        # match up requested fields to table fields
        requested_fields_chores = \
            [r for r in requested_fields if r in chore_fields]
        requested_fields_user = \
            [r for r in requested_fields if r in user_fields]

        # await query results
        records = await chore_service.get_user_and_chore_data(
            user_id=user_id,
            user_fields=requested_fields_user if len(requested_fields_user) else [],
            chore_fields=requested_fields_chores if len(requested_fields_chores) else [],
        )

        return records


class QueryTest(graphene.ObjectType):
    # "hello" needs to be included in fn name below
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        # "*_hello" needs to match ^
        return "Hello " + name
