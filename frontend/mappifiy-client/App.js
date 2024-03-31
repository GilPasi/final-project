import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import {Page} from "./Components/Page"
import {AccelerometerPage} from "./Components/AccelerometerPage"


export default function App() {
  return (
    <View style={styles.container}>
      {/* <Page/> */}
      <AccelerometerPage/>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
