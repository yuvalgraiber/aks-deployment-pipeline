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
                        az aks get-credentials \
                          --name ${env.CLUSTER_NAME} \
                          --resource-group ${env.RESOURCE_GROUP} \
                          --overwrite-existing
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

                        # Syntax validation
                        python3 -m py_compile main.py models.py

                        # Optional: add tests if available
                        # pytest || exit 1

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
                        helm lint .
                    """
                }
            }
        }

        stage('Deploy') {
            when { expression { params.ACTION == 'deploy' } }
            steps {
                echo "Starting Helm Upgrade..."

                sh """
                    set -e
                    export KUBECONFIG=${env.KUBECONFIG}

                    helm upgrade --install simple-web ${env.CHART_PATH} \
                        --namespace ${env.NAMESPACE} \
                        -f ${env.CHART_PATH}/values.yaml \
                        --wait \
                        --timeout 5m
                """

                echo "Verifying Rollout..."

                sh """
                    set -e
                    export KUBECONFIG=${env.KUBECONFIG}

                    kubectl rollout status deployment/simple-web \
                        -n ${env.NAMESPACE} \
                        --timeout=120s \
                    || (
                        echo "Rollout failed. Collecting diagnostics..."
                        kubectl get pods -n ${env.NAMESPACE}
                        kubectl describe pods -n ${env.NAMESPACE}
                        exit 1
                    )
                """

                echo "Basic service check..."
                sh """
                    set -e
                    export KUBECONFIG=${env.KUBECONFIG}
                    kubectl get svc -n ${env.NAMESPACE}
                """
            }
        }

        stage('Destroy') {
            when { expression { params.ACTION == 'destroy' } }
            steps {
                echo "Uninstalling release..."

                sh """
                    set -e
                    export KUBECONFIG=${env.KUBECONFIG}

                    helm status simple-web -n ${env.NAMESPACE} \
                    && helm uninstall simple-web -n ${env.NAMESPACE} \
                    || echo "Release already removed"
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
            echo "Pipeline completed successfully!"
        }

        failure {
            echo "Pipeline failed. Check logs above for details."
        }

        always {
            cleanWs()
        }
    }
}