pipeline {
    agent any
    
    environment {
        // Set Python environment
        PYTHONPATH = "${WORKSPACE}/app"
        FLASK_APP = "app.py"
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
        
        // NEW: Verify Node.js/npm are installed
        stage('Verify Node.js Installation') {
            steps {
                echo "========================================"
                echo "🔍 CHECKING NODE.JS INSTALLATION"
                echo "========================================"
                script {
                    try {
                        if (isUnix()) {
                            sh '''
                            echo "Node.js version:"
                            node --version || exit 1
                            echo "npm version:"
                            npm --version || exit 1
                            '''
                        } else {
                            bat '''
                            echo "Node.js version:"
                            node --version || exit /b 1
                            echo "npm version:"
                            npm --version || exit /b 1
                            '''
                        }
                        echo "✅ Node.js and npm are properly installed"
                    } catch (Exception e) {
                        echo """
                        ❌ NODE.JS/NPM MISSING!
                        Install Node.js on the Jenkins server first:
                        
                        For Ubuntu/Debian:
                        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
                        sudo apt-get install -y nodejs
                        
                        Or use a Docker agent with:
                        agent { docker { image 'node:18' } }
                        """
                        error("Node.js/npm not found")
                    }
                }
            }
        }
        
        stage('Install Backend Dependencies') {
            steps {
                echo "========================================"
                echo "🐍 INSTALLING PYTHON DEPENDENCIES"
                echo "========================================"
                script {
                    try {
                        if (isUnix()) {
                            sh '''
                            python3 --version
                            pip3 install -r requirements.txt
                            pip3 list
                            '''
                        } else {
                            bat '''
                            python --version
                            pip install -r requirements.txt
                            pip list
                            '''
                        }
                        echo "✅ Backend dependencies installed"
                    } catch (Exception e) {
                        echo "❌ Python dependency install failed"
                        error(e.toString())
                    }
                }
            }
        }
        
        // stage('Install Frontend Dependencies') {
        //     steps {
        //         echo "========================================"
        //         echo "🖥️ INSTALLING FRONTEND DEPENDENCIES"
        //         echo "========================================"
        //         dir('frontend') {
        //             script {
        //                 try {
        //                     if (isUnix()) {
        //                         sh '''
        //                         echo "Node.js version: $(node --version)"
        //                         echo "npm version: $(npm --version)"
        //                         echo "Installing packages..."
        //                         npm install 
        //                         echo "Installed packages:"
        //                         npm list --depth=0
        //                         '''
        //                     } else {
        //                         bat '''
        //                         node --version
        //                         npm --version
        //                         npm install --loglevel verbose
        //                         npm list --depth=0
        //                         '''
        //                     }
        //                     echo "✅ Frontend dependencies installed"
        //                 } catch (Exception e) {
        //                     echo """
        //                     ❌ FRONTEND INSTALL FAILED!
        //                     Common fixes:
        //                     1. Verify package.json exists in frontend/
        //                     2. Check npm debug log: ${WORKSPACE}/frontend/npm-debug.log
        //                     3. Ensure network connectivity
        //                     """
        //                     error(e.toString())
        //                 }
        //             }
        //         }
        //     }
        // }
        
        stage('Run Backend Tests') {
        steps {
            echo "========================================"
            echo "🧪 RUNNING BACKEND TESTS"
            echo "========================================"
            dir('app') {
                script {
                    try {
                        if (isUnix()) {
                            sh '''
                            echo "Installing pytest..."
                            python -m pip install pytest
                            echo "Running tests..."
                            python -m pytest test.py -v
                            '''
                        } else {
                            bat '''
                            echo "Installing pytest..."
                            python -m pip install pytest
                            echo "Running tests..."
                            python -m pytest test.py -v
                            '''
                        }
                        echo "✅ All tests passed"
                    } catch (Exception e) {
                        echo "❌ TESTS FAILED"
                        echo "Error details: ${e.toString()}"
                        echo "Possible solutions:"
                        echo "1. Check if tests.py exists in app/"
                        echo "2. Verify test dependencies are installed"
                        error("Test execution failed")
                    }
                }
            }
        }
    }
        
        // stage('Build Frontend') {
        //     steps {
        //         echo "========================================"
        //         echo "🏗️ BUILDING FRONTEND"
        //         echo "========================================"
        //         dir('frontend') {
        //             script {
        //                 try {
        //                     if (isUnix()) {
        //                         sh '''
        //                         npm run build
        //                         echo "Build output:"
        //                         ls -la dist/
        //                         '''
        //                     } else {
        //                         bat '''
        //                         npm run build
        //                         dir dist\\
        //                         '''
        //                     }
        //                     echo "✅ Frontend built successfully"
        //                 } catch (Exception e) {
        //                     echo "❌ Frontend build failed"
        //                     error(e.toString())
        //                 }
        //             }
        //         }
        //     }
        // }
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