import React, {useEffect, useState} from "react";
import moment from "moment";
import {Header} from "./Header";
import ErrorMessage from "./ErrorMessage";

export const Orders = () => {
    const [token] = useState(localStorage.getItem("awesomeLeadsToken"));
    const [orders, setOrders] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);

    const getOrders = React.useCallback(async () => {
        const requestOptions_email = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
        };
        const response_email = await fetch("http://127.0.0.1:8081/api/users/me", requestOptions_email);
        console.log(response_email)
        console.log(response_email.email)

        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "zakolesnik.m@ya.ru" //"Bearer " + token,
            },
        };
        const response = await fetch("/api/v1/reservations", requestOptions);
        if (!response.ok) {
            // alert('bad');
            setErrorMessage("Something went wrong. Couldn't load the orders");
            setLoaded(true);
        } else {
            const data = await response.json();
            setOrders(data);
            setLoaded(true);
        }
    }, []);

    useEffect(() => {
        getOrders();
        // console.log(moment());
    }, []);

    return (
        <>
            <Header title="Project"></Header>
            <div className="has-text-centered m-6">
                <h1 className="title is-2">Заказы</h1>
            </div>
            {errorMessage.length > 0 ? (
                <ErrorMessage message={errorMessage} />
                ): (<></>)
            }
            {loaded && orders ? (
                <table className="table is-fullwidth">
                    <thead>
                    <tr>
                        <th>Статус</th>
                        <th>Устройство</th>
                        <th>Бренд устройства</th>
                        <th>Рентал</th>
                        <th>Адрес</th>
                        <th>Начало аренды</th>
                        <th>Конец аренды</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>

                    {orders.map((order) => (
                        <tr>
                            <td>{order.status}</td>
                            <td>{order.device.name}</td>
                            <td>{order.device.brand}</td>
                            <td>{order.rental.name}</td>
                            <td>{order.rental.city}, {order.rental.address}</td>
                            <td>{moment(order.startDate).format("MMM Do YY")}</td>
                            <td>{moment(order.tillDate).format("MMM Do YY")}</td>
                            <td>
                                {(order.status === "RENTED") ? (
                                    <button className="button mr-2 is-info is-light">
                                        Сдать
                                    </button>
                                ):(<></>)
                            }
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            ) : (!loaded ?(
                <section className="section">
                    <div className="container">
                        <div className="columns is-centered">
                            <div className="column is-half">
                                <progress className="progress is-large is-info" max="100">
                                    60%
                                </progress>
                            </div>
                        </div>
                    </div>
                </section>
                    ):(<></>)
            )}
        </>
    );
}
