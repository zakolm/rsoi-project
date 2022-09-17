import React, {useEffect, useState} from "react";
import {Navigate} from "react-router-dom";
import axios from "axios";

export function CreateOrder(rental, device, tillDate) {
    // const [token] = useState(localStorage.getItem("awesomeLeadsToken"));


    // console.log('aaaa')
    // console.log(token)
    // const requestOptions = {
    //     method: "GET",
    //     headers: {
    //         "Content-Type": "application/json",
    //         Authorization: "Bearer " + token,
    //     },
    // };
    //
    // const response = await fetch("/api/v1/me", requestOptions);


    const data = {
        "deviceUid": device.deviceUid,
        "rentalUid": rental.rentalUid,
        "tillDate": tillDate
    };
    const response_ = axios.post("/api/v1/reservations", data, {
            headers:{'accept': 'application/json',
                'Authorization': 'zakolesnik.m@ya.ru'}
        });

    // console.log(await response_)
}

