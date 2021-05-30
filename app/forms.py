from django import forms
from .models import Profile, Order, ORDER_TYPE_CHOICES


class OrderForm(forms.ModelForm):
    order_type = forms.ChoiceField(choices=ORDER_TYPE_CHOICES, required=True)
    price = forms.FloatField(required=True, initial=0.0)
    quantity = forms.FloatField(required=True, initial=0.0)

    class Meta:
        model = Order
        fields = ['order_type', 'quantity', 'price']

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")

        if quantity <= 0:
            raise forms.ValidationError("Please enter a valid quantity")

        return quantity

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price <= 0:
            raise forms.ValidationError("Please enter a valid price")

        return price

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        price = cleaned_data.get("price")
        quantity = cleaned_data.get("quantity")
        order_type = cleaned_data.get("order_type")
        user_profile = Profile.objects.filter(user=self.request.user)[0]

        if (price is not None) and (quantity is not None):
            if order_type == "Sell" and (user_profile.btc_balance < quantity):
                raise forms.ValidationError("You don't have enough Bitcoins")
            elif order_type == "Buy" and (user_profile.usd_balance < price):
                raise forms.ValidationError("You don't have enough USD")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(OrderForm, self).__init__(*args, **kwargs)
