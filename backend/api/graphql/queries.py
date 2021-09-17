import graphene
from api.models.graphql_query_result import QueryResultGQL
from api.models.chore import Chore
from api.models.user import User
from services import graphql_service

# get list of table fields
chore_fields = list(Chore.schema().get('properties').keys())
chore_fields = ["chore_" + x if x == "id" else x for x in chore_fields]
chore_fields = ["chore_" + x if x == "name" else x for x in chore_fields]

user_fields = list(User.schema().get('properties').keys())
user_fields = ["user_" + x if x == "id" else x for x in user_fields]
user_fields = ["user_" + x if x == "name" else x for x in user_fields]

# initially false
join_flag = False


class QueryTest(graphene.ObjectType):
    # "hello" needs to be included in fn name below
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        # "*_hello" needs to match ^
        return "Hello " + name


class Query(graphene.ObjectType):
    results = graphene.List(QueryResultGQL)
    # results = graphene.List(graphene.ObjectType)

    async def resolve_results(self, info):
        # get the fields requested from graphql
        requested_fields = [f.name.value for f in info.field_asts[0].selection_set.selections]
        print("Fields requested")
        print("---------------------------------------------")
        print(requested_fields)

        # see if we need to do a join
        requested_fields_chores = \
            [r for r in requested_fields if r in chore_fields]
        requested_fields_user = \
            [r for r in requested_fields if r in user_fields]

        requested_fields_chores

        records = await graphql_service.query(
            user_fields=requested_fields_user if len(requested_fields_user) else None,
            chore_fields=requested_fields_chores if len(requested_fields_chores) else None,
        )

        return records
