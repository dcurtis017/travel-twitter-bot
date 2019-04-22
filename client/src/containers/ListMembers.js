import React, { Component } from "react";
import { API } from "aws-amplify";
import { ListGroup } from "react-bootstrap";
import "./ListMembers.css";

import Loader from "../components/Loader";
import ListMember from "./ListMember";

class ListMembers extends Component {
  constructor(props) {
    super(props);
    this.state = {
      list_members: [],
      isLoading: true
    };
  }

  async componentDidMount() {
    try {
      const list_members = await API.get("flight-deals", "/list-members");
      this.setState({ list_members });
    } catch (e) {
      console.log(e);
    }
    this.setState({ isLoading: false });
  }
  render() {
    if (this.state.isLoading === true) {
      return <Loader />;
    }
    const members = this.state.list_members.map((lm, iterator) => {
      return (
        <ListGroup.Item key={iterator}>
          <ListMember key={iterator} {...lm} />
        </ListGroup.Item>
      );
    });
    return (
      <div>
        <h2 className="text-center">FOLLOWING</h2>
        <ListGroup>{members}</ListGroup>
      </div>
    );
  }
}

export default ListMembers;
