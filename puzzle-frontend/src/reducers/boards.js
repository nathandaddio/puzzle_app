import store from './store';


export default function boards(state = store.boards, action) {
  switch (action.type) {
    case 'RECEIVE_BOARDS':
      {console.log(action); return action.boards;}
    default:
      return state;
  }
}
