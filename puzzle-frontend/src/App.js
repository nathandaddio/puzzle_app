import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Board } from './components/Board';
import { connect } from 'react-redux'
import { solveBoard } from './actions'


class App extends Component {
  renderBoard(board) {
    return (
        <Board
          name={board.id}
          cells={board.cells}
          rows={board.number_of_rows}
          columns={board.number_of_columns}
          key={board.id}
          solve={() => this.props.solveBoardClick(board.id)}
        />
    );
  }

  render() {
    return (
      <div className="boards">
        {this.props.boards.map((board) => this.renderBoard(board))}
      </div>
    )
  }
}

function mapStateToProps(state) {
  return state
}

const mapDispatchToProps = dispatch => {
  return {
    solveBoardClick: id => dispatch(solveBoard(id))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)
