import { CameraView } from 'expo-camera';
import { useEffect, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import ThemedButton from '../Components/ThemedButton';
import Title from '../Components/Title';
import LoadingBar from '../Components/LoadingBar';
import { usePipeline, FAILURE_MSG, SUCCESS_MSG } from '../Hooks/usePipeline';
import useGyro from '../Hooks/useGyro'
import useCam from '../Hooks/useCam';
import theme from '../Components/StaticStyle';


export default function RecordingScreen() {
  const [isRecording, setIsRecording] = useState(false)
  const { uploadProgress, uploadStatus, uploadVideo, csrfToken } = usePipeline()
  const cam = useCam(isRecording)
  const gyro = useGyro(isRecording)


  useEffect(() => {
    cam.requestPermissions();
  }, []);

  function toggleRecord() {
    if (isRecording) {
      console.log("Recording stopped")
      gyro.stopRecording()
      cam.stopRecording()
      setIsRecording(false)
    }
    else {
      console.log("Recording started")
      gyro.startRecording()
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

  if (!csrfToken){
    return (
    <View style={styles.container} >
      <Title text={`A connection\n error has occurred.`} isError={true} size='big'/>
      <Text style={{color: theme.colors.error,textAlign:'center'}}>
        {`please check your \n internet connection and refresh the page.
        Alternatively check the console's logs for \nfarther trouble-shooting`}
        </Text>
    </View>
    )
  }

  if (cam.videoUri ) {
    return (<View style={{ ...styles.container, alignItems: cam.videoUri ? 'center' : 'left' }}>
      {uploadStatus != SUCCESS_MSG && <ThemedButton
        title="Send Video"
        onPress={() => uploadVideo(cam.videoUri, gyro.data)}
      />}
      <Title text={uploadStatus} size={40} />
      <LoadingBar progress={uploadProgress} />
    </View>)
  }

  else return (
    <View style={{ ...styles.container, alignItems: cam.videoUri ? 'center' : 'left' }}>
      <View style={styles.camera}>
        <CameraView mode="video" style={styles.camera} ref={cam.cameraRef}>
          <View style={styles.buttonContainer}>
            <TouchableOpacity style={styles.button} onPress={toggleRecord}>
              <Text style={styles.recButton}>{isRecording ? "■" : "⬤"}</Text>
            </TouchableOpacity>
          </View>
        </CameraView>
      </View>
    </View>)
  }

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
    },
    recButton: {
      fontSize: 100,
      color: "#C41E3A"
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