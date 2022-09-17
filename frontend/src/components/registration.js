import React, {useState} from "react";
import axios from "axios";
import {Navigate} from "react-router-dom";
import {Header} from "./Header";

export const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  // const [errorMessage, setErrorMessage] = useState("");
  const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"));
  // const [, setToken] = useContext(UserContext);

  const submitRegistration = React.useCallback(async () => {

    const email = document.forms[0][0].value;
    const password = document.forms[0][1].value;
    console.log(email, password);
    const response = axios.post("http://localhost:8081/api/users", {
      email: email, hashed_password: password
    })

    let resdata = (await response).data;
    console.log(resdata.ok);

    if (resdata.ok) {
      // setIsAuth(true);
      localStorage.setItem("awesomeLeadsToken", resdata.access_token);
      setToken(resdata.access_token);
    } else {
      alert('gg');
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length > 5) {
      submitRegistration();
    } else {
      alert("error");
      // setErrorMessage(
      //   "Ensure that the passwords match and greater than 5 characters"
      // );
    }
  };

  return (
      <>
        <Header title="Project"></Header>
        {token ? (
            <Navigate to="/"/>
        ):(
            <div className="column">
              <form className="box" onSubmit={handleSubmit}>
                <h1 className="title has-text-centered">Register</h1>
                <div className="field">
                  <label className="label">Email Address</label>
                  <div className="control">
                    <input
                        type="email"
                        placeholder="Enter email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="input"
                        required
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label">Password</label>
                  <div className="control">
                    <input
                        type="password"
                        placeholder="Enter password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="input"
                        required
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label">Confirm Password</label>
                  <div className="control">
                    <input
                        type="password"
                        placeholder="Enter password"
                        value={confirmationPassword}
                        onChange={(e) => setConfirmationPassword(e.target.value)}
                        className="input"
                        required
                    />
                  </div>
                </div>
                <br />
                <button className="button is-primary" type="submit">
                  Register
                </button>
              </form>
            </div>
        )}
      </>
  );
};
