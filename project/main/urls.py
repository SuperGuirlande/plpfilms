from django.urls import path
from . import views
from portfolio import views as portfolio_views
from blog     import views as blog_views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    # Portfolio public
    path('portfolio/',               portfolio_views.portfolio_list,   name='portfolio_list'),
    path('portfolio/<slug:slug>/',   portfolio_views.portfolio_detail, name='portfolio_detail'),
    # Blog public
    path('blog/',                    blog_views.blog_list,   name='blog_list'),
    path('blog/<slug:slug>/',        blog_views.blog_detail, name='blog_detail'),
]
