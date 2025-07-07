from rest_framework import serializers
from .models import Work

class WorkSerializer(serializers.ModelSerializer):
    coverImage = serializers.URLField(source='cover_image')

    class Meta:
        model = Work
        fields = ('id',
                  'title', 
                  'author', 
                  'coverImage',
                  'description')
