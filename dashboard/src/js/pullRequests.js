import React, { Component } from 'react';

class PullRequests extends Component {
  constructor(props) {
    super(props);
    this.state = {
      page_loaded:1,
      pulls: []
    }
  }


  resolveErrorState(response) {
    console.error(response);
  }


  get_pull_requests() {
    var url = 'http://127.0.0.1:5000/pulls?page=' + this.state.page_loaded;
    let promise = window.fetch(url, {
      method: 'GET',
      credentials:'same-origin',
      headers: {
        // 'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    promise.then((response) => {
      if (response.ok) {
        this.setState({pulls:this.state.pulls.push(response.json())})
      }
      else this.resolveErrorState(response);
    })
    .catch((response) => this.resolveErrorState(response));
  }

  render() {

    this.get_pull_requests()
    console.log(this.state.pulls)
    return (
      <div className={`contentWrapper pullRequests ${this.props.active}`} >
        <ul>
          {this.state.pulls.map((pr, i) => <li className='pritem' >This is my pr</li>)}
        </ul>
      </div>
    );
  }
}

export default PullRequests;
