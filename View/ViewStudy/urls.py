from django.urls import path
from .views import *

urlpatterns = [
    path('publisher/', PublisherListView.as_view(), name='pub'),
    path('book/<publisher>/', PublisherBookListView.as_view()),
    path('authors/', AuthorListView.as_view(), name ='author-list'),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name='author-detail'),
    path('contact/', ContactFormView.as_view()),
    path('author/add/', AuthorCreateView.as_view(), name='author-add'),
    path('author/<int:pk>/', AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete')
]
