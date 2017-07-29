import React from 'react';


class Board extends React.Component {
    renderCell(cell) {
        return (
            <Cell
                value={cell.value}
                key={cell.id}
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

    renderRows() {
        return (
            <div className='board-rows'>
                {this.props.cells.map((row, index) => this.renderRow(row, index))}
            </div>
        );
    }


    render () {
        return (
            <form>
                {this.renderRows()}
            </form>
        );
    }
}


class Cell extends React.Component {
    render () {
        return (
            <input type='text' className='board-cell' defaultValue={this.props.value} />
        );
    }
}


export { Board };
