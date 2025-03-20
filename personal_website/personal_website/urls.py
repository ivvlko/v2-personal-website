from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<str:category>/", views.portfolio, name="portfolio_category"),
    path("portfolio/<str:category>/<int:item_id>/", views.portfolio_item_detail, name="portfolio_item_detail"),
    path('blog/', views.blog, name='blog'),
    path('contacts/', views.contacts, name='contacts'),
    path('admin/', admin.site.urls),
]