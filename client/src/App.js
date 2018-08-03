import React, { Component } from 'react';
import { Card, Typography, AppBar, Toolbar, CircularProgress} from '@material-ui/core';
import './App.css';

const Info = props => {
  return (
    <Card className={'card ' + props.class}>
      <Typography variant="display3">{props.title}</Typography>
      {props.value !== "" && <Typography className="value" variant={props.variant}>{props.value} {props.unit}</Typography>}
      {props.value === "" && <CircularProgress className="progress"/>}
    </Card>
  )
}

const Emoji = props => (
  <span
      className="emoji"
      role="img"
      aria-label={props.label ? props.label : ""}
      aria-hidden={props.label ? "false" : "true"}
  >
      {props.symbol}
  </span>
);

const LEVEL = {
  Good: <Emoji symbol="😎"/>,
  Ok: <Emoji symbol="😐"/>,
  Bad: <Emoji symbol="😩"/>,
}

class App extends Component {
  constructor(props) {
    super(props);
    this.url = new URL(window.location.href)
    this.funcLoc = this.url.searchParams.get("func_loc")
    this.asset = this.url.searchParams.get("asset")
    this.state = {
      temp: "",
      hum: "",
      pres: "",
      gas: "",
      pred: "",
      vote: "",
    }
  }

  componentDidMount() {
    let source = new EventSource("http://localhost:5000/grpc/" + this.funcLoc + "/" + this.asset)
    let data = {}

    source.addEventListener('delta', e => {
      data = JSON.parse(e.data)
      if (data.inspection_point === 'temperature') {
        this.setState({temp: data.node_data.toFixed(2)})
      }
      else if (data.inspection_point === 'pressure') {
        this.setState({pres: data.node_data.toFixed(2)})
      }
      else if (data.inspection_point === 'humidity') {
        this.setState({hum: data.node_data.toFixed(2)})
      }
      else if (data.inspection_point === 'gas') {
        this.setState({gas: (data.node_data/1000).toFixed(2)})
      }
      else if (data.inspection_point === 'air_quality') {
        this.setState({pred: data.node_data})
      }
      else if (data.inspection_point === 'vote') {
        this.setState({vote: data.node_data})
      }
    })
  }

  render() {
    return (
      <div>
        <AppBar position="static" style={{ backgroundColor: '#185cd3' }}>
          <Toolbar>
            <Typography variant="title" style={{ color: '#ffffff' }}>
              <Emoji symbol='🏡'/> {String(this.funcLoc).split("_").join(" ").toUpperCase()} <Emoji symbol='👉'/> {String(this.asset).toUpperCase()}
            </Typography>
          </Toolbar>
        </AppBar>
        <div className="App">
          <Info variant="display2" title="Temperature" value={this.state.temp} unit="C°"/>
          <Info variant="display2" title="Humidity" value={this.state.hum} unit="%"/>
          <Info variant="display2"title="Pressure" value={this.state.pres} unit="hPa"/>
          <Info variant="display2"title="Gas" value={this.state.gas} unit="kΩ"/>
          <Info variant="display4" class="bottom" title="Air quality" value={LEVEL[this.state.pred]}/>
          <Info variant="display4" class="bottom recent" title="Last vote" value={LEVEL[this.state.vote]}/>
        </div>
      </div>
    );
  }
}

export default App;
