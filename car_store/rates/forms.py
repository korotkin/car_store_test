from django import forms


class ExchangeRequestForm(forms.Form):
    amount = forms.IntegerField(required=True, min_value=0, max_value=10 ** 9)
    initial = forms.CharField(required=True, min_length=3, max_length=3)
    target = forms.CharField(required=True, min_length=3, max_length=3)
