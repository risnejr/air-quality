import React, { Component } from 'react';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      temp: -1,
      hum: -1,
      pres: -1,
      gas: -1,
    }
  }

  componentDidMount() {
    let source = new EventSource("http://127.0.0.1:5000/grpc")
    let data = {}

    source.addEventListener('delta', e => {
      data = JSON.parse(e.data)
      if (data.node_id === process.env.REACT_APP_TEMP) {
        this.setState({temp: data.node_data.toFixed()})
      }
      else if (data.node_id === process.env.REACT_APP_PRES) {
        this.setState({pres: data.node_data.toFixed()})
      }
      else if (data.node_id === process.env.REACT_APP_HUM) {
        this.setState({hum: data.node_data.toFixed()})
      }
      else if (data.node_id === process.env.REACT_APP_GAS) {
        this.setState({gas: (data.node_data/1000).toFixed()})
      }
    })
  }

  render() {
    return (
      <div className="App">
       <h1>{this.state.temp} C°</h1>
       <h1>{this.state.hum} %</h1>
       <h1>{this.state.pres} hPa</h1>
       <h1>{this.state.gas} kΩ</h1>
      </div>
    );
  }

}

export default App;
