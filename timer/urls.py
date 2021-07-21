from django.urls import path
from timer import views


urlpatterns = [
    path('', views.hello, name='hello'),
]
