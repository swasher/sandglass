from django.urls import path, include
from timer import views

from django.contrib.auth import views as auth_views
from timer.forms import UserLoginForm


urlpatterns = [
    path('', views.hello, name='hello'),

    # path('', auth_views.LoginView.as_view(
    #     template_name='timer.html',
    #     authentication_form=UserLoginForm), name='hello'),

    # path('accounts/profile', views.hello, name='hello'),

    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='timer.html',
        authentication_form=UserLoginForm), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('click_start/', views.click_start, name='click_start'),
    path('click_stop/', views.click_stop, name='click_stop'),
    path('click_cancel/', views.click_cancel, name='click_cancel'),
    path('get_latest_jobnotes/', views.get_latest_jobnotes, name='get_latest_jobnotes'),
]
