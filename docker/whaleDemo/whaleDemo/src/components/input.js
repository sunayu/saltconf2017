import React, {Component} from 'react';

class Input extends Component {
  constructor(props){
    super()
    this.state = {
      value: props.value
    }
  }
  handleChange(evt){
    this.setState({
      value: evt.target.value
    }, () => {
      this.props.onChange(this.props.property, this.state.value)
    })
  }

  render(){
    return (
      <div className='inputField'>
        <span className='attribute'>{this.props.attribute}</span>
        <input onChange={this.handleChange.bind(this)} value={this.state.value || ''}/>
      </div>
    )
  }
}

export default Input;
