import fetch from 'isomorphic-fetch'


export const RECEIVE_BOARDS = 'RECEIVE_BOARDS'
function receiveBoards(json) {
    return {
        type: RECEIVE_BOARDS,
        boards: json
    }
}

export function fetchBoards() {
    return function (dispatch) {
        return fetch('http://localhost:6543/hitori_boards')
            .then(
                response => response.json(),
                error => console.log("Uh oh")
            )
            .then(
                json => dispatch(receiveBoards(json))
            )
    }
}


export function solveBoard(id) {
  return function (dispatch) {
    return fetch(`http://localhost:6543/hitori_boards/${id}/solve`)
      .then(
        response => response.json(),
        error => console.log("Uh oh again")
       )
      .then(
        json => poll(
            () => fetch(`http://localhost:6543/hitori_solves/${json.solve_id}`).then(
                response => response.json()).then(json => json.status),
            200
          )
       ).then(
        response => dispatch(fetchBoards())
       )
  }
}


export function cloneBoard(id) {
  return function(dispatch) {
    return fetch(`http://localhost:6543/hitori_boards/${id}/clone`, {method: "POST"})
      .then(
        response => response.json()
      )
      .then(
        response => dispatch(fetchBoards())
      )
  }
}


export function updateCellValue(payload) {
  return function (dispatch) {
    return fetch(`http://localhost:6543/hitori_cells/${payload.id}/value`, {method: "POST", body: JSON.stringify({value: payload.value})})
      .then(
          response => response.json(),
          error => console.log("Uh oh")
      )
      .then(
          json => dispatch(fetchBoards())
      )
  }
}


export function makeNewBoard(payload) {
  console.log("Make new board")
  console.log(payload);
  return function(dispatch) {
    return fetch(
        `http://localhost:6543/hitori_boards`,
        {
          method: "POST",
          body: JSON.stringify({number_of_rows: payload.numberOfRows, number_of_columns: payload.numberOfColumns})
        })
      .then(response => dispatch(fetchBoards()))
  }
}

var sleep = time => new Promise(resolve => setTimeout(resolve, time))

var poll = (promiseFn, time) => promiseFn().then(
             response => {
                console.log(response);
                if (response === "SUCCESS") {return response}
                return sleep(time).then(() => poll(promiseFn, time));
            })
