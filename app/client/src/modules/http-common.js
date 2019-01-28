import axios from 'axios';
import { getCookie } from './cookies-helpers'
const _baseApiURL = `/lettres/api/1.0`;
const _baseAppURL = `/lettres`;


export const baseApiURL = _baseApiURL;
export const baseAppURL = _baseAppURL;
export const http = axios.create({
  baseURL: _baseApiURL,
  headers: {
    //Authorization: 'Bearer {token}'
    //'Authorization': 'Bearer ' + getCookie('csrf_access_token'),
    //'X-CSRFToken': getCookie('csrf_access_token'),
    'X-CSRF-Token': getCookie('csrf_access_token'),
    //'CSRF': getCookie('csrf_access_token'),
  }
});


