from django.db import models
from django.utils.translation import gettext_lazy as _



class BaseUserManager(models.Manager):
    @classmethod
    def normalize_username(cls, username):
        """
        Normalize the username by lowercasing it.
        """
        username = username or ""
        if len(username) < 4:
            raise ValueError(_('username must have at least 4 characters'))
        return username.lower()

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError(_('Users must have a username'))

        user = self.model(
            username=self.normalize_username(username)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
