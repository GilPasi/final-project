import React, { Component } from "react";
import { StyleSheet, View, Text } from "react-native";
import theme from "../Components/StaticStyle";
import ThemedButton  from '../Components/ThemedButton';
import Title  from '../Components/Title';
import { useNavigation } from '@react-navigation/native';

export function Page() {
  const navigation = useNavigation();
  return (
    <View style={styles.container}>
      <Title text='Welcome To Mappify!'/> 
      <ThemedButton
        title="Start Scan"
        onPress={() => {
          navigation.navigate('Record Video');
        }}
      />
      <ThemedButton
        title="Search Map"
        onPress={()=>navigation.navigate('Maps')}
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
