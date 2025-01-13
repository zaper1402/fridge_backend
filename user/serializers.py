from .models import User
from rest_framework import serializers

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
    
    