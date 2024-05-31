import axios from 'axios';
import {getBaseUrl} from '../utilities/utils'

export const API_BASE_URL = `${getBaseUrl()}/api`

export const api = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});



