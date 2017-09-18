import PropTypes from 'prop-types'

import React from 'react';


class Board extends React.Component {
    renderCell(cell) {
        return (
            <Cell
                value={cell.value}
                inSolution={cell.included_in_solution}
                key={cell.id}
                handleInputChange={event => this.props.updateCellValue({id: cell.id, value: event.target.value})}
            />
        );
    }

    renderRow(row, key) {
        return (
            <div className='board-row' key={key}>
                {row.map((cell) => this.renderCell(cell))}
            </div>
        );
    }

    renderRows(cells) {
        return (
            <div className='board-rows'>
                {cells.map((row, index) => this.renderRow(row, index))}
            </div>
        );
    }


    render () {
        var matrix = toMatrix(this.props.cells, this.props.columns);
        return (
          <div className='board'>
            <div className='board-name'>
              {this.props.name}
            </div>

            <div className='feasibility'>
              {this.props.feasible === false ? "Board is infeasible" : ""}
            </div>

            <form onSubmit={(e) => {e.preventDefault(); this.props.solve(); }}>
                {this.renderRows(matrix)}
                <SolveButton/>
            </form>

            <form onSubmit={(e) => {e.preventDefault(); this.props.clone(); }}>
                <CloneButton/>
            </form>
          </div>
        );
    }
}


class SolveButton extends React.Component {
    render () {
        return (
          <div className='Solve-button'>
            <button onClick={this.props.onClick}>Solve</button>
          </div>
        );
    }
}


class CloneButton extends React.Component {
    render () {
        return (
          <div className='Clone-button'>
            <button onClick={this.props.onClick}>Clone</button>
          </div>
        );
    }
}


class Cell extends React.Component {
    render () {
        return (
            <input
              type='text'
              className={(this.props.inSolution || this.props.inSolution === null) ? 'board-cell' : 'board-cell-not-in-solution'}
              defaultValue={this.props.value}
              onChange={this.props.handleInputChange}
            />
        );
    }
}


class NewBoardForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            numberOfRows: 9,
            numberOfColumns: 9
        }
    }
    render () {
        return (
            <div className='New-board-form'>
                Make new board
                <form onSubmit={
                    (e) => {
                        e.preventDefault();
                        this.props.newBoard({numberOfRows: this.state.numberOfRows, numberOfColumns: this.state.numberOfColumns});
                    }}>
                    <div>
                        <label>
                        Number of rows:
                            <input
                              type='text'
                              name='numberOfRows'
                              defaultValue={this.state.numberOfRows}
                              className='new-board-input'
                              onChange={(e) => this.setState({numberOfRows: e.target.value})}
                              // value={this.state.numberOfRows}
                            />
                        </label>
                    </div>

                    <div>
                        <label>
                        Number of columns:
                            <input
                              type='text'
                              name='numberOfColumns'
                              defaultValue={this.state.numberOfColumns}
                              className='new-board-input'
                              onChange={(e) => this.setState({numberOfColumns: e.target.value})}
                              // value={this.state.numberOfColumns}
                            />
                        </label>
                    </div>

                    <button>Make new board</button>
                </form>
            </div>
        )
    }
}


const toMatrix = (arr, width) =>
    arr.reduce((rows, key, index) => (index % width == 0 ? rows.push([key])
      : rows[rows.length-1].push(key)) && rows, []);

Board.propTypes = {
    cells: PropTypes.arrayOf(
        PropTypes.shape({
            value: PropTypes.number,
            id: PropTypes.number.isRequired
        })
    ).isRequired,
    columns: PropTypes.number.isRequired,
    rows: PropTypes.number.isRequired,
    feasible: PropTypes.bool
}


Cell.propTypes = {
    value: PropTypes.number,
    inSolution: PropTypes.bool
}

// const mapStateToProps = state => {
//   return {
//     todos: getVisibleTodos(state.todos, state.visibilityFilter)
//   }
// }

// const mapDispatchToProps = dispatch => {
//   return {
//     onTodoClick: id => {
//       dispatch(toggleTodo(id))
//     }
//   }
// }

// const VisibleTodoList = connect(
//   mapStateToProps,
//   mapDispatchToProps
// )(TodoList)

export { Board, NewBoardForm };
