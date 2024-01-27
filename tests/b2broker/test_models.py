from decimal import Decimal

import pytest
from b2broker.models import Wallet, Transaction


@pytest.mark.django_db
def test_wallet_balance():
    wallet = Wallet.objects.create(label="me")
    assert wallet.balance == 0

    Transaction.objects.create(
        wallet=wallet,
        amount=10,
        txid="123",
    )
    assert wallet.balance == 10


@pytest.mark.django_db
def test_wallet_balance_precision():
    wallet = Wallet.objects.create(label="me")
    assert wallet.balance == 0

    Transaction.objects.create(
        wallet=wallet,
        amount=Decimal("10.000000000000000001"),
        txid="123",
    )
    Transaction.objects.create(
        wallet=wallet,
        amount=Decimal("10.000000000000000001"),
        txid="124",
    )
    assert wallet.balance == Decimal("20.000000000000000002")
