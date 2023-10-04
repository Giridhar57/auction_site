from rest_framework import serializers
from .models import Auction

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'start_time', 'end_time', 'start_price', 'item_name', 'winner')
