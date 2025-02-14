from django.contrib import admin
from books.models import Book,BorrowedBook,Comment

# Register your models here.
admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(Comment)