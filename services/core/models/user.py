from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone


class UserManager(auth_models.BaseUserManager):
    def create_user(self, email, password=None, is_active=False, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError("The given email address must be set")
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email, is_staff=False, is_active=is_active, is_superuser=False, last_login=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    ###########################################################################
    def create_superuser(self, email, password, **extra_fields):
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_active = False
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser

    ###########################################################################
    def get_queryset(self):
        return super().get_queryset().exclude(is_deleted=True)

    # Returns not filtered queryset(include deleted users)
    # Usage: User.objects.get_base_queryset(is_blocked=False)
    def get_base_queryset(self):
        return super().get_queryset()


###############################################################################
###############################################################################
class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_login_blocked = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    ###########################################################################
    ###########################################################################
    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        app_label = "core"

    def block(self):
        self.is_blocked = True
        self.save()

    def unblock(self):
        self.is_blocked = False
        self.save()