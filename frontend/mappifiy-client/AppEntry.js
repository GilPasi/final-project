import {useEffect} from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import IndexScreen from './Screens/IndexScreen';
import RecordingScreen from './Screens/RecordingScreen';
import VideoListScreen from './Screens/VideoListScreen';
import AppEntry from './AppEntry'


const Stack = createNativeStackNavigator();

function AppEntry() {
  return <App/>
}

export default AppEntry;
