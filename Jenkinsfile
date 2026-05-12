pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
    }

    parameters {
        choice(name: 'ACTION', choices: ['deploy', 'destroy'], description: 'Deploy or destroy the environment')
    }

    environment {
        NAMESPACE        = 'yuvalgr'
        CHART_PATH       = './simple-web'
        PYTHON_TASK_PATH = './python-task'
        CLUSTER_NAME     = 'devops-interview-aks'
        RESOURCE_GROUP   = 'devops-interview-rg'
        KUBECONFIG       = "/var/lib/jenkins/.kube/config"
    }

    stages {
        stage('AKS Login') {
            steps {
                echo "Authenticating with AKS..."
                retry(2) {
                    sh """
                        set -e
                        az login --identity
                        az aks get-credentials --name ${env.CLUSTER_NAME} --resource-group ${env.RESOURCE_GROUP} --overwrite-existing
                        kubelogin convert-kubeconfig -l msi
                    """
                }
            }
        }

        stage('Python Task & Tests') {
            when { expression { params.ACTION == 'deploy' } }
            steps {
                dir("${env.PYTHON_TASK_PATH}") {
                    sh """
                        set -e
                        rm -rf venv
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --no-cache-dir -r requirements.txt
                        python3 -m py_compile main.py models.py
                        python main.py
                    """
                }
            }
        }

        stage('Helm Lint') {
            when { expression { params.ACTION == 'deploy' } }
            steps {
                dir("${env.CHART_PATH}") {
                    sh """
                        set -e
                        helm dependency update
                        helm lint .
                    """
                }
            }
        }

        stage('Deploy') {
            when { expression { params.ACTION == 'deploy' } }
            steps {
                echo "Ensuring Namespace and Deploying..."
                sh """
                    set -e
                    export KUBECONFIG=${env.KUBECONFIG}
                    kubectl create namespace ${env.NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
                    
                    helm upgrade --install simple-web ${env.CHART_PATH} \
                        --namespace ${env.NAMESPACE} \
                        -f ${env.CHART_PATH}/values.yaml \
                        --wait --timeout 5m
                """

                sh """
                    set -e
                    export KUBECONFIG=${env.KUBECONFIG}
                    kubectl rollout status deployment/simple-web -n ${env.NAMESPACE} --timeout=120s || (
                        echo "Rollout failed. Diagnostics:"
                        kubectl describe pods -n ${env.NAMESPACE}
                        exit 1
                    )
                """
            }
        }

        stage('Destroy') {
            when { expression { params.ACTION == 'destroy' } }
            steps {
                sh """
                    set -e
                    export KUBECONFIG=${env.KUBECONFIG}
                    helm uninstall simple-web -n ${env.NAMESPACE} || echo "Already removed"
                """
            }
        }
    }

    post {
        success {
            script {
                if (params.ACTION == 'deploy') {
                    archiveArtifacts artifacts: "${env.PYTHON_TASK_PATH}/*.json", allowEmptyArchive: true
                }
            }
        }
        always { cleanWs() }
    }
}