from django.contrib import admin
from tableau.models import RatingsModel, ContentMetaDataModel


class RatingsModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "item",
        "rating",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("rating", "is_active", "created_at", "updated_at")
    search_fields = (
        "id",
        "user",
        "item",
        "rating",
        "is_active",
        "created_at",
        "updated_at",
    )
    ordering = ("user", "item", "rating", "is_active", "created_at", "updated_at")


class ContentMetaDataModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "luid",
        "name",
        "type",
        "parent_luid",
        "owner_name",
        "views",
    )
    list_filter = ("type",)
    search_fields = ("luid", "name", "type", "parent_luid", "owner_name", "views")
    ordering = ("type",)


admin.site.register(ContentMetaDataModel, ContentMetaDataModelAdmin)
admin.site.register(RatingsModel, RatingsModelAdmin)
