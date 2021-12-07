import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./Login.css";

export const LoginForm = (props) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const { handleSubmit, validateForm } = props;

    const onValidate = () => {
        return validateForm(username, password);
    }

    const onSubmit = (event) => {
        const authResult = !handleSubmit(username, password)
        event.preventDefault();
        if (authResult) {
            alert("Error")
        }
    }

    return (
        <div className="Login">
            <Form onSubmit={onSubmit}>
                <Form.Group size="lg" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                    autoFocus
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    />
                </Form.Group>
                <Form.Group size="lg" controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    />
                </Form.Group>
                <Button variant="primary" size="lg" type="submit" disabled={!onValidate()}>
                    Login
                </Button>
            </Form>
      </div>
    );
}