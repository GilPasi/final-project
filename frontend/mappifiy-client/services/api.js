import axios from 'axios';
import {getBaseUrl} from '../utilities/utils'

export const API_BASE_URL = `${getBaseUrl()}/api`

export const api = axios.create({
  baseURL:API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});



