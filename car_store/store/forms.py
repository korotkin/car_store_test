from django import forms

from car_store.store.models import Car, CarMake, CarModel, CarSubmodel


class CarSearchForm(forms.Form):
    price__gt = forms.IntegerField(required=False, min_value=0, max_value=10 ** 9)
    price__lte = forms.IntegerField(required=False, min_value=0, max_value=10 ** 9)
    mileage__gt = forms.IntegerField(required=False, min_value=0, max_value=10 ** 9)
    mileage__lte = forms.IntegerField(required=False, min_value=0, max_value=10 ** 9)
    model__name__icontains = forms.CharField(required=False, max_length=50)
    submodel__name__icontains = forms.CharField(required=False, max_length=50)


class CarModelForm(forms.ModelForm):
    make = forms.ModelChoiceField(
        queryset=CarMake.objects.filter(active=True), to_field_name="name"
    )
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.filter(active=True), to_field_name="name"
    )
    submodel = forms.ModelChoiceField(
        queryset=CarSubmodel.objects.filter(active=True), to_field_name="name"
    )

    class Meta:
        model = Car
        fields = [
            "year",
            "mileage",
            "price",
            "make",
            "model",
            "submodel",
            "body_type",
            "transmission",
            "fuel_type",
            "exterior_color",
        ]
