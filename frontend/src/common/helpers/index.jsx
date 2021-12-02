import React from "react";
import Toast from 'react-bootstrap/Toast'


export const ErrorToast = (props) => {
    const {message, title, type} = props; 
    return (
        <Toast className="d-inline-block m-1" bg={type}>
            <Toast.Header>
                <strong className="me-auto">{title}</strong>
            </Toast.Header>
            <Toast.Body className="Dark">
                {message}
            </Toast.Body>
        </Toast>
    )
}