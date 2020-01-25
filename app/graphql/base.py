from graphene.types.objecttype import ObjectType
from graphene.types.mutation import Mutation


class BaseType(ObjectType):
    pass

class BaseQuery(ObjectType):
    pass


class BaseMutation(Mutation):
    def mutate(self, *arg, **kwargs):
        pass

