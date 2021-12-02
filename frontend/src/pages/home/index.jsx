import React, { useState } from "react";
import { useFetchJobs } from "../../api/useFetchJobs";
import { Container, Spinner } from "react-bootstrap";

import { Job, JobsPagination, SearchForm } from '../../components'

export const SerpPage = () => {
    const [params, setParams] = useState({})
    const [page, setPage] = useState(1)
    const { jobs, loading, error, hasNextPage } = useFetchJobs(page);

    return (
        <Container className="my-4" style={{maxWidth: 900}}>
            <SearchForm />
            {!loading && <JobsPagination page={page} setPage={setPage} hasNextPage={hasNextPage} />}
            {loading && <Spinner animation="border" variant="dark" style={{width: 100, height: 100, display: "flex", margin: "auto", marginTop: 200}} />}
            {error && <h1>Error</h1>}
            {!loading && jobs.map(job => {return <Job key={job.uid} job={job}/>})}
            {!loading && <JobsPagination page={page} setPage={setPage} hasNextPage={hasNextPage} />}
        </Container>
    )

}