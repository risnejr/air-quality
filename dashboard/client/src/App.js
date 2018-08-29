import React, { Component } from 'react';
import { Card, Typography, AppBar, Toolbar, CircularProgress} from '@material-ui/core';
import './App.css';

const Info = props => {
  return (
    <Card className={'card ' + props.class}>
      <Typography variant="display3">{props.title} <Emoji style={{float: "right"}} symbol={props.trend}/></Typography>
      {props.value !== "" && <Typography className="value" variant={props.variant}>{props.value} {props.unit}</Typography>}
      {props.value === "" && <CircularProgress className="progress"/>}
    </Card>
  )
}

const Emoji = props => (
  <span
      className="emoji"
      role="img"
      style={props.style}
      aria-label={props.label ? props.label : ""}
      aria-hidden={props.label ? "false" : "true"}
  >
      {props.symbol}
  </span>
);

class App extends Component {
  constructor(props) {
    super(props);
    this.url = new URL(window.location.href)
    this.funcLoc = this.url.searchParams.get("func_loc")
    this.asset = this.url.searchParams.get("asset")
    this.state = {
      temperature: {val: "", trend: ""},
      humidity: {val: "", trend: ""},
      pressure: {val: "", trend: ""},
      gas: {val: "", trend: ""}
    }
  }

  componentDidMount() {
    let source = new EventSource("http://localhost:5000?func_loc=" + this.funcLoc + "&asset=" + this.asset)
    let data = {}

    source.onmessage = e => {
      data = JSON.parse(e.data)
      let newData = {val: data.node_data.toFixed(2),
                     trend: data.node_data > this.state[data.point_name].val ? "📈" : "📉"}
      if (data.point_name === 'temperature') {
        this.setState({temperature: newData})
      }
      else if (data.point_name === 'pressure') {
        this.setState({pressure: newData})
      }
      else if (data.point_name === 'humidity') {
        this.setState({humidity: newData})
      }
      else if (data.point_name === 'gas') {
        newData.val = (newData.val/1000).toFixed(2)
        this.setState({gas: newData})
      }
    }
  }

  toTitleCase(name) {
    name = name.split("_").join(" ")
    return name.replace(/\w\S*/g, txt => {return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();})
  }

  render() {
    return (
      <div>
        <AppBar position="static" style={{ backgroundColor: '#185cd3' }}>
          <Toolbar>
            <Typography variant="title" style={{ color: '#ffffff', padding: 10 }}>
              <Emoji symbol='🏡'/> {this.toTitleCase(this.funcLoc)} <br/> <Emoji symbol='📦'/> {this.toTitleCase(this.asset)}
            </Typography>
          </Toolbar>
        </AppBar>
        <div className="App">
          <Info variant="display2" title="Temperature" value={this.state.temperature.val} unit="C°" trend={this.state.temperature.trend}/>
          <Info variant="display2" title="Humidity" value={this.state.humidity.val} unit="%" trend={this.state.humidity.trend}/>
          <Info variant="display2" title="Pressure" value={this.state.pressure.val} unit="hPa" trend={this.state.pressure.trend}/>
          <Info variant="display2" title="Gas" value={this.state.gas.val} unit="kΩ" trend={this.state.gas.trend}/>
        </div>
      </div>
    );
  }
}

export default App;
