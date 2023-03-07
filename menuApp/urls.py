#  Django модули
from django.urls import path
#  Модули проекта
from .views import * 


urlpatterns = [
    path(r'<str:name>/', index),
]