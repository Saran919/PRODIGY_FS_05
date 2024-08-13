
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PostFeed from './components/PostFeed';
import CreatePost from './components/CreatePost';

function App() {
    return (
        <Router>
            <div>
                <h1>Social Media</h1>
                <Switch>
                    <Route path="/" exact component={PostFeed} />
                    <Route path="/create-post" component={CreatePost} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;
