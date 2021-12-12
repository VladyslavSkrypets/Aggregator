import React from "react";
import { Form, Button } from "react-bootstrap";

import "./filters.block.css"

export const FiltersBlock = ({ onParamChange, onApply }) => {
    return (
        <div className="filters-container">
            <Form className="filters-container-wrapper">
                <div className="filters-reader">
                    Filters
                </div>
                <div className="filters-block">
                    <div className="filter-block">
                        <div className="filter-block-header">
                            Type of employment
                        </div>
                        <div className="inner-block">
                            <Form.Check name="job-type" type="checkbox" label="Full-time" onChange={onParamChange} />
                        </div>
                    </div>
                    <div className="filter-block">
                        <div className="filter-block-header">
                            Type of job
                        </div>
                        <div className="inner-block">
                            <Form.Check name="remote-type" type="checkbox" label="Remote job" onChange={onParamChange} />
                        </div>
                    </div>
                    <div className="filter-block">
                        <div className="filter-block-header">
                            Salary
                        </div>
                        <div className="inner-block">
                            <Form.Control  placeholder="Example: 15 000" name="salary" type="text" onChange={onParamChange} />
                        </div>
                    </div>
                    <Button onClick={onApply}>Apply filters</Button>
                </div>
            </Form>
        </div>
    )
}