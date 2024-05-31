import { CameraView, useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import { useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import {api} from '../services/api';
import ThemedButton  from '../Components/ThemedButton';
import {getBaseUrl} from '../utilities/utils'


export default function App() {
  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [microphonePermission, requestMicrophonePermission] = useMicrophonePermissions();
  const [isRecording, setIsRecording] = useState(false)
  const [videoUri, setVideoUri] = useState(null);

  let cameraRef = useRef()
  let csrfRef = useRef(null)

  async function requestPermissions() {
    const cameraStatus = await requestCameraPermission();
    const microphoneStatus = await requestMicrophonePermission();

    if (cameraStatus.granted && microphoneStatus.granted) {
      console.log("Permissions granted");
    } else {
      console.log("Permissions not granted");
    }
  }


  const sendVideoToServer = async (uriObj) => {
    const uri = uriObj.uri;
    const fileType = uri.split('.').pop();
  
    let formData = new FormData();
    formData.append('video', {
      uri,
      name: `video.${fileType}`,
      type: `video/${fileType}`
    });
  
    const url = '/upload/'; 
  
    try {
      const response = await api.post(url, formData, {
        headers: {
          'X-CSRFToken': csrfRef.current
        }
      });
  
      if (response.status === 201) {
        console.log('Video uploaded successfully!');
      } else {
        console.log('Video upload failed.');
      }
    } catch (error) {
      console.log('Error while trying to upload to server:', error);
    }
  };
  const fetchCsrfToken = async () => {
    try {
      url = `/get-csrf-token/`
      const response = await api.get(url);
      const token = extractCsrfToken(response);
      csrfRef.current = token
      console.log("CSRF Token:", token);
    } catch (err) {
      console.error("Something went wrong while querying CSRF token:", err);
    }
  };

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


  useEffect(() => {
    requestPermissions();
    fetchCsrfToken()
  }, []);

  


  const startRecording = async () => {
    if (cameraRef.current) {
      try {
        setIsRecording(true);
        await cameraRef.current.recordAsync()
          .then(vidUri => {
            console.log("Video got ", vidUri)
            setVideoUri(vidUri)
          })
          .catch(err => console.log("something went wrong", err))
        setIsRecording(false);

      } catch (error) {
        setIsRecording(false);
      }
    }};

  const stopRecording = () => {
    if (cameraRef.current && isRecording) {
      cameraRef.current.stopRecording();
    }
  };

  function toggleRecord(){
    if(isRecording){
      console.log("Recording stopped")
      stopRecording()
    }
    else{
      console.log("Recording started")
      startRecording()
    }
  }

  if (!cameraPermission || !microphonePermission) {
    return <View />;
  }

  if (!cameraPermission.granted || !microphonePermission.granted) {
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
        <ThemedButton onPress={requestPermissions} title="Grant Permission" />
      </View>
    );
  }

  return (
    <View style={{...styles.container, alignItems: videoUri ? 'center': 'left'}}>
      {videoUri ? (
        <ThemedButton
            title="Send Video"
            onPress={() => sendVideoToServer(videoUri)}
          />
        ):(
          <CameraView mode="video" style={styles.camera} ref={cameraRef}>
            <View style={styles.buttonContainer}>
              <TouchableOpacity style={styles.button} onPress={toggleRecord}>
                <Text style={{fontSize:100, color:"#C41E3A"}}>{isRecording? "■" : "⬤" }</Text>
              </TouchableOpacity>
            </View>
          </CameraView>
    )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 5,
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});




// import { useState, useEffect } from 'react';
// import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
// import { Gyroscope } from 'expo-sensors';
// import {getSmartPhoneFps} from '../utilities/utils'

// export default function App() {
//   const [{ x, y, z }, setData] = useState({
//     x: 0,
//     y: 0,
//     z: 0,
//   });
//   const [subscription, setSubscription] = useState(null);
//   const [recording, setRecording] = useState([])


//   const _subscribe = () => {
//     setSubscription(
//       Gyroscope.addListener(gyroscopeData => {
//         setData(gyroscopeData);
//         setRecording([...recording,gyroscopeData])
//       })
//     );
//   };

//   const _unsubscribe = () => {
//     subscription && subscription.remove();
//     setSubscription(null);
//   };

//   useEffect(() => {
//     _subscribe();
//     Gyroscope.setUpdateInterval(getSmartPhoneFps())
//     return () => _unsubscribe();
//   }, []);

//   return (
//     <View style={styles.container}>
//       <Text style={styles.text}>Gyroscope:</Text>
//        <Text style={styles.text}>x: {x}</Text>
//       <Text style={styles.text}>y: {y}</Text>
//       <Text style={styles.text}>z: {z}</Text>
//      <View style={styles.buttonContainer}>
//         <TouchableOpacity 
//           onPress={subscription ? _unsubscribe : _subscribe}
//           style={styles.button}
//         >
//           <Text>{subscription ? 'On' : 'Off'}</Text>
//         </TouchableOpacity>
//       </View>
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//     paddingHorizontal: 10,
//   },
//   text: {
//     textAlign: 'center',
//   },
//   buttonContainer: {
//     flexDirection: 'row',
//     alignItems: 'stretch',
//     marginTop: 15,
//   },
//   button: {
//     flex: 1,
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: '#eee',
//     padding: 10,
//   },
//   middleButton: {
//     borderLeftWidth: 1,
//     borderRightWidth: 1,
//     borderColor: '#ccc',
//   },
// });
