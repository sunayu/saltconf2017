import React, {Component} from 'react';
import Input from '../components/input'

class PhysicsControls extends Component {
  constructor(props){
    super(props)
    let physicsProperties = {
      acceleration: props.physicsProperties.acceleration,
      velocity: props.physicsProperties.velocity,
      timeBtwRequests: props.physicsProperties.timeBtwRequests,
      load: props.physicsProperties.load
    }
    this.state = physicsProperties
  }

  handleFieldChange(property, value){
    let physicsProperties = this.state
    physicsProperties[property] = parseFloat(value)
    this.setState(physicsProperties)
  }

  submit(){
    this.props.onSubmit(this.state)
  }

  render(){
    return (
      <div className="controller">
        <header>Physics Controls</header>
        <Input value={this.state.acceleration}
               onChange={this.handleFieldChange.bind(this)}
               property={"acceleration"}
               attribute={"Gravity:"} />
        <Input value={this.state.velocity}
               onChange={this.handleFieldChange.bind(this)}
               property={"velocity"}
               attribute={"Thrust:"} />
        <Input value={this.state.timeBtwRequests}
               onChange={this.handleFieldChange.bind(this)}
               property={"timeBtwRequests"}
               attribute={"Interval:"} />
        <Input value={this.state.load}
               onChange={this.handleFieldChange.bind(this)}
               property={"load"}
               attribute={"Load:"} />
        <div className='button set' onClick={this.submit.bind(this)}>Set Values</div>
        <div className='button thrust' onClick={this.props.thrust}>Thrust</div>
      </div>
    )
  }
}

export default PhysicsControls;
