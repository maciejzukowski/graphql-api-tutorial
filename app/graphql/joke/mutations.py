import graphene
from graphql import GraphQLError
from app.graphql.base import BaseMutation
from app.helpers.security import authentication_required
from .types import Joke
import app.models as models


class CreateJoke(BaseMutation):
    class Arguments:
        text = graphene.String()

    ok = graphene.Boolean()
    joke = graphene.Field(lambda: Joke)

    @authentication_required
    def mutate(self, info, text):
        session = info.context['session']
        current_user_id = info.context['current_user_id']
        joke = models.Joke(
            text=text,
            user_id=current_user_id
        )
        session.add(joke)
        session.commit()

        return CreateJoke(joke=joke, ok=True)


class EditJoke(BaseMutation):
    class Arguments:
        id = graphene.ID()
        text = graphene.String()

    ok = graphene.Boolean()
    joke = graphene.Field(lambda: Joke)

    @authentication_required
    def mutate(self, info, id, text):
        session = info.context['session']
        current_user_id = info.context['current_user_id']

        joke = session.query(models.Joke) \
            .filter(
                models.Joke.id == id,
                models.Joke.user_id==current_user_id
            ) \
            .one_or_none()

        if not joke:
            raise GraphQLError('Not authorized')

        joke.text=text
        session.commit()

        return EditJoke(joke=joke, ok=True)