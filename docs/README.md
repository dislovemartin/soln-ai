
# AutoML Project with FastAPI, Training Jobs, and Helm Deployment

This project includes an AutoML pipeline using FastAPI for the API, distributed training jobs, and scheduled retraining tasks. The deployment is managed via Helm on a Kubernetes cluster with CI/CD integration. It also supports data drift monitoring with Evidently AI.

## 1. Prerequisites

- **Docker**: Used to build and run containers.
- **Helm**: Manages Kubernetes deployments.
- **Kubernetes**: For container orchestration.
- **GitLab CI/CD** (or similar): For automating build and deployment tasks.
- **Poetry**: Python dependency management.

### Installing Required Tools

```bash
# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

## 2. Project Setup

### Initializing Poetry

The project uses Poetry for dependency management. To set up the environment:

```bash
poetry install
```

This will install all dependencies specified in `pyproject.toml`.

## 3. Building Docker Images

To manually build the Docker images for the **FastAPI** service and the **training jobs**, run the following:

```bash
# Build FastAPI image
docker build -t my-fastapi-image:latest .

# Build training image
docker build -t my-training-image:latest ./training

# Push images to DockerHub (or another registry)
docker push my-fastapi-image:latest
docker push my-training-image:latest
```

## 4. Helm Chart Deployment

To deploy the project using **Helm**, run the following:

```bash
# Install the Helm chart to Kubernetes
helm install automl-deployment ./my-automl-chart

# Upgrade the Helm chart after making changes
helm upgrade automl-deployment ./my-automl-chart

# Rollback in case of failure
helm rollback automl-deployment 1
```

## 5. Kubernetes Management

To manage Kubernetes resources (FastAPI, training jobs, CronJobs):

```bash
# Check the status of Kubernetes deployments
kubectl get deployments

# Check the status of jobs and CronJobs
kubectl get jobs
kubectl get cronjobs
```

## 6. CI/CD Pipeline with GitLab

The **GitLab CI/CD pipeline** automates building Docker images and deploying the Helm chart.

- **GitLab Environment Variables**:
    - `DOCKER_USERNAME`: Your DockerHub username.
    - `DOCKER_PASSWORD`: Your DockerHub password.

The `.gitlab-ci.yml` file:

```yaml
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
    - poetry install
    - docker build -t my-fastapi-image:latest .
    - docker build -t my-training-image:latest ./training
    - docker push my-fastapi-image:latest
    - docker push my-training-image:latest

deploy:
  stage: deploy
  script:
    - helm upgrade --install automl-deployment ./my-automl-chart
```

## 7. Monitoring and Alerts with Prometheus & Grafana

To set up **Prometheus** and **Grafana** for monitoring API usage and scheduling alerts:

```bash
# Add Helm repositories for Prometheus and Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/prometheus

# Install Grafana
helm install grafana grafana/grafana
```

---

## 8. Project Structure

```
/my-automl-chart/      # Helm chart for deployment
/templates/            # Kubernetes templates for FastAPI, Jobs, and CronJobs
/pyproject.toml        # Poetry dependency configuration
/.gitlab-ci.yml        # GitLab CI/CD pipeline
Dockerfile_fastapi     # Dockerfile for FastAPI
Dockerfile_training    # Dockerfile for training jobs
README.md              # Project documentation
```

## 9. Dependency Management with Poetry

To add a new dependency to the project:

```bash
poetry add <dependency_name>
```

To update the dependencies:

```bash
poetry update
```

## 10. Updating the Helm Chart

Whenever changes are made to the project, update the Helm chart by running:

```bash
helm upgrade automl-deployment ./my-automl-chart
```

---

This project is now ready for automated deployments, version-controlled dependencies via Poetry, and scalable deployments with Kubernetes and Helm.
