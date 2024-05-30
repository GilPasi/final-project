import { CameraView, useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import { useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import {api, videoApi, API_BASE_URL} from '../services/api';
import axios from 'axios'
import ThemedButton  from '../Components/ThemedButton';




const sendVideoToServer = async (uriObj) => {
  uri = uriObj.uri
  let fileType = uri.split('.').pop();

  let formData = new FormData();
  formData.append('video', {
    uri,
    name: `video.${fileType}`,
    type: `video/${fileType}`
  });


  const response = await fetch('http://10.0.2.2:8000/upload/', {
    method: 'POST',
    body: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  console.log("4")


  if (response.ok) {
    console.log('Video uploaded successfully!');
  } else {
    console.log('Video upload failed.');
  }
};

const sendVideoToServer1 = async (videoUri) => {
    const videoFile = {
      uri: videoUri,
      name: 'video.mp4',
      type: 'video/mp4',
    };

    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('title', 'Sample Video');

    console.log("vidfile ,",typeof(videoFile))


    const getFormData = object => Object.keys(object).reduce((formData, key) => {
      formData.append(key, object[key]);
      return formData;
  }, new FormData());

    const response = await videoApi.post('/upload/', getFormData(formData));

    const videoData = {
      title: 'Sample Video',
      description: 'This is a sample video description',
    };

    objectToSend = videoData

    // const response = await api.get('/upload/');
    // console.log(response)

    // const response2 = await api.post('/upload/', videoData);

    // console.log('Server response:', response.data);

}


export default function App() {
  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [microphonePermission, requestMicrophonePermission] = useMicrophonePermissions();
  const [isRecording, setIsRecording] = useState(false)
  const [videoUri, setVideoUri] = useState(null);

  let cameraRef = useRef()

  async function requestPermissions() {
    const cameraStatus = await requestCameraPermission();
    const microphoneStatus = await requestMicrophonePermission();

    if (cameraStatus.granted && microphoneStatus.granted) {
      console.log("Permissions granted");
    } else {
      console.log("Permissions not granted");
    }
  }

  useEffect(() => {
    requestPermissions();
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
// import {get_smartphone_fps} from '../utilities/utils'

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
//     Gyroscope.setUpdateInterval(get_smartphone_fps())
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
