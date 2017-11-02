import React, {Component} from 'react';
import seaweedImages from './seaweedImages';

class Seaweed extends Component{
  constructor(props){
    super(props)
    let imageUrl = seaweedImages[Math.floor(Math.random()*seaweedImages.length)];
    let zIndex=Math.floor(Math.random() * 3) + 10
    let top = (window.innerHeight - window.innerHeight / 2) + parseInt(Math.random() * (window.innerHeight  / 2) - 200, 10)
    let left = parseInt(Math.random() * 100, 10)
    let location = {
      top,
      left
    }
    let styles = {
      top: `${location.top}px`,
      left: `${location.left}%`
    }
    this.state = {
      isBottom: props.isBottom,
      location,
      styles,
      imageUrl,
      zIndex
    }
    this.start()
  }

  start(){
    this.intervalId = setInterval(() => {
      if(!this.props.isBottom){
        this.moveWeed()
      }
    }, this.props.intervalLength)
  }

  moveWeed(){
    let location = {
      top: this.state.location.top,
      left: this.state.location.left + 0.3
    }
    let zIndex = this.state.zIndex
    let imageUrl = this.state.imageUrl
    if(location.left > 105){
      zIndex=Math.floor(Math.random() * 3) + 10
      imageUrl = seaweedImages[Math.floor(Math.random()*seaweedImages.length)];
      location.top = (window.innerHeight - window.innerHeight / 2) + parseInt(Math.random() * (window.innerHeight  / 2) - 200, 10)
      location.left = Math.random() * 10 - 15
    }
    let styles = {
      top: `${location.top}px`,
      left: `${location.left}%`,
      zIndex
    }
    this.setState({location, styles, imageUrl, zIndex})
  }

  render(){
    return (
      <img alt={"seaweed"} className='seaweed' src={this.state.imageUrl} style={this.state.styles} />
    )
  }
}

export default Seaweed
