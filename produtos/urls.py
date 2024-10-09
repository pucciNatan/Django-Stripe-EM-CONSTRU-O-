from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('create-checkout-session/<int:id>', views.create_checkout_session, name="create_checkout_session"),
    path('stripe_webhook', views.stripe_webhook, name="stripe_webhook"),
    path('sucesso/', views.sucesso, name = "sucesso"),
    path('erro/', views.erro, name = "erro")
]
