from rest_framework import serializers
from user.models import UserProduct, Entry
from product.enums import Categories
from user.serializers import UserProductSerializer
from django.utils.timezone import now
from recipes.models import Recipe
from recipes.serializers import CuisineSerializer
from recipes.enums import Cuisine

class HomeDataSerializer(serializers.Serializer):
    inventory = serializers.SerializerMethodField()
    alerts = serializers.SerializerMethodField()
    cuisines =serializers.SerializerMethodField()


    def get_inventory(self, obj):
        inventory = []
        user_id = self.initial_data.get('user_id')
        for category in Categories:
            category_data = {
                "id": category.name,
                "name": category.value,
                "products": []
            }
            products = UserProduct.objects.filter(user_id=user_id, product__category=category)
            serialized_products = UserProductSerializer(products, many=True).data
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
    
    def get_cuisines(self, obj):
        cuisines = []
        cuisines = Cuisine.names
        distinct_cuisines = list(set(cuisines))
        return distinct_cuisines
    
def create_alert_if_needed(user_product: UserProduct):
    alerts = []
    if user_product:
        for entries in user_product.entries:
            days_left = (entries.expiry_date - now().date()).days
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