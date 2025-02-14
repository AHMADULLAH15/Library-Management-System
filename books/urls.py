from django.urls import path
from books.views import BookDetailsView, BookBorrowView, BorrowBookListView, BookReturnView, add_comment

urlpatterns = [
    path('details/<int:pk>/', BookDetailsView.as_view(), name='details'),
    path('book/<int:book_id>/comment/', add_comment, name='add_comment'),  
    path('borrow_book/<int:id>/', BookBorrowView.as_view(), name='borrow_book'),
    path('borrow_book_lists/', BorrowBookListView.as_view(), name='borrow_book_lists'),
    path('return_book/<int:id>/', BookReturnView.as_view(), name='return_book'),
]
