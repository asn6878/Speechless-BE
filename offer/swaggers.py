from rest_framework import serializers

class OfferCreateRequestSerializer(serializers.Serializer):
    content = serializers.CharField(help_text="content")
    price = serializers.IntegerField(help_text="price")
