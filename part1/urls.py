from django.urls import path
from .views import NewsList, NewsCreateView

urlpatterns = [
    path('add/', NewsCreateView.as_view()),

    path('list/', NewsList.as_view()),
]