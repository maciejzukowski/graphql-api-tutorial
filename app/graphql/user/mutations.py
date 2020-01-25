import graphene
from graphql import GraphQLError
from app.graphql.base import BaseMutation
import app.models as models
from app.helpers.security import authentication_required
from .types import User

class SignUp(BaseMutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User)
    token = graphene.String()

    def mutate(self, info, email, password):
        #do some validation
        if len(email) < 4 or len(password) < 4:
            raise GraphQLError("invalid length")

        session = info.context['session']
        email = email.lower().strip()
        exists = session.query(models.User).filter(models.User.email == email).count()

        if exists:
            raise GraphQLError("User already exists")

        user = models.User(email=email)
        user.set_password(password)
        session.add(user)
        session.commit()

        return SignUp(user=user, ok=True, token=user.encode_auth_token().decode())

class Login(BaseMutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()
    token = graphene.String()
    user = graphene.Field(lambda: User)

    def mutate(self, info, email, password):
        session = info.context['session']
        email = email.lower().strip()
        user = session.query(models.User).filter(models.User.email == email).one_or_none()

        if not user or not user.check_password(password):
            raise GraphQLError('Invalid login')

        return Login(user=user, ok=True, token=user.encode_auth_token().decode())


class ChangePassword(BaseMutation):
    class Arguments:
        old_password = graphene.String()
        new_password = graphene.String()

    ok = graphene.Boolean()

    @authentication_required
    def mutate(self, info, old_password, new_password):
        session = info.context['session']
        current_user_id = info.context['current_user_id']
        user = session.query(models.User).get(current_user_id)

        if not user or not user.check_password(old_password):
            raise GraphQLError('Invalid current password')

        user.set_password(new_password)
        session.commit()

        return ChangePassword(ok=True)

class Logout(BaseMutation):
    ok = graphene.Boolean()

    @authentication_required
    def mutate(self, info):
        # Not much to do on server
        # Need to delete token client side

        return Logout(ok=True)