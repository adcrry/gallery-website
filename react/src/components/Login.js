import React, {useState} from 'react';
import './../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col } from 'react-bootstrap';
import DjangoCSRFToken from 'django-react-csrftoken'

export default function Login() {

    return (
        <>
            <Container>
                <Row>
                    <Col>
                        <div className="login-container">
                            <img className="login-logo" src="/static/assets/img/logo-ponthe.png"/>
                            <form className="login-form" method="post" action="/login/">
                                <DjangoCSRFToken/>
                                <input type="email" className="login-input" placeholder="prenom.nom@eleves.enpc.fr" name="username"required/>
                                <input type="password" className="login-input" placeholder="mot de passe" name="password" required/>
                                <button type="submit" className="login-button">Se connecter</button>
                            </form>
                            <a href="/accounts/login" className="login-link">Connexion SSO</a>
                        </div>
                    </Col>
                </Row>
            </Container>
        </>
    )
    
}