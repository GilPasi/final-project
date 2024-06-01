import { CameraView, useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import { useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import ThemedButton  from '../Components/ThemedButton';
import Title  from '../Components/Title';
import LoadingBar  from '../Components/LoadingBar';
import usePipeline from '../Hooks/usePipeline';
import useGyro from '../Hooks/useGyro'


export default function RecordingScreen() {
  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [microphonePermission, requestMicrophonePermission] = useMicrophonePermissions();
  const [isRecording, setIsRecording] = useState(false)
  const [videoUri, setVideoUri] = useState(null);

  const {uploadProgress, uploadStatus, uploadVideo } = usePipeline()
  const gyro = useGyro()

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
      setIsRecording(true);
      try {
        gyro.startRecord()
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
    gyro.stopRecord()
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
        <View>
          {uploadProgress != 100 &&<ThemedButton
            title="Send Video"
            onPress={() => uploadVideo(videoUri)}
          />}
            <Title text={uploadStatus} size={40}/>
            <LoadingBar progress={uploadProgress}/>
        </View>

        ):(
          <View style={styles.camera}>
            <CameraView mode="video" style={styles.camera} ref={cameraRef}>
              <View style={styles.buttonContainer}>
                <TouchableOpacity style={styles.button} onPress={toggleRecord}>
                  <Text style={{fontSize:100, color:"#C41E3A"}}>{isRecording? "■" : "⬤" }</Text>
                </TouchableOpacity>
              </View>
            </CameraView>
            <Text>{gyro.data.x}</Text>
            <Text>{gyro.data.y}</Text>
            <Text>{gyro.data.z}</Text>
          </View>
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