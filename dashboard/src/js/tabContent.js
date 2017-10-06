import React, { Component } from 'react';

class TabContent extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className={`contentWrapper tabContent ${this.props.active}`} >
          Insert other data here
      </div>
    );
  }
}

export default TabContent;
