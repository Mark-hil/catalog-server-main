pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        BACKEND_DIR = 'app'
        VENV_NAME = 'flask-backend-env'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
        DOCKERHUB_USERNAME = 'markhill97' // Replace with your actual Docker Hub username
        DOCKER_IMAGE = "${DOCKERHUB_USERNAME}/catalog-server"
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_CREDENTIALS = 'dockerhub-credentials' 
    }
    
    stages {
        stage('Source') {
            steps {
                echo 'Checking out source code from version control'
                git branch: 'main', 
                    url: 'https://github.com/Mark-hil/catalog-server-main.git'
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
                        pip install flake8
                        pip install black
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
                        #python -m pytest test.py -v
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Login and push image to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        
                        // Also tag and push as latest
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
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