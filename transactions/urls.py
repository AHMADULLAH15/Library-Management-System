from django.urls import path
from transactions.views import UserDepositView

urlpatterns = [
    path('deposit', UserDepositView.as_view(), name='deposit_money')
]