pipeline {
    agent any

    environment {
        // Define the namespace to be used across the pipeline
        NAMESPACE = 'yuvalgr'
        CHART_PATH = './simple-web'
        PYTHON_TASK_PATH = './python-task'
    }

    stages {
        stage('Python Setup & Execute') {
            steps {
                dir("${PYTHON_TASK_PATH}") {
                    sh """
                        # Create a temporary virtualenv for the CI run
                        python3 -m venv venv
                        . venv/bin/activate
                        # Install dependencies from requirements.txt
                        pip install -r requirements.txt
                        # Run the book fetcher script
                        python main.py
                    """
                }
            }
        }

        stage('Helm Lint') {
            steps {
                dir("${CHART_PATH}") {
                    // Verify the Helm chart syntax
                    sh "helm lint ."
                }
            }
        }

       stage('Deploy to AKS') {
            steps {
                // We explicitly tell Helm where the config file is
                withEnv(["KUBECONFIG=/var/lib/jenkins/.kube/config"]) {
                    sh """
                        helm upgrade --install my-release ${CHART_PATH} \
                        --namespace ${NAMESPACE} \
                        --create-namespace
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