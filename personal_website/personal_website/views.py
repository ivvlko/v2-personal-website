from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import ProgrammingItem, StockItem, WorkoutItem, HistoryItem, PoliticsItem

from django.shortcuts import render, get_object_or_404
from .models import StockPortfolioItem
import yfinance as yf
from datetime import datetime, timedelta



def home(request):
    return render(request, 'home.html')


def portfolio(request, category="programming"):
    categories = {
        "programming": ProgrammingItem,
        "stocks": StockPortfolioItem,
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


def blog(request):
    return render(request, 'blog.html')


def contacts(request):
    return render(request, 'contacts.html')


def portfolio_item_detail(request, category, item_id):
    categories = {
        "programming": ProgrammingItem,
        "stocks": StockPortfolioItem,
        "workouts": WorkoutItem,
        "history": HistoryItem,
        "politics": PoliticsItem,
    }

    model = categories.get(category)
    if not model:
        return render(request, "404.html")

    item = get_object_or_404(model, id=item_id)

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if not start_date and not end_date:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=180)
    else:
        try:
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError as e:
            return render(request, "portfolio_detail.html", {
                "item": item,
                "category": category,
                "error_message": "Invalid date format. Please use YYYY-MM-DD."
            })

    dividend_data = {}
    for stock in item.stocks.all():
        dividend_data[stock.name] = {
            'dividends': float(stock.get_dividends(start_date=start_date, end_date=end_date)),
            'current_shares_count': stock.current_shares_count,
            'yahoo_link': stock.yahoo_link,
            'current_price': stock.get_current_price(),
        }

    return render(request, "portfolio_detail.html", {
        "item": item,
        "category": category,
        "start_date": start_date,
        "end_date": end_date,
        "dividend_data": dividend_data,
    })