import React, { useState } from "react";
import { Container, Button, Table } from "react-bootstrap";
import { adminApi } from "../../api";
import { openNotificationWithIcon } from "../../common/helpers";
import { useFetchAdminInfo } from "../../api/useFetchAdminInfo";


import "./settings.css"

export const SettingsPage = () => {
    const [activeRun, setActiveRun] = useState({});
    const { adminInfo, loading } = useFetchAdminInfo();

    let runActiveState = {}

    if (!loading) {
        for (const item of adminInfo['gathers_info']) {
            runActiveState[item['id']] = item['is_active'];
        }
    }


    const onParserRun = async (e) => {
        const parserId = e.target.getAttribute("data-id")
        runActiveState[parserId] = true;
        if (Object.keys(activeRun).length !== 3) {
            setActiveRun(prevParams => ({
                ...prevParams,
                ...runActiveState,
                [parserId]: true
            }))
        } else {
            setActiveRun(prevParams => ({
                ...prevParams,
                [parserId]: true
            }))
        }
        openNotificationWithIcon({
            title: 'Seccess !',
            type: 'success',
            text: 'The service was launched successfully !'
        })
        const response = await adminApi.runParser({'parser_id': parserId});
        
    }

    return (
        <Container>
            <div className="manager__page">
                <div className="manager-page-container top">
                    <div className="jobs-in-base-block sub-block">
                        <h3 className="text-center" style={{marginTop: '40px'}}>Current filling of the database with vacancies</h3>
                        <div className="jobs_count">
                            <h1 className="text-center" style={{marginTop: '50px'}}>{adminInfo['total_jobs']}</h1>
                        </div>
                    </div>
                    <div className="parser-control-block sub-block">
                        {!loading && <Table className="gathers-table" striped bordered hover>
                            <thead>
                                <tr>
                                    <th>Service id</th>
                                    <th>Service name</th>
                                    <th>Service type</th>
                                    <th>Command Button</th>
                                </tr>
                            </thead>
                            <tbody>
                                {adminInfo['gathers_info'].map(item => {
                                    return <tr key={item['id']}>
                                                <th>{item['id']}</th>
                                                <th>{item['name']}</th>
                                                <th>{item['type']}</th>
                                                <th><Button className="run-button" data-id={item['id']} onClick={(e) => onParserRun(e)} disabled={Object.keys(activeRun).length !== 0 ? activeRun[item['id']] : runActiveState[item['id']]}>Run</Button></th>
                                            </tr>
                                })}
                            </tbody>
                        </Table>}
                    </div>
                </div>
                <div className="manager-page-container bottom">
                    <div className="job-clicks-block">
                    <h3 style={{textAlign: 'center'}}>Jobs clicks for last 24 hours</h3>
                    {!loading && <Table className="gathers-table" striped bordered hover>
                            <thead>
                                <tr>
                                    <th>Job Title</th>
                                    <th>Total Clicks</th>
                                    <th>Job Link</th>
                                </tr>
                            </thead>
                            <tbody>
                                {adminInfo['clicks_statistic'].map(item => {
                                    return <tr key={item['uid']}>
                                                <th style={{width: '550px'}}>{item['job_title']}</th>
                                                <th>{item['total_clicks']}</th>
                                                <th><Button href={`/job/${item['uid']}?utm_source=admin`}>Link</Button></th>
                                            </tr>
                                })}
                            </tbody>
                        </Table>}
                    </div>
                </div>
            </div>
        </Container>
    )
}