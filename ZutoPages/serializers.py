from rest_framework import serializers
from .models import Work

class WorkSerializer(serializers.ModelSerializer):
    typeindex  = serializers.IntegerField(source='type_index', write_only=True)
    coverImage = serializers.URLField(source='cover_image')

    class Meta:
        model = Work
        fields = ('id',
                  'typeindex',
                  'title', 
                  'author', 
                  'coverImage',
                  'description')
