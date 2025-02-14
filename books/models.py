from django.db import models
from accounts.models import UserAccount
from categories.models import Category
from django.utils import timezone

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    borrowed_price = models.IntegerField()
    category = models.ForeignKey(Category, related_name='categories', on_delete= models.CASCADE)
    image = models.ImageField(upload_to='books/media/uploads/')

    def __str__(self) -> str:
        return self.title
    
class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='users')
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_on']

    def __str__(self) :
        return self.book.title
    
class Comment(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name='comments')

    def __str__(self) -> str:
        return self.name