from django.urls import path
from .view import index

urlpatterns = [
    path(r'', index.index),
    path(r'index/', index.index),
    path(r'Welcome/', index.Welcome),
]
