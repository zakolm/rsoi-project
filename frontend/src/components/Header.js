import React, {useState} from "react";


export function Header(title) {
    const [token] = useState(localStorage.getItem("awesomeLeadsToken"));

    console.log(token);

  return (
      <>
        <nav className="navbar is-light" role="navigation" aria-label="main navigation">
          <div className="navbar-brand">
            <a className="navbar-item" href="/">
              <h1 className="title">Аренда оборудования</h1>
            </a>
          </div>

          <div id="navbarBasicExample" className="navbar-menu">
            <div className="navbar-end">
              <div className="navbar-item">
                {token ? (
                    <div className="buttons">
                        <div class="navbar-item has-dropdown is-hoverable">
                            <a class="navbar-link">
                                <img src={require('../user.svg').default} alt='mySvgImage' />
                            </a>
                            <div class="navbar-dropdown">
                                <a href="/orders" class="navbar-item">
                                    Заказы
                                </a>
                                <hr class="navbar-divider"/>

                                <a href="/logout" className="navbar-item is-danger">
                                    <strong>Выйти</strong>
                                </a>
                            </div>
                        </div>
                    </div>
                ): (
                    <div className="buttons">
                      <a href="/reg" className="button is-primary">
                        <strong>Регистрация</strong>
                      </a>
                      <a href="/login" className="button is-light">
                        Войти
                      </a>
                    </div>
                  )}
              </div>
            </div>
          </div>
        </nav>
      </>
    );
  {/*  */}
        {/*</div>*/}
}

