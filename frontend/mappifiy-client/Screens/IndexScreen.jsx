import React, { Component } from "react";
import { StyleSheet, View, Text} from "react-native";
import theme from "../Components/StaticStyle"
import { Button } from 'react-native-elements';
import { useNavigation } from '@react-navigation/native';
export function Page() {
  const navigation = useNavigation();

    return (
    <View style={styles.container}>
        <Text style={styles.title}>Welcom To Mappify!</Text>
        <Button 
            title="Start Scan"
            buttonStyle={styles.button}
            titleStyle={styles.buttonText}
            onPress={() => {
              console.log("Start Scan button pressed"); // Log message
              navigation.navigate('Accelerometer'); // Navigate to AccelerometerScreen
            }}
          />

        <Button 
            title="Search"
            buttonStyle={styles.button}
            titleStyle={styles.buttonText}
            onPress={()=>console.log("search was pressed")}
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
