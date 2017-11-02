add container {{ data['container_id'] }} on {{ data['id'] }} to docker_stats:
  runner.queue.insert:
  - args:
      queue: docker_stats
      items: 
      - "{{ data['id'] }}:{{ data['container_id'] }}:{{ data['service_name'] }}"
