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
      this.handleDemo = this.handleDemo.bind(this);
      // this.handleTaskStatistics = this.handleSubmit.bind(this);
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

  handleDemo(event) {
    axios.get(`http://localhost:5000/show_demo`)
  }

  // handleTaskStatistics(event) {
  //   axios.post(`http://localhost:5000/get_task_statistics`, '')
  //   .then((res) => {
  //     console.log(res)
  //   })
  // }

  render() {
    var info = this.state.exec_profiler_info;
    var result = [];
    for(var i in info)
        result.push(info[i]);

    return (
      <div className="appForm">
        <div className="config mb-4">
          <h4 className="mb-3">Config Parameters</h4>
          <div className="subtitle mb-3">
            Config parameters before the Jupiter deployment.
          </div>
          <form className="mb-3 w-50" onSubmit={this.handleSubmit}>
            <div className="input-group mb-3">
              <div className="input-group-prepend">
                <span className="input-group-text">App path:</span>
              </div>
              <input
                name="appPath"
                className="form-control"
                type="text"
                placeholder="Enter the app path (Like 'app_specific_files/network_monitoring_app')"
                required
                onChange={this.handleChange}
              />
            </div>

            <div className="input-group mb-3">
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
              <div className="input-group mb-3">
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
              <div className="input-group mb-3">
                <div className="input-group-prepend">
                  <span className="input-group-text">Node information: </span>
                </div>
                <textarea
                  name="nodesDetails"
                  className="form-control"
                  rows="5"
                  placeholder="Enter the node information here.&#x0a;e.g  home master&#x0a;node2 usa-east-nodea&#x0a;node3 usa-west-nodeb"
                  required
                  onChange={this.handleNodesChange}
                />
              </div>
            </div>

            <div className="submit">
              <input
                type="submit"
                className="btn btn-outline-primary "
                value="Submit"
              />
            </div>
          </form>
        </div>

        <div className="exec mb-4">
          <h4 className="mb-3">Run Execution Profiler</h4>
          <div className="subtitle mb-4">
            Click this to see the execution time of each task on each node and the amount of data it passes to its child tasks.
          </div>
          <div className="d-flex justify-content-start align-items-center">
            <button className="btn btn-outline-primary p-3" onClick={this.handleRunExecProfiler}>Run</button>
            <table className="ml-5">
              <thead>
                <tr>
                  <th scope="col">Node</th>
                  <th scope="col">Task</th>
                  <th scope="col">Time (sec)</th>
                  <th scope="col">Output_data (Kbit)</th>
                </tr>
              </thead>
              { result.length == 0 ? (
                  <tbody>
                    <th className="font-weight-normal">N/A</th>
                    <th className="font-weight-normal">N/A</th>
                    <th className="font-weight-normal">N/A</th>
                    <th className="font-weight-normal">N/A</th>
                  </tbody>
                  ) : (
                  <tbody>
                  {
                    result.map((item, key) => {
                      return <tr key={key}>
                          <th className="font-weight-normal">home</th>
                          <th className="font-weight-normal">{item.split(",")[0]}</th>
                          <th className="font-weight-normal">{item.split(",")[1]}</th>
                          <th className="font-weight-normal">{item.split(",")[2]}</th>
                        </tr>;
                      })
                  }
                  </tbody>
                  )
                }
            </table>
          </div>
        </div>

        <div className="mqtt mb-4">
          <h4 className="mb-3">Test mqtt with Jupiter running pods</h4>
          <button className="btn btn-outline-primary" onClick={this.handleDemo}>Start and keep listening to Jupiter</button>
        </div>

        <div className="network mb-4">
          <h4 className="mb-3">Get Network Statistics</h4>
          <div className="subtitle mb-4">
            Click this to see communication information of all links between nodes in the network.
            <br/>
            It will give the quadratic regression parameters of each link representing the corresponding communication cost.
          </div>
          <div className="d-flex justify-content-start align-items-center">
            <button className="btn btn-outline-primary">Run</button>
            <table className="ml-3">
              <thead>
                <tr>
                  <th scope="col">Task_name</th>
                  <th scope="col">local_input_file</th>
                  <th scope="col">Enter_time</th>
                  <th scope="col">Execute_time</th>
                  <th scope="col">Finish_time</th>
                  <th scope="col">Elapse_time</th>
                  <th scope="col">Duration_time</th>
                  <th scope="col">Waiting_time </th>
                </tr>
              </thead>
              <tbody>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    )
  };
};

export default AppForm;