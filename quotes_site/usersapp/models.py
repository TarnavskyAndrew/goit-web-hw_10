import os
import uuid
from django.utils.deconstruct import deconstructible
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # генеруємо унікальне ім'я
        filename = f"{uuid.uuid4().hex}.{ext}"
        return os.path.join(self.path, filename)


def upload_to_avatar(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"avatars/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=upload_to_avatar,
        blank=True,
        null=True,
        default="avatars/default_avatar.jpg",  # дефолтне фото
    )

    def __str__(self):
        return f"Profile of {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            max_size = (300, 300)

            try:
                resample_filter = Image.Resampling.LANCZOS
            except AttributeError:
                resample_filter = Image.ANTIALIAS

            img.thumbnail(max_size, resample_filter)
            img.save(self.avatar.path)
