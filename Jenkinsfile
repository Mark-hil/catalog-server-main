pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}/app"
        FLASK_APP = "app.py"
        VENV_DIR = "${WORKSPACE}/venv"  // Virtualenv directory
    }
    
    stages {
        stage('Checkout Code') {
            steps { checkout scm }
        }

        stage('Setup Python Virtualenv') {
            steps {
                echo "========================================"
                echo "🐍 CREATING PYTHON VIRTUAL ENVIRONMENT"
                echo "========================================"
                script {
                    try {
                        if (isUnix()) {
                            sh """
                            # Verify Python exists
                            python3 --version || { echo "❌ Python not found"; exit 1; }
                            
                            # Cleanup previous venv if exists
                            rm -rf "${VENV_DIR}" || true
                            
                            # Create new venv
                            python3 -m venv "${VENV_DIR}" || { echo "❌ Virtualenv creation failed"; exit 1; }
                            
                            # Activate and verify
                            source "${VENV_DIR}/bin/activate"
                            python -m pip install --upgrade pip
                            echo "✅ Virtualenv ready at ${VENV_DIR}"
                            pip --version
                            """
                        } else {
                            bat """
                            python --version || exit /b 1
                            rmdir /s /q "${VENV_DIR}" 2>nul
                            python -m venv "${VENV_DIR}" || exit /b 1
                            call "${VENV_DIR}\\Scripts\\activate"
                            python -m pip install --upgrade pip
                            pip --version
                            """
                        }
                    } catch (Exception e) {
                        echo """
                        ❌ VIRTUALENV SETUP FAILED
                        Common solutions:
                        1. Verify Python is installed (python3 --version)
                        2. Check disk space on Jenkins server
                        3. Ensure Jenkins has write permissions
                        4. Try specifying full Python path: /usr/bin/python3 -m venv ...
                        """
                        error("Virtualenv creation failed: ${e.toString()}")
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('app') {
                    script {
                        try {
                            if (isUnix()) {
                                sh """
                                source "${VENV_DIR}/bin/activate"
                                echo "Installing dependencies..."
                                pip install -r requirements.txt pytest pytest-cov
                                echo "Installed packages:"
                                pip list
                                """
                            } else {
                                bat """
                                call "${VENV_DIR}\\Scripts\\activate"
                                pip install -r requirements.txt pytest pytest-cov
                                pip list
                                """
                            }
                        } catch (Exception e) {
                            echo """
                            ❌ DEPENDENCY INSTALLATION FAILED
                            Verify:
                            1. requirements.txt exists in app/
                            2. File has correct permissions
                            3. Network connectivity
                            """
                            error(e.toString())
                        }
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('app') {
                    script {
                        try {
                            if (isUnix()) {
                                sh """
                                source "${VENV_DIR}/bin/activate"
                                echo "Running tests..."
                                python -m pytest test.py -v --cov=. --cov-report=term-missing
                                """
                            } else {
                                bat """
                                call "${VENV_DIR}\\Scripts\\activate"
                                python -m pytest test.py -v --cov=. --cov-report=term-missing
                                """
                            }
                        } catch (Exception e) {
                            echo """
                            ❌ TESTS FAILED
                            Last error output:
                            """
                            if (isUnix()) {
                                sh 'tail -n 20 .pytest_cache/v/cache/lastfailed || echo "No failure details"'
                            } else {
                                bat 'type .pytest_cache\\v\\cache\\lastfailed | more +20 || echo "No failure details"'
                            }
                            error("Tests failed")
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}