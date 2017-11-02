visualizer stack:
  file.managed:
  - name: /opt/visualizer-stack.yml
  - source: salt://demo/files/visualizer-stack.yml

docker example stack:
  file.managed:
  - name: /opt/example-docker-stack.yml
  - source: salt://demo/files/example-docker-stack.yml

sunayu docker stack:
  file.managed:
  - name: /opt/sunayu-docker-stack.yml
  - source: salt://demo/files/sunayu-docker-stack.yml

sunayu dev docker stack:
  file.managed:
  - name: /opt/sunayu-docker-stack-dev.yml
  - source: salt://demo/files/sunayu-docker-stack-dev.yml

gimmestats app:
  file.managed:
  - name: /opt/gimmestats.py
  - source: salt://demo/files/gimmestats.py

gimmestats app run:
  cmd.run:
  - name: python /opt/gimmestats.py &
  - bg: true
