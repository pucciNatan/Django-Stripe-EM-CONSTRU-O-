from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('create-payment-intent/<int:id>', views.create_payment, name = "create-payment-intent"),
    path('stripe_webhook', views.stripe_webhook, name = "stripe_webhook"),
    path('sucesso/', views.sucesso, name = "sucesso"),
    path('erro/', views.erro, name = "erro")
]
