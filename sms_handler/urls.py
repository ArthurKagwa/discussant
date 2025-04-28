# sms_handler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('receive-sms/', views.receive_sms, name='receive_sms'),
    path('callback/', views.sms_callback, name='sms_callback'),

]