import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import theme from '../Components/StaticStyle';
import { Button } from 'react-native-elements';
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';

export function Page() {
  const navigation = useNavigation();

  async function fetchData() {
    try {
      const response = await axios.get('http://localhost:8000/api/videos/'); // Replace with your actual API endpoint
      console.log(response.data); // Handle the response data here
    } catch (error) {
      console.error(error); // Handle errors here
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome To Mappify!</Text>
      <Button
        title="Start Scan"
        buttonStyle={styles.button}
        titleStyle={styles.buttonText}
        onPress={() => {
          fetchData(); // Call the fetchData function here
          console.log('Start Scan button pressed');
          navigation.navigate('Accelerometer');
        }}
      />
      <Button
        title="Search"
        buttonStyle={styles.button}
        titleStyle={styles.buttonText}
        onPress={() => console.log('search was pressed')}
      />
      <Button
        title="Go to Video List"
        buttonStyle={styles.button}
        titleStyle={styles.buttonText}
        onPress={() => {
          console.log('Go to Video List button pressed');
          navigation.navigate('Videos');
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: '100%',
    backgroundColor: theme.colors.background,
    flexDirection: 'column',
    alignItems: 'center',
  },
  title: {
    fontFamily: theme.fonts.primary,
    color: theme.colors.dominant,
    fontSize: 55,
    textAlign: 'center',
    width: '100%',
    marginTop: 130,
    marginBottom: 50,
  },
  button: {
    backgroundColor: theme.colors.secondary,
    marginTop: 30,
    width: 200,
    height: 100,
    borderRadius: 10,
  },
  buttonText: {
    fontSize: 30,
    color: theme.colors.primary,
  },
});

export default Page;
