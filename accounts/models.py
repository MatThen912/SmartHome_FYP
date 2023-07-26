from django.conf import settings
from random import randrange
from django.core import validators
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission

import uuid

USER_ROLE = (
    ('Super Admin', 'Super Admin'),
    ('Admin', 'Admin'),
    ('User', 'User'),
)


class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, farm_code, name, dob, email, role, contact_number, password):

        user = self.model(
            username=username,
            farm_code=farm_code,
            name=name,
            dob=dob,
            email=self.normalize_email(email),
            role=role,
            contact_number=contact_number,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, name, dob, email, role, contact_number, password):

        user = self.model(
            username=username,
            name=name,
            dob=dob,
            email=self.normalize_email(email),
            role=role,
            contact_number=contact_number,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)

        return user





class Account(AbstractBaseUser, PermissionsMixin):

    account_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(
        max_length=60, unique=True, blank=True, null=True)
    role = models.CharField(choices=USER_ROLE, max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="img/profile")
    contact_number = models.CharField(max_length=11, unique=True, blank=True, null=True, validators=[
        RegexValidator(
            regex='(\+?0{1,9})[0-46-9][0-9]{7,9}$',
            message='Please use the correct contact number',
            code='invalid_contact_number'
        ), ])
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'dob', 'email',
                       'role', 'contact_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.name







class LoggedInUser(models.Model):
    user = models.OneToOneField(
        Account, related_name='logged_in_user', on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Userlog (models.Model):

    user = models.CharField(max_length=200, blank=True, null=True)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP')
    device=models.CharField(max_length=200, blank=True, null=True)
    last_activation_date = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username