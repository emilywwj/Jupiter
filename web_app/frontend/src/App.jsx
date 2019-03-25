import React, { Component } from 'react';

import AppForm from './components/AppForm';

class App extends Component {

  render() {
    return (
      <div className="App m-4">
        <h3> Jupiter User Interface </h3>
        <AppForm />
      </div>
    );
  }
}

export default App;

// export REACT_APP_URL=http://localhost