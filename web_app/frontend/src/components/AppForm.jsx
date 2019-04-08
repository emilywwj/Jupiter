import React, { Component } from 'react';
import axios from 'axios';
import './AppForm.css';

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
        exec_profiler_info: '',
      };
      this.handleChange = this.handleChange.bind(this);
      this.handleNodesChange = this.handleNodesChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.handleRunExecProfiler = this.handleRunExecProfiler.bind(this);
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

  handleSubmit(event) {
    event.preventDefault()

    const data = this.state;
    axios.post(`http://localhost:5000/data`, data)
    .then((res) => { 
      this.setState((state) => ({
        ...state,
        appPath: '',
        SCHEDULER: '',
        nodes: 
        {
          nodesNum: '',
          nodesDetails: '',
        },
      }));
    })
    .catch((err) => { console.log(err); });
  };

  handleRunExecProfiler(event) {
    axios.post(`http://localhost:5000/run_exec_profiler`, '')
    .then((res) => { 
      var processed_info = JSON.parse(res.data.exec_profiler_info)

      console.log(processed_info)
      console.log(typeof(processed_info))
      this.setState((state) => ({
        ...state,
        exec_profiler_info: processed_info,
      }))
    })
  }

  render() {
    var info = this.state.exec_profiler_info;
    var result = [];
    for(var i in info)
        result.push(info[i]);

    return (
      <div>
        <form className="mb-3" onSubmit={this.handleSubmit}>
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

        <div>
          <h4>Run Execution Profiler</h4>
          <div className="d-flex justify-content-start align-items-center">
            <button className="btn btn-primary" onClick={this.handleRunExecProfiler}>Run</button>
            <table className="ml-3">
              <thead>
                <tr>
                  <th scope="col">Task</th>
                  <th scope="col">Time (sec)</th>
                  <th scope="col">Output_data (Kbit)</th>
                </tr>
              </thead>
              <tbody>
                { result.map((item, key) => {
                    return <tr key={key}>
                        <th scope="col">{item.split(",")[0]}</th>
                        <th scope="col">{item.split(",")[1]}</th>
                        <th scope="col">{item.split(",")[2]}</th>
                      </tr>;
                  })
                }
              </tbody>
            </table>
          </div>

        </div>

      </div>
    )
  };
};

export default AppForm;