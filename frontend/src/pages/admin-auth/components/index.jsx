import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import { adminApi } from "../../../api";
import { useNavigate } from "react-router-dom";
import { openNotificationWithIcon } from "../../../common/helpers";
import Button from "react-bootstrap/Button";
import "./Login.css";

export const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        let response = await adminApi.login({username, password});
        if (response['status'] === 200) {
            localStorage.setItem('adminToken', response['token']);
            navigate('/admin/settings-manager');
            window.location.reload();
        } else {
            openNotificationWithIcon({
                title: 'Authorization Error!',
                type: 'error',
                text: response['message']
            })
        }
    }

    const validateForm = () => {
        return username.length > 3 && password.length > 2;
    }

    return (
        <div className="Login">
            <Form onSubmit={handleSubmit}>
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
                <Button variant="primary" size="lg" type="submit" disabled={!validateForm()}>
                    Login
                </Button>
            </Form>
      </div>
    );
}