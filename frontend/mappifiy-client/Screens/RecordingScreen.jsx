import { CameraView, useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import { useEffect, useRef, useState } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

function printObjectMethods(obj) {
  let methods = [];
  let currentObj = obj;

  // Traverse the prototype chain to get all methods, including inherited ones
  while (currentObj) {
    const properties = Object.getOwnPropertyNames(currentObj);

    properties.forEach(property => {
      if (typeof obj[property] === 'function' && !methods.includes(property)) {
        methods.push(property);
      }
    });

    currentObj = Object.getPrototypeOf(currentObj);
  }

  // Print all the methods
  methods.forEach(method => console.log(method));
}


export default function App() {
  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [microphonePermission, requestMicrophonePermission] = useMicrophonePermissions();
  const [isRecording, setIsRecording] = useState(false)
  let cameraRef = useRef()
  let videoRef = useRef()


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
          .then(vidUri => console.log("Video got ", vidUri))
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
        <Button onPress={requestPermissions} title="Grant Permission" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView mode="video" style={styles.camera} ref={cameraRef}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={toggleRecord}>
            <Text style={{fontSize:100, color:"red"}}>{isRecording? "■" : "⬤" }</Text>
          </TouchableOpacity>
        </View>
      </CameraView>
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
    margin: 64,
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
