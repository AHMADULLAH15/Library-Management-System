from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from transactions.models import Transaction
from transactions.forms import DepositForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(user, amount, email_type, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
            'type': email_type,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
# Create your views here.
class UserDepositView(CreateView):
    template_name = 'transactions/deposit_form.html'
    model = Transaction
    form_class = DepositForm

    def form_valid(self, form):
        account = self.request.user.account
        amount = form.cleaned_data.get('amount')
        account.balance += amount
        account.save(update_fields = ['balance'])
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.amount = amount
        transaction.save()
        messages.success(self.request, f'your account has been successfully depostied {amount} tk')
        send_transaction_email(self.request.user,amount, 'deposit', 'Deposit Successful Message', 'transactions/email_template.html')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Depsoit Money"
        return context
    