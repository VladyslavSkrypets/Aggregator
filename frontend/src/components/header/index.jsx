import React from "react";
import { Form, Row, Button, InputGroup } from "react-bootstrap";
import { BiSearch, BiCurrentLocation } from "react-icons/bi"

import "./header.css"

export const Header = ({onParamChange, onSearch}) => {
    return (
        <header className="header-container">
            <Form>
                <Row className="search-row-container">
                    <div className="search-inputs">
                        <InputGroup className="input-search-group job-title">
                            <InputGroup.Text className="input-search-icon">
                                <BiSearch />
                            </InputGroup.Text>
                            <Form.Control className="search-input title" placeholder="I'm looking for vacancies..." name="job-title" type="text" onChange={onParamChange} />
                        </InputGroup>
                        <InputGroup className="input-search-group job-region">
                            <InputGroup.Text className="input-search-icon" style={{borderTopLeftRadius: 0, borderBottomLeftRadius: 0}}>
                                <BiCurrentLocation />
                            </InputGroup.Text>
                            <Form.Control className="search-input region" placeholder="In the region..." name="job-region" type="text" onChange={onParamChange} />
                        </InputGroup>
                        <Button id="findButton" onClick={onSearch}>Find</Button>
                    </div>
                </Row>
            </Form>
        </header>
    )
}