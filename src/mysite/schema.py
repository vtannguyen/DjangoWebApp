import graphene
import yelpCamp.schema


class Query(yelpCamp.schema.Query, graphene.ObjectType):
    pass


class Mutation(yelpCamp.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)