from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework_json_api.views import RelationshipView

from b2broker.models import Wallet, Transaction
from b2broker.serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wallets to be viewed or edited.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_fields = ("id", "label")


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ("id", "wallet", "txid")
