import React, {useState} from "react";

import useApi from "./api";
import axios from "axios";
import {Navigate, Outlet} from "react-router-dom";
import { createBrowserHistory } from 'history';
import {Header} from "./Header";

export const Login = () => {
    const [email, setEmail] = useState();
    const [password, setPassword] = useState();
    // const [errorMessage, setErrorMessage] = useState("");
    // const [, setToken] = useContext(UserContext);
    // const [result, setRes] = useState(false);
    const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"));
    // const [myItems, handleRegistration, isAuth, handleLogin] = useApi();

    const submitLogin = React.useCallback(async () => {

        // const {email, password} = document.forms[0]

        const tttmp = JSON.stringify(
            `grant_type=&username=${document.forms[0][0].value}&password=${document.forms[0][1].value}&scope=&client_id=&client_secret=`
        )

        console.log(tttmp)

        const response = axios.post("http://localhost:8081/api/token", tttmp, {
            headers:{'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'}
        });

        let resdata = (await response).data;

        if (resdata) {
            localStorage.setItem("awesomeLeadsToken", resdata.access_token);
            setToken(resdata)
            const history = createBrowserHistory();
        } else {
            alert('gg');
            // setErrorMessage(data.detail);
        }

    }, [token]);

    const handleSubmit = (e) => {
        e.preventDefault();
        submitLogin();
    };

    return (
        <>
            <Header title="Project"></Header>
            {token ? (
                <Navigate to="/"/>
            ) : (
                <div className="column">
                    <form className="box" onSubmit={handleSubmit}>
                        <h1 className="title has-text-centered">Вход</h1>
                        <div className="field">
                            <label className="label">Email</label>
                            <div className="control">
                                <input
                                    type="email"
                                    placeholder="Введите email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Пароль</label>
                            <div className="control">
                                <input
                                    type="password"
                                    placeholder="Введите пароль"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <br />
                        <button className="button is-primary" type="submit">
                            Войти
                        </button>
                    </form>
                </div>
            )}
        </>
    );
};
