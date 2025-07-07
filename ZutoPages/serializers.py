from rest_framework import serializers
from .models import Work
from .models import Write

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
        
class WriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Write
        fields = ()
