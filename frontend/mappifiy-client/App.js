import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import IndexScreen from './Screens/IndexScreen';
import {View, Text} from  'react-native'
import AccelerometerScreen from './Screens/AccelerometerScreen';

const Stack = createNativeStackNavigator();

function App() {
  return (
    // <View>
    //   <IndexScreen/>
    //   <AccelerometerScreen/>
    // </View>
 
    <NavigationContainer>
      <Stack.Navigator>  
        <Stack.Screen name="Index" component={IndexScreen} />
        <Stack.Screen name="Accelerometer" component={AccelerometerScreen} />
      </Stack.Navigator>
    </NavigationContainer>
    


  );
}

export default App;
