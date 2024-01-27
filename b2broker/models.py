from decimal import Decimal

from django.db import models
from django.db.models import Sum


class Wallet(models.Model):
    label = models.CharField(max_length=100)

    @property
    def balance(self):
        return (
            Transaction.objects.filter(wallet=self).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or Decimal("0.0")
        )


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
        db_column="wallet_id",
    )
    txid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(
        max_digits=36, decimal_places=18, default=Decimal("0.0")
    )
