import {useEffect} from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import IndexScreen from './Screens/IndexScreen';
import RecordingScreen from './Screens/RecordingScreen';
import VideoListScreen from './Screens/VideoListScreen';

const Stack = createNativeStackNavigator();

function App() {
    const { fontsLoaded, fontError, onLayoutRootView } = useLoadFonts();

    useEffect(() => {
      onLayoutRootView();
    }, [onLayoutRootView]);

    if (!fontsLoaded && !fontError) {
      return null;
    }

  return ( 
    <NavigationContainer>
      <Stack.Navigator>  
        <Stack.Screen name="Index" component={IndexScreen} />
        <Stack.Screen name="Record Video" component={RecordingScreen} />
        <Stack.Screen name="Videos" component={VideoListScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;
