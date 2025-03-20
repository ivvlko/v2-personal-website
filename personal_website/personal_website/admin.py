from django.contrib import admin
from .models import BlogPost
from .models import (
    ProgrammingItem, CodeSnippet, StockItem,
    HistoryItem, WorkoutItem, PoliticsItem
)


class CodeSnippetInline(admin.TabularInline):
    model = CodeSnippet
    extra = 1


@admin.register(ProgrammingItem)
class ProgrammingItemAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "repo_link", "demo_link")
    search_fields = ("title", "description")
    inlines = [CodeSnippetInline]


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "external_link")
    search_fields = ("title", "description")


@admin.register(HistoryItem)
class HistoryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "video_url")
    search_fields = ("title", "description")


@admin.register(WorkoutItem)
class WorkoutItemAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "video_url")
    search_fields = ("title", "description")


@admin.register(PoliticsItem)
class PoliticsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "video_url")
    search_fields = ("title", "description")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title', 'content')
    list_filter = ('date',)
