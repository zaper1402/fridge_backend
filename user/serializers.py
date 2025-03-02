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
    subname = serializers.SerializerMethodField()

    def get_subname(self, obj):
        subname = self.context.get('subname', '')
        return subname

    def get_total_qt(self, obj):
        user_id = self.context.get('user_id', '')
        if user_id:
            user_product = UserProduct.objects.filter(user_id=user_id, product_id=obj.id).first()
            entries = Entry.objects.filter(user_inventory=user_product.id).values_list("quantity", flat=True)
            return sum(entries)
        return 0
        
    class Meta:
        model = Product
        fields = ['total_qt', 'name', 'standard_expiry_days', 'category', 'allergy_tags', 'subname']

class EntrySerializer(serializers.ModelSerializer):
    subname = serializers.SerializerMethodField()

    def get_subname(self, obj):
        return obj.user_inventory.subname or obj.user_inventory.product.name

    class Meta:
        model = Entry
        fields = ['subname', 'quantity', 'expiry_date', 'creation_date', 'quantity_type', 'id']

class UserProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    entries = EntrySerializer(source='entry_set', many=True)
    name = serializers.CharField(source='subname')

    def get_product(self, obj):
        return ProductSerializer(obj.product, context={**self.context, 'subname': obj.subname}).data

    class Meta:
        model = UserProduct
        fields = ['product', 'entries', 'name']


class AddProductFormSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    subname = serializers.CharField(max_length=100, required=False)
    expiry = serializers.DateField(required=False)
    allergy_tags = serializers.MultipleChoiceField(choices=AllergyTags.choices, required=False)
    quantity = serializers.FloatField(required=True)
    user_id = serializers.IntegerField(required=True)
    quantity_type = serializers.ChoiceField(choices=QuantityType.choices, required=False)
    
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
        product = Product.objects.filter(id = validated_data.get('id', '')).first()
        user_product, _ = UserProduct.objects.get_or_create(
            user_id=validated_data['user_id'],
            subname=validated_data.get('subname', '') if validated_data.get('subname', '') else product.name,
            product_id=validated_data.get('id', '')
        )
        entry = Entry.objects.create(
            user_inventory=user_product,
            quantity=validated_data['quantity'],
            expiry_date=self.set_expiry_date(product.standard_expiry_days, validated_data.get('expiry', None)),
            quantity_type=validated_data.get('quantity_type', '')
        )
        # return user product with all entries 
        user_product_data = UserProductSerializer(user_product).data
        return user_product_data
