import React, { Component } from "react";
import { StyleSheet, View, Text } from "react-native";
import theme from "../Components/StaticStyle";
import { Button } from 'react-native-elements';
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';

export function Page() {
  const navigation = useNavigation();

  async function fetchData() {
    try {
      const response = await axios.get('http://localhost:8000/'); // Replace with your actual API endpoint
      console.log(response.data); // Handle the response data here
    } catch (error) {
      console.error(error); // Handle errors here
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome To Mappify!</Text>
      <Button
        title="To Scan"
        buttonStyle={styles.button}
        titleStyle={styles.buttonText}
        onPress={() => {
          navigation.navigate('Accelerometer');
        }}
      />
      <Button
        title="Start Scan"
        buttonStyle={styles.button}
        titleStyle={styles.buttonText}
        onPress={() => {
          fetchData(); 
          console.log("Start Scan button pressed");
          navigation.navigate('Accelerometer');
        }}
      />
      <Button
        title="Search"
        buttonStyle={styles.button}
        titleStyle={styles.buttonText}
        onPress={() => console.log("search was pressed")}
      />
    </View>
  );
}
  const styles = StyleSheet.create({
    container: {
      width: "100%",
      height: "100%",
      backgroundColor:theme.colors.background,
      flexDirection: 'column',
      alignItems: 'center',
    },
    title: {
        fontFamily: theme.fonts.primary,
        color: theme.colors.dominant,
        fontSize: 55,
        textAlign: "center",
        width:"100%",
        marginTop: 130,
        marginBottom: 50
      },
      button: {
        backgroundColor: theme.colors.secondary,
        marginTop: 30,
        width: 200,
        height: 100,
        borderRadius: 10
      },
      buttonText: {
        fontSize:30, 
        color: theme.colors.primary
    }
  });

export default Page;
