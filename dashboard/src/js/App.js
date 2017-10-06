import React, { Component } from 'react';
import '../css/App.css';
import Container from './container';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p className="App-title">Dashboard</p>
        </header>
        <Container className="container"/>
      </div>
    );
  }
}

export default App;
