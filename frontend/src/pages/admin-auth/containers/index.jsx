import React from "react";
import { adminApi } from "../../../api";
import { useNavigate } from "react-router-dom";
import { LoginForm } from "../components";

export const Login = () => {
    const navigate = useNavigate();

    const handleSubmit = async (username, password) => {
        let response = await adminApi.login({username, password});
        if (response['status'] === 200) {
            localStorage.setItem('adminToken', response['token']);
            navigate('/admin/settings-manager');
        } else {
        }
    }

    const validateForm = (username, password) => {
        return username.length > 3 && password.length > 2;
    }
  
    return <LoginForm validateForm={validateForm} handleSubmit={handleSubmit}/>;
  };