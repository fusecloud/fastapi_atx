import graphene
from api.graphql.types import Chore
from services import chore_service


class CreateChore(graphene.Mutation):
    class Arguments:
        chore_name = graphene.String()
        category = graphene.String()
        type = graphene.String()
        alert_days = graphene.Int()

    ok = graphene.Boolean()
    chore = graphene.Field(lambda: Chore)

    async def mutate(
            self, info,
            chore_name,
            category,
            type,
            alert_days
    ):
        # get the metadata of the request
        request_data = info.context['request']

        # get the user_id of the requesting user
        user_id = request_data.state.user_id

        chore = Chore(
            user_id=user_id,
            chore_name=chore_name,
            category=category,
            type=type,
            alert_days=alert_days
        )

        # insert into db
        await chore_service.add_chore(
            user_id=chore.user_id,
            name=chore.chore_name,
            category=chore.category,
            type=chore.type,
            alert_days=chore.alert_days
        )

        ok = True

        return CreateChore(chore=chore, ok=ok)


class EditChore(graphene.Mutation):
    class Arguments:
        chore_id = graphene.Int()
        chore_name = graphene.String()
        category = graphene.String()
        type = graphene.String()
        alert_days = graphene.Int()

    ok = graphene.Boolean()
    chore = graphene.Field(lambda: Chore)

    async def mutate(
            self, info,
            chore_id,
            chore_name,
            category,
            type,
            alert_days
    ):
        # get the metadata of the request
        request_data = info.context['request']

        # get the user_id of the requesting user
        user_id = request_data.state.user_id

        # construct the chore
        chore = Chore(
            user_id=user_id,
            chore_name=chore_name,
            category=category,
            type=type,
            alert_days=alert_days
        )

        # insert into db
        await chore_service.edit_chore(
            id=chore_id,
            user_id=chore.user_id,
            name=chore.chore_name,
            category=chore.category,
            type=chore.type,
            alert_days=chore.alert_days
        )

        ok = True

        return EditChore(chore=chore, ok=ok)
        # return chore


class RemoveChore(graphene.Mutation):
    class Arguments:
        chore_id = graphene.Int()

    ok = graphene.Boolean()

    async def mutate(
            self, info,
            chore_id
    ):
        # get the metadata of the request
        request_data = info.context['request']

        # get the user_id of the requesting user
        user_id = request_data.state.user_id

        # insert into db
        await chore_service.remove_chore(
            id=chore_id,
            user_id=user_id
        )

        ok = True

        return RemoveChore(ok=ok)


class Mutation(graphene.ObjectType):
    create_chore = CreateChore.Field()
    edit_chore = EditChore.Field()
    remove_chore = RemoveChore.Field()
