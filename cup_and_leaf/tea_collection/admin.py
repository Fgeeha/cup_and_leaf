from django.contrib import admin
from django.utils.html import format_html

from .models import TeaType, TeaOrigin, TeaPost, TeaComment


@admin.register(TeaType)
class TeaTypeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "is_published",
        "created_at",
    )
    list_editable = ("is_published",)
    search_fields = ("title", "description")
    list_filter = ("is_published",)


@admin.register(TeaOrigin)
class TeaOriginAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "is_published",
        "created_at",
    )
    list_editable = ("is_published",)
    search_fields = ("name", "description")
    list_filter = ("is_published",)


@admin.register(TeaPost)
class TeaPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "author",
        "origin",
        "production_year",
        "tea_grade",
        "appearance",
        "created_at",
        "updated_at",
        "image_preview",
    )
    search_fields = ("title", "description", "origin")
    list_filter = ("type", "tea_grade", "origin", "author")
    readonly_fields = ("created_at", "updated_at")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>', obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(TeaComment)
class TeaCommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "tea_post",
        "author",
        "rating",
        "created_at",
    )
    search_fields = ("text", "tea_post__title", "author__username")
    list_filter = ("rating", "created_at")
    readonly_fields = ("created_at",)
