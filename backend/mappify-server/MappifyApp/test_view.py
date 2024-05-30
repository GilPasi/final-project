from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video = request.FILES.get('video')
        if video:
            input_dir = os.path.join('media', 'input')
            os.makedirs(input_dir, exist_ok=True)
            video_path = os.path.join(input_dir, video.name)

            with open(video_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)
                    
            return JsonResponse({'message': 'Video uploaded successfully!'})
    return JsonResponse({'message': 'Video upload failed.'}, status=400)
