import axios from 'axios';
import { getCookie } from './cookies-helpers'
const _baseApiURL = `/lettres/api/1.0`;
const _baseAppURL = `/lettres`;


export const baseApiURL = _baseApiURL;
export const baseAppURL = _baseAppURL;

export const http = axios.create({
  baseURL: _baseApiURL,
  headers: {}
});

function http_with_csrf_token() {
  return axios.create({
    baseURL: _baseApiURL,
    headers: {
     'X-CSRF-Token': getCookie('csrf_access_token'),
    }
  });
}

http.interceptors.response.use(function (response) {
  return response
}, function (error) {
  const { config, response: { status } } = error;
  const originalRequest = config;

  if (status === 401) {
    return  new Promise((resolve) => {
      console.warn("MAJ HEADERS");
      console.warn("from ", originalRequest.headers['X-CSRF-Token']);
      originalRequest.headers['X-CSRF-Token'] = getCookie('csrf_access_token');
      originalRequest.baseURL = '';
      console.warn("to ", originalRequest.headers['X-CSRF-Token']);
      resolve(axios(originalRequest));

    });
  }
  return Promise.reject(error)
});

export default http_with_csrf_token;


