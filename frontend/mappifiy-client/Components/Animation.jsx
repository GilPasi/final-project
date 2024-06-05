import React from 'react';
import { View } from 'react-native';
import SvgUri from 'react-native-svg-uri'; // if you want to use URI

import Logo from './assets/logo.svg'; // Adjust the path accordingly

export default function App() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Logo width={200} height={200} />
    </View>
  );
}
