import React from "react";
import axios from "axios";

export default function useApi() {
  const [myItems, setMyItems] = React.useState();

  const [isAuth, setIsAuth] = React.useState(false);

  const handleLogin = React.useCallback(async (data) => {

    const tttmp = JSON.stringify(
        `grant_type=&username=ritmic@gmail.com&password=string&scope=&client_id=&client_secret=`
      )
    const response = axios.post("/api/v1/login", tttmp, {
      headers:{'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'}
    });

    let resdata = (await response).data;

    if (resdata) {
      alert('ok');
      setIsAuth(true);

      //setToken(data.access_token);

    } else {

      alert('gg');
    }
  }, []);

  const handleRegistration = React.useCallback(async (data) => {

    const response = axios.post("/api/v1/registration", {
      email: data.email, hashed_password: data.hashed_password
    })

    let resdata = (await response).data;

    if (resdata) {
            alert('ok');
      setIsAuth(true);
      //setToken(data.access_token);

    } else {

      alert('gg');
    }
  }, []);

  React.useEffect(() => {
    axios.get("/api/v1/rentals?city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&page=1&size=10").then((response) => {
      setMyItems(response.data);
    });
  }, []);

  return [myItems, handleRegistration, isAuth, handleLogin];
}
