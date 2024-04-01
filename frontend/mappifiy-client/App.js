import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Page from './Components/Page';
import {View, Text} from  'react-native'
import AccelerometerScreen from './Components/AccelerometerScreen';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <View>
      {/* <Page/> */}
      <AccelerometerScreen/>
    </View>
    // <NavigationContainer>
    //   <Stack.Navigator>
    //     <Stack.Screen name="Home" component={Page} />
    //     <Stack.Screen name="Details" component={Accelerometer} />
    //   </Stack.Navigator>
    // </NavigationContainer>
  );
}

export default App;
