from django import forms 
from transactions.models import Transaction

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        min_deposit_amount = 100

        if amount < min_deposit_amount:
            raise forms.ValidationError(f'you can not deposit less than {min_deposit_amount}')
        return amount
        
    