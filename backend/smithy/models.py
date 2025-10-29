from django.db import models

# Create your models here.

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
        default="Materials"  # Set a sensible default
    )

    def __str__(self):
        return self.name


class CraftingRecipe(models.Model):
    # The item being crafted
    discovered = models.BooleanField(default=False)
    item_a = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="combinationsWithA"
        )

    item_b = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="combinationsWithB"
    )

    result = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="createdBy"
    )
    def __str__(self):
        return f"{self.item_a.name} + {self.item_b.name} = {self.result.name}"

    class NoDuplicate:
        unique_together = ('item_a', 'item_b')

    def __str__(self):
        return (
            f"{self.item_a.name} + {self.item_b.name} = "
            f"{self.result.name}")
