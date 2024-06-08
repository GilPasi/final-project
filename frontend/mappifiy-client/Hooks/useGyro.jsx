import { Gyroscope } from 'expo-sensors';
import { useState, useEffect, useRef, useCallback } from 'react';
import { getSmartPhoneFps } from '../utilities/utils';

export default function useGyro(isRecording) {
  const [data, setData] = useState([]);
  const [subscription, setSubscription] = useState(null);
  const timerId = useRef(null);
  const startTime = useRef(null);
  const [timeElapsed, setTimeElapsed] = useState(0);

  const startTimer = useCallback(() => {
    if (timerId.current === null) {
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
    }
  }, []);

  const startRecording = useCallback(() => {
    setData([]);
    startTimer();
    setSubscription(
      Gyroscope.addListener((gyroscopeData) => {
        setData((prevData) => [...prevData, gyroscopeData]);
      })
    );
  }, [startTimer]);

  const stopRecording = useCallback(() => {
    _safeUnsubscribe();
    stopTimer();
  }, [stopTimer]);

  const _safeUnsubscribe = useCallback(() => {
    if (subscription) {
      subscription.remove();
      setSubscription(null);
      console.log('Gyroscope data collected: ', data.slice(0, 2), '\n...');
    }
  }, [subscription, data]);

  useEffect(() => {
    const millisecondsInSecond = 1000;
    const frameInterval = millisecondsInSecond / getSmartPhoneFps();
    Gyroscope.setUpdateInterval(frameInterval);
    // console.log('Gyro INTERVAL ', frameInterval);

    return () => _safeUnsubscribe();
  }, [_safeUnsubscribe]);

  const isReady = () => new Promise((resolve) => {
    const interval = setInterval(() => {
      if (Gyroscope) {
        clearInterval(interval);
        resolve();
      }
    }, 100);
  });

  return { data, startRecording, stopRecording, timeElapsed, isReady };
}
