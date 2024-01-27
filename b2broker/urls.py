from rest_framework import routers

from b2broker import views

router = routers.DefaultRouter()
router.register(r"wallets", views.WalletViewSet)
router.register(r"transactions", views.TransactionViewSet)

urlpatterns = router.urls
