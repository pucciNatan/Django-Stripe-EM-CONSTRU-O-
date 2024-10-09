from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Produto
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado.'}, status=404)

    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'BRL',
                    'unit_amount': int(produto.preco * 100),  # Converting to cents
                    'product_data': {
                        'name': produto.nome,
                    },
                },
                'quantity': 1,
            },
        ],
        payment_method_types=[
            'card',
            'boleto',
        ],
        metadata={
            'id_produto': produto.id,
        },
        mode='payment',
        success_url=YOUR_DOMAIN + '/produtos/sucesso',
        cancel_url=YOUR_DOMAIN + '/produtos/erro',
    )
    return JsonResponse({'id': checkout_session.id})

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
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
   
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
    return HttpResponse(status=200)