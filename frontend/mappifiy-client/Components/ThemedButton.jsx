import { StyleSheet, Text } from "react-native";
import {TouchableOpacity} from 'react-native'
import theme from "./StaticStyle"

function ThemedButton({title, buttonStyle, textStyle, onPress}) {
  return (
    <TouchableOpacity 
          style={buttonStyle? buttonStyle : styles.container}
          onPress = {onPress} 
    >

      <Text style={styles.text}> 
        {title}
      </Text>
    </TouchableOpacity>

    );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.secondary,
    marginTop: 30,
    width: 200,
    borderRadius: 10
  },
    text: {
      textAlign:"center",
      fontSize:30, 
      margin: 15,
      color: theme.colors.primary,
      fontFamily: theme.fonts.primary
  },
})

export default ThemedButton;
