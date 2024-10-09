# Generated by Django 5.1.1 on 2024-10-09 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0004_rename_produto_id_pedido_produto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='nome',
        ),
        migrations.AddField(
            model_name='pedido',
            name='valor_pago',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedido',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
