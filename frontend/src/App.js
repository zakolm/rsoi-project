import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link, useLocation, Navigate, Outlet,
    HistoryRouterProps, useNavigate,
} from "react-router-dom";

import {_About, _Home} from "./components/gallery";
import {Device} from "./components/device";
import React, {useContext, useState} from "react";
// import {UserContext} from "./context/UserContext";
import RouteGuard, {RouteGuard_private} from "./components/RouteGuard";
import {setAuthToken} from "./components/setAuthToken";
import axios from "axios";
import {Header} from "./components/Header";
import {Login} from "./components/login";
import {Register} from "./components/registration";
import {Orders} from "./components/orders";
// import axios from "axios";
// import {useEffect} from "react";

function App() {
  return (
      <>
      <Router>
        <div>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Routes>
            <Route exact path='/' element={<RouteGuard navigate="/login" />}>
                <Route exact path='/' element={<_Home/>}/>
            </Route>
            <Route exact path='/about' element={<RouteGuard navigate="/login" />}>
                <Route path="/about" element={<_About />}/>
            </Route>
            <Route exact path='/device' element={<RouteGuard navigate="/login" />}>
                <Route path="/device" element={<Device />}/>
            </Route>

            <Route path="/logout" element={<Logout />}/>


            <Route path="/login" element={<Login />}/>

            <Route path="/reg" element={<Register />}/>

            <Route exact path='/orders' element={<RouteGuard_private navigate="/login" />}>
                <Route path="/orders" element={<Orders />} />
            </Route>

        {/*  <Route path="/users" element={<Users />}>*/}
        {/*  </Route>*/}
        {/*  <Route path="/" element={<Users />}>*/}
        {/*  </Route>*/}
        </Routes>
      </div>
    </Router>
        </>
  );
}

function Logout(props) {
    localStorage.setItem("awesomeLeadsToken", "");

    return <Navigate to="/"/>
}

export default App;
