pipeline {
    agent any
    
    environment {
        // Set Python environment
        PYTHONPATH = "${WORKSPACE}/app"
        FLASK_APP = "app.py"
        VENV_DIR = "${WORKSPACE}/venv"  // Virtualenv directory
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "========================================"
                echo "🚀 STARTING PIPELINE EXECUTION"
                echo "========================================"
                checkout scm
                echo "✅ Repository cloned successfully"
                
                // Debug: Show workspace structure
                script {
                    if (isUnix()) {
                        sh 'echo "Workspace contents:" && ls -la'
                    } else {
                        bat 'echo "Workspace contents:" && dir'
                    }
                }
            }
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
                            python -m venv "${VENV_DIR}"
                            source "${VENV_DIR}/bin/activate"
                            python -m pip install --upgrade pip
                            echo "Virtualenv created at: ${VENV_DIR}"
                            """
                        } else {
                            bat """
                            python -m venv "${VENV_DIR}"
                            call "${VENV_DIR}\\Scripts\\activate"
                            python -m pip install --upgrade pip
                            echo "Virtualenv created at: ${VENV_DIR}"
                            """
                        }
                    } catch (Exception e) {
                        echo "❌ VIRTUALENV CREATION FAILED"
                        error(e.toString())
                    }
                }
            }
        }
        
        stage('Install Backend Dependencies') {
            steps {
                echo "========================================"
                echo "🐍 INSTALLING PYTHON DEPENDENCIES"
                echo "========================================"
                dir('app') {
                    script {
                        try {
                            if (isUnix()) {
                                sh """
                                source "${VENV_DIR}/bin/activate"
                                echo "Python version:"
                                python --version
                                echo "Installing dependencies..."
                                pip install -r requirements.txt pytest pytest-cov
                                echo "Installed packages:"
                                pip list
                                """
                            } else {
                                bat """
                                call "${VENV_DIR}\\Scripts\\activate"
                                python --version
                                pip install -r requirements.txt pytest pytest-cov
                                pip list
                                """
                            }
                            echo "✅ Backend dependencies installed"
                        } catch (Exception e) {
                            echo "❌ PYTHON DEPENDENCY INSTALL FAILED"
                            error(e.toString())
                        }
                    }
                }
            }
        }
        
        stage('Run Backend Tests') {
            steps {
                echo "========================================"
                echo "🧪 RUNNING BACKEND TESTS"
                echo "========================================"
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
                            1. Verify test.py exists in app/ and contains valid tests
                            2. Check requirements.txt includes all test dependencies
                            3. Last error output:
                            """
                            if (isUnix()) {
                                sh 'tail -n 20 .pytest_cache/v/cache/lastfailed || echo "No failure details"'
                            } else {
                                bat 'type .pytest_cache\\v\\cache\\lastfailed | more +20 || echo "No failure details"'
                            }
                            error("Test execution failed")
                        }
                    }
                }
            }
        }
        
        // Node.js stages commented out as per your original pipeline
        // You can uncomment them when needed
    }
    
    post {
        always {
            echo "========================================"
            echo "🏁 PIPELINE FINISHED - STATUS: ${currentBuild.currentResult}"
            echo "========================================"
            cleanWs()
        }
        success {
            echo "🎉 PIPELINE SUCCEEDED!"
            // slackSend message: "Build succeeded: ${env.BUILD_URL}"
        }
        failure {
            echo "❌ PIPELINE FAILED"
            // mail to: 'team@example.com', subject: "Build failed"
        }
    }
}