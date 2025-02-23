from rest_framework import serializers
from user.models import UserProduct, Entry, Meals
from product.enums import Categories
from user.serializers import UserProductSerializer
from django.utils.timezone import now
from user.models import User



class RecipesSerializer(serializers.ModelSerializer):
    recipe_choice = serializers.CharField(source='get_recipe_type_display')
    meal_type_choice = serializers.CharField(source='get_meal_type_display')
    category_name = serializers.CharField(source='category.name')
    is_fav = serializers.SerializerMethodField()
    missing_items = serializers.SerializerMethodField()

    def get_missing_items(self, obj):
        user_id = self.context.get('user_id', '') 
        if user_id:
            ingredients = obj.ingredients or []
            product_ids = set([item.get('id', '') for item in ingredients])
            user_prod = UserProduct.objects.filter(product_id__in=product_ids, user_id=user_id).values_list('id', flat=True)
            # print(product_ids - set(user_prod), product_ids, user_prod)
            return len(product_ids - set(user_prod))
        return 0

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
        inventory = []
        user_id = self.initial_data.get('user_id')
        for category in Categories:
            category_data = {
                "id": category.name,
                "name": category.label,
                "products": []
            }
            products = UserProduct.objects.filter(user_id=user_id, product__category=category)
            serialized_products = UserProductSerializer(products, many=True, context={"user_id": user_id}).data
            category_data["products"].extend(serialized_products)
            if category_data.get('products'):
                inventory.append(category_data)
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