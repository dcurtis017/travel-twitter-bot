import React, { Component } from "react";
import { API } from "aws-amplify";
import { Alert } from "react-bootstrap";
import "./City.css";

import Loader from "../components/Loader";
import FlightDeal from "./FlightDeal";

class City extends Component {
  constructor(props) {
    super(props);
    this.state = {
      deals: [],
      isLoading: true
    };
  }

  async getTweets(airport_city) {
    let deals = [];
    this.setState({ isLoading: true });
    try {
      deals = await API.post("flight-deals", "/tweets", {
        body: {airport_city}
      });
    } catch (e) {
      console.log(e);
    }
    this.setState({ isLoading: false, deals });
  }

  componentDidMount() {
   this.getTweets(this.props.match.params.name); 
  }

  componentWillReceiveProps(newProps) {
    this.getTweets(newProps.match.params.name);
  }
  render() {
    if (this.state.isLoading === true) {
      return <Loader />;
    }
    if (this.state.deals.length === 0) {
      return <Alert variant="danger">There were no deals found</Alert>;
    }
    const items = this.state.deals.map((d, iterator) => {
      return <FlightDeal key={iterator} {...d} />;
    });
    return (
      <div className="deal-city">
        <h2 className="text-center">
          Deals for {this.props.match.params.name}
        </h2>
        <div>{items}</div>
      </div>
    );
  }
}

export default City;
