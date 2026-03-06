from django.urls import path
from .views import UploadFeed, MySnap, Main, UploadReply

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('mysnap', MySnap.as_view()),
    path('main', Main.as_view())
]
