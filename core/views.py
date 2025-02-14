from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book
from categories.models import Category

# Create your views here.
class HomeView(ListView):
    template_name = 'index.html'
    model = Book
    context_object_name = 'books'

    def get(self, request, *args, **kwargs):
        category_slug = kwargs.get('category_slug')
        self.object_list = self.model.objects.all()

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            self.object_list = self.object_list.filter(category=category)

        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    