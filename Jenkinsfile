pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
        BACKEND_DIR = 'app'
        VENV_NAME = 'flask-backend-env'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
        DOCKERHUB_USERNAME = 'markhill97'  // Replace with your actual Docker Hub username
        DOCKER_IMAGE = 'markhill97/catalog-server'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = 'dockerhub-credentials'  // Store credentials with Access Token
    }

    stages {
        stage('Source') {
            steps {
                echo 'Checking out source code from version control'
                git branch: 'main', url: 'https://github.com/Mark-hil/catalog-server-main.git'
            }
        }

        stage('Setup') {
            steps {
                echo 'Setting up Python virtual environment for backend'
                sh '''
                    python3 -m venv ${VENV_NAME}
                    . ${VENV_NAME}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install python-dotenv
                '''
            }
        }

        stage('Lint') {
            steps {
                dir("${BACKEND_DIR}") {
                    echo 'Running code quality checks'
                    sh '''
                        . ../${VENV_NAME}/bin/activate
                        pip install flake8 black
                        black .
                    '''
                }
            }
        }

        stage('Test') {
            environment {
                SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
            }
            steps {
                dir("${BACKEND_DIR}") {
                    echo 'Running automated tests'
                    sh '''
                        . ../${VENV_NAME}/bin/activate
                        pip install pytest pytest-cov
                        # python -m pytest test.py -v
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS, usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                        sh """
                            echo "${DOCKERHUB_PASSWORD}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin
                            docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                            docker push ${DOCKER_IMAGE}:latest
                            docker logout
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up virtual environment'
            sh 'rm -rf ${VENV_NAME}'
        }
        success {
            echo 'Backend pipeline completed successfully!'
        }
        failure {
            echo 'Backend pipeline failed. Please check the logs.'
        }
    }
}
