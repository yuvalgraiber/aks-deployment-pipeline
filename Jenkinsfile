pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 10, unit: 'MINUTES')
    }

    parameters {
        choice(name: 'ACTION', choices: ['deploy', 'destroy'], description: 'Choose whether to deploy or destroy the environment')
    }

    environment {
        NAMESPACE = 'yuvalgr'
        CHART_PATH = './simple-web'
        PYTHON_TASK_PATH = './python-task'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
    }

    stages {
        stage('Python Setup & Execute') {
            steps {
                dir("${PYTHON_TASK_PATH}") {
                    sh """
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        python3 -m py_compile main.py models.py
                        python main.py
                    """
                }
            }
        }

        stage('Helm Lint') {
            steps {
                dir("${CHART_PATH}") {
                    sh "helm lint ."
                }
            }
        }

        stage('Deploy / Destroy') {
            steps {
                script {
                    if (params.ACTION == 'deploy') {
                        sh """
                            export KUBECONFIG=${KUBECONFIG}
                            helm upgrade --install my-release ${CHART_PATH} --namespace ${NAMESPACE} --create-namespace --wait
                        """
                    } else {
                        sh """
                            export KUBECONFIG=${KUBECONFIG}
                            helm uninstall my-release --namespace ${NAMESPACE}
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}