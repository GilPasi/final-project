// import {useEffect} from 'react';
// import { NavigationContainer } from '@react-navigation/native';
// import { createNativeStackNavigator } from '@react-navigation/native-stack';
// import useLoadFonts from './Hooks/useLoadFonts'
// import IndexScreen from './Screens/IndexScreen';
// import RecordingScreen from './Screens/RecordingScreen';
// import VideoListScreen from './Screens/VideoListScreen';
// import { View, ActivityIndicator } from 'react-native';

// const Stack = createNativeStackNavigator();

// function App() {
//   const { fontsLoaded, fontError, onLayoutRootView } = useLoadFonts();

//   useEffect(() => {
//     onLayoutRootView();
//   }, [onLayoutRootView]);

//   if (!fontsLoaded && !fontError) {
//     return (
//       <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
//         <ActivityIndicator size="large" />
//       </View>
//     );
//   }

//   return ( 
//     <NavigationContainer>
//       <Stack.Navigator>  
//         <Stack.Screen name="Index" component={IndexScreen} />
//         <Stack.Screen name="Record Video" component={RecordingScreen} />
//         <Stack.Screen name="Videos" component={VideoListScreen} />
//       </Stack.Navigator>
//     </NavigationContainer>
//   );
// }

// export default App;



import { Image } from 'expo-image';
import { StyleSheet, View } from 'react-native';


export default function App() {

  return (
    <View style={styles.container}>
      <Image 
        alt="dsadsa" 
        source='http://10.0.0.2:8000/api/media/maps/2.png'
        style={styles.image}
       />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    flex: 1,
    width: '100%',
    backgroundColor: '#0553',
  },
});
