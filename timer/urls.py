from django.urls import path
from timer import views


urlpatterns = [
    path('', views.hello, name='hello'),
    path('click_startz/', views.click_startz, name='click_startz'),
    path('click_stopz/', views.click_stopz, name='click_stopz'),
    path('click_stopm/', views.click_stopm, name='click_stopm'),
    path('click_stopm/', views.click_stopm, name='click_stopm'),
]
