from .models import User
from rest_framework import serializers
from product.models import Product
from user.models import Entry, UserProduct
from product.enums import Categories, QuantityType, AllergyTags
from django.utils.timezone import localtime, now
from datetime import timedelta

class UserSerializer(serializers.ModelSerializer):
    mutable_empty_fields = ['email', 'phone_number','gender','date_of_birth']
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'preferences': {'required': False},
            'photo': {'required': False},
            'phone_number': {'required': False},
        }


    def validate(self, data):
        if self.instance: 
            for field_name, new_value in data.items():
                # Check if the fields are empty and can be modified
                if field_name in self.mutable_empty_fields and new_value not in [None, '', []]:
                    current_value = getattr(self.instance, field_name)
                    if current_value not in [None, '', []] and current_value != new_value:
                        if field_name == 'email':
                            new_value = current_value
                        else:
                            raise serializers.ValidationError(
                                {field_name: f"Field '{field_name}' can only be modified when not set"}
                            )
        return data

class ProductSerializer(serializers.ModelSerializer):
    total_qt= serializers.SerializerMethodField()

    def get_total_qt(self, obj):
        user_id = self.context.get('user_id', '')
        if user_id:
            user_product = UserProduct.objects.filter(user_id=user_id, product_id=obj.id).first()
            entries = Entry.objects.filter(user_inventory=user_product.id).values_list("quantity", flat=True)
            return sum(entries)
        return 0
        
    class Meta:
        model = Product
        fields = ['total_qt', 'name','brand', 'standard_expiry_days', 'category', 'allergy_tags', 'quantity_type']

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

class UserProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    entries = EntrySerializer(source='entry_set', many=True)

    class Meta:
        model = UserProduct
        fields = '__all__'


class AddProductFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    category = serializers.ChoiceField(choices=Categories.choices, required=True)
    brand = serializers.CharField(max_length=100, required=False)
    expiry = serializers.DateField(required=False)
    allergy_tags = serializers.MultipleChoiceField(choices=AllergyTags.choices, required=False)
    quantity = serializers.FloatField(required=True)
    quantity_type = serializers.ChoiceField(choices=QuantityType.choices, required=True)
    user_id = serializers.IntegerField(required=True)
    
    def set_expiry_date(self, standard_expiry_days, expiry_date):
        if expiry_date is None and standard_expiry_days is None:
            raise serializers.ValidationError("Expiry date is required.")
        elif expiry_date is None:
            return now() + timedelta(days=standard_expiry_days)
        else:
            if expiry_date < now().date():
                raise serializers.ValidationError("Expiry date cannot be in the past.")
            else:
                return expiry_date

    def create(self, validated_data):
        product_filter = {
            'name__iexact': validated_data['name'],
            'category': validated_data['category']
        }
        if 'brand' in validated_data and validated_data['brand']:
            product_filter['brand__iexact'] = validated_data['brand']

        product, created = Product.objects.get_or_create(
            defaults={
                'name': validated_data['name'],
                'category': validated_data['category'],
                'brand': validated_data.get('brand', None),
                'standard_expiry_days': None,
                'allergy_tags': list(validated_data.get('allergy_tags', [])),
                'quantity_type': validated_data['quantity_type'],

                
            },
            **product_filter
        )
        user_product, _ = UserProduct.objects.get_or_create(
            user_id=validated_data['user_id'],
            product_id=product.id,
            defaults={
                'product': product,
            }
        )
        entry = Entry.objects.create(
            user_inventory=user_product,
            quantity=validated_data['quantity'],
            expiry_date=self.set_expiry_date(product.standard_expiry_days, validated_data.get('expiry', None))
        )
        # return user product with all entries 
        user_product_data = UserProductSerializer(user_product).data
        return user_product_data
