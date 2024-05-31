from rest_framework import generics, status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.http import HttpResponse
import os 



# class VideoListCreate(generics.ListCreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
    

# class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer


# class UploadVideo(generics.CreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer

#     # parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         try:
#             print('request is: ', request)
#             print('POST is: ', request.POST)
#             print('FILES is: ', request.FILES)

#             serializer = self.get_serializer(data=request.data)
#             print("2")
#             if serializer.is_valid():
#                 print("3")

#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 print("4")
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as err: 
#             print("error:", err)
# views.py

import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoUploadSerializer

class UploadVideoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.validated_data['video']
            input_dir = os.path.join('media', 'input')
            os.makedirs(input_dir, exist_ok=True)
            video_path = os.path.join(input_dir, video.name)

            with open(video_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)
            
            return Response({'message': 'Video uploaded successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def example_request(request):
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


def get_csrf_token(request):
    csrf_token = get_token(request)
    print(f"CSRF Token: {csrf_token}")
    return JsonResponse({'csrfToken': csrf_token})