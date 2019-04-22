import React from "react";
import "./FlightDeal.css";
import { Row, Col } from "react-bootstrap";
import moment from "moment";

export default function FlightDeal(props) {
  const dt = moment(props.created_at);
  return (
    <div className="flight-deal-card rounded">
      <Row>
        <h3>
          <a
            href={`https://twitter.com/${props.screen_name}/status/${
              props.tweet_id
            }`}
            className="tweet_link"
            target="_blank"
            rel="noopener noreferrer"
          >
            {props.text}
          </a>
        </h3>
      </Row>
      <Row>
        <Col>
          <a
            href={`https://twitter.com/${props.screen_name}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            {props.screen_name}
          </a>
        </Col>
        <Col className="pull-right">
          <a href="#">{dt.format("MMM D")}</a>
        </Col>
      </Row>
    </div>
  );
}
