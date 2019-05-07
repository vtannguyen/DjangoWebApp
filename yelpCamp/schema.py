import graphene
from django.utils import timezone
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Campground, Comment
from django.contrib.auth.models import User


class CampgroundType(DjangoObjectType):
    class Meta:
        model = Campground


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(ObjectType):
    campground = graphene.Field(CampgroundType, id=graphene.Int())
    campgrounds = graphene.List(CampgroundType)
    comments = graphene.List(CommentType, id=graphene.Int())

    def resolve_campground(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Campground.objects.get(pk=id)

        return None

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_comments(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Comment.objects.filter(campground__id__exact=id)

        return None

    def resolve_campgrounds(self, info, **kwargs):
        return Campground.objects.all()


class CampgroundInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    imageUrl = graphene.String()
    price = graphene.Float()


class CommentInput(graphene.InputObjectType):
    text = graphene.String()


class CreateCampground(graphene.Mutation):
    class Arguments:
        input = CampgroundInput(required=True)
        username = graphene.String(required=True)

    ok = graphene.Boolean()
    campground = graphene.Field(CampgroundType)

    @staticmethod
    def mutate(root, info, username, input=None):
        ok = False
        user = User.objects.get(username__exact=username)
        if user:
            ok = True
            campground_instance = Campground(
                name=input.name,
                description=input.description,
                imageUrl=input.imageUrl,
                price=input.price,
                user=user
            )
            campground_instance.save()
            return CreateCampground(ok=ok, campground=campground_instance)

        return CreateCampground(ok=ok, campground=None)


class UpdateCamground(graphene.Mutation):
    class Argument:
        input = CampgroundInput(required=True)
        id = graphene.String(required=True)

    ok = graphene.Boolean()
    campground = graphene.Field(CampgroundType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        campground_instance = Campground.objects.get(pk=id)
        if campground_instance:
            ok = True
            campground_instance.name = input.name
            campground_instance.imageUrl = input.imageUrl
            campground_instance.description = input.description
            campground_instance.price = input.price
            campground_instance.save()
            return UpdateCamground(ok=ok, campground=campground_instance)

        return UpdateCamground(ok=ok, campground=None)


class CreateComment(graphene.Mutation):
    class Argument:
        input = CommentInput(required=True)
        campgroundId = graphene.Int(required=True)
        username = graphene.String(required=True)

    ok = graphene.Boolean()
    comment = graphene.Field(CommentType)

    @staticmethod
    def mutate(root, info, campgroundId, username, input=None):
        ok = False
        campground_instance = Campground.objects.get(pk=campgroundId)
        if campground_instance:
            user = User.objects.get(username__exact=username)
            if user:
                ok = True
                comment_instance= Comment(
                    text=input.text,
                    user=user,
                    campground=campground_instance,
                    timestamp=timezone.now()
                )
                comment_instance.save()
                return CreateCampground(ok=ok, comment=comment_instance)

        return CreateCampground(ok=ok, comment=None)


class Mutation(graphene.ObjectType):
    create_campground = CreateCampground.Field()
    update_campground = UpdateCamground.Field()
    create_comment = CreateComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
