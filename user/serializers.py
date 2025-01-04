from .models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    mutable_empty_fields = ['email', 'phone_number']
    class Meta:
        model = User
        fields = ['name', 'email', 'age', 'photo','phone_number','preferences']
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
                    if current_value not in [None, '', []]:
                        raise serializers.ValidationError(
                            {field_name: f"Field '{field_name}' can only be modified when not set"}
                        )
        return data
    
    