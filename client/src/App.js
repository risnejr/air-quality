import React, { Component } from 'react';
import './App.css';

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

const initialState = {
  goodSymbol: <Emoji symbol='🙌'/>,
  okSymbol: <Emoji symbol='💁‍'/>,
  badSymbol: <Emoji symbol='😷'/>
}

class App extends Component {
  constructor() {
    super();
    this.state = initialState;
  }

  render() {
    return (
      <div className="App">
        <button className="good label" onClick={() => this.label('Good')}>{this.state.goodSymbol}</button>
        <button className="ok label" onClick={() => this.label('Ok')}>{this.state.okSymbol}</button>
        <button className="bad label" onClick={() => this.label('Bad')}>{this.state.badSymbol}</button>
      </div>
    );
  }

  reset() {
    this.setState(initialState)
  }

  label(ans) {
    this.setEmoji(ans)

    let funcLoc = window.location.pathname.split("/").reverse()[1]
    let asset = window.location.pathname.split("/").reverse()[0]

    fetch(process.env.REACT_APP_API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        func_loc: funcLoc,
        asset: asset,
        answer: [ans]
      })
    })
  }

  setEmoji(ans) {
    if (ans === 'Good') {
      this.setState({
        goodSymbol: <Emoji symbol='👏'/>
      })
    }
    if (ans === 'Ok') {
      this.setState({
        okSymbol: <Emoji symbol='🙆‍'/>
      })
    }
    if (ans === 'Bad') {
      this.setState({
        badSymbol: <Emoji symbol='😵'/>
      })
    }
    setTimeout(() => this.reset(), 1000)
  }
}

export default App;
