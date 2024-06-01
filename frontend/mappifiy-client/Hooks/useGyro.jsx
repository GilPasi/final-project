
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

  const _subscribe = () => {
    setSubscription(
      Gyroscope.addListener(gyroscopeData => {
        setData(prevData=> [...prevData, gyroscopeData]);
      })
    );
  };

  const _unsubscribe = () => {
    if (!isRecording && subscription) {
      subscription.remove();
      setSubscription(null);
    }
  };
  

  useEffect(() => {
    _subscribe();
    const milisecondsInSecond = 1000 
    Gyroscope.setUpdateInterval(milisecondsInSecond / getSmartPhoneFps())
    return () => _unsubscribe();
  }, []);

  const startRecord = () => {
    setData([])
    _subscribe()
  }

  const stopRecord = () =>{
    _unsubscribe()
    console.log(data.slice(0, 10), "\n...")
  }
  
  return {data, startRecord, stopRecord};
}
