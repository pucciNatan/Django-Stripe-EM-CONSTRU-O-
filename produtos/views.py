from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Produto, Pedido
import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment(request, id):
    produto = Produto.objects.get(id = id)
    email = json.loads(request.body)['email']

    intent = stripe.PaymentIntent.create(
        amount = int(produto.preco),
        currency = 'BRL',
        metadata = {
            'produto_id': produto.id,
            'email': email
        }
    )
    
    return JsonResponse({
        'clientSecret': intent['client_secret'],
    })

    
def home(request):
    try:
        produto = Produto.objects.get(id=1)
    except Produto.DoesNotExist:
        produto = None 

    return render(request, 'home.html', {'produto': produto, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})

def sucesso(request):
    return HttpResponse('Sucesso!')

def erro(request):
    return HttpResponse('Erro.')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Payload inválido
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Assinatura inválida
        return HttpResponse(status=400)

    # Lidar com o evento
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        email = None

        # Obter o ID do Payment Method do Payment Intent
        payment_method_id = payment_intent.get('payment_method')
        if payment_method_id:
            # Recuperar o objeto Payment Method
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
            email = payment_method['billing_details'].get('email')

            pedido = Pedido(produto_id = payment_intent['metadata']['produto_id'],
                            payment_intent = payment_intent['id'],
                            email = email,
                            valor_pago = payment_intent['amount'],
                            status = payment_intent['status'])
            print('Pedido salvo')
            pedido.save()
    else:
        # Evento não esperado
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)

