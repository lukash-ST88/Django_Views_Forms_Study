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
    path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),
    path('TV/', TV.as_view(), name='TVpattern'),
    path('RV/<int:pk>', RV.as_view(), name='RVpattern'),
    path('RV2/<int:pk>', RV2.as_view(), name='RV2pattern'),
    path('LV/', LV.as_view(), name='lVpattern'),
    path('LV/<str:country>', LV2.as_view()),
    path('DV/<slug:slug1>', DV.as_view(), name='DVpattern'),
    path('FV/', FV.as_view()),
    path('FV2/', FV2.as_view()),
    path('CV/', CV.as_view()),
    path('DV/<slug:slug2>/UV/', UV.as_view()),
    path('DV/<slug:slug3>/DelV/', DelV.as_view())
]
