# AKS Deployment Pipeline Task

This repository demonstrates a production-oriented DevOps solution, covering a full CI/CD workflow, Kubernetes deployment using Helm, and automated data processing with Python.

---

## 🔄 End-to-End Flow

Jenkins Pipeline → Python Processing → Helm Deployment → AKS Cluster → KEDA Autoscaling → Application Pods

---

## 🧩 Architecture & Components

### 1. CI/CD Pipeline (Jenkins)

A declarative pipeline implementing a full CI/CD lifecycle with strong focus on reliability and observability.

**Parameterized Execution**

* `deploy` – build, validate, and deploy the application
* `destroy` – safely remove all deployed resources

**Pipeline Stages**

* AKS authentication using Azure Managed Identity
* Python environment isolation (`venv`)
* Syntax validation (`py_compile`)
* Helm chart linting
* Deployment using `helm upgrade --install`
* Rollout verification using `kubectl rollout status`

**Resilience & Reliability**

* **Retry mechanism** for AKS authentication (handles transient failures)
* **Fail-fast execution** using `set -e` to prevent partial deployments
* **Timeouts** to avoid hanging pipelines
* **Automated diagnostics**:

  * On failure, the pipeline automatically runs:

    * `kubectl get pods`
    * `kubectl describe pods`
  * This provides immediate root-cause visibility directly in Jenkins logs

**Post Actions**

* Archives generated JSON artifacts
* Cleans workspace after every run

---

### 2. Kubernetes & Helm (AKS)

* Modular Helm chart for the `simple-web` application

**Deployment Strategy**

* RollingUpdate (`maxSurge: 1`, `maxUnavailable: 0`) ensuring zero downtime

**Health & Self-Healing**

* Liveness and Readiness probes implemented

**Resource Management**

* CPU and Memory requests/limits defined for predictable performance

**Traffic Management**

* Ingress routes traffic via `/yuvalgr`

**Autoscaling with KEDA**

* CPU & Memory trigger Memory trigger based on utilization
* Cron-based scaling:

  * 3 replicas between 08:00–00:00 (Asia/Jerusalem)

---

### 3. Python Automation (Book Fetcher)

* Fetches metadata from the Open Library API
* Uses **Pydantic** for strict validation

**Processing Logic**

* Filters books:

  * Published after 1950
  * Matching specific keywords

**Design**

* Extensible via `OutputHandler` abstraction
* Easily supports future outputs (CSV, DB, etc.)

**Output**

* Saves results to `filtered_books.json`

---

## ⚙️ Prerequisites

* Jenkins agent with:

  * Python 3
  * Helm 3
  * Azure CLI
  * kubectl + kubelogin

* Azure VM configured with **Managed Identity**

* Access to AKS cluster (`devops-interview-aks`)

> AKS authentication is performed dynamically during pipeline execution using `az login --identity`.

---

## 🚀 Usage

### 1. Run the Pipeline

1. Open Jenkins
2. Select the pipeline job
3. Click **Build with Parameters**
4. Choose:

   * `deploy` – deploy or update the application
   * `destroy` – remove all resources

---

### 2. Access the Application

Retrieve the external endpoint dynamically:

```bash
kubectl get ingress -n yuvalgr
```

Access via:

```
http://<EXTERNAL-IP>/yuvalgr
```

---

### 3. Verify Deployment & Scaling

```bash
kubectl get pods -n yuvalgr
kubectl get svc -n yuvalgr
kubectl get scaledobjects -n yuvalgr
```

---

### 4. View Python Results

* Available in Jenkins **Console Output**
* Or downloadable via **Build Artifacts**

---

## 🔍 Observability & Debugging

The pipeline is designed to be **self-diagnosing**.

In case of failure, Jenkins logs will include:

* Helm lint results
* Python syntax validation
* Deployment rollout status
* Full pod diagnostics (`describe + logs`)

Manual commands:

```bash
kubectl get pods -n yuvalgr
kubectl describe pods -n yuvalgr
kubectl logs -l app.kubernetes.io/name=simple-web -n yuvalgr
kubectl rollout status deployment/simple-web -n yuvalgr
```

---

## 💡 Key Design Principles

* Idempotent deployments using Helm
* Fail-fast CI/CD to prevent inconsistent states
* Built-in observability for rapid debugging
* Clear separation between application logic and infrastructure
* Scalable architecture using Kubernetes + KEDA

---

## 👤 Author

**Yuval Graiber**
DevOps Engineer
