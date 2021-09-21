import graphene
from api.models.graphql import Chore
from services import chore_service


class CreateChore(graphene.Mutation):
    class Arguments:
        chore_name = graphene.String()
        category = graphene.String()
        type = graphene.String()
        alert_days = graphene.Int()

    Output = Chore

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

        chore = Chore()
        chore.user_id = user_id
        chore.chore_name = chore_name
        chore.category = category
        chore.type = type
        chore.alert_days = alert_days

        # insert into db
        await chore_service.add_chore(
            user_id=chore.user_id,
            name=chore.chore_name,
            category=chore.category,
            type=chore.type,
            alert_days=chore.alert_days
        )

        return chore


# todo: expiriment with optional parameters
class EditChore(graphene.Mutation):
    class Arguments:
        chore_id = graphene.Int()
        chore_name = graphene.String()
        category = graphene.String()
        type = graphene.String()
        alert_days = graphene.Int()

    Output = Chore

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

        chore = Chore()
        chore.user_id = user_id
        chore.chore_name = chore_name
        chore.category = category
        chore.type = type
        chore.alert_days = alert_days

        # insert into db
        await chore_service.edit_chore(
            id=chore_id,
            user_id=chore.user_id,
            name=chore.chore_name,
            category=chore.category,
            type=chore.type,
            alert_days=chore.alert_days
        )

        return chore


class RemoveChore(graphene.Mutation):
    class Arguments:
        chore_id = graphene.Int()

    Output = Chore

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

        return chore_id


class Mutation(graphene.ObjectType):
    create_chore = CreateChore.Field()
    edit_chore = EditChore.Field()
    delete_chore = RemoveChore.Field()
