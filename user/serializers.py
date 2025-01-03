from .models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'age', 'preferences']
        extra_kwargs = {
            'preferences': {'required': False}
        }
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    