import React from "react";
import {Route, Switch} from "react-router-dom";
import Home from "./containers/Home";
import City from "./containers/City";
import NotFound from "./containers/NotFound";

export default () =>
<Switch>
    <Route path="/" exact component={Home} />
    <Route path="/City/:name" exact component={City} />
    <Route component={NotFound} />
</Switch>