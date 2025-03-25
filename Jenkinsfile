pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        BACKEND_DIR = 'app'
        VENV_NAME = 'flask-backend-env'
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
            steps {
                dir("${BACKEND_DIR}") {
                    echo 'Running automated tests'
                    sh '''
                        . ../${VENV_NAME}/bin/activate
                        pip install pytest pytest-cov
                        #python -m pytest test.py -v
                       # PYTHONPATH=.. pytest --cov=. --cov-report=xml
                    '''
                }
                post {
                    always {
                        cobertura coberturaReportFile: "${BACKEND_DIR}/coverage.xml"
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                dir("${BACKEND_DIR}") {
                    echo 'Preparing deployable artifact'
                    sh '''
                        . ../${VENV_NAME}/bin/activate
                        pip freeze > ../requirements.txt
                    '''
                    
                    // Optional: Build Docker image for backend
                    // script {
                    //     docker.build("flask-backend:${env.BUILD_NUMBER}")
                    // }
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