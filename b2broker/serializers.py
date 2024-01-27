from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.views import RelationshipView

from b2broker.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance", "url"]

    @staticmethod
    def get_balance(obj):
        return str(obj.balance)


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=36, decimal_places=18, default=0, allow_null=True
    )

    class Meta:
        model = Transaction
        fields = ["id", "wallet", "txid", "amount", "url"]
