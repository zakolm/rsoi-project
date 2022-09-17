import React, {useState} from "react";
import {CreateOrder} from "./createOrder";
import {Navigate, useLocation, useNavigate} from "react-router-dom";

export const DeviceModal = ({active, handleModal, token}) => {
    const {state, prev_state} = useLocation();
    const [tillDate, setTillDate] = useState("");

    let navigate = useNavigate();
    const routeChange = () => {
        CreateOrder(state.rental, state.device, tillDate);
        navigate('/orders');
    }

    return (
        <>
            <div className={`modal ${active && "is-active"}`}>
                <div className="modal-background"></div>
                <div className="modal-card">
                    <header className="modal-card-head has-background-primary-light">
                        <p className="modal-card-title">Выберите до какой даты аренда</p>
                        <button className="delete" aria-label="close" onClick={handleModal}></button>
                    </header>
                    <section className="modal-card-body">
                        <form>
                            <div className="field">
                                <label className="label">Note</label>
                                <div className="control">
                                    <input
                                        type="date"
                                        placeholder="Enter note"
                                        value={tillDate}
                                        onChange={(e) => setTillDate(e.target.value)}
                                        className="input"
                                    />
                                </div>
                            </div>
                        </form>
                    </section>
                    <footer className="modal-card-foot has-background-primary-light">
                        <button className="button is-primary" onClick={routeChange}>Аренда</button>
                        <button className="button" onClick={handleModal}>Закрыть</button>
                    </footer>
                </div>
            </div>
        </>
    );
}
