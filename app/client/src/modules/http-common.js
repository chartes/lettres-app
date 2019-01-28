import axios from 'axios';

const _baseApiURL = `/lettres/api/1.0`;
const _baseAppURL = `/lettres`;


export const baseApiURL = _baseApiURL;
export const baseAppURL = _baseAppURL;
export const http = axios.create({
  baseURL: _baseApiURL,
  /*headers: {
    Authorization: 'Bearer {token}'
  }*/
});


