from django.urls import path
from .api_views import VideoListCreate, VideoDetail, UploadVideo

urlpatterns = [
    path('videos/', VideoListCreate.as_view(), name='api_video_list_create'),
    path('videos/<int:pk>/', VideoDetail.as_view(), name='api_video_detail'),
    path('upload/', UploadVideo.as_view(), name='api_video_upload'), 
]
