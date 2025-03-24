from django.contrib import admin
from .models import BlogPost
from .models import (
    ProgrammingItem, CodeSnippet, StockPortfolioItem, StockItem,
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


class StockItemInline(admin.TabularInline):
    model = StockItem
    extra = 1

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("name", "stock_code", "current_shares_count", "yahoo_link")
    search_fields = ("name", "stock_code")

@admin.register(StockPortfolioItem)
class StockPortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "external_link")
    search_fields = ("title", "description")
    inlines = [StockItemInline]

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
