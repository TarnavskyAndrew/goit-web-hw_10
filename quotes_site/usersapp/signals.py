from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


# сигнал, який буде створювати профіль користувача при його створенні
@receiver(post_save, sender=User) # підписка на сигнал post_save для моделі User
def create_profile(sender, instance, created, **kwargs):
    if created:  # якщо користувач був створений
        Profile.objects.create(user=instance) # створення профілю при створенні користувача
