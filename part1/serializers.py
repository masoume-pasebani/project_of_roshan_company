from rest_framework import serializers
from .models import News

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'text', 'tags', 'source', 'category']
        read_only_fields = ['id']
    
    
def create(self, validated_data):
    request = self.context.get('request')
    user = request.user if request else None
    
    print(f"Validated Data: {validated_data}")
    print(f"User: {user}")

    instance = News.objects.create(user=user, **validated_data)
    return instance
