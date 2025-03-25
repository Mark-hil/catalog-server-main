pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}/app"
        FLASK_APP = "app.py"
        VENV_DIR = "${WORKSPACE}/venv"  // Virtualenv directory
        PYTHON_BIN = "/usr/bin/python3"  // Update this path as needed
    }
    
    stages {
        stage('System Diagnostics') {
            steps {
                echo "========================================"
                echo "🛠️ SYSTEM DIAGNOSTICS (PRE-CHECKS)"
                echo "========================================"
                script {
                    if (isUnix()) {
                        sh """
                        echo "1. Python availability:"
                        which python3 || echo "Python3 not found in PATH"
                        python3 --version || echo "Python3 not working"
                        
                        echo "\n2. Disk space:"
                        df -h ${WORKSPACE}
                        
                        echo "\n3. Write permissions:"
                        touch ${WORKSPACE}/write_test && rm ${WORKSPACE}/write_test && echo "Write OK" || echo "Write failed"
                        
                        echo "\n4. Python modules:"
                        python3 -c "import venv; print('venv module available')" || echo "venv module missing"
                        """
                    } else {
                        bat """
                        echo "1. Python availability:"
                        where python || echo "Python not found"
                        python --version || echo "Python not working"
                        
                        echo "\n2. Disk space:"
                        dir /-c ${WORKSPACE}
                        
                        echo "\n3. Write permissions:"
                        echo. > write_test && del write_test && echo Write OK || echo Write failed
                        """
                    }
                }
            }
        }

        stage('Setup Virtualenv') {
            steps {
                echo "========================================"
                echo "🐍 VIRTUALENV CREATION (WITH FALLBACKS)"
                echo "========================================"
                script {
                    try {
                        if (isUnix()) {
                            sh """
                            # Attempt 1: Standard venv
                            echo "Attempting standard venv..."
                            python3 -m venv "${VENV_DIR}" && {
                                source "${VENV_DIR}/bin/activate"
                                python -m pip install --upgrade pip
                                echo "✅ Standard venv created"
                                exit 0
                            }
                            
                            # Attempt 2: Specified Python path
                            echo "Falling back to explicit Python path..."
                            ${PYTHON_BIN} -m venv "${VENV_DIR}" && {
                                source "${VENV_DIR}/bin/activate"
                                python -m pip install --upgrade pip
                                echo "✅ Venv created with ${PYTHON_BIN}"
                                exit 0
                            }
                            
                            # Attempt 3: virtualenv package
                            echo "Falling back to virtualenv package..."
                            python3 -m pip install --user virtualenv && \
                            python3 -m virtualenv "${VENV_DIR}" && {
                                source "${VENV_DIR}/bin/activate"
                                echo "✅ Virtualenv package succeeded"
                                exit 0
                            }
                            
                            echo "❌ All venv creation attempts failed"
                            exit 1
                            """
                        } else {
                            bat """
                            python -m venv "${VENV_DIR}" || exit /b 1
                            call "${VENV_DIR}\\Scripts\\activate" || exit /b 1
                            python -m pip install --upgrade pip || exit /b 1
                            """
                        }
                    } catch (Exception e) {
                        echo """
                        ❌ VIRTUALENV CREATION FAILED
                        Full diagnostics:
                        1. Python path: ${PYTHON_BIN}
                        2. Workspace: ${WORKSPACE} (${currentBuild.number})
                        3. Disk space: ${isUnix() ? 'Run df -h' : 'Check disk space'}
                        
                        Immediate fixes:
                        a) SSH into Jenkins server and verify:
                           sudo -u jenkins python3 -m venv /tmp/test_venv
                        b) Consider using Docker agent:
                           agent { docker { image 'python:3.11' } }
                        """
                        error("Virtualenv creation failed after multiple attempts")
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
                                echo "Python: $(which python)"
                                echo "Pip: $(pip --version)"
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
                            ❌ DEPENDENCY INSTALL FAILED
                            Debug tips:
                            1. Check requirements.txt syntax
                            2. Run manually on server:
                               source ${VENV_DIR}/bin/activate && pip install -r ${WORKSPACE}/app/requirements.txt
                            3. Check network connectivity
                            """
                            error("Dependency installation failed")
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
                            ❌ TEST FAILURE
                            Debug data:
                            - Python path: $(which python)
                            - Test file: ${WORKSPACE}/app/test.py
                            - Last error:
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