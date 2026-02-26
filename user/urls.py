from .views import Join, Login
from django.urls import path

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view())

]