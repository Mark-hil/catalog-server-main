pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        BACKEND_DIR = 'app'
        VENV_NAME = 'flask-backend-env'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
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
                
                DATABASE_URI = 'sqlite:///test.db'
                SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
            }
            steps {
                dir("${BACKEND_DIR}") {
                    echo 'Running automated tests'
                    sh '''
                        . ../${VENV_NAME}/bin/activate
                        pip install pytest pytest-cov
                        PYTHONPATH=.. DATABASE_URI='sqlite:///test.db' SQLALCHEMY_DATABASE_URI='sqlite:///test.db' python -m pytest test.py -v
                    '''
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