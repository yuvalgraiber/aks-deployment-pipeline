# DevOps Interview Task

## Components
- **Python App**: Fetches book data from Open Library API using Pydantic.
- **Helm Chart**: Deploys a simple web server with KEDA autoscaling.
- **CI/CD**: Jenkins pipeline for automated testing and deployment.

## How to run
1. Python: `cd python-task && pip install -r requirements.txt && python main.py`
2. Helm: `helm upgrade --install my-release ./simple-web -n yuvalgr`