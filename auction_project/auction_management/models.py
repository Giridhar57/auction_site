from django.db import models
from user_management.models import CustomUser

class Auction(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_name = models.CharField(max_length=100)
    winner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)

class Bid(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey('auction_management.Auction', on_delete=models.CASCADE)  # Assuming your app is named 'auction_management'
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Bid by {self.user.username} on {self.auction.item_name}'

    # class Meta:
    #     ordering = ['-amount']