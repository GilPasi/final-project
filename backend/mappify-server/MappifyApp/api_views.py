from django.middleware.csrf import get_token
from django.http import HttpResponse,FileResponse, Http404
from django.core.files.uploadedfile import InMemoryUploadedFile
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
        elif self.request.path.endswith('/'):
            return self.example_request(request)
        else:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def get_csrf_token(self, request):
        csrf_token = get_token(request)
        print(f"CSRF Token: {csrf_token}")
        return Response({'csrfToken': csrf_token})

    def example_request(self, request):
        query_post_example = """
        let formData = new FormData();
        formData.append('video', {
          uri,
          name: `video.${fileType}`,
          type: `video/${fileType}`
        });

         url = `${getBaseUrl()}/api/upload/`
        const response = await fetch(url, {
          method: 'POST',
          body: formData,
          headers: {
            'X-CSRFToken': csrfToken
          },
         })
        ===================================
        If case of 403 error consider getting
        a csrf cookie prior to the request
        in the path /api/get_csrf_token
        use it like so:
        ===================================


          const fetchCsrfToken = async () => {
        try {
          url = `${getBaseUrl()}/api/get-csrf-token/`
          const response = await fetch(url);
          const token = extractCsrfToken(response);
          csrfRef.current = token
          console.log("CSRF Token:", token);
        } catch (err) {
          console.error("Something went wrong while querying CSRF token:", err);
        }
      };"""
        
        return HttpResponse(query_post_example, content_type="text/plain")
    
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

def get_image(request, image_name):
    image_path = os.path.join(settings.MEDIA_ROOT, 'maps', image_name)
    if os.path.exists(image_path):
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    else:
        raise Http404("Image not found")

    
