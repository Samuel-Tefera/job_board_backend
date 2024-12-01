"""Database models."""

from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
)


class JobCategory(models.Model):
    """Model for Job Categories"""
    category_name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class UserManager(BaseUserManager):
    """User models manager."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set.')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class UserType(models.TextChoices):
    """Enumerated user type choices"""
    JOB_FINDER = 'JF', 'Job Finder'
    JOB_POSTER = 'JP', 'Job Poster'
    Admin = 'Ad', 'Admin'


class GenderChoices(models.TextChoices):
    """Enumerated user gender choices"""
    MALE = 'M', 'Male'
    Female = 'F', 'Female'


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""
    first_name = models.CharField(max_length=34)
    last_name = models.CharField(max_length=34)
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices
    )
    user_type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.JOB_FINDER
    )
    bio = models.TextField()
    profile_pic_url = models.URLField(max_length=200, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')
    resume_url = models.URLField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    job_category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'bio', 'gender']
