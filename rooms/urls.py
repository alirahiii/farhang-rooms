from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('works/<slug:slug>/', views.work_detail, name='work_detail'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('request-a-work/', views.work_request, name='work_request'),
]
