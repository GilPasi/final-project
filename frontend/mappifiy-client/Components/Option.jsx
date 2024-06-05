import { StyleSheet, Text } from "react-native";
import {TouchableOpacity} from 'react-native'
import theme from "./StaticStyle"

export default function Option({text, value, buttonStyle, textStyle, onPress, size}) {
  
  const getSizes = () => {
    let _fontSize = 0
    let _width = 0
    
    switch (size){
      case 'small':
        _width = 100
        _fontSize = 10  
        break

      default: 
        _width = "80%"
        _fontSize = 20
    }

    return {_fontSize, _width}
  }
  
  const {_fontSize, _width} = getSizes()


  const handlePress = () => {
    if (onPress) {
      onPress(value);
    }
  };

  return (
    <TouchableOpacity 
          style={ {...styles.container, width:_width}}
          onPress = {handlePress} 
    >

      <Text style={{...styles.text, fontSize: _fontSize}}> 
        {text}
      </Text>
    </TouchableOpacity>

    );
}


const styles = StyleSheet.create({
  container: {
    borderColor: theme.colors.primary,
    borderWidth: 2,
    margin: 10,
    borderBottomLeftRadius: 5,
    borderBottomRightRadius: 5,
    borderStyle: "solid",
  },
    text: {
      textAlign:"center",
      margin: 15,
      color: "black", 
      fontFamily: theme.fonts.primary
  },
})