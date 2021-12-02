import React from "react";
import { useParams } from "react-router";
import { FaRegBuilding } from "react-icons/fa";
import { ImLocation } from "react-icons/im"
import { Card, Container, Button } from "react-bootstrap";

import { useFetchJob } from "../../../api/useFetchJobs";

import "./job.css";


export const JobPage = () => {

    const { uid } = useParams();
    const { job, loading } = useFetchJob(uid);

    return (
        <Container className="job__container">
            {!loading && <Card className="job__card">
                <Card.Body>
                    <div>
                        <Card.Title className="job__title" as="h2">{job.title}</Card.Title>
                        {job.salary ? <Card.Subtitle className="job__job-salary">{job.salary}</Card.Subtitle> : ''}
                        {job.job_type ? <Card.Subtitle className="job__job-type">{job.job_type}</Card.Subtitle> : ''}
                        {job.company ? <Card.Subtitle className="job__job-company job-subtitle"><FaRegBuilding className="icon" />{job.company}</Card.Subtitle> : ''}
                        {job.region ? <Card.Subtitle className="job__job-location job-subtitle"><ImLocation className="icon" />{job.region}</Card.Subtitle> : ''}
                        {job.remote_type ? <div className="remote-job">Remote job</div> : ''}
                        <Button variant="primary" className="job__apply-button apply-button-header" href={job.url}>
                            Apply {job.redirect_domain ? ` on ${job.redirect_domain}`: ' here'}
                        </Button>
                    </div>
                    <hr />
                    <div>
                        <Card.Text className="job__description-text" style={{marginBottom: 50}}>
                            <div dangerouslySetInnerHTML={{__html: job.description}}/>
                        </Card.Text>
                        <hr />
                        <Button variant="primary" className="job__apply-button apply-button-footer" href={job.url}>
                            Apply {job.redirect_domain ? ` on ${job.redirect_domain}`: ' here'}
                        </Button>
                    </div>
                </Card.Body>
            </Card>
            }
        </Container>
    )
}