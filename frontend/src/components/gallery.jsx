import React, {useEffect, useState} from "react";
import useApi from "./api";
import {useLocation, useNavigate} from "react-router-dom";
import axios from "axios";
import {Header} from "./Header";


export function _Home() {
    const [myItems, handleRegistration, isAuth, handleLogin] = useApi();
    const navigate = useNavigate()
    const [loaded, setLoaded] = useState(false);


console.log(myItems)
  return <>
      <Header title="Project"></Header>
      <div className="has-text-centered m-6">
          <h1 className="title is-2">Ренталы</h1>
      </div>
    {/*<button onClick={()=>handleRegistration({email:'ritmwsgic@gmail.com', hashed_password:'string'})}>registration</button>*/}
    {/*<button onClick={()=>handleLogin({username:'ritmic@gmail.com', password:'string'})}>login</button>*/}
      {myItems ? (
          <div className="houses">
              {myItems?.items.map(e => (
                  <div className="house"
                       onClick={() => navigate('/about', {state: e})}>
                      <a className="img">
                          <img src="https://zakolesnik.ru/RentaPhoto.jpeg"
                               alt={e.name}/>
                          <div className="columns is-centered">
                              <p className="has-text-black-bis  has-text-weight-bold">{e.name}</p>
                          </div>
                          <div className="columns is-centered">
                              <p className="has-text-black">{e.city}, {e.address}</p>
                          </div>
                      </a>
                  </div>

              ))}
          </div>
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
    {/*// myItems?.items.map(e=><p onClick={() => navigate('/about', { state: e })}>{e.name}</p>)*/}
  </>;
}


export function _About(props) {
    const {state} = useLocation();
    const navigate = useNavigate()

    const [myItems, setMyItems] = React.useState();

    React.useEffect(() => {
    axios.get(`/api/v1/rentals/${state.rentalUid}/devices?city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&page=1&size=10`).then((response) => {
      setMyItems(response.data);
    });
  }, []);

    console.log(myItems)
  return <>
      <Header title="Project"></Header>
      <div className="has-text-centered m-6">
          <h1 className="title is-2">{state.name}</h1>
      </div>
          <div className="houses">
              {myItems?.items.map((e) => (
              <div className="house" onClick={() => navigate('/device', { state: {rental: state, device: e} })}>
                  <a className="img" >
                      <img src="https://mobile.photoprocenter.ru/files/20160302161705Profoto_901024_D1_Air_500_w_s_605739.jpg" alt={e.name}/>
                  </a>
                  <h2>
                      <a >
                          {e.name} {e.brand}
                      </a>
                  </h2>
              </div>
              ))}
          </div>
  </>;
}

// <p >{e.name} {e.brand}</p>)