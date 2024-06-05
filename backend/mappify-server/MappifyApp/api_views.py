from django.middleware.csrf import get_token
from django.http import FileResponse, Http404, JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoUploadSerializer

import json 
import sys
import os 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..','..',))

sys.path.append(parent_dir)
from algorithm.map_producing import produce_map

class UploadVideoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.path.endswith('get-csrf-token/'):
            return self.get_csrf_token(request)
        else:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def get_csrf_token(self, request):
        csrf_token = get_token(request)
        print(f"CSRF Token: {csrf_token}")
        return Response({'csrfToken': csrf_token})
    
    def post(self, request, *args, **kwargs):
        if self.request.path.endswith('upload/'):
            return self.upload_map_data(request)
        else:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    def upload_map_data(self, request, *args, **kwargs):
        adaptedGyroData = [json.loads(request.data['gyroscopeData'])]
        request.data['gyroscopeData'] = adaptedGyroData 

        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.validated_data['video']
            produce_map(video)


            # input_dir = os.path.join('media', 'videos')
            # os.makedirs(input_dir, exist_ok=True)
            # video_path = os.path.join(input_dir, video.name)

            # with open(video_path, 'wb+') as destination:
            #     for chunk in video.chunks():
            #         destination.write(chunk)
            
            return Response({'message': 'Video uploaded successfully!'}, status=status.HTTP_201_CREATED)
        print("Serializer error: ",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ImageView(APIView):

    def get(self, request, image_name, format=None):
        print("1")
        if request.path.endswith('all/'):
            print("2")
            return self.get_all_maps_names()
        else:
            print("3")
            return self.get_map(image_name)



    def get_map(self, image_name):
        image_path = os.path.join(settings.MEDIA_ROOT, 'maps', image_name)
        if os.path.exists(image_path):
            return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
        else:
            raise Http404("Image not found")
    
    def get_all_maps_names(self):
        media_root = settings.MEDIA_ROOT
        maps_dir = os.path.join(media_root, 'maps')
        
        if not os.path.exists(maps_dir):
            return JsonResponse({'error': 'Maps directory does not exist'}, status=404)
        
        file_paths = []
        for root, dirs, files in os.walk(maps_dir):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), media_root)
                file_paths.append(file_path)
        
        return JsonResponse({'files': file_paths})
        
    
      
    
