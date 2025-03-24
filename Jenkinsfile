pipeline {
    agent any
    
    environment {
        // Set Python environment
        PYTHONPATH = "${WORKSPACE}/app"
        FLASK_APP = "app.py"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Backend Dependencies') {
            steps {
                dir('app') {
                    script {
                        if (isUnix()) {
                            sh 'python -m pip install --upgrade pip'
                            sh 'pip install -r requirements.txt'
                        } else {
                            bat 'python -m pip install --upgrade pip'
                            bat 'pip install -r requirements.txt'
                        }
                    }
                }
            }
        }
        
        stage('Install Frontend Dependencies') {
            steps {
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm install'
                        } else {
                            bat 'npm install'
                        }
                    }
                }
            }
        }
        
        stage('Run Backend Tests') {
            steps {
                dir('app') {
                    script {
                        if (isUnix()) {
                            sh 'python -m pytest tests/'
                        } else {
                            bat 'python -m pytest tests/'
                        }
                    }
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm run build'
                        } else {
                            bat 'npm run build'
                        }
                    }
                }
            }
        }
        
        // stage('Build Docker Image') {
        //     when {
        //         expression { 
        //             // Only build Docker image if Dockerfile exists
        //             fileExists 'Dockerfile' 
        //         }
        //     }
        //     steps {
        //         script {
        //             docker.build("my-flask-app:${env.BUILD_ID}")
        //         }
        //     }
        // }
        
        // stage('Deploy to Staging') {
        //     steps {
        //         script {
        //             echo "Deploying to staging environment..."
        //             // Add your deployment commands here
        //             // Example for simple deployment:
        //             // sh 'rsync -avz --delete . user@staging-server:/path/to/app'
        //         }
        //     }
        // }
    }
    
    post {
        always {
            echo 'Pipeline completed'
            cleanWs() // Clean up workspace
        }
        success {
            echo 'Pipeline succeeded!'
            // slackSend channel: '#deployments', message: "Pipeline succeeded: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        failure {
            echo 'Pipeline failed!'
            // mail to: 'team@example.com', subject: "Pipeline failed: ${env.JOB_NAME}", body: "Check console at ${env.BUILD_URL}"
        }
    }
}