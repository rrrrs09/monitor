from django.urls import path

from . import views
from .models import Post, Favorite, Spam, Archive

urlpatterns = [
    path('reports/', views.ReportView.as_view(), name='reports'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view()),

    path('reports/<int:pk>/all/', views.PostlistView.as_view()),
    path('reports/<int:pk>/spam/', views.PostlistView.as_view(model=Spam)),
    path('reports/<int:pk>/favorites/',
         views.PostlistView.as_view(model=Favorite)),
    path('reports/<int:pk>/archive/',
         views.PostlistView.as_view(model=Archive)),

    path('favorite/', views.CategoryToggleView.as_view(model=Favorite)),
    path('spam/', views.CategoryToggleView.as_view(model=Spam)),
    path('archive/', views.CategoryToggleView.as_view(model=Archive)),

    path('post/<int:pk>/', views.PostDetailView.as_view()),

]