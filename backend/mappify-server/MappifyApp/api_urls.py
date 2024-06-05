from django.urls import path
from .api_views import UploadVideoAPIView,ImageView, get_image
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('get-csrf-token/', UploadVideoAPIView.as_view(), name='example_of_how_to_make_request'),
    path('upload/', UploadVideoAPIView.as_view(), name='upload_video'),
    # path('media/maps/<str:image_name>/', get_image, name='get_image'),
    path('media/maps/<str:image_name>/', ImageView.as_view(), name='get_image'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

