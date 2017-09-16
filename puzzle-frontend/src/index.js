import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { Provider } from 'react-redux'
import { createStore, applyMiddleware, compose } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import rootReducer from './reducers'
import { fetchBoards } from './actions'


const loggerMiddleware = createLogger()

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

let store = createStore(
    rootReducer,
    composeEnhancers(
        applyMiddleware(
            thunkMiddleware,
            loggerMiddleware
        )
    )
)

store.dispatch(fetchBoards())


ReactDOM.render(
    <Provider store={store}>
      <App />
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
