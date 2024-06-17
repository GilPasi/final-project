import { StyleSheet, Text } from "react-native";
import {TouchableOpacity} from 'react-native'
import theme from "./StaticStyle"

function ThemedButton({title, buttonStyle, textStyle, onPress, size, disabled}) {
  
  const getSizes = () => {
    let _fontSize = 0
    let _width = 0
    
    switch (size){
      case 'small':
        _width = 100
        _fontSize = 25  
        break

      default: 
        _width = 200
        _fontSize = 35
    }

    return {_fontSize, _width}
  }
  
  const {_fontSize, _width} = getSizes()

  return (
    <TouchableOpacity 
          style={ {...styles.container, width:_width}}
          onPress = {onPress} 
          disabled={disabled}
    >
      <Text style={{...styles.text, fontSize: _fontSize}}> 
        {title}
      </Text>
    </TouchableOpacity>

    );
}
export default ThemedButton;


const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.secondary,
    marginTop: 30,
    borderRadius: 10
  },
    text: {
      textAlign:"center",
      margin: 15,
      color: theme.colors.primary,
      fontFamily: theme.fonts.primary
  },
})