from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
    
    def to_internal_value(self, data):
        data["name"] = data["name"].capitalize()
        return data
