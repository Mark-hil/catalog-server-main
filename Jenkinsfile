pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}/app"
        FLASK_APP = "app.py"
        VENV_DIR = "${WORKSPACE}/venv"
        # Add database URI configuration
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  // Or your test database URI
    }
    
    stages {
        stage('Checkout Code') {
            steps { 
                checkout scm 
            }
        }

        stage('Setup Virtualenv') {
            steps {
                script {
                    try {
                        if (isUnix()) {
                            sh '''
                            set -e
                            
                            # Ensure python3 and venv are available
                            which python3 || (echo "Python3 not found" && exit 1)
                            
                            # Remove existing venv directory if it exists
                            rm -rf "${VENV_DIR}" || true
                            
                            # Create virtualenv using full path to python3
                            python3 -m venv "${VENV_DIR}"
                            
                            # Activate virtualenv and upgrade pip
                            . "${VENV_DIR}/bin/activate"
                            python3 -m pip install --upgrade pip
                            
                            echo "✅ Virtualenv successfully created at ${VENV_DIR}"
                            '''
                        } else {
                            bat '''
                            @echo off
                            if exist "%VENV_DIR%" rmdir /s /q "%VENV_DIR%"
                            python -m venv "%VENV_DIR%"
                            call "%VENV_DIR%\\Scripts\\activate"
                            python -m pip install --upgrade pip
                            echo Virtualenv successfully created at %VENV_DIR%
                            '''
                        }
                    } catch (Exception e) {
                        error("Virtualenv setup failed: ${e.getMessage()}")
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        if (isUnix()) {
                            sh '''
                            . "${VENV_DIR}/bin/activate"
                            python3 -m pip install -r "${WORKSPACE}/requirements.txt" pytest pytest-cov
                            python3 -c "import flask; print(f'Flask version: {flask.__version__}')"
                            '''
                        } else {
                            bat '''
                            call "%VENV_DIR%\\Scripts\\activate"
                            pip install -r "%WORKSPACE%\\requirements.txt" pytest pytest-cov
                            python -c "import flask; print(f'Flask version: {flask.__version__}')"
                            '''
                        }
                    } catch (Exception e) {
                        error("Dependencies installation failed: ${e.getMessage()}")
                    }
                }
            }
        }

        stage('Run Tests') {
            environment {
                # Explicitly set database URI for tests
                SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
            }
            steps {
                dir('app') {
                    script {
                        try {
                            if (isUnix()) {
                                sh '''
                                . "${VENV_DIR}/bin/activate"
                                python3 -m pytest test.py -v --cov=. --cov-report=term-missing
                                '''
                            } else {
                                bat '''
                                call "%VENV_DIR%\\Scripts\\activate"
                                python -m pytest test.py -v --cov=. --cov-report=term-missing
                                '''
                            }
                        } catch (Exception e) {
                            error("Tests failed: ${e.getMessage()}")
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'app/.pytest_cache/**/*', allowEmptyArchive: true
            cleanWs()
        }
    }
}