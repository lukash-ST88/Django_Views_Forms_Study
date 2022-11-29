from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .form import *
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class PublisherListView(ListView):
    queryset = Publisher.objects.all()
    context_object_name = 'my_favorite_publishers'
    template_name = 'ViewStudy/publishers.html'


class AuthorListView(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'ViewStudy/authorlist.html'


class PublisherBookListView(ListView):
    template_name = 'ViewStudy/books_of_pub.html'
    context_object_name = 'books'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.publisher
        return context


class AuthorDetailView(DetailView):
    model = Author  # same as: queryset = author.objects.all()
    context_object_name = 'authors'
    template_name = 'ViewStudy/authors.html'

    def get_object(self):  # сохраняем время последнего просмотра страницы автора
        obj = super().get_object()
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class ContactFormView(FormView):
    template_name = 'ViewStudy/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('pub')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class AuthorCreateView(CreateView):
    model = Author
    fields = ['name']
    context_object_name = 'add'
    template_name = 'ViewStudy/addauthor.html'

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['name', 'salutation', 'email']
    context_object_name = 'add'
    template_name = 'ViewStudy/addauthor.html'

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy(AuthorListView)
    context_object_name = 'add'
    template_name = 'ViewStudy/addauthor.html'