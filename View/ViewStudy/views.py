from django.contrib.auth.views import redirect_to_login
from django.db.models import F, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import *
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView, RedirectView
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import formset_factory
from django.forms import modelformset_factory
from .utils import *


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
    context_object_name = 'author'
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


"""Built-in class-based views API"""

"""TemplateView"""


class TV(TemplateView):
    template_name = 'ViewStudy/TV.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Author'] = Author.objects.get(pk=1)
        context['Age'] = 'Context age of author'
        return context


"""RedirectView"""


class RV(RedirectView):
    # url = 'https://www.youtube.com/watch?v=NeQM1c-XCDc'
    pattern_name = 'RV2pattern'

    # permanent = True - определяет статус запроса (301 или 302)

    def get_redirect_url(self, *args, **kwargs):
        # author = get_object_or_404(Author, pk=kwargs['pk'])
        # author.num = F('d') + 1
        # author.save()

        author = Author.objects.filter(pk=kwargs['pk'])
        author.update(d=F('d') + 1)
        return super().get_redirect_url(*args, **kwargs)


class RV2(TemplateView):
    template_name = 'ViewStudy/RV2.html'


"""DetailView"""


class DV(DataMixin, DetailView):
    model = Author
    template_name = 'ViewStudy/DV.html'
    context_object_name = 'author'
    slug_url_kwarg = 'slug1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.filter(slug=self.kwargs['slug1'])
        author.update(d=F('d') + 1)
        context['time'] = timezone.now()
        mixin_context = self.get_user_context(title=context['author'])
        return dict(list(context.items()) + list(mixin_context.items()))



"""ListView"""


class LV(DataMixin, ListView):
    model = Author
    template_name = 'ViewStudy/LV.html'
    context_object_name = 'authors'
    paginate_by = 3
    paginate_orphans = 1  # /?page=2
    # queryset = Author.objects.all()[0:2]

    # def get_queryset(self):
    #     return Author.objects.all()[0:4]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Список')
        return dict(list(context.items()) + list(mixin_context.items()))

class LV2(ListView):
    model = Author
    template_name = 'ViewStudy/LV.html'
    context_object_name = 'authors'

    def get_queryset(self, *args, **kwargs):
        return Author.objects.filter(book__publisher__country__icontains=self.kwargs['country']).distinct()


"""FormView"""


class FV(FormView):
    template_name = 'ViewStudy/FV.html'
    form_class = FF

    # success_url = reverse_lazy('lVpattern')

    def form_valid(self, form):
        form.save()
        return redirect('lVpattern')
        # return super().form_valid(form) - возвращает success_url


class FV2(FormView):
    template_name = 'ViewStudy/FV2.html'
    form_class = FF2
    success_url = reverse_lazy('lVpattern')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


"""CreateView"""


class CV(DataMixin, CreateView):
    model = Author
    # fields = ['name', 'salutation', 'email', 'd']
    form_class = FF
    template_name = 'ViewStudy/CV.html'
    success_url = reverse_lazy('lVpattern')

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['name'] = "The author name"
        initial['salutation'] = 'The author salutation'
        initial['email'] = "The author's name"
        initial['d'] = "Here's a number"
        return initial

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Создать')
        return dict(list(context.items()) + list(mixin_context.items()))

"""AccessView"""


class AccV(PermissionRequiredMixin):
    def dispatch(self, request, *args,
                 **kwargs):  # метод принимающий request of view с аргументами и возвращающий response
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('lVpattern')
        return super(AccV, self).dispatch(request, *args, **kwargs)


"""UpdateView"""


class UV(AccV,DataMixin, UpdateView):
    permission_required = 'ViewStudy.change_author'  # требование допуска заданной формы у пользователя
    raise_exception = True  # отображение ошибки 403
    redirect_field_name = 'next'  # как это упоминается в template и куда переходит страница после login
    login_url = 'http://127.0.0.1:8000/admin/login/?next=/admin/'  # перенаправляет на login форму пользователей не прошедших тест

    model = Author
    # fields = ['name', 'salutation', 'email', 'd']
    form_class = FF
    template_name = 'ViewStudy/CV.html'
    success_url = reverse_lazy('lVpattern')
    slug_url_kwarg = 'slug2'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Изменить')
        return dict(list(context.items()) + list(mixin_context.items()))

"""DeleteView"""


class DelV(DataMixin, DeleteView):
    model = Author
    template_name = 'ViewStudy/DelV.html'
    success_url = reverse_lazy('lVpattern')
    slug_url_kwarg = 'slug3'
    context_object_name = 'author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Удалить')
        return dict(list(context.items()) + list(mixin_context.items()))

"""Forms"""
"""formset_factory"""


class ArticleView(FormView):
    template_name = 'ViewStudy/ArticleTemplate.html'
    form_class = formset_factory(ArticleForm, can_delete=True, extra=2)  # возможность создания сразу двух и более форм

    success_url = reverse_lazy('lVpattern')


def manage_authors(request):  # список всех выброных авторов для редактирования
    AuthorFormSet = modelformset_factory(Author, fields=('salutation', 'name', 'email', 'd'), extra=0)
    Queryset = Author.objects.filter(book__publisher__country__icontains='Russia').distinct()
    if request.method == 'POST':
        formset = AuthorFormSet(request.POST, request.FILES, queryset=Queryset)
        if formset.is_valid():
            formset.save()
            return redirect('lVpattern')
    else:
        formset = AuthorFormSet(queryset=Queryset)
    return render(request, 'ViewStudy/manage_authors.html', {'formset': formset})


def test(request):
    # if this is a POST request we need to process the form data
    data = {'subject': 'hello', 'message': 'Hi there', 'sender': 'foo@example.com', 'cc_myself': True}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)

            return redirect('lVpattern')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm(data) #первый заход на страницу предзаполнение
        #form = ContactForm(initial=data) #инициализированые данные

    return render(request, 'ViewStudy/FV.html', {'form': form})



def bootstrap(request):
    authors = Author.objects.all()
    return render(request, 'ViewStudy/bootstrap.html', {'as': authors})


""" Search window"""

class Search(DataMixin, ListView):
    model = Author
    template_name = 'ViewStudy/LV.html'
    context_object_name = 'authors'
    paginate_by = 3
    paginate_orphans = 1

    def get_queryset(self):
        query = self.request.GET.get('author_name')
        object_list = Author.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Результат поиска')
        return dict(list(context.items()) + list(mixin_context.items()))
