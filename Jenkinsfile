pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}/app"
        FLASK_APP = "app.py"
        // Add any other environment variables needed
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "========================================"
                echo "STARTING PIPELINE EXECUTION"
                echo "BUILD ID: ${env.BUILD_ID}"
                echo "BUILD URL: ${env.BUILD_URL}"
                echo "========================================"
                
                echo "Cloning repository from ${env.GIT_URL}..."
                checkout scm
                
                echo "========================================"
                echo "CODE CHECKOUT COMPLETED"
                echo "Working directory contents:"
                script {
                    if (isUnix()) {
                        sh 'ls -la'
                    } else {
                        bat 'dir'
                    }
                }
                echo "========================================"
            }
        }
        
        stage('Install Backend Dependencies') {
            steps {
                echo "========================================"
                echo "INSTALLING BACKEND DEPENDENCIES"
                echo "Working in ./app directory..."
                echo "========================================"
                
                dir('app') {
                    script {
                        try {
                            if (isUnix()) {
                                sh '''
                                echo "Upgrading pip..."
                                python -m pip install --upgrade pip
                                echo "Installing requirements..."
                                pip install -r requirements.txt
                                echo "Installed packages:"
                                pip list
                                '''
                            } else {
                                bat '''
                                echo "Upgrading pip..."
                                python -m pip install --upgrade pip
                                echo "Installing requirements..."
                                pip install -r requirements.txt
                                echo "Installed packages:"
                                pip list
                                '''
                            }
                            echo "✅ Backend dependencies installed successfully"
                        } catch (Exception e) {
                            echo "❌ Failed to install backend dependencies"
                            error("Backend dependency installation failed")
                        }
                    }
                }
                echo "========================================"
            }
        }
        
        stage('Install Frontend Dependencies') {
            steps {
                echo "========================================"
                echo "INSTALLING FRONTEND DEPENDENCIES"
                echo "Working in ./frontend directory..."
                echo "========================================"
                
                dir('frontend') {
                    script {
                        try {
                            if (isUnix()) {
                                sh '''
                                echo "Node version:"
                                node --version
                                echo "NPM version:"
                                npm --version
                                echo "Installing dependencies..."
                                npm install
                                echo "Installed packages:"
                                npm list --depth=0
                                '''
                            } else {
                                bat '''
                                echo "Node version:"
                                node --version
                                echo "NPM version:"
                                npm --version
                                echo "Installing dependencies..."
                                npm install
                                echo "Installed packages:"
                                npm list --depth=0
                                '''
                            }
                            echo "✅ Frontend dependencies installed successfully"
                        } catch (Exception e) {
                            echo "❌ Failed to install frontend dependencies"
                            error("Frontend dependency installation failed")
                        }
                    }
                }
                echo "========================================"
            }
        }
        
        stage('Run Backend Tests') {
            steps {
                echo "========================================"
                echo "RUNNING BACKEND TESTS"
                echo "Working in ./app/tests directory..."
                echo "========================================"
                
                dir('app') {
                    script {
                        try {
                            if (isUnix()) {
                                sh '''
                                echo "Running pytest with verbose output..."
                                python -m pytest tests/ -v
                                echo "Test coverage report:"
                                python -m pytest --cov=. tests/
                                '''
                            } else {
                                bat '''
                                echo "Running pytest with verbose output..."
                                python -m pytest tests/ -v
                                echo "Test coverage report:"
                                python -m pytest --cov=. tests/
                                '''
                            }
                            echo "✅ All backend tests passed successfully"
                        } catch (Exception e) {
                            echo "❌ Backend tests failed"
                            error("Backend tests failed")
                        }
                    }
                }
                echo "========================================"
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo "========================================"
                echo "BUILDING FRONTEND"
                echo "Working in ./frontend directory..."
                echo "========================================"
                
                dir('frontend') {
                    script {
                        try {
                            if (isUnix()) {
                                sh '''
                                echo "Building frontend assets..."
                                npm run build
                                echo "Build output:"
                                ls -la dist/
                                '''
                            } else {
                                bat '''
                                echo "Building frontend assets..."
                                npm run build
                                echo "Build output:"
                                dir dist\
                                '''
                            }
                            echo "✅ Frontend built successfully"
                        } catch (Exception e) {
                            echo "❌ Frontend build failed"
                            error("Frontend build failed")
                        }
                    }
                }
                echo "========================================"
            }
        }
    }
    
    post {
        always {
            echo "========================================"
            echo "PIPELINE FINISHED"
            echo "Current build status: ${currentBuild.currentResult}"
            echo "Build duration: ${currentBuild.durationString}"
            echo "Cleaning up workspace..."
            cleanWs()
            echo "========================================"
            
            // Archive test results if you have JUnit format
            // junit 'app/tests/results/*.xml'
            
            // Archive build artifacts
            // archiveArtifacts artifacts: 'frontend/dist/**/*', fingerprint: true
        }
        
        success {
            echo "========================================"
            echo "PIPELINE SUCCEEDED 🎉"
            echo "All stages completed successfully!"
            echo "========================================"
            
            // Uncomment to enable Slack notifications
            /*
            slackSend (
                color: 'good',
                message: "SUCCESS: Job '${env.JOB_NAME}' [${env.BUILD_NUMBER}] \n(<${env.BUILD_URL}|Open>)"
            )
            */
        }
        
        failure {
            echo "========================================"
            echo "PIPELINE FAILED ❌"
            echo "Failed stage: ${env.STAGE_NAME}"
            echo "Check the logs for details: ${env.BUILD_URL}console"
            echo "========================================"
            
            // Uncomment to enable email notifications
            /*
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME}' [${env.BUILD_NUMBER}]",
                body: """
                Check console output at <a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>
                """,
                to: 'dev-team@example.com',
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
            */
        }
        
        unstable {
            echo "Pipeline completed with unstable status"
            // Handle unstable build (e.g., when tests fail but build continues)
        }
    }
}