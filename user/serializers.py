from .models import User
from rest_framework import serializers
from product.models import Product
from product.serializers import ProductSerializer
from user.models import Entry, UserProduct
from product.enums import Categories, QuantityType
from django.utils.timezone import localtime, now
from datetime import timedelta, datetime
from user.models import User

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

    def to_internal_value(self, data):
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                date_str = data['date_of_birth']
                if isinstance(date_str, str):
                    # Try to parse date in dd/mm/yyyy format
                    try:
                        data['date_of_birth'] = datetime.strptime(date_str, '%d/%m/%Y').date()
                    except ValueError:
                        # If dd/mm/yyyy fails, try yyyy-mm-dd
                        try:
                            data['date_of_birth'] = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            raise serializers.ValidationError({
                                'date_of_birth': 'Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD'
                            })
            except ValueError:
                raise serializers.ValidationError({
                    'date_of_birth': 'Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD'
                })
        return super().to_internal_value(data)


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

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

class UserProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    brand = serializers.CharField(read_only=True)
    quantity_type = serializers.CharField()
    quantity = serializers.FloatField()
    expiry = serializers.DateField(read_only=True)
    name = serializers.CharField(read_only=True)
    # entries = EntrySerializer(source='entry_set', many=True)

    class Meta:
        model = UserProduct
        fields = '__all__'


class AddProductFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    brand = serializers.CharField(max_length=100, required=False)
    expiry = serializers.DateField(required=False)
    # allergy_tags = serializers.MultipleChoiceField(choices=AllergyTags.choices, required=False)
    quantity = serializers.FloatField(required=True)
    quantity_type = serializers.ChoiceField(choices=QuantityType.choices, required=True)
    user_id = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    
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
        product = Product.objects.filter(id=validated_data['product_id']).first()
        if not product:
            raise serializers.ValidationError("Product not found.")
        
          # Get user by ID
        user = User.objects.filter(id=validated_data['user_id']).first()
        if not user:
            raise serializers.ValidationError("User not found.")
    
        
        user_product = UserProduct.objects.create(
            user=user,
            product=product,
            brand=validated_data.get('brand', None),
            name=validated_data['name'],
            quantity_type=validated_data['quantity_type'],
            quantity=validated_data['quantity'],
            expiry_date=self.set_expiry_date(product.standard_expiry_days, validated_data.get('expiry', None)) 
        )
        user_product_data = UserProductSerializer(user_product).data
        return user_product_data


def convertDate(date_str):
        print(date_str)
        if date_str:
            parsed_date =  None
            try:
                if isinstance(date_str, str):
                    # Try to parse date in dd/mm/yyyy format
                    try:
                        parsed_date = datetime.strptime(date_str, '%d/%m/%Y').date()
                    except ValueError:
                        # If dd/mm/yyyy fails, try yyyy-mm-dd
                        try:
                            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            raise serializers.ValidationError({
                                'date_of_birth': 'Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD'
                            })
            except ValueError:
                raise serializers.ValidationError({
                    'date_of_birth': 'Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD'
                })
            print(parsed_date)
        return parsed_date

class NotifSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    expiry_date = serializers.DateField(required=False)
    name = serializers.CharField(required=True)
    category = serializers.ChoiceField(choices=Categories.choices, required=False)
    message = serializers.SerializerMethodField()

    def get_message(self, obj):
        #if expired
        if obj.expiry_date < now().date():
            return f"{obj.name} has expired"
        #if today
        elif obj.expiry_date == now().date():
            return f"{obj.name} is expiring today"
        #if tomorrow
        elif obj.expiry_date == now().date() + timedelta(days=1):
            return f"{obj.name} is expiring tomorrow"
        #if in the future
        else:
            return f"{obj.name} is expiring in {(obj.expiry_date - now().date()).days} days"