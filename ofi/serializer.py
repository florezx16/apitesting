from rest_framework import serializers
from .models import Client

class ClientMainSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField()
    class Meta():
        model = Client
        fields = ['fullname','local_id','income']
        