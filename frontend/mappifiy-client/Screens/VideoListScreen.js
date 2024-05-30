import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, FlatList } from 'react-native';
import api from '../services/api';

const VideoListScreen = () => {
  const [videos, setVideos] = useState([]);
  const [error, setError] = useState(null);
  const [message, setmessage] = useState('');

  const fetchVideos = async () => {
    try {
      console.log('Fetching videos...');
      const response = await api.get('/videos/1');
      console.log('Response:', response.data);
      setmessage('' + response)
      setVideos(response.data);
    } catch (err) {
      console.error('Error fetching videos:', err.message);
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchVideos();
  }, []);

  return (
    <View style={styles.container}>
       <Text style={styles.title}>Video List</Text>
      {error && <Text style={styles.error}>Error: {error}</Text>}
      <Text > {'' + message.data} </Text>
      
      {/*<FlatList
        data={videos}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.videoItem}>
            <Text>{item.title}</Text>
            <Text>{item.upload_date}</Text>
          </View>
        )}
      /> */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  error: {
    color: 'red',
    marginBottom: 20,
  },
  videoItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
});

export default VideoListScreen;
