import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

class App extends Component{
  state = {
    selectedFile: null
  }

  fileSelectHandler = event =>{
    this.setState({
      selectedFile: event.target.files[0]
    })
  }

  fileUploadHandler = () => {
    const fd = new FormData();
    fd.append('image', this.state.selectedFile, this.state.selectedFile.name);
    axios.post('http://localhost:8080',fd).then(res => {
      console.log(res);
    });
  }

 render() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Maze Solver
        </p>
        <input type = "file" onChange = {this.fileSelectHandler} />
        <button onClick = {this.fileUploadHandler}> Upload </button>
      </header>
      
    </div>
  );
}
}

export default App;
