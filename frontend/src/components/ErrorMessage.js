import React from "react";

const ErrorMessage = ({message}) => (
    <section className="section">
        <div className="container">
            <div className="columns is-centered">
                <div className="column is-half">
                    <article className="message is-danger">
                        <div className="message-header">
                            <p>Error</p>
                            <button className="delete" aria-label="delete"></button>
                        </div>
                        <div className="message-body">
                            {message}
                        </div>
                    </article>
                </div>
            </div>
        </div>
    </section>
);

export default ErrorMessage;
