import React from "react";
import { Image } from "react-bootstrap";
import "./ListMember.css";

export default function ListMember(props) {
  return (
    <div className="box-list-member">
      <Image
        src={props.profile_image}
        alt={`Profile for ${props.display_name}`}
        rounded
      />
      <div className="list-member-text">
        <span className="displayname">
          <a href={`https://twitter.com/${props.screen_name}`} target="_blank" rel="noopener noreferrer">
            {props.display_name}
          </a>
        </span>
      </div>
    </div>
  );
}
