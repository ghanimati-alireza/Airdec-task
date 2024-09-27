from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel
import uuid

phone_regex = RegexValidator(
    regex=r"^\+{1}989\d{9}$",
    message="Phone number must be entered in the format: "
            "'+989xxxxxxxxx'. Up to 14 digits allowed.",
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name=_("Email Address"), )
    birthday = models.DateField(null=True, blank=True, verbose_name=_("Birthday"))
    phone_number = models.CharField(max_length=20, null=True, blank=True,
                                    validators=[phone_regex], unique=True, verbose_name=_("Phone Number"))
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return str(self.email)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
