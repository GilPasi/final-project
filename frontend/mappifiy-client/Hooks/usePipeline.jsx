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
      console.error("No CSRF token found in set-cookie header");
      return null;
    }
  };

export const usePipeline = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('');
  const csrfToken = useRef()

  useEffect(() => {
    getCsrfToken();
  }, []);


  const getCsrfToken = async () => {
    if(csrfToken.current){
      return csrfToken.current
    }
    
    try {
      const response = await api.get('/get-csrf-token'); // Replace with your endpoint
      csrfToken.current = extractCsrfToken(response)
    } catch (error) {
      console.error('Error fetching CSRF token:', error);
    }
    return csrfToken.current
  };

  const uploadVideo = async (uriObj, gyroscopeData) => {

    const uri = uriObj.uri;
    const fileType = uri.split('.').pop();
    formData = new FormData()
    const gyroscopeData1 = [
      {x: 1.5, y: 3.14, z: 55.875},
      {x: 1.5, y: 3.5, z: 55.875},
      {x: 2.5, y: 5.14, z: 55.55},
    ];
    
    formData.append('video', {
      uri,
      name: `video.${fileType}`,
      type: `video/${fileType}`,
    });
    
    formData.append('gyroscopeData', JSON.stringify(gyroscopeData1));

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

  return {uploadProgress, uploadStatus, uploadVideo, getCsrfToken };
};