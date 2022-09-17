import React, {useState} from "react";
import {useLocation} from "react-router-dom";

import {Header} from "./Header";
import {DeviceModal} from "./deviceModal";

export function Device(props) {
    const {state, prev_state} = useLocation();
    const [activeModal, setActiveModal] = useState(false);
    const [token] = useState(localStorage.getItem("awesomeLeadsToken"));

    const handleModal = () => {
        setActiveModal(!activeModal);
        // getLeads();
        // setId(null);
    };

    console.log(prev_state);
    return <>
        <Header title="Project"></Header>
        <DeviceModal
            active={activeModal}
            handleModal={handleModal}
            token={token}
        />
        <div className="has-text-centered m-6">
            <div className="table-container">
                <table className="table is-fullwidth">
                    <thead>
                    <tr>
                        <td rowSpan="2"><img src="https://zakolesnik.ru/Sony_FX3.jpeg" alt={state.device.name}/></td>
                        <td><h2 className="title is-4">{state.device.name} {state.device.brand}</h2></td>
                    </tr>
                    <tr>
                        <td>
                            В наличие: {state.device.available_count} шт.
                            <br/>
                            <button className="button is-primary" onClick={() => setActiveModal(true)}>
                                Арендовать
                            </button>
                        </td>
                    </tr>
                    </thead>
                </table>
            </div>
        </div>
    </>
}
