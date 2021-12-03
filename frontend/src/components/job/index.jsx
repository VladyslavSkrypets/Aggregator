import React from "react";
import { FaRegBuilding, FaCalendarAlt } from "react-icons/fa";
import { ImLocation } from "react-icons/im"
import { Card } from "react-bootstrap";


export const Job = ({ job }) => {
    return (
        <Card className="mb-3" style={{boxShadow: '0 0 2px rgb(5 20 41 / 6%), 0 2px 3px rgb(5 20 41 / 8%)'}}>
            <Card.Body>
                <div className="d-flex justify-content-between">
                    <div>
                        <Card.Title style={{fontSize: '1.5rem'}}>
                            <a style={{textDecoration: 'none'}} href={'/job/' + job.uid}>{job.title}</a>
                        </Card.Title>
                        <Card.Subtitle className="mt-2">
                            {job.salary ? <Card.Subtitle className="mt-2">{job.salary}</Card.Subtitle>: ''}
                        </Card.Subtitle>
                        <Card.Text style={{fontSize: '14px', marginTop: 15}}>
                            {job.description}
                        </Card.Text>
                        <hr />
                        <Card.Subtitle className="text-muted font-weight-light">
                            {job.company ? <div className="job-info-box"><FaRegBuilding className="icon" />{job.company}</div> : ''}
                        </Card.Subtitle>
                        <Card.Subtitle className="text-muted">
                            {job.posted_at ? <div className="job-info-box"><FaCalendarAlt className="icon" />{job.posted_at}</div> : ''}
                        </Card.Subtitle>
                        <Card.Subtitle className="text-muted">
                            {job.region ? <div className="job-info-box"><ImLocation className="icon" />{job.region}</div> : ''}
                        </Card.Subtitle>
                    </div>
                </div>
            </Card.Body>
        </Card>
    )
}
