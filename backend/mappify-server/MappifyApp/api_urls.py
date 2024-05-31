from django.urls import path
from .api_views import upload_video, example_request, get_csrf_token
from .api_views import UploadVideoAPIView


urlpatterns = [
    path('upload/', upload_video, name='api_video_list_create'),
    path('', example_request, name='example_of_how_to_make_request'),
    path('get-csrf-token/', get_csrf_token, name='example_of_how_to_make_request'),
    path('upload1/', UploadVideoAPIView.as_view(), name='upload_video'),
]
