from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CATEGORIES = [
    ("Materials", "Materials"),
    ("Location", "Location"),
    ("Final Item", "Final Item"),
]


class Item(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORIES,
        default="Materials"
    )

    def __str__(self):
        return self.name


class UserList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discovered_items = models.ManyToManyField(
        Item,
        related_name="discovered_by",
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class CraftingRecipe(models.Model):
    item_a = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="combinationsWithA")
    item_b = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="combinationsWithB")
    result = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="createdBy")

    class Meta:
        unique_together = (('item_a', 'item_b'),)

    def __str__(self):
        return f"{self.item_a.name} + {self.item_b.name} = {self.result.name}"


@receiver(post_save, sender=User)
def create_user_list(sender, instance, created, **kwargs):
    if created:
        UserList.objects.get_or_create(user=instance)
