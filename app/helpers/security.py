from functools import wraps

from flask import request
from graphql import GraphQLError
import app.models as m



def authentication_required(func):
    @wraps(func)
    def wrap(obj, info, **kwargs):
        current_user_id = m.User.decode_auth_token(request)

        if not current_user_id:
            raise GraphQLError("Not authorized")

        info.context['current_user_id'] = current_user_id

        return func(obj, info, **kwargs)

    return wrap

