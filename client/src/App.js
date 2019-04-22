import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Navbar, Nav, Container, Row, Col } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import ListMembers from "./containers/ListMembers";
import "./App.css";

import Routes from "./Routes";

class App extends Component {
  render() {
    return (
      <div className="App container">
        <Navbar collapseOnSelect>
          <Navbar.Brand>
            <Link to="/">Flight Deals</Link>
          </Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse>
            <Nav>
              <LinkContainer to="/City/Atlanta">
                <Nav.Link>Atlanta</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/City/Charlotte">
                <Nav.Link>Charlotte</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/City/Raleigh">
                <Nav.Link>Raleigh</Nav.Link>
              </LinkContainer>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <Container>
          <Row>
            <Col md={8}>
              <Routes />
            </Col>
            <Col md={4}><ListMembers /></Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
