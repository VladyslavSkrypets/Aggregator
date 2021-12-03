import React, { useState } from "react";
import { useFetchJobs } from "../../api/useFetchJobs";
import { Container, Spinner } from "react-bootstrap";

import { Job, JobsPagination, Header, FiltersBlock, EmptyPage } from '../../components'

import "./home.css"


export const SerpPage = () => {
    const [params, setParams] = useState({})
    const [filters, setFilters] = useState({})
    const [page, setPage] = useState(1)
    const { jobs, loading, error, hasNextPage } = useFetchJobs(page, filters);

    const handleParamChange = (e) => {
        const param = e.target.name;
        let value = null;
        if (param === 'job-type' || param === 'remote-type') {
            value = e.target.checked;
        } else {
            value = e.target.value;
        };
        setPage(1)
        setParams(prevParams => ({
             ...prevParams, 
            [param]: value 
        }))
    }

    const onSubmit = () => {
        setFilters(() => ({
            ...params
        }))
    }

    return (
        <>
            <Header params={params} onParamChange={handleParamChange} onSearch={onSubmit}/>
            <div className="page-container">
                <FiltersBlock onParamChange={handleParamChange} onApply={onSubmit} />
                <div className="serp-container">
                    <Container>
                        {!loading && jobs.length !==0 && <JobsPagination page={page} setPage={setPage} hasNextPage={hasNextPage} />}
                        {loading && <Spinner animation="border" variant="dark" style={{width: 100, height: 100, margin: '145px 0 0 355px'}} />}
                        {error && <h1>Error</h1>}
                        {!loading && jobs.map(job => {return <Job key={job.uid} job={job}/>})}
                        {!loading && jobs.length !==0 && <JobsPagination page={page} setPage={setPage} hasNextPage={hasNextPage} />}
                    </Container>
                </div>
                {jobs.length == 0 && !loading && <EmptyPage />}
            </div>
        </>
    )

}