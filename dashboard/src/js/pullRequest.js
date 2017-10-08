import React, { Component } from 'react';
import '../css/pullRequest.css';

class PullRequest extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className='pullRequest' >
        <div className='pullNum' > <a href={this.props.json['url']} >{this.props.json['number']} </a></div>
        <div className= 'pullTitle' > <a href={this.props.json['url']} >{this.props.json['title']}</a></div>
      </div>
    );
  }
}

export default PullRequest;
