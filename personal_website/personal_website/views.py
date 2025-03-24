from .models import BlogPost

from .models import ProgrammingItem, WorkoutItem, HistoryItem, PoliticsItem

from django.shortcuts import get_object_or_404
from .models import StockPortfolioItem
from datetime import datetime, timedelta


from django.core.mail import send_mail
from django.shortcuts import render


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
    categories = {k: v for k, v in categories.items() if v.objects.exists()}

    return render(request, "portfolio.html", {
        "categories": categories.keys(),
        "selected_category": category,
        "items": items,
    })


def blog(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'blog_posts': blog_posts})


def blog_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    return render(request, 'blog_detail.html', {'blog_post': blog_post})

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
    if category == "stocks":
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
                'net_change': stock.calculate_net_change(start_date),
            }

        return render(request, "portfolio_detail.html", {
            "item": item,
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "dividend_data": dividend_data,
        })

    return render(request, "portfolio_detail.html", {
        "item": item,
        "category": category
    })


def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            send_mail(
                f"Message from {name} ({email})",
                message,
                email,
                ['ivankoevbg@gmail.com'],
                fail_silently=False,
            )
            return render(request, 'contacts.html', {'success': True})
        except Exception as ec:
            print(str(ec))
            return render(request, 'contacts.html', {'error': True})

    return render(request, 'contacts.html')