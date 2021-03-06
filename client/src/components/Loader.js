import React from "react";
import { Spinner } from "react-bootstrap";
import "./Loader.css";

export default ({ loadingText = "Loading..." }) => (
  <Spinner animation="border" role="status">
    <span className="sr-only">{loadingText}</span>
  </Spinner>
);
