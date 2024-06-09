import { useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import { useState, useRef, useEffect, useCallback } from 'react';

export default function useCam(isRecording) {
  const [timerActive, setTimerActive] = useState(false);
  const timerId = useRef(null);
  const startTime = useRef(null);
  const [timeElapsed, setTimeElapsed] = useState(0);

  const startTimer = useCallback(() => {
    if (timerId.current === null) {
      setTimerActive(true);
      startTime.current = Date.now();
      timerId.current = setInterval(() => {
        setTimeElapsed(Date.now() - startTime.current);
      }, 1000);
    }
  }, []);

  const stopTimer = useCallback(() => {
    if (timerId.current !== null) {
      clearInterval(timerId.current);
      timerId.current = null;
      setTimerActive(false);
    }
  }, []);

  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [microphonePermission, requestMicrophonePermission] = useMicrophonePermissions();
  const [videoUri, setVideoUri] = useState(null);
  const cameraRef = useRef();

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
        startTimer();
        const video = await cameraRef.current.recordAsync();
        stopTimer();
        setVideoUri(video.uri);
        endTime = Date.now()
        console.log(`Camera start time ${startTime.current} `,
          `| end time ${endTime} | delta ${ endTime - startTime.current} `)
        } catch (error) {
        console.log("Error while recording video", error);
      }
    }
  };

  const stopRecording = () => {
    if (cameraRef.current && isRecording) {
      cameraRef.current.stopRecording();
      stopTimer();
    }
  };

  const isReady = () => new Promise((resolve) => {
    if (cameraRef.current) {
      resolve();
    } else {
      const interval = setInterval(() => {
        if (cameraRef.current) {
          clearInterval(interval);
          resolve();
        }
      }, 100);
    }
  });

  return {
    startRecording,
    stopRecording,
    requestPermissions,
    cameraPermission,
    microphonePermission,
    videoUri,
    cameraRef,
    timeElapsed,
    isReady,
  };
}
