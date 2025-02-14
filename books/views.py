from typing import Any
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import Book, BorrowedBook, Comment
from books.forms import CommentForm
from django.utils import timezone
from transactions.views import send_transaction_email

class BookDetailsView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['form'] = CommentForm()
        context['comments'] = book.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.save()
            return redirect('details', pk=book.id)

        return self.render_to_response(self.get_context_data(form=form))



# class BookBorrowView(LoginRequiredMixin, View):
#     def get(self, request, id, **kwargs):
#         book = get_object_or_404(Book, id=id)
#         user = self.request.user

#         if user.account.balance >= book.borrowed_price:
#             user.account.balance -= book.borrowed_price
#             user.account.save(update_fields=['balance'])
#             BorrowedBook.objects.create(book=book, user=request.user.account, created_on=timezone.now())
#             messages.success(request, 'Book borrowed successfully!')
#             return redirect('borrow_book_lists')
#         else:
#             messages.error(request, 'Insufficient balance to borrow the book')
#             return redirect('home')

class BookBorrowView(LoginRequiredMixin, View):
    def get(self, request, id, **kwargs):
        book = get_object_or_404(Book, id=id)
        user = self.request.user

        if user.account.balance >= book.borrowed_price:
            user.account.balance -= book.borrowed_price
            user.account.save(update_fields=['balance'])
            borrowed_book = BorrowedBook.objects.create(book=book, user=user.account, created_on=timezone.now())

            messages.success(request, 'Book borrowed successfully!')

            # Send Borrow Email
            send_transaction_email(
                user=user,
                amount=book.borrowed_price,
                email_type='borrow',
                subject='Book Borrow Confirmation',
                template='transactions/borrow_book_email.html'
            )

            return redirect('borrow_book_lists')
        else:
            messages.error(request, 'Insufficient balance to borrow the book')
            return redirect('home')




class BorrowBookListView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = 'books/borrowed_book.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        user_id = self.request.user.id
        return BorrowedBook.objects.filter(user__user_id=user_id)


class BookReturnView(LoginRequiredMixin, View):
    def get(self, request, id, **kwargs):
        book = get_object_or_404(BorrowedBook, id=id)
        user = self.request.user
        user.account.balance += book.book.borrowed_price
        user.account.save(update_fields=['balance'])
        book.delete()
        messages.success(request, 'Book returned successfully!')


        send_transaction_email(
            user=user,
            amount=book.book.borrowed_price,
            email_type='return_book',
            subject='Book Return Confirmation',
            template='transactions/return_book_email.html',
        )
        return redirect(reverse_lazy('borrow_book_lists'))
        # return redirect('borrow_book_lists')


def add_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.save()
            return HttpResponseRedirect(reverse('details', args=[book_id]))  

    return render(request, 'books/book_detail.html', {'form': form, 'book': book})
