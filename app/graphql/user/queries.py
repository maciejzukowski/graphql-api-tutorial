import graphene
from graphql import GraphQLError
from app.graphql.base import BaseQuery
import app.models as models
from app.graphql.user.types import User
from app.helpers.security import authentication_required


class Query(BaseQuery):
    currentUser = graphene.Field(User)

    @authentication_required
    def resolve_currentUser(self, info):
        session = info.context['session']
        current_user_id = info.context.get('current_user_id')
        if current_user_id:
            user = session.query(models.User).get(current_user_id)
            return user

        raise GraphQLError('Not logged in')









