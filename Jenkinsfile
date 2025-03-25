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

        stage('Setup Virtualenv') {
            steps {
                echo "========================================"
                echo "🐍 CREATING PYTHON VIRTUAL ENVIRONMENT"
                echo "========================================"
                script {
                    try {
                        if (isUnix()) {
                            sh """
                            # Clean existing venv if present
                            rm -rf "${VENV_DIR}" || true
                            
                            # Create fresh virtualenv
                            python3 -m venv "${VENV_DIR}" || exit 1
                            
                            # Activate and upgrade pip
                            source "${VENV_DIR}/bin/activate"
                            python -m pip install --upgrade pip
                            echo "✅ Virtualenv ready at ${VENV_DIR}"
                            """
                        } else {
                            bat """
                            rmdir /s /q "${VENV_DIR}" 2>nul
                            python -m venv "${VENV_DIR}" || exit /b 1
                            call "${VENV_DIR}\\Scripts\\activate"
                            python -m pip install --upgrade pip
                            """
                        }
                    } catch (Exception e) {
                        echo """
                        ❌ VIRTUALENV CREATION FAILED
                        Debug steps:
                        1. Verify Python is installed: python3 --version
                        2. Check disk space: df -h ${WORKSPACE}
                        3. Test manually: python3 -m venv /tmp/test_venv
                        """
                        error("Virtualenv setup failed")
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
                                echo "Verifying Flask installation:"
                                python -c "import flask; print(f'Flask version: {flask.__version__}')"
                                """
                            } else {
                                bat """
                                call "${VENV_DIR}\\Scripts\\activate"
                                pip install -r requirements.txt pytest pytest-cov
                                python -c "import flask; print(f'Flask version: {flask.__version__}')"
                                """
                            }
                            echo "✅ Dependencies installed"
                        } catch (Exception e) {
                            echo """
                            ❌ DEPENDENCY INSTALLATION FAILED
                            Verify:
                            1. requirements.txt exists in app/
                            2. File contains 'flask' package
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
                                echo "Running tests with coverage..."
                                python -m pytest test.py -v --cov=. --cov-report=term-missing
                                """
                            } else {
                                bat """
                                call "${VENV_DIR}\\Scripts\\activate"
                                python -m pytest test.py -v --cov=. --cov-report=term-missing
                                """
                            }
                            echo "✅ All tests passed"
                        } catch (Exception e) {
                            echo """
                            ❌ TEST FAILURE DETAILS:
                            1. Verify test.py imports match your virtualenv
                            2. Check .pytest_cache for error details
                            3. Last error:
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
            archiveArtifacts artifacts: 'app/.pytest_cache/**/*', allowEmptyArchive: true
            cleanWs()
        }
    }
}