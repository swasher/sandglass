from django.urls import path
from timer import views


urlpatterns = [
    path('', views.hello, name='hello'),
    path('click_start/', views.click_start, name='click_start'),
    path('click_stop/', views.click_stop, name='click_stop'),
    path('click_cancel/', views.click_cancel, name='click_cancel'),
]
