runtime: python
env: flex
entrypoint: gunicorn -b :$PORT main:app
service: flex-demo
runtime_config:
  operating_system: "ubuntu22"
  runtime_version: "3.12"
automatic_scaling:
  min_num_instances: 1
  max_num_instances: 2
