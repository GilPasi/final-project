from django.urls import path
from .views import video_list, video_detail, delete_video, upload_video

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('videos/', video_list, name='video_list'),
    path('videos/<int:pk>/', video_detail, name='video_detail'),
    path('videos/<int:pk>/delete/', delete_video, name='delete_video'),
]
