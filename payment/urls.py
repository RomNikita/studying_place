from django.urls import path
from rest_framework.routers import DefaultRouter

from payment.apps import PaymentConfig
from payment.views import CreatePaymentView

app_name = PaymentConfig.name



urlpatterns = [
                  path('payment/create/', CreatePaymentView.as_view(), name='create-pay' )

              ]
