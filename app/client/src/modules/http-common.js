import axios from 'axios';

const HTTP = axios.create({
  baseURL: `/lettres/api/1.0`,
  /*headers: {
    Authorization: 'Bearer {token}'
  }*/
})

export default HTTP;