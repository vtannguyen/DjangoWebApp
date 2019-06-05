from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            userSet = UserModel.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).distinct()
        except UserModel.DoesNotExist:
            return None
        else:
            for user in userSet:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
        return None
