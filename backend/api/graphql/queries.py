import graphene
from api.models.chore import Chore as ChorePydantic
from api.models.user import User as UserPydantic
from api.models.graphql import User, Chore, UserChore
from services import graphql_service

# get list of table fields
chore_fields = list(ChorePydantic.schema().get('properties').keys())
user_fields = list(UserPydantic.schema().get('properties').keys())

# initially false
join_flag = False


class Query(graphene.ObjectType):
    user_chores = graphene.List(UserChore)

    async def resolve_user_chores(self, info):
        # get the fields requested from graphql
        requested_fields = [f.name.value for f in info.field_asts[0].selection_set.selections]
        print("Fields requested")
        print("---------------------------------------------")
        print(requested_fields)

        requested_fields_chores = \
            [r for r in requested_fields if r in chore_fields]
        requested_fields_user = \
            [r for r in requested_fields if r in user_fields]

        records = await graphql_service.query(
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
