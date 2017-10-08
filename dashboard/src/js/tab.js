import React, { Component } from 'react';

class Tab extends Component {
  constructor(props) {
    super(props);
  }

  handleTabClick () {
    this.props.handleTabClick(this.props.name);
  }

  render() {
    return (
      <li
        role="presentation"
        className={this.props.active}
        onClick={this.handleTabClick.bind(this)}
      >
        <a>{this.props.displayName}</a>
      </li>
    );
  }
}

export default Tab;
