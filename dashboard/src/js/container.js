import React, { Component } from 'react';
import Tab from './tab';
import PullRequests from './pullRequests';
import TabContent from './tabContent';

class Container extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTab: 'pulls'
    }
  }

  handleTabClick(name) {
    this.setState({
      activeTab:name
    });
  }

  render() {
    return (
      <div className="content">
        <ul className="nav nav-tabs">
          <Tab name="pulls" displayName="Pull Requests" active={this.state.activeTab === 'pulls' ? "active" : ""} handleTabClick={this.handleTabClick.bind(this)} />
          <Tab name="other" displayName="Other data" active={this.state.activeTab === 'other' ? "active" : ""} handleTabClick={this.handleTabClick.bind(this)} />
        </ul>
        <div className="viewContainer">
          <PullRequests className="PullRequests" active={this.state.activeTab === 'pulls' ? "active" : "inactive"} />
          <TabContent className="TabContent" active={this.state.activeTab === 'other' ? "active" : "inactive"} />
        </div>
      </div>
    );
  }
}

export default Container;
