from os.path import splitext
from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import UserManager
from yogalevels.models import YogaLevel
from yogaposes.models import YogaPose


def profile_picture_folder(_, filename):
    _, ext = splitext(filename)
    return f"pfp/{uuid4()}{ext}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=70)
    profile_picture = models.ImageField(
        upload_to=profile_picture_folder,
        max_length=50,
        blank=True,
        db_column="profile_picture_file_path",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name


class YogaUser(models.Model):
    _INITIAL_POINTS = 0

    @staticmethod
    def get_default_yoga_level(initial_points=None):
        if initial_points is None:
            initial_points = YogaUser._INITIAL_POINTS
        default_yoga_level = YogaLevel.objects.filter(
            minimum_points__lte=initial_points
        ).last()
        default_yoga_level_pk = getattr(default_yoga_level, "pk", None)
        if default_yoga_level_pk is None:
            raise ValueError("No matching level found for the given points")
        return default_yoga_level_pk

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="yoga_user", primary_key=True
    )
    total_points = models.PositiveSmallIntegerField(default=_INITIAL_POINTS)
    yoga_level = models.ForeignKey(YogaLevel, on_delete=models.RESTRICT)
    yoga_poses = models.ManyToManyField(YogaPose, through="yogahistories.YogaHistory")

    class Meta:
        db_table = "yoga_user"

    def __str__(self):
        return self.user.name

    def has_done_yoga_pose(self, yoga_pose_id):
        return self.yoga_poses.filter(id=yoga_pose_id).exists()
