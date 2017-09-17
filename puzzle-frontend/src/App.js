import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Board, NewBoardForm } from './components/Board';
import { connect } from 'react-redux'
import { solveBoard, cloneBoard, updateCellValue, makeNewBoard } from './actions'


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
          clone={() => this.props.cloneBoardClick(board.id)}
          updateCellValue={this.props.updateCellValueOnChange}
        />
    );
  }

  render() {
    return (
      <div className="app">
        <NewBoardForm newBoard={this.props.newBoard} />
        <div className="boards">
          {this.props.boards.map((board) => this.renderBoard(board))}
        </div>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return state
}

const mapDispatchToProps = dispatch => {
  return {
    solveBoardClick: id => dispatch(solveBoard(id)),
    cloneBoardClick: id => dispatch(cloneBoard(id)),
    updateCellValueOnChange: payload => dispatch(updateCellValue(payload)),
    newBoard: payload => dispatch(makeNewBoard(payload))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)
