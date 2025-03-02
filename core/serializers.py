from rest_framework import serializers
from collections import defaultdict
from user.models import UserProduct, Entry, Meals
from product.enums import Categories
from user.serializers import UserProductSerializer, EntrySerializer
from django.utils.timezone import now
from user.models import User



class RecipesSerializer(serializers.ModelSerializer):
    recipe_choice = serializers.CharField(source='get_recipe_type_display')
    meal_type_choice = serializers.CharField(source='get_meal_type_display')
    category_name = serializers.CharField(source='category.name')
    is_fav = serializers.SerializerMethodField()
    missing_items = serializers.SerializerMethodField()

    def get_missing_items(self, obj):
        user_id = self.context.get('user_id')  
        if not user_id:
            return 0

        ingredients = obj.ingredients or []
        product_ids = {item.get('id') for item in ingredients if item.get('id')}
        user_prod = set(Entry.objects.filter(user_inventory__product_id__in=product_ids, user_inventory__user_id=user_id, quantity__gt=0, expiry_date__gt=now())
                        .values_list('user_inventory__product_id', flat=True))
        return len(ingredients) - len(user_prod)

    def get_is_fav(self, obj):
        fav_meals = self.context.get('fav_meals', []) or []
        favs = self.context.get('favs', False) or False
        if fav_meals:
            if obj.id in fav_meals:
                return True
        return favs

    class Meta:
        model = Meals
        fields = ['id', 'name', 'subtitle',  'recipe_time', 'is_fav', 'recipe_choice', 'meal_type_choice', 'category_name', 'category', 'image_url', "missing_items"]

class RecipeDetailsSerializer(serializers.ModelSerializer):
    recipe_choice = serializers.CharField(source='get_recipe_type_display')
    meal_type_choice = serializers.CharField(source='get_meal_type_display')
    category_name = serializers.CharField(source='category.name')
    is_fav = serializers.SerializerMethodField()
    missing_items = serializers.SerializerMethodField()

    def get_missing_items(self, obj):
        return 0

    def get_is_fav(self, obj):
        fav_meals = self.context.get('fav_meals', []) or []
        if obj.id in fav_meals:
            return True
        return False

    class Meta:
        model = Meals
        fields = ['id', 'name', 'subtitle',  'recipe_time', 'is_fav', 'recipe_choice', 'meal_type_choice', 'category_name', 'category', 'details', 'ingredients', 'steps', 'image_url', 'missing_items']


class HomeDataSerializer(serializers.Serializer):
    inventory = serializers.SerializerMethodField()
    alerts = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        username = self.initial_data.get('username', {})
        name = username.get('name', '')
        return name

    def get_inventory(self, obj):
        user_id = self.initial_data.get('user_id')
        inventory = []

        user_products = UserProduct.objects.filter(user_id=user_id).select_related('product')

        # Group products by category and then by product name
        category_wise_products = defaultdict(lambda: defaultdict(lambda: {"total_qt": 0, "entries": []}))

        for user_product in user_products:
            category = user_product.product.category
            product_name = user_product.product.name
            category_label = Categories(category).label

            # Aggregate total quantity
            total_quantity = sum(
                Entry.objects.filter(user_inventory=user_product).values_list("quantity", flat=True)
            )
            category_wise_products[category][product_name]["total_qt"] += total_quantity

            # Serialize entries and append
            serialized_entries = EntrySerializer(user_product.entry_set.all(), many=True).data
            category_wise_products[category][product_name]["entries"].extend(serialized_entries)

            # Track unique subnames
            # if user_product.subname:
            #     category_wise_products[category][product_name]["subnames"].add(user_product.subname)

            # Store additional product attributes
            category_wise_products[category][product_name].update({
                "name": product_name,
                "standard_expiry_days": user_product.product.standard_expiry_days,
                "category": category_label,
                "allergy_tags": user_product.product.allergy_tags,
            })

        # Convert the grouped data into the required format
        for category, products in category_wise_products.items():
            product_list = []
            category_label = Categories(category).label
            for name, details in products.items():            
                entries = details.pop("entries", [])
                if entries:
                    product_list.append({"product": details, "entries": entries})
            if product_list:
                inventory.append({"id": category, "name": category_label, "products": product_list})

        return inventory
    
    def get_alerts(self, obj):
        alerts = []
        user_id = self.initial_data.get('user_id')
        products = UserProduct.objects.filter(user_id=user_id)
        for product in products:
            product.entries = Entry.objects.filter(user_inventory=product)
            alerts += create_alert_if_needed(product)
        return alerts
    
def create_alert_if_needed(user_product: UserProduct):
    alerts = []
    if user_product:
        for entries in user_product.entries:
            days_left = (entries.expiry_date - now()).days
            if days_left < 0:
                alerts.append({
                    "id": entries.id,
                    "Title": f"{user_product.product.name} already expired"
                })
            elif days_left < 1000:
                alerts.append({
                    "id": entries.id,
                    "Title": f"{user_product.product.name} expiring in {days_left} days"
                })
    return alerts