import { useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import { useState, useRef } from 'react';

export default function useCam(isRecording) {
    const [cameraPermission, requestCameraPermission] = useCameraPermissions();
    const [microphonePermission, requestMicrophonePermission] = useMicrophonePermissions();
    const [videoUri, setVideoUri] = useState(null);
    cameraRef = useRef() 

      
  async function requestPermissions() {
    const cameraStatus = await requestCameraPermission();
    const microphoneStatus = await requestMicrophonePermission();

    if (cameraStatus.granted && microphoneStatus.granted) {
      console.log("Permissions granted");
    } else {
      console.log("Permissions not granted");
    }

  }

  const startRecording = async () => {
    if (cameraRef.current) {
      try {

        await cameraRef.current.recordAsync()
          .then(vidUri => {
            console.log("Video got ", vidUri)
            setVideoUri(vidUri)
          })
          .catch(err => console.log("Unable to prodice video uri", err))
      } catch (error) {
        console.log("Error while recording video", error)
      }
    }};

  const stopRecording = () => {
    if (cameraRef.current && isRecording) {
      cameraRef.current.stopRecording();
    }
  };

  return {
        startRecording,
        stopRecording,
        requestPermissions,
        cameraPermission,
        microphonePermission,
        videoUri,
        cameraRef,
    }
}