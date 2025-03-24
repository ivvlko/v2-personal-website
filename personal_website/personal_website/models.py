from django.db import models
from .utils import process_youtube_link

from django.db import models
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    images = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    video = models.FileField(upload_to='blog_videos/', blank=True, null=True)

    def __str__(self):
        return self.title


class PortfolioItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    video = models.FileField(upload_to='portfolio_videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[("programming", "Programming"),
                                                        ("stocks", "Stocks"),
                                                        ("workouts", "Workouts"),
                                                        ("history", "History"),
                                                        ("politics", "Politics"), ])

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.video_url:
            self.video_url = process_youtube_link(self.video_url)
        super().save(*args, **kwargs)


class ProgrammingItem(PortfolioItem):
    repo_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)


class CodeSnippet(models.Model):
    programming_item = models.ForeignKey(ProgrammingItem, on_delete=models.CASCADE, related_name="snippets")
    language = models.CharField(max_length=50000, choices=[("python", "Python"),
                                                           ("javascript", "JavaScript"),
                                                           ("jupyter", "Jupyter")])
    code = models.TextField()
    description = models.TextField(blank=True, null=True)


class StockItem(models.Model):
    portfolio = models.ForeignKey("StockPortfolioItem", on_delete=models.CASCADE, related_name="stocks")
    name = models.CharField(max_length=255)
    stock_code = models.CharField(max_length=10, unique=True)
    yahoo_link = models.URLField()
    current_shares_count = models.IntegerField(default=0)
    dividend_earned = None
    def get_current_price(self):
        stock = yf.Ticker(self.stock_code)
        history = stock.history(period="1d")
        return history["Close"].iloc[-1] if not history.empty else None

    def get_dividends(self, start_date=None, end_date=None):
        stock = yf.Ticker(self.stock_code)
        dividends = stock.dividends
        dividends.index = pd.to_datetime(dividends.index).tz_localize(None)

        if start_date:
            start_date = pd.to_datetime(start_date)
            dividends = dividends[dividends.index >= start_date]

        if end_date:
            end_date = pd.to_datetime(end_date)
            dividends = dividends[dividends.index <= end_date]

        total_dividends = dividends.sum() * self.current_shares_count
        return total_dividends

    def __str__(self):
        return f"{self.name} ({self.stock_code})"


class StockPortfolioItem(PortfolioItem):
    external_link = models.URLField(blank=True, null=True)

    def get_total_dividends(self):
        return sum(stock.get_dividends() for stock in self.stocks.all())

    def __str__(self):
        return self.title


class HistoryItem(PortfolioItem):
    text_content = models.TextField(blank=True, null=True)


class WorkoutItem(PortfolioItem):
    text_content = models.TextField(blank=True, null=True)


class PoliticsItem(PortfolioItem):
    text_content = models.TextField(blank=True, null=True)

