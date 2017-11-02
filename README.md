Assumes you have 3 centos 7 machines d1, d2, d3 and a saltmaster as sm running as a docker registry.

Demo commands!

# Final configuration of our systems

salt -b 1 'd*' state.highstate

# Initialize Docker Swarm using orchestration

salt-run state.orch docker.orch.swarm.bootstrap

# Deploy sunayu demo app

salt-run docker.stack_deploy /opt/sunayu-docker-stack.yml sunayu

salt d1 docker_stack.ps sunayu

Open app in chrome:

http://192.168.56.103

# Generate load to trigger autoscaling!

cd /opt/gitrepos/saltconf2017/scripts/evil_whale
./attack_whale.sh

