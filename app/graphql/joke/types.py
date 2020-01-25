from graphene_sqlalchemy import SQLAlchemyObjectType
from app.graphql.base import BaseType
import app.models as m


class Joke(BaseType, SQLAlchemyObjectType):

    class Meta:
        model = m.Joke
