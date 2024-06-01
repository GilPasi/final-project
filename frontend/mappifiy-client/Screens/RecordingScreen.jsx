import { CameraView, useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import { useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import ThemedButton  from '../Components/ThemedButton';
import Title  from '../Components/Title';
import LoadingBar  from '../Components/LoadingBar';
import usePipeline from '../Hooks/usePipeline';
import useGyro from '../Hooks/useGyro'
import useCam from '../Hooks/useCam';


export default function RecordingScreen() {
  const [isRecording, setIsRecording] = useState(false)
  const {uploadProgress, uploadStatus, uploadVideo } = usePipeline()
  const cam = useCam(isRecording)
  const gyro = useGyro(isRecording)


  useEffect(() => {
    cam.requestPermissions();
  }, []);

  function toggleRecord(){
    if(isRecording){
      console.log("Recording stopped")
      gyro.stopRecord()
      cam.stopRecording()
      setIsRecording(false)
    }
    else{
      console.log("Recording started")
      gyro.startRecord()
      cam.startRecording()
      setIsRecording(true)
    }
  }

  if (!cam.cameraPermission || !cam.microphonePermission) {
    return <View />;
  }

  if (!cam.cameraPermission.granted || !cam.microphonePermission.granted) {
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
        <ThemedButton onPress={cam.requestPermissions} title="Grant Permission" />
      </View>
    );
  }

  return (
    <View style={{...styles.container, alignItems: cam.videoUri ? 'center': 'left'}}>
      {cam.videoUri ? (
        <View>
          {uploadProgress != 100 &&<ThemedButton
            title="Send Video"
            onPress={() => uploadVideo(cam.videoUri)}
          />}
            <Title text={uploadStatus} size={40}/>
            <LoadingBar progress={uploadProgress}/>
        </View>

        ):(
          <View style={styles.camera}>
            <CameraView mode="video" style={styles.camera} ref={cam.cameraRef}>
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