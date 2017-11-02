import React, { Component } from 'react';
import axios from 'axios'
import './App.css';
import PhysicsControls from './containers/PhysicsControls'
import WhaleModel from './models/whale';
import Whale from './components/whale';
import Wave from './components/wave';
import Seaweed from './components/seaweed';
// import Bubble from './components/bubble';
import dockerSadUp from './images/dockerSadUp.png';
import dockerHappyUp from './images/dockerHappyUp.png';
import dockerHappyDown from './images/dockerHappyDown.png';

class App extends Component {
  constructor(props){
    super(props)
    let whale = new WhaleModel(100, 10)
    let imageUrl = dockerHappyUp
    let physicsProperties = {
      acceleration: -50,
      velocity: 115,
      timeBtwRequests: 0.89,
      load: 1500
    }
    let intervalLength = 30
    this.state = {
      whale,
      imageUrl,
      physicsProperties,
      intervalLength,
      cpuUsageStats: []
    }
    this.start()
    this.startRequests(this.state.physicsProperties.timeBtwRequests * 1000)
    this.startStatRequests()
    this.pingStats().then((res) => {
        let cpuUsageStats = this.parseData(res)
        this.setState({cpuUsageStats})
    })
  }

  parseData(data){
    let dataKeys = Object.keys(data)
    let hostObjs = []
    dataKeys.forEach((key) => {
      let hostObj = { name: key, stats: data[key].stats }
      hostObjs.push(hostObj)
    })
    return hostObjs
  }

  startRequests(interval){
    this.reqIntervalId = setTimeout(() => {
      this.ping().then(() => {
        this.thrust()
        this.startRequests(this.state.physicsProperties.timeBtwRequests * 1000)
      })
    }, interval)
  }

  startStatRequests(){
    this.statReqIntervalId = setInterval(() => {
      this.pingStats().then((res) => {
        let cpuUsageStats = this.parseData(res)
        this.setState({cpuUsageStats})
      })
    }, 15000)
  }

  ping(){
    return axios.get(`http://192.168.56.102:4567/${this.state.physicsProperties.load}`)
  }

  pingStats() {
    return axios.get('http://192.168.56.102:9999').then((res)=>{
        return res.data
    })
  }

  thrust(){
    this.setState({
      imageUrl: dockerHappyDown
    })
    setTimeout(() => {
      this.setState({
        imageUrl: dockerHappyUp
      })
    }, 500)
    let whale = this.state.whale
    whale.initVelocity = this.state.physicsProperties.velocity
    whale.initPosY = whale.posY
    whale.time = 0
    whale.isBottom = false
    if(!this.intervalId){
      this.start()
    }
    this.setState({
      whale: whale
    })

  }

  start(){
    this.intervalId = setInterval(() => {
      let whale = this.state.whale
      whale.incrementTime(0.10, window.innerHeight)
      if(whale.isBottom){
        clearInterval(this.intervalId)
        this.intervalId = null
        this.setState({imageUrl: dockerSadUp})
      }
      this.setState({whale})
    }, this.state.intervalLength)
  }

  setPhysicsProperties(physicsProps){
    let whale = this.state.whale
    whale.acceleration = physicsProps.acceleration
    let physicsProperties = this.state.physicsProperties
    physicsProperties.velocity = physicsProps.velocity
    physicsProperties.timeBtwRequests = physicsProps.timeBtwRequests
    physicsProperties.load = physicsProps.load
    this.setState({whale, physicsProperties})
  }

  render() {
    let seaweed = [1,2,3,4,5, 6].map((el) => {
      return <Seaweed key={el} isBottom={this.state.whale.isBottom} intervalLength={this.state.intervalLength}/>
    })
    // TODO: too slow for now, maybe add bubble but reduce interval for motion to higher than 20
    // let bubbles = [1,2,3,4,5, 6].map((el) => {
    //   return <Bubble key={el} isBottom={this.state.whale.isBottom}/>
    // })
    let sandTransitionStyle = {
      width: `${window.innerWidth}px`,
      top: `${window.innerHeight - window.innerHeight / 1.5}px`
    }
    let sandStyle = {
      width: `${window.innerWidth}px`,
      top: `${window.innerHeight + 200 - window.innerHeight / 1.5}px`
    }

    let cpuUsageStats = this.state.cpuUsageStats.map((stat) => {
        return (
          <div key={stat.name} className='stat'>
            <header>{stat.name}</header>
            {
              stat.stats.map((indstat,i)=>{
                return (
                  <div className="indstat" key={i}>
                    <span className='name'>{indstat.name}</span>
                    <span className='percentage'>{indstat.cpu_percent}</span>
                  </div>
                )
              })
            }
         </div>
        )
    })

    return (
      <div className="App">
        <PhysicsControls physicsProperties={this.state.physicsProperties}
                         onSubmit={this.setPhysicsProperties.bind(this)}
                         thrust={this.thrust.bind(this)}/>
        <div className='usageStats'>
          {cpuUsageStats}
        </div>

        <Wave isBottom={this.state.whale.isBottom}
              top={50}
              offSet={-52}
              intervalLength={this.state.intervalLength}/>
        <Wave isBottom={this.state.whale.isBottom}
              top={115}
              offSet={-14}
              intervalLength={this.state.intervalLength}/>
        <Wave isBottom={this.state.whale.isBottom}
              top={195}
              offSet={-36}
              intervalLength={this.state.intervalLength}/>
        {seaweed}
        <Whale
          whale={this.state.whale}
          imageUrl={this.state.imageUrl} />
        <div className='sand-transition' style={sandTransitionStyle}></div>
        <div className='sand' style={sandStyle}></div>

      </div>
    );
  }
}

export default App;
