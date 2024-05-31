from django.urls import path
from .api_views import UploadVideoAPIView


urlpatterns = [
    path('', UploadVideoAPIView.as_view(), name='example_of_how_to_make_request'),
    path('get-csrf-token/', UploadVideoAPIView.as_view(), name='example_of_how_to_make_request'),
    # path('', example_request, name='example_of_how_to_make_request'),
    # path('get-csrf-token/', get_csrf_token, name='example_of_how_to_make_request'),
    path('upload/', UploadVideoAPIView.as_view(), name='upload_video'),

]
