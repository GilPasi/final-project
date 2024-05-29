import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import IndexScreen from './Screens/IndexScreen';
import RecordingScreen from './Screens/RecordingScreen';

const Stack = createNativeStackNavigator();

function App() {
  return ( 
    <NavigationContainer>
      <Stack.Navigator>  
        <Stack.Screen name="Index" component={IndexScreen} />
        <Stack.Screen name="Accelerometer" component={RecordingScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;
