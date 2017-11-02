Sunayu SaltConf '17 Demo App
=========


Getting started
---------------
To create an image for flappy, run in this directory:
```
docker build -t flappy .
```
The image can then be run on a Docker Swarm via:
```
docker stack deploy --compose-file docker-stack.yml flappy
```
