import React, {Component} from 'react';

class Wave extends Component {
  constructor(props){
    super(props)
    let top = props.top
    let left = props.offSet
    let location = {top, left}
    let styles = {
      top: `${location.top}px`,
      left: `${location.left}%`
    }
    let baseSpeed = Math.floor(Math.random() * 8)
    let speed = baseSpeed +  Math.floor(Math.random() * 3)
    this.state = {
      baseTop: top,
      location,
      styles,
      speed,
      baseSpeed
    }
    this.time = Math.random()* this.props.offSet * 6.18 / 100
    this.start()
  }

  start(){
    this.intervalId = setInterval(() => {
      if(!this.props.isBottom){
        // 2 pi is full sinusoidal wave
        // if i want 2000 seconds to take the full sinusoidal wave need to increment
        this.time += (6.18 / 100)
        this.move()
      }
    }, this.props.intervalLength)
  }

  move(){
    let location = {
      top: this.state.location.top + Math.sin(this.time)/2,
      left: this.state.location.left - 0.5 * this.state.speed
    }

    if(location.left < (-1 * (window.innerWidth / 6 - this.props.offSet))){
      location.left = this.props.offSet
    }

    let styles = {
      top: `${location.top}px`,
      left: `${location.left}px`
    }
    let speed = this.state.baseSpeed +  Math.floor(Math.random() * 3)
    this.setState({location, styles, speed})
  }

  render(){
    let numWaves = 18
    let waves = [1,2,3,4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24 ].map((num) => {
      let style={
        left: `${num * window.innerWidth / numWaves - window.innerWidth /numWaves}px`,
        width: `${window.innerWidth / numWaves + 5}px`
      }
      return (
        <div key={num} className='wavelet' style={style}></div>
      )
    })

    let circles = [1,2,3,4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24 ].map((num) => {
      let style={
        left: `${num * window.innerWidth / numWaves - window.innerWidth /numWaves - 17}px`,

      }
      return (
        <div key={num} className='circles' style={style}></div>
      )
    })
    return(
      <div className='wave' style={this.state.styles}>
        {waves}
        {circles}
      </div>
    )
  }
}

export default Wave;
