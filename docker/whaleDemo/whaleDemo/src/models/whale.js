class Whale {
  constructor(initPosY, initVelocity){
    this.initPosY = initPosY
    this.posY = initPosY
    this.initVelocity =0
    this.time = 0
    this.acceleration = -60
    this.responseTimes = [0]
  }

  setVelocity(){
    this.velocity = this.initVelocity + this.acceleration * this.time
  }

  setPosY(){
    this.posY = this.initPosY - (this.initVelocity * this.time + 1/2 * this.acceleration * Math.pow(this.time, 2))
  }

  incrementTime(time, maxPosY){
    this.time += time
    this.setVelocity()
    this.setPosY()
    if(this.posY > maxPosY - 150) {
      this.posY = maxPosY - 150
      this.isBottom = true
    } else {
      this.posY = this.posY
    }
    // The "Actual" position of the whale will still be increased depending on paramters
    // ie this.setPosY() will still calculate the actual posY this will just reset
    // it to be the top of the screen
    this.posY = this.posY < 0 ? 0 : this.posY
  }
}

export default Whale
