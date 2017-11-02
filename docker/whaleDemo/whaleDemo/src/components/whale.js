import React, { Component } from 'react';

class Whale extends Component {
  constructor(props){
    super(props)
    this.state = {
      whale: props.whale,
      imageUrl: props.imageUrl
    }
  }

  setStyle(){
   return {top: `${this.state.whale.posY}px`}
  }

  render(){
    return(
      <img alt={"docker whale"} src={this.props.imageUrl} style={this.setStyle()} className='whale'/>
    )
  }
}

export default Whale;
