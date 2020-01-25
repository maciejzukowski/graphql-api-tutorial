import graphene
import os
import importlib
from inspect import getmembers, isclass
from graphene import ObjectType

def schema_operations_builder(operationName, operationModule, operationBase, clsName):

    op_base_classes = build_base_classes(operationName, operationModule, operationBase, clsName)

    if len(op_base_classes) == 0:
        raise ValueError("Found no '{0}' classes in '{1}' module of subdirectories.".format(
            operationBase, operationModule
        ))

    properties = {}
    # filter on scopes before this
    if operationBase == 'BaseQuery':
        for base_class in op_base_classes:
            properties.update(base_class.__dict__['_meta'].fields)

        return type(operationName, tuple(op_base_classes), properties)
    elif operationBase == 'BaseMutation':
        for base_class in op_base_classes:
            mutationName = base_class.__name__[0].lower() + base_class.__name__[1:]
            properties.update({mutationName:base_class.Field()})

        return type(operationName, tuple([ObjectType]), properties)

    elif operationBase == 'BaseType':
        return op_base_classes

    return None


def build_base_classes(operationName, operationModule, operationBase, clsName):
    class OperationAbstract(ObjectType):
        scopes = ['unauthorized']
        pass

    current_directory = os.path.dirname(os.path.abspath(__file__))
    current_module = current_directory.split('/')[-1]
    subdirectories = [
        x for x in os.listdir(current_directory)
            if os.path.isdir(os.path.join(current_directory, x))
               and x != '__pycache__'
               and x != 'root'
    ]
    op_base_classes = []

    for directory in subdirectories:
        try:
            module = importlib.import_module(
                '{0}.{1}.{2}'.format("app.graphql", directory, operationModule)
            )
            if module:
                classes = [x for x in getmembers(module, isclass)]
                opers = [x[1] for x in classes if x[1].__bases__[0].__name__ == operationBase and x[0] != operationBase]
                op_base_classes += opers
            else:
                print("Something wrong with graphql folder structure. "+current_directory)

        except ImportError: # ModuleNotFoundError?
            pass

    return op_base_classes

ALL_QUERIES = schema_operations_builder(
    operationName='Query',
    operationModule='queries',
    operationBase='BaseQuery',
    clsName='Query'
)

ALL_MUTATIONS = schema_operations_builder(
    'Mutations',
    'mutations',
    'BaseMutation',
    'Mutation'
)

ALL_TYPES = schema_operations_builder(
    'Types',
    'types',
    'BaseType',
    'Type'
)

schema = graphene.Schema(query=ALL_QUERIES, mutation=ALL_MUTATIONS, types=ALL_TYPES)
