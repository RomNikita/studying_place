import stripe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings


class CreatePaymentView(APIView):
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        amount = request.data.get('amount')

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )

            return Response({'client_secret': payment_intent.client_secret}, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

