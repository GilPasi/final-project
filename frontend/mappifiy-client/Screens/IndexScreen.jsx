import React, { Component } from "react";
import { StyleSheet, View, Text } from "react-native";
import theme from "../Components/StaticStyle";
import ThemedButton  from '../Components/ThemedButton';
import Title  from '../Components/Title';
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';

export function Page() {
  const navigation = useNavigation();

  async function fetchData() {
    try {

      const response = await axios.get('http://localhost:8000/api/videos/'); 
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <View style={styles.container}>
      <Title text='Welcome To Mappify!'/> 
      <ThemedButton
        title="To Scan"
        onPress={() => {
          navigation.navigate('Record Video');
        }}
      />
      <ThemedButton
        title="Start Scan"
        onPress={() => {
          fetchData(); 
          console.log("Start Scan button pressed");
          navigation.navigate('Record Video');

        }}
      />
      <ThemedButton
        title="Search"
        onPress={() => console.log("search was pressed")}
      />
      <ThemedButton
        title="Go to Video List"
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
  });
export default Page;
