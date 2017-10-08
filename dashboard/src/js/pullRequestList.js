import React, { Component } from 'react';
import PullRequest from './pullRequest';
import '../css/pullRequest.css';
import * as Constants from './constants.js';


class PullRequestList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      total_pages: 1,
      next_page: 1,
      pulls: []
    }
    this.get_total_pages();
    this.get_pull_requests();
  }

  resolveErrorState(response) {
    console.error(response);
  }

  get_total_pages() {
    var url = Constants.FLASK_APP_URL + '/pulls/pages/';
    let promise = window.fetch(url, {
      method: 'GET',
      credentials:'same-origin',
      headers: {
        'Accept': 'application/json'
      }
    });
      promise.then((response) => {
      if (response.ok) {
        return response.json().then(response => this.setState({total_pages:parseInt(response)}));
      }
      else this.resolveErrorState(response);
    })
    .catch((response) => this.resolveErrorState(response));
  }

  get_pull_requests() {
    if (this.state.next_page > this.state.total_pages) {
      return;
    }
    var url = Constants.FLASK_APP_URL + '/pulls?page=' + this.state.next_page;
    let promise = window.fetch(url, {
      method: 'GET',
      credentials:'same-origin',
      headers: {
        'Accept': 'application/json'
      }
    });
      promise.then((response) => {
      if (response.ok) {
        this.state.next_page++;
        return response.json().then(response => this.setState({pulls:this.state.pulls.concat(response)}));
      }
      else this.resolveErrorState(response);
    })
    .catch((response) => this.resolveErrorState(response));
  }

  render() {
    return (
      <div className={`contentWrapper pullRequestList ${this.props.active}`} >
        <ul>
        {this.state.pulls.map((pull, index) =>
          <li className='pullLi' key={index}>
            <PullRequest json={pull} />
          </li>
        )}
        </ul>
        <button className='button loadMore' onClick={this.get_pull_requests.bind(this)}> Load more </button>

      </div>
    );
  }
}

export default PullRequestList;
