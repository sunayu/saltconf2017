docker:
  swarm:
    managers:
    - d1
    workers:
    - d2
    - d3
  registries:
  - host: sm
    port: 5000
  nic: enp0s3
