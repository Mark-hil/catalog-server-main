pipeline {
    agent any
    
    environment {
        // Set Python environment
        PYTHONPATH = "${WORKSPACE}/app"  // Helps Python find your app modules
        FLASK_APP = "app.py"              // For Flask projects
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "========================================"
                echo "STARTING PIPELINE EXECUTION"
                echo "========================================"
                checkout scm
                echo "Repository cloned successfully"
            }
        }
        
        stage('Install Backend Dependencies') {
            steps {
                echo "========================================"
                echo "INSTALLING PYTHON DEPENDENCIES"
                echo "Using requirements.txt from root directory"
                echo "========================================"
                
                script {
                    try {
                        if (isUnix()) {
                            sh '''
                            echo "Python version:"
                            python3 --version
                            echo "Installing dependencies..."
                            pip3 install -r requirements.txt
                            echo "Installed packages:"
                            pip3 list
                            '''
                        } else {
                            bat '''
                            echo "Python version:"
                            python --version
                            echo "Installing dependencies..."
                            pip install -r requirements.txt
                            echo "Installed packages:"
                            pip list
                            '''
                        }
                        echo "✅ Backend dependencies installed successfully"
                    } catch (Exception e) {
                        echo "❌ BACKEND DEPENDENCY INSTALLATION FAILED"
                        error(e.toString())
                    }
                }
            }
        }
        
        stage('Install Frontend Dependencies') {
            steps {
                echo "========================================"
                echo "INSTALLING FRONTEND DEPENDENCIES"
                echo "Working in ./frontend directory"
                echo "========================================"
                
                dir('frontend') {
                    script {
                        try {
                            if (isUnix()) {
                                sh '''
                                echo "Node version:"
                                node --version
                                echo "Installing npm packages..."
                                npm install
                                '''
                            } else {
                                bat '''
                                echo "Node version:"
                                node --version
                                echo "Installing npm packages..."
                                npm install
                                '''
                            }
                            echo "✅ Frontend dependencies installed successfully"
                        } catch (Exception e) {
                            echo "❌ FRONTEND DEPENDENCY INSTALLATION FAILED"
                            error(e.toString())
                        }
                    }
                }
            }
        }
        
        stage('Run Backend Tests') {
            steps {
                echo "========================================"
                echo "RUNNING BACKEND TESTS"
                echo "Working in ./app/tests directory"
                echo "========================================"
                
                dir('app') {
                    script {
                        try {
                            if (isUnix()) {
                                sh 'python -m pytest tests.py -v'
                            } else {
                                bat 'python -m pytest tests.py -v'
                            }
                            echo "✅ All backend tests passed"
                        } catch (Exception e) {
                            echo "❌ BACKEND TESTS FAILED"
                            error(e.toString())
                        }
                    }
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo "========================================"
                echo "BUILDING FRONTEND"
                echo "========================================"
                
                dir('frontend') {
                    script {
                        try {
                            if (isUnix()) {
                                sh 'npm run build'
                            } else {
                                bat 'npm run build'
                            }
                            echo "✅ Frontend built successfully"
                        } catch (Exception e) {
                            echo "❌ FRONTEND BUILD FAILED"
                            error(e.toString())
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "========================================"
            echo "PIPELINE FINISHED - STATUS: ${currentBuild.currentResult}"
            echo "========================================"
            cleanWs()
        }
        success {
            echo "🎉 PIPELINE SUCCEEDED!"
            // slackSend message: "Pipeline succeeded! ${env.BUILD_URL}"
        }
        failure {
            echo "❌ PIPELINE FAILED"
            // mail to: 'team@example.com', subject: "Pipeline failed"
        }
    }
}