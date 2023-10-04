from django import forms
from .models import Auction

class AuctionCreationForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['start_time', 'end_time', 'start_price', 'item_name']  # Add other fields as needed
    widgets = {
        'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }

from django import forms

class BidForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

