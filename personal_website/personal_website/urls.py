from django.urls import path
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<str:category>/", views.portfolio, name="portfolio_category"),
    path("portfolio/<str:category>/<int:item_id>/", views.portfolio_item_detail, name="portfolio_item_detail"),
    path('blog/', views.blog, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('admin/', admin.site.urls),
    path('stocks/<int:item_id>/', views.portfolio_item_detail, name='stock_portfolio_detail'),
    path('contact/', views.send_email, name='send_email'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)