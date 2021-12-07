import React from 'react';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { AppRoute } from './common/enums/app-route.enum';

import { Login, SerpPage, JobPage, SettingsPage } from './pages';


export const App = () => {
  const isAdminAuth = localStorage.getItem('adminToken');  

  return (
    <Router>
      <Routes>
        <Route exact path={AppRoute.HOME} element={<SerpPage />} />
        <Route path={AppRoute.JOB} element={<JobPage />}/>
        <Route path={AppRoute.LOGIN} element={<Login />} />
        {isAdminAuth ? <Route path={AppRoute.ADMIN_PAGE} element={<SettingsPage />} /> : null}
        {/* <Route path={AppRoute.ADMIN_PAGE} element={isAdminAuth ? <SettingsPage /> : <Login />} /> */}
      </Routes>
    </Router>
  );
}
