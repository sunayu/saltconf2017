# Whale Demo

## Installation

```bash
$ npm install
```

> If you want to run this against a rest service, comment lines 35 and 38 back in and configure the endpoint on line 43

## Example

```js
startRequests(interval){
  this.reqIntervalId = setTimeout(() => {
    this.ping().then(() => {
      this.thrust()
      this.startRequests(this.state.physicsProperties.timeBtwRequests * 1000)
    })
  }, interval)
}

ping(){
  return axios.get("http://localhost:4000/test")
}
```
