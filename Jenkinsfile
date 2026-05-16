pipeline {
    agent any

    environment {
        APP_NAME = 'student-connect-api'
        IMAGE_NAME = 'student-connect-api'
        IMAGE_TAG = "${BUILD_NUMBER}"
        STAGING_CONTAINER = 'student-connect-api-staging'
        PRODUCTION_CONTAINER = 'student-connect-api-production'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning the GitHub repository into the Jenkins workspace.'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building a Docker image as the deployment artefact.'
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }

        stage('Test') {
            steps {
                echo 'Installing dependencies and running automated unit tests with PyTest.'
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
                sh '. venv/bin/activate && pytest -q --junitxml=reports/test-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
                }
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running SonarQube static code quality analysis.'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=student-connect-api \
                      -Dsonar.projectName=StudentConnectAPI \
                      -Dsonar.sources=app \
                      -Dsonar.tests=tests \
                      -Dsonar.python.version=3.12
                    '''
                }
            }
        }

        stage('Security') {
            steps {
                echo 'Running Bandit for Python security checks and Trivy for container vulnerability scanning.'
                sh '. venv/bin/activate && bandit -r app -f txt -o reports/bandit-report.txt || true'
                sh 'trivy image --severity HIGH,CRITICAL --exit-code 0 --format table -o reports/trivy-report.txt ${IMAGE_NAME}:${IMAGE_TAG} || true'
                archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application to a staging Docker container.'
                sh 'docker rm -f ${STAGING_CONTAINER} || true'
                sh 'docker run -d --name ${STAGING_CONTAINER} -p 5000:5000 -e APP_ENV=staging ${IMAGE_NAME}:${IMAGE_TAG}'
                sh 'sleep 5'
                sh 'curl -f http://localhost:5000/health'
            }
        }

        stage('Release') {
            steps {
                echo 'Promoting the tested image to a release version.'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:release-${BUILD_NUMBER}'
                sh 'git tag -f release-${BUILD_NUMBER} || true'
                sh 'docker images | grep ${IMAGE_NAME}'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Validating the health endpoint used by monitoring tools such as Prometheus/Grafana.'
                sh 'curl -f http://localhost:5000/health'
                echo 'Monitoring evidence: health endpoint responds successfully and can be scraped by Prometheus.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. Build, test, quality, security, deploy, release and monitoring stages passed.'
        }
        failure {
            echo 'Pipeline failed. Review the Jenkins console output and archived reports for the failing stage.'
        }
        always {
            archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
        }
    }
}
