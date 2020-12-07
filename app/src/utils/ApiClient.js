import Endpoint from './Endpoint';

const register = (accessToken) => {
  const requestOptions = {
    method: 'POST',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  return fetch(Endpoint.register(), requestOptions).then(res => res.json());
}

export default register;