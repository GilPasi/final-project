
import { Gyroscope } from 'expo-sensors';
import { useState, useEffect } from 'react';
import {getSmartPhoneFps} from '../utilities/utils'

export default function useGyro(isRecording) {
  const [data, setData] = useState([{
    x: 0,
    y: 0,
    z: 0,
  }]);
  
  const [subscription, setSubscription] = useState(null);

  const startRecording = () => {
    setData([])
    setSubscription(
      Gyroscope.addListener(gyroscopeData => {
        setData(prevData=> [...prevData, gyroscopeData]);
      })
    );
  };

  const stopRecording = () => {
    if (!isRecording && subscription) {
      subscription.remove();
      setSubscription(null);
      console.log("Gyroscope data collected: ", data.slice(0, 2), "\n...")
    }
  };
  

  useEffect(() => {
    startRecording();
    const milisecondsInSecond = 1000 
    Gyroscope.setUpdateInterval(milisecondsInSecond / getSmartPhoneFps())
    return () => stopRecording();
  }, []);

  return {data, startRecording, stopRecording};
}
