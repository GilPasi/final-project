from django.urls import path
# from .api_views import VideoListCreate, VideoDetail, UploadVideo, test_get
from .api_views import upload_video, example_request, get_csrf_token

urlpatterns = [
    path('upload/', upload_video, name='api_video_list_create'),
    path('', example_request, name='example_of_how_to_make_request'),
    path('get-csrf-token/', get_csrf_token, name='example_of_how_to_make_request'),


    # path('videos/', VideoListCreate.as_view(), name='api_video_list_create'),
    # path('videos/<int:pk>/', VideoDetail.as_view(), name='api_video_detail'),
    # path('upload/', UploadVideo.as_view(), name='api_video_upload'), 
    # path('test_get', test_get, name='test_get'), 
]
