from graphene_sqlalchemy import SQLAlchemyObjectType
from app.graphql.base import BaseType
from app.models import User as UserModel

class User(BaseType, SQLAlchemyObjectType):

    class Meta:
        model = UserModel
        exclude_fields=('password_hash')