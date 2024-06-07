import { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';

export const SUCCESS_MSG = 'Video uploaded successfully!'
export const FAILURE_MSG = 'Upload failed.'

const extractCsrfToken = (response) => {
    const cookies = response.headers.get('set-cookie');
    if (cookies) {
      const token = cookies[0].split(';').find(cookie => cookie.trim().startsWith('csrftoken=')).split('=')[1];
      return token;
    } else {
      console.error("No CSRF token found in set-cookie header.");
      return null;
    }
  };

export const usePipeline = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('');
  const csrfToken = useRef(null)

  useEffect(() => {
    getCsrfToken();
  }, []);

  const getCsrfToken = async () => {
    
    if(csrfToken.current){
      return csrfToken.current
    }
    try {
      const response = await api.get('/get-csrf-token');
      csrfToken.current = extractCsrfToken(response)
    } catch (error) {
      console.error("Fetching CSRF token failed. Possible solutions: ",
      "\n1. Make sure that SERVER_IP in frontend/mappifiy-client/utilities/utils.js",
      " is configured for your actual IP address",
      "\n2. Make sure your IP address is indeed one of the ALLOWED_HOSTS in backend/mappify-server/MappifyDjango/settings.py");
    }
    return csrfToken.current
  };

  const uploadVideo = async (uriObj, gyroscopeData) => {
    const uri = uriObj.uri;
    const fileType = uri.split('.').pop();
    formData = new FormData()
    
    formData.append('video', {
      uri,
      name: `video.${fileType}`,
      type: `video/${fileType}`,
    });
    
    formData.append('gyroscopeData', JSON.stringify(gyroscopeData));

    try {
      const response = await api.post('/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRF-TOKEN': csrfToken,
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        },
      });


      if (response.status === 201) {
        console.log(SUCCESS_MSG);
      } else {
        console.log(FAILURE_MSG);
      }

      setUploadStatus(SUCCESS_MSG);
      console.log('Upload response:', response.data);
    } catch (error) {
      setUploadStatus(FAILURE_MSG);
      console.error('Error uploading video:', error);
    }
  };

  return {uploadProgress, uploadStatus, uploadVideo, csrfToken };
};
