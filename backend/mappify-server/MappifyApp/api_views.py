from rest_framework import generics, status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from django.conf import settings
import os 

class VideoListCreate(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    

class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class UploadVideo(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            print('request is: ', request)
            print('POST is: ', request.POST)
            print('FILES is: ', request.FILES)

            serializer = self.get_serializer(data=request.data)
            print("2")
            if serializer.is_valid():
                print("3")

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("4")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err: 
            print("error:", err)
    
    


    # def post(self, request, *args, **kwargs):
    #     file = request.FILES['file']

    #     save_dir = os.path.join(settings.BASE_DIR, '..', 'algorithm', 'input')
    #     os.makedirs(save_dir, exist_ok=True)
    #     file_path = os.path.join(save_dir, file.name)
        
    #     with open(file_path, 'wb+') as destination:
    #         for chunk in file.chunks():
    #             destination.write(chunk)
        
    #     return Response({"message": "Video uploaded successfully"}),

    def get(self, request, *args, **kwargs):
        data = {"message": "This is a GET request response"}
        return Response(data, status=status.HTTP_200_OK)