# AKS Deployment Pipeline Task

This repository contains a comprehensive solution for the DevOps technical task, demonstrating a full CI/CD lifecycle, infrastructure management, and automated data processing.

## Architecture & Components

### 1. CI/CD Pipeline (Jenkins)
- **Automated Workflow**: End-to-end pipeline defined in a `Jenkinsfile` (Declarative Pipeline).
- **Stages**: Python environment setup, dependency installation, Pydantic validation, Helm linting, and multi-mode deployment.
- **Dynamic Control**: Includes a **Deploy/Destroy** parameter toggle for easy environment management.
- **Environment Compatibility**: The pipeline is designed to run on a Linux-based agent (as provided in the task environment) to support Bash commands and Python virtual environments.

### 2. Kubernetes & Helm (AKS)
- **Helm Chart**: Modularized configuration for the `simple-web` application.
- **Resiliency & Health**:
    - **Liveness & Readiness Probes**: Implemented to ensure zero-downtime deployments and automatic self-healing.
    - **Resource Management**: Explicit CPU/Memory **Requests and Limits** configured for predictable performance and stable scaling.
- **Traffic Management**: Ingress rules configured to route traffic via the `/yuvalgr` path.
- **KEDA Autoscaling**: Advanced autoscaling using a `ScaledObject` with three triggers:
    - **CPU Utilization**: Scales when exceeding 50%.
    - **Memory Usage**: Scales when exceeding 100Mi.
    - **Cron Schedule**: Forced scaling to 3 replicas between **08:00 AM and 12:00 AM** (Asia/Jerusalem timezone).

### 3. Python Automation (Book Fetcher)
- **API Integration**: Fetches real-time metadata from the Open Library API.
- **Data Validation**: Uses **Pydantic** models to ensure type safety and data integrity.
- **Processing Logic**: 
    - Filters results based on publication year (>1950) and specific keywords.
    - **Extensible Architecture**: Designed with an `OutputHandler` interface to easily support future formats (CSV, Database, etc.).
- **Persistence**: Exports the filtered results to a structured `filtered_books.json` file.

---

## Prerequisites
- **Jenkins**: Must have Python3, `venv`, and Helm 3 installed.
- **Cluster Access**: Kubernetes config must be available at `/var/lib/jenkins/.kube/config`.
- **Managed Identity**: Ensure the VM is logged in via `az login -i` to interact with AKS.

---

## Usage

1. **Run the Pipeline**:
   - Navigate to the Jenkins Dashboard.
   - Select the `aks-deployment-pipeline` job.
   - Click **Build with Parameters**.
   - Choose `deploy` to create/update the environment or `destroy` to clean up resources.

2. **Access the Application**:
   - The application is accessible via the Public IP at: `http://20.71.162.74/yuvalgr`

3. **Verify Python Results**:
   - The filtered data results can be inspected in the Jenkins **Console Output** or by checking the generated `filtered_books.json` file in the workspace.