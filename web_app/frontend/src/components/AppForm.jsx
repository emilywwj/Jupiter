import React, { Component } from 'react';

class AppForm extends Component {
  constructor() {
    super();
      this.state = {
        appPath: '',
        SCHEDULER: '',
        nodes: 
        {
          nodesNum: '',
          nodesDetails: '',
        },
      };
      this.handleChange = this.handleChange.bind(this);
      this.handleNodesChange = this.handleNodesChange.bind(this);
      // this.addNode = this.addNode.bind(this);
  };

  handleChange(event) {
    const name = event.target.name;
    const value = event.target.value;
    this.setState((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  handleNodesChange(event) {
    event.preventDefault()

    const name = event.target.name;
    const value = event.target.value;
    this.setState((prevState) => ({
      ...prevState,
      nodes: {
        ...prevState.nodes, 
        [name]: value,
      },
    }));
  };

  // addNode() {
  //   this.setState((prevState) => ({
  //     ...prevState,
  //     nodes: [
  //       ...prevState.nodes,
  //       {node: ''},
  //     ],
  //   }));
  // }

  render() {
    let nodes = this.state.nodes;

    return (
      <form className="mb-3">
        <div className="input-group mb-2">
          <div className="input-group-prepend">
            <span className="input-group-text">App path:</span>
          </div>
          <input
            name="appPath"
            className="form-control"
            type="text"
            placeholder="Enter the app path"
            required
            onChange={this.handleChange}
          />
        </div>

        <div className="input-group mb-2">
          <div className="input-group-prepend">
            <label className="input-group-text">Task mapper:</label>
          </div>
          <select defaultValue="Choose task mapper" name="SCHEDULER" onChange={this.handleChange}>
            <option defaultValue="" disabled hidden>Choose task mapper</option>
            <option value="0">HEFT</option>
            <option value="1">WAVE_RANDOM</option>
            <option value="2">WAVE_GREEDY</option>
            <option value="3">HEFT_MODIFIED</option>
          </select>
        </div>

        <div className="nodesInfo">
          <div className="input-group mb-2">
            <div className="input-group-prepend">
              <span className="input-group-text">Number of nodes: </span>
            </div>
            <input
              name="nodesNum"
              className="form-control"
              placeholder="Enter the number of nodes"
              required
              onChange={this.handleNodesChange}
            />
          </div>
          <div className="input-group mb-2">
            <div className="input-group-prepend">
              <span className="input-group-text">Node information: </span>
            </div>
            <textarea
              name="nodesDetails"
              className="form-control"
              placeholder="Enter the node information (Like 'home name1' followed by 'node2 name2')"
              required
              onChange={this.handleNodesChange}
            />
          </div>
        </div>

        <div className="submit">
          <input
            type="submit"
            className="btn btn-secondary"
            value="Submit"
          />
        </div>
      </form>
    )
  };
};

export default AppForm;