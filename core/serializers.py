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
        user_id = self.context.get('user_id')  
        if not user_id:
            return 0

        ingredients = obj.ingredients or []
        product_ids = {item.get('id') for item in ingredients if item.get('id')}
        user_prod = set(Entry.objects.filter(user_inventory__product_id__in=product_ids, user_inventory__user_id=user_id, quantity__gt=0, expiry_date__gt=now())
                        .values_list('user_inventory__product_id', flat=True))

        return len(product_ids - user_prod)

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
            prod_list = [product for product in serialized_products if len(product.get('entries'))>0]
            # if serialized_products.get('entries', []):
            category_data["products"].extend(prod_list)
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