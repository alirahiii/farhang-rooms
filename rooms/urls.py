from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('works/<slug:slug>/', views.work_detail, name='work_detail'),
]
