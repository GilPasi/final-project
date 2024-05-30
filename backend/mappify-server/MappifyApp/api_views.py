from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer

class VideoListCreate(generics.ListCreateAPIView):
    print('we are in VideoListCreate')
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    

class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    print('we are in VideoDetail')
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
