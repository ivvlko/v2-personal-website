from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import ProgrammingItem, StockItem, WorkoutItem, HistoryItem, PoliticsItem


def home(request):
    return render(request, 'home.html')


def portfolio(request, category="programming"):
    categories = {
        "programming": ProgrammingItem,
        "stocks": StockItem,
        "workouts": WorkoutItem,
        "history": HistoryItem,
        "politics": PoliticsItem,
    }

    model = categories.get(category, ProgrammingItem)
    items = model.objects.all()

    return render(request, "portfolio.html", {
        "categories": categories.keys(),
        "selected_category": category,
        "items": items,
    })


def portfolio_item_detail(request, category, item_id):
    categories = {
        "programming": ProgrammingItem,
        "stocks": StockItem,
        "workouts": WorkoutItem,
        "history": HistoryItem,
        "politics": PoliticsItem,
    }

    model = categories.get(category)
    if not model:
        return render(request, "404.html")  # Handle invalid category

    item = get_object_or_404(model, id=item_id)

    return render(request, "portfolio_detail.html", {
        "item": item,
        "category": category,
    })


def blog(request):
    return render(request, 'blog.html')


def contacts(request):
    return render(request, 'contacts.html')