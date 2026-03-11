from django.urls import path
from .views import UploadFeed, MySnap, Main, UploadReply, ToggleLike, ToggleBookmark

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('mysnap', MySnap.as_view()),
    path('main', Main.as_view())
]
