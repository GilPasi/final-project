import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { api } from '../services/api';



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

const usePipeline = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('');
  const csrfToken = useRef()

  useEffect(() => {
    getCsrfToken();
  }, []);


  const getCsrfToken = async () => {
    if(csrfToken){
      return csrfToken
    }
    
    try {
      const response = await api.get('/get-csrf-token'); // Replace with your endpoint
      csrfToken.current = extractCsrfToken(response)
    } catch (error) {
      console.error('Error fetching CSRF token:', error);
    }
    return csrfToken.current
  };

  const uploadVideo = async (uriObj) => {

    const uri = uriObj.uri;
    const fileType = uri.split('.').pop();
    const time = new Date().getSeconds()
    let formData = new FormData();
    formData.append('video', {
      uri,
      name: `video.${fileType}`,
      type: `video/${fileType}`
    });
  

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
        console.log('Video uploaded successfully!');
      } else {
        console.log('Video upload failed.');
      }

      setUploadStatus('Upload successful!');
      console.log('Upload response:', response.data);
    } catch (error) {
      setUploadStatus('Upload failed.');
      console.error('Error uploading video:', error);
    }
  };

  return {uploadProgress, uploadStatus, uploadVideo, getCsrfToken };
};

export default usePipeline;
