import graphene
import app.models as models
from app.graphql.base import BaseQuery
from .types import Joke


class Query(BaseQuery):
    jokes = graphene.List(Joke)
    joke = graphene.Field(Joke, id=graphene.ID())

    def resolve_jokes(self, info):
        session = info.context['session']
        jokes =  session.query(models.Joke) \
            .all()

        return jokes

    def resolve_joke(self, info, id):
        session = info.context['session']
        return session.query(models.Joke) \
            .filter(
                models.Joke.id==id
            ) \
            .one()