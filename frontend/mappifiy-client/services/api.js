import axios from 'axios';
import {get_server_host_name} from '../utilities/utils'

export const API_BASE_URL = `${get_server_host_name()}/api`


export const api = axios.create({
  baseURL: API_BASE_URL, 
});

export const videoApi = axios.create({
  baseURL: API_BASE_URL, 
  headers: {'Content-Type': 'multipart/form-data'},
});



