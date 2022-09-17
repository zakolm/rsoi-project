import React, {useEffect, useState} from 'react';
import {Navigate, Outlet} from 'react-router-dom';
import axios from "axios";

const RouteGuard = (navigate) => {
    const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"));

    useEffect(() => {
        const fetchUser = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
            };

            const response = await fetch("/api/v1/me", requestOptions);

            // console.log(response);
            if (!response.ok) {
                setToken("");
            }
            localStorage.setItem("awesomeLeadsToken", token);
        };
        fetchUser();
        }, [token]);

    // console.log(token)
    localStorage.setItem("awesomeLeadsToken", token);

    return (
        <Outlet/>
        // token ? <Outlet/> : <Navigate to={navigate}/>
    );
};

export const RouteGuard_private = (navigate) => {
    const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"));

    useEffect(() => {
        const fetchUser = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
            };

            const response = await fetch("/api/v1/me", requestOptions);

            console.log(response.ok);
            if (!response.ok) {
                setToken("");
            }
            localStorage.setItem("awesomeLeadsToken", token);
        };
        fetchUser();
        }, [token]);

    // console.log(token)
    localStorage.setItem("awesomeLeadsToken", token);

    return (
        // <Outlet/>
        token ? <Outlet/> : <Navigate to="/login"/>
    );
};

export default RouteGuard;
