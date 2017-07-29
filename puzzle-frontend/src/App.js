import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Board } from './components/Board';

class App extends Component {
  render() {
    var cells = [
      [
        {id: 0, value: 0},
        {id: 1, value: 5},
        {id: 2, value: 3}
      ],
      [
        {id: 3, value: 1},
        {id: 4, value: 2},
        {id: 5, value: 3}
      ]
    ];

    return (
      <div className="board">
        <Board
          cells={cells}
        />
      </div>
    );
  }
}

export default App;
