import os
import json
from django.db import migrations

def load_data():
    """Helper to load the JSON file from the same directory as this migration."""
    file_path = os.path.join(os.path.dirname(__file__), 'materials.json')
    with open(file_path, 'r') as f:
        return json.load(f)

def add_initial_items(apps, schema_editor):
    Item = apps.get_model('smithy', 'Item')
    CraftingRecipe = apps.get_model('smithy', 'CraftingRecipe')
    
    data = load_data()
    

    # 1. Create Items
    for item_data in data['items']:
        obj, created = Item.objects.get_or_create(
            name=item_data["name"],
            defaults={'category': item_data["category"]}
        )
        
        if created:
            print(f"  Created: {obj.name} (Category: {obj.category})")
        else:
            print(f"  Skipped (already exists): {obj.name}")

    print("\nAdding initial recipes from JSON...")

    for recipe_list in data['recipes']:
        # Unpack the list [ItemA, ItemB, Result]
        a_name, b_name, result_name = recipe_list

        try:
            item_a = Item.objects.get(name=a_name)
            item_b = Item.objects.get(name=b_name)
            result_item = Item.objects.get(name=result_name)

            recipe, created = CraftingRecipe.objects.get_or_create(
                item_a=item_a,
                item_b=item_b,
                defaults={
                    'result': result_item,
                }
            )

            if created:
                print(f"  Created recipe: {item_a.name} + {item_b.name} = {result_item.name}")
            else:
                print(f"  Skipped recipe (already exists): {item_a.name} + {item_b.name}")

        except Item.DoesNotExist:
            print(f"  ERROR: Could not create recipe. Item not found for: {a_name}, {b_name}, or {result_name}")

def remove_initial_items(apps, schema_editor):
    Item = apps.get_model('smithy', 'Item')
    CraftingRecipe = apps.get_model('smithy', 'CraftingRecipe')
    
    data = load_data()

    item_names = [item["name"] for item in data['items']]
    
    result_names = {recipe[2] for recipe in data['recipes']}

    # remove combos first
    recipes_to_delete = CraftingRecipe.objects.filter(
        result__name__in=result_names
    )
    count, _ = recipes_to_delete.delete()
    print(f"\n{count} recipes deleted")

    items_to_delete = Item.objects.filter(name__in=item_names)
    count, _ = items_to_delete.delete()
    print(f"{count} items deleted")

class Migration(migrations.Migration):

    dependencies = [
        ('smithy', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_items, remove_initial_items)
    ]