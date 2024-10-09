from django.contrib import admin
from .models import Produto, Pedido
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

admin.site.register(Produto)

@admin.action(description="Reembolsar cliente")
def reembolsar_cliente(modeladmin, request, queryset):
    for pedido in queryset:
        refund = stripe.Refund.create(payment_intent = pedido.payment_intent)

        if refund['status'] == 'succeeded':
            pedido.status = "Reembolsado"
            pedido.save()


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display= ('produto', 'email', 'valor_pago', 'status', 'payment_intent')
    actions = [reembolsar_cliente]