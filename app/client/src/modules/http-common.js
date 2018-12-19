import axios from 'axios';

const _baseApiURL = `/lettres/api/1.0`;
const _baseAppURL = `/lettres`;

const http = axios.create({
  baseURL: _baseApiURL,
  /*headers: {
    Authorization: 'Bearer {token}'
  }*/
});

export const baseApiURL = _baseApiURL;
export const baseAppURL = _baseAppURL;
export default http;

