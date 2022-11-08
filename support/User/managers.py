from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Represents the manager for the creation of the user."""

    def create_user(self, login, email, first_name, last_name, password, alias=None):
        user = self.model(
            login=login,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
                    )
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, login, email, first_name, last_name, password):
        user = self.create_user(login=login, email=email, first_name=first_name,last_name=last_name, password=password)
        user.is_staff()
        user.is_superuser = True
        user.save()
        return user