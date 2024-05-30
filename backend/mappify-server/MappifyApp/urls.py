from django.urls import path
from .views import video_list, video_detail, delete_video, get_csrf_token
from .test_view import upload_video

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('videos/', video_list, name='video_list'),
    path('videos/<int:pk>/', video_detail, name='video_detail'),
    path('videos/<int:pk>/delete/', delete_video, name='delete_video'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
]
