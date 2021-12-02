import React from "react";

import { Card, Badge, Button } from "react-bootstrap";


export const Job = ({ job }) => {
    return (
        <Card className="mb-3">
            <Card.Body>
                <div className="d-flex justify-content-between">
                <div>
                    <Card.Title>
                        {job.title} <span style={{}} className="text-muted font-weight-light">{job.company ? ' - ' + job.company: ''}</span>
                    </Card.Title>
                    <Card.Subtitle className="text-muted mb-2">
                    {job.posted_at}
                    </Card.Subtitle>
                    <Badge variant="secondary" className="mr-2">{job.job_type}</Badge>
                    <Badge variant="secondary">{job.region}</Badge>
                </div>
                </div>
                <div style={{marginTop: 15}}>
                    <Button
                        href={'/job/' + job.uid}
                        variant="primary"
                        size="sm"
                    >
                        View Details
                    </Button>
                </div>
            </Card.Body>
        </Card>
    )
}
