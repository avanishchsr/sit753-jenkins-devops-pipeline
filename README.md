# Student Connect API - Jenkins DevOps Pipeline

This project is a small Flask API created for the SIT223/SIT753 High Distinction task: DevOps Pipeline with Jenkins.

## Features
- Health endpoint for deployment and monitoring checks
- Job card API endpoint
- Student community group API endpoint
- PyTest automated tests
- Docker-based build and deployment
- Jenkinsfile with Build, Test, Code Quality, Security, Deploy, Release and Monitoring stages

## Local Run
```bash
pip install -r requirements.txt
python -m pytest
python app/main.py
```

Open: http://localhost:5000/health

## Docker Run
```bash
docker build -t student-connect-api:latest .
docker run -p 5000:5000 student-connect-api:latest
```

## Jenkins Tools Required
- Jenkins Pipeline plugin
- Docker installed and accessible to Jenkins
- Python 3.12
- SonarQube server and sonar-scanner configured as `SonarQube`
- Bandit Python package
- Trivy CLI

## Pipeline Stages
1. Checkout
2. Build
3. Test
4. Code Quality
5. Security
6. Deploy
7. Release
8. Monitoring
