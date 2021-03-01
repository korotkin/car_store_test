#
# Not needed for the task. Used in data analysis
#


from django.contrib import admin

from car_store.store.models import (
    Car,
    CarBodyType,
    CarColor,
    CarFuelType,
    CarMake,
    CarModel,
    CarSubmodel,
    CarTransmission,
)


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active")
    readonly_fields = ("created_at", "updated_at")


class CarModelAdmin(admin.ModelAdmin):
    raw_id_fields = ("make",)
    list_display = ("id", "name", "active")
    list_filter = ("make", "active")
    readonly_fields = ("created_at", "updated_at")


class CarSubmodelAdmin(admin.ModelAdmin):
    raw_id_fields = ("model",)
    list_display = ("id", "name", "active")
    readonly_fields = ("created_at", "updated_at")


class CarAdmin(admin.ModelAdmin):
    raw_id_fields = (
        "make",
        "model",
        "submodel",
    )
    readonly_fields = ("created_at", "updated_at")


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarSubmodel, CarSubmodelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarColor)
admin.site.register(CarTransmission)
admin.site.register(CarBodyType)
admin.site.register(CarFuelType)
