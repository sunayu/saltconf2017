import React, {Component} from 'react';
import bubbleImages from './bubbleImages';

class Bubble extends Component{
  constructor(props){
    super(props)
    let imageUrl = bubbleImages[Math.floor(Math.random()*bubbleImages.length)];
    let zIndex=Math.floor(Math.random() * 3) + 10
    let top = (window.innerHeight - window.innerHeight / 1.5) + parseInt(Math.random() * 500)
    let left = parseInt(Math.random() * 100)
    let location = {
      top,
      left
    }
    let size = Math.random() * 40 + 20
    let styles = {
      top: `${location.top}px`,
      left: `${location.left}%`,
      height: `${size}px`,
      width: `${size}px`
    }
    this.state = {
      isBottom: props.isBottom,
      location,
      styles,
      imageUrl,
      zIndex,
      size
    }
    this.start()
  }

  start(){
    this.intervalId = setInterval(() => {
      if(!this.props.isBottom){
        this.move()
      }
    }, 20)
  }

  move(){
    let location = {
      top: this.state.location.top,
      left: this.state.location.left + Math.random() * 0.4
    }
    let zIndex = this.state.zIndex
    let imageUrl = this.state.imageUrl
    let size = this.state.size
    if(location.left > 105){
      zIndex=Math.floor(Math.random() * 3) + 10
      imageUrl = bubbleImages[Math.floor(Math.random()*bubbleImages.length)];
      location.top = (window.innerHeight - window.innerHeight / 1.5) + parseInt(Math.random() * 500)
      location.left = Math.random() * 10 - 15
      size = Math.random() * 40 + 20
    }

    let styles = {
      top: `${location.top}px`,
      left: `${location.left}%`,
      height: `${size}px`,
      width: `${size}px`,
      zIndex
    }
    this.setState({location, styles, imageUrl, zIndex, size})
  }

  render(){


    return (
      <img className='bubble' src={this.state.imageUrl} style={this.state.styles} />
    )
  }
}

export default Bubble
