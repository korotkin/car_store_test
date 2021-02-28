#
# Not needed for the task. Used in data analysis
#


from django.contrib import admin
from car_store.store.models import CarMake, CarModel, CarSubmodel, Car


class CarMakeAdmin(admin.ModelAdmin):
    model = CarMake
    list_display = ("name", "active")
    readonly_fields = ("created_at", "updated_at")


class CarModelAdmin(admin.ModelAdmin):
    raw_id_fields = ("make",)
    list_display = ("name", "make", "active")
    list_filter = ("make", "active")
    model = CarModel
    readonly_fields = ("created_at", "updated_at")


class CarSubmodelAdmin(admin.ModelAdmin):
    raw_id_fields = ("model",)
    list_display = ("name", "model", "active")
    list_filter = ("model", "active")
    model = CarSubmodel
    readonly_fields = ("created_at", "updated_at")


class CarAdmin(admin.ModelAdmin):
    raw_id_fields = (
        "make",
        "model",
        "submodel",
    )
    model = Car
    readonly_fields = ("created_at", "updated_at")


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarSubmodel, CarSubmodelAdmin)
admin.site.register(Car, CarAdmin)
